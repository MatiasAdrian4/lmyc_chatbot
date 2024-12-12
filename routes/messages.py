from typing import Annotated

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

        # stream the user prompt so that can be displayed straight away
        yield MessageTypeAdapter.dump_json(UserPrompt(content=prompt)) + b"\n"

        # get the chat history so far to pass as context to the agent
        messages = list(database.get_messages())

        # run the agent with the user prompt and the chat history
        async with agent.run_stream(prompt, message_history=messages) as result:
            async for text in result.stream(debounce_by=0.01):
                # text here is a `str` and the frontend wants
                # JSON encoded ModelTextResponse, so we create one
                m = ModelTextResponse(content=text, timestamp=result.timestamp())
                yield MessageTypeAdapter.dump_json(m) + b"\n"

        # add new messages (e.g. the user prompt and the agent response in this case) to the database
        database.add_messages(result.new_messages_json())

    return StreamingResponse(stream_messages(), media_type="text/plain")
