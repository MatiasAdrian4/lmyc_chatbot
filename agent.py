from typing import List

from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

from settings import GEMINI_API_KEY


model = GeminiModel("gemini-1.5-flash", api_key=GEMINI_API_KEY)
agent = Agent(
    model,
    system_prompt=(
        "Hola! Eres una asistente virtual que ayudara con cualquier tarea "
        "relacionada con la app."
    ),
)


class Sale(BaseModel):
    id: int
    description: str
    date: str


@agent.tool_plain
def get_sales() -> List[Sale]:
    """Returns a list of sales"""
    sales_data = [
        {"id": 1, "description": "abc", "date": "31/08/2024"},
        {"id": 2, "description": "def", "date": "02/12/2024"},
        {"id": 3, "description": "ghi", "date": "12/12/2024"},
    ]
    return [Sale(**data) for data in sales_data]
