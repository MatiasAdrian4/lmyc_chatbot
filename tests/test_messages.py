import json
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestMessages:
    def test_get_message(self, setup_database):
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

        with patch("routes.messages.database", database):

            response = client.get("/messages")

            assert response.status_code == 200
            assert response.headers["content-type"] == "text/plain; charset=utf-8"

            response_data = [json.loads(line) for line in response.content.splitlines()]

            assert len(response_data) == 2

            assert response_data[0]["content"] == "Hello!"
            assert response_data[0]["timestamp"] == "2024-12-12T00:00:00"
            assert response_data[0]["role"] == "user"

            assert response_data[1]["content"] == "Hello, how can I help you?"
            assert response_data[1]["timestamp"] == "2024-12-12T00:00:00"
            assert response_data[1]["role"] == "model-text-response"

    def test_post_message(self, setup_database):
        # TODO: implement
        pass
