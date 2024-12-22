from typing import List
from datetime import datetime

from pydantic import BaseModel
from pydantic_ai import Agent

from pydantic_ai.models.groq import GroqModel

from service.lmyc_client import MOCK_SALES
from utils.date import date_to_str, str_to_date

# model = GeminiModel("gemini-1.5-flash", api_key=GEMINI_API_KEY)
model = GroqModel("llama-3.1-70b-versatile")
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
def current_date() -> str:
    """
    Returns the current date as a string in the format "dd/mm/yyyy".
    Returns:
        str: The current date in the format "dd/mm/yyyy".
    """

    return date_to_str(datetime.now())


@agent.tool_plain
def sales(start_date: str, end_date: str) -> List[Sale]:
    """
    Returns a list of sales between start_date and end_date.
    Args:
        start_date (str): The start date in the format 'dd/mm/yyyy'.
        end_date (str): The end date in the format 'dd/mm/yyyy'.
    Returns:
        List[Sale]: A list of Sale between the start and end dates.
    """

    start = str_to_date(start_date)
    end = str_to_date(end_date)

    sales_data = [
        sale for sale in MOCK_SALES if start <= str_to_date(sale["date"]) <= end
    ]

    return [Sale(**data) for data in sales_data]
