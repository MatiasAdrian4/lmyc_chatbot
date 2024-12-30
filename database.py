from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from pydantic_ai.messages import ModelMessage, ModelMessagesTypeAdapter

THIS_DIR = Path(__file__).parent


@dataclass
class Database:
    """Very rudimentary database to store chat messages in a JSON lines file."""

    file: Path = THIS_DIR / ".chatbot_messages.jsonl"

    def add_messages(self, messages: bytes):
        with self.file.open("ab") as f:
            f.write(messages + b"\n")

    def get_messages(self) -> Iterator[ModelMessage]:
        if self.file.exists():
            with self.file.open("rb") as f:
                for line in f:
                    if line:
                        yield from ModelMessagesTypeAdapter.validate_json(line)

    def clear_messages(self):
        if self.file.exists():
            self.file.unlink()


database = Database()
