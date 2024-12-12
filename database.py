from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from pydantic_ai.messages import Message, MessagesTypeAdapter

THIS_DIR = Path(__file__).parent


@dataclass
class Database:
    """Very rudimentary database to store chat messages in a JSON lines file."""

    file: Path = THIS_DIR / ".chatbot_messages.jsonl"

    def add_messages(self, messages: bytes):
        with self.file.open("ab") as f:
            f.write(messages + b"\n")

    def get_messages(self) -> Iterator[Message]:
        if self.file.exists():
            with self.file.open("rb") as f:
                for line in f:
                    if line:
                        yield from MessagesTypeAdapter.validate_json(line)


database = Database()
