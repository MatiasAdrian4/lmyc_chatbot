import json
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestMessages:
    def test_get_message(self, setup_database):
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

        with patch("routes.messages.database", database):

            response = client.get("/messages")

            assert response.status_code == 200
            assert response.headers["content-type"] == "text/plain; charset=utf-8"

            response_data = [json.loads(line) for line in response.content.splitlines()]

            assert len(response_data) == 2

            assert response_data[0]["content"] == "Hello!"
            assert response_data[0]["timestamp"] == "2024-12-20T21:57:11.489869+00:00"
            assert response_data[0]["role"] == "user"

            assert response_data[1]["content"] == "Hello, how can I help you?\n"
            assert response_data[1]["timestamp"] == "2024-12-20T21:57:12.880159+00:00"
            assert response_data[1]["role"] == "model"

    def test_post_message(self, setup_database):
        # TODO: implement
        pass
