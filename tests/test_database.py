import json
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from database import Database


class TestDatabase:
    @pytest.fixture(autouse=True)
    def setup_database(self):
        """Fixture to provide a temporary database for testing."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            self.temp_file = Path(tmp.name)
        self.database = Database(file=self.temp_file)
        yield
        self.temp_file.unlink()  # clean up after tests

    def test_add_messages(self):
        message_data = b'[{"content": "Hello!", "timestamp": "2024-12-12T00:00:00", "role": "user"}]'
        self.database.add_messages(message_data)

        with self.database.file.open("rb") as f:
            lines = f.readlines()

        assert len(lines) == 1
        assert lines[0].strip() == message_data

    def test_get_messages(self):
        user_message = {
            "content": "Hello!",
            "timestamp": "2024-12-12T00:00:00",
            "role": "user",
        }
        model_message = {
            "content": "Hello, how can I help you?",
            "timestamp": "2024-12-12T00:00:00",
            "role": "model-text-response",
        }
        message_data = json.dumps([user_message, model_message]).encode("utf-8")
        self.database.add_messages(message_data)

        retrieved_messages = list(self.database.get_messages())

        assert len(retrieved_messages) == 2

        assert retrieved_messages[0].content == "Hello!"
        assert retrieved_messages[0].timestamp == datetime(2024, 12, 12, 0, 0)
        assert retrieved_messages[0].role == "user"

        assert retrieved_messages[1].content == "Hello, how can I help you?"
        assert retrieved_messages[1].timestamp == datetime(2024, 12, 12, 0, 0)
        assert retrieved_messages[1].role == "model-text-response"
