from typing import Annotated

# from devtools import debug
from fastapi import APIRouter, Form
from fastapi.responses import Response, StreamingResponse
from pydantic import TypeAdapter, Field
from pydantic_ai.messages import Message, UserPrompt, ModelTextResponse

from agent import agent
from database import database

router = APIRouter()


MessageTypeAdapter: TypeAdapter[Message] = TypeAdapter(
    Annotated[Message, Field(discriminator="role")]
)


@router.get("/")
async def get_messages() -> Response:
    messages = database.get_messages()
    return Response(
        b"\n".join(MessageTypeAdapter.dump_json(msg) for msg in messages),
        media_type="text/plain",
    )


@router.post("/")
async def post_message(prompt: Annotated[str, Form()]) -> StreamingResponse:
    async def stream_messages():
        """Streams new line delimited JSON `Message`s to the client."""

        yield MessageTypeAdapter.dump_json(UserPrompt(content=prompt)) + b"\n"

        # TODO: check if I really need previous messages or I can start a new
        # conversation and delete the chat history. That can be based on the
        # message's date or something similar.

        messages = list(database.get_messages())

        async with agent.run_stream(prompt, message_history=messages) as result:
            # debug(result)
            async for text in result.stream(debounce_by=0.01):
                m = ModelTextResponse(content=text, timestamp=result.timestamp())
                yield MessageTypeAdapter.dump_json(m) + b"\n"

        database.add_messages(result.new_messages_json())

    return StreamingResponse(stream_messages(), media_type="text/plain")
