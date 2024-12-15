import json
from datetime import datetime


class TestDatabase:

    def test_add_messages(self, setup_database):
        database = setup_database

        message_data = b'[{"content": "Hello!", "timestamp": "2024-12-12T00:00:00", "role": "user"}]'
        database.add_messages(message_data)

        with database.file.open("rb") as f:
            lines = f.readlines()

        assert len(lines) == 1
        assert lines[0].strip() == message_data

    def test_get_messages(self, setup_database):
        database = setup_database

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
        database.add_messages(message_data)

        retrieved_messages = list(database.get_messages())

        assert len(retrieved_messages) == 2

        assert retrieved_messages[0].content == "Hello!"
        assert retrieved_messages[0].timestamp == datetime(2024, 12, 12, 0, 0)
        assert retrieved_messages[0].role == "user"

        assert retrieved_messages[1].content == "Hello, how can I help you?"
        assert retrieved_messages[1].timestamp == datetime(2024, 12, 12, 0, 0)
        assert retrieved_messages[1].role == "model-text-response"
