import json
from datetime import datetime, timezone


class TestDatabase:

    def test_add_messages(self, setup_database):
        database = setup_database

        message_data = b'[{"parts":[{"content":"Hello!","timestamp":"2024-12-20T21:57:11.489869Z","part_kind":"user-prompt"}],"kind":"request"}]'
        database.add_messages(message_data)

        with database.file.open("rb") as f:
            lines = f.readlines()

        assert len(lines) == 1
        assert lines[0].strip() == message_data

    def test_get_messages(self, setup_database):
        database = setup_database

        user_message = {
            "parts": [
                {
                    "content": "Hello!",
                    "timestamp": "2024-12-20T21:57:11.489869Z",
                    "part_kind": "user-prompt",
                }
            ],
            "kind": "request",
        }
        model_message = {
            "parts": [
                {
                    "content": "Hello, how can I help you?\n",
                    "part_kind": "text",
                }
            ],
            "timestamp": "2024-12-20T21:57:12.880159Z",
            "kind": "response",
        }
        message_data = json.dumps([user_message, model_message]).encode("utf-8")
        database.add_messages(message_data)

        retrieved_messages = list(database.get_messages())

        assert len(retrieved_messages) == 2

        assert retrieved_messages[0].parts[0].content == "Hello!"
        assert retrieved_messages[0].parts[0].timestamp == datetime(
            2024, 12, 20, 21, 57, 11, 489869, tzinfo=timezone.utc
        )
        assert retrieved_messages[0].parts[0].part_kind == "user-prompt"

        assert retrieved_messages[1].parts[0].content == "Hello, how can I help you?\n"
        assert retrieved_messages[1].timestamp == datetime(
            2024, 12, 20, 21, 57, 12, 880159, tzinfo=timezone.utc
        )
        assert retrieved_messages[1].parts[0].part_kind == "text"
