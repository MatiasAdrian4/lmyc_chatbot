import json
from datetime import datetime, timezone
from typing import Annotated, Literal

# from devtools import debug
from fastapi import APIRouter, Form
from fastapi.responses import Response, StreamingResponse
from pydantic_ai import UnexpectedModelBehavior
from pydantic_ai.messages import (
    ModelMessage,
    ModelResponse,
    ModelRequest,
    UserPromptPart,
    TextPart,
)
from typing_extensions import TypedDict

from agent import agent
from database import database

router = APIRouter()


class ChatMessage(TypedDict):
    """Format of messages sent to the browser"""

    role: Literal["user", "model"]
    timestamp: str
    content: str


def to_chat_message(m: ModelMessage) -> ChatMessage:
    first_part = m.parts[0]
    if isinstance(m, ModelRequest):
        if isinstance(first_part, UserPromptPart):
            return {
                "role": "user",
                "timestamp": first_part.timestamp.isoformat(),
                "content": first_part.content,
            }
    elif isinstance(m, ModelResponse):
        if isinstance(first_part, TextPart):
            return {
                "role": "model",
                "timestamp": m.timestamp.isoformat(),
                "content": first_part.content,
            }
    raise UnexpectedModelBehavior(f"Unexpected message type for chat app: {m}")


@router.get("/")
async def get_messages() -> Response:
    messages = database.get_messages()
    return Response(
        b"\n".join(
            json.dumps(to_chat_message(msg)).encode("utf-8") for msg in messages
        ),
        media_type="text/plain",
    )


@router.post("/")
async def post_message(prompt: Annotated[str, Form()]) -> StreamingResponse:
    async def stream_messages():
        """Streams new line delimited JSON `Message`s to the client."""

        yield json.dumps(
            {
                "role": "user",
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
                "content": prompt,
            }
        ).encode("utf-8") + b"\n"

        messages = list(database.get_messages())

        async with agent.run_stream(prompt, message_history=messages) as result:
            # debug(result)
            async for text in result.stream(debounce_by=0.01):
                msg = ModelResponse.from_text(
                    content=text, timestamp=result.timestamp()
                )
                yield json.dumps(to_chat_message(msg)).encode("utf-8") + b"\n"

        database.add_messages(result.new_messages_json())

    return StreamingResponse(stream_messages(), media_type="text/plain")
