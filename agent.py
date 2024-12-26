from typing import List, Optional
from datetime import datetime

from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

from settings import GROQ_API_KEY

from services.lmyc_client.models import Client, Sale
from services.lmyc_client.service import LMYCClient
from utils.date import date_to_str

# model = GeminiModel("gemini-1.5-flash", api_key=GEMINI_API_KEY)
model = GroqModel("llama-3.1-70b-versatile", api_key=GROQ_API_KEY)
agent = Agent(
    model,
    system_prompt=(
        "Hola! Eres una asistente virtual que ayudara con cualquier tarea "
        "relacionada con la app. Quiero que seas conciso con tus respuestas y proveas "
        "informacion de ventas o fechas solo cuando se te pida."
    ),
)


@agent.tool_plain
def current_date() -> str:
    """
    Returns the current date as a string in the format "dd/mm/yyyy".
    Returns:
        str: The current date in the format "dd/mm/yyyy".
    """

    return date_to_str(datetime.now())


@agent.tool_plain
def clients(name: str) -> List[Client]:
    """
    Retrieve a list of clients based on the provided name.
    Args:
        name (str): The name of the client to search for.
    Returns:
        List[Client]: A list of Client objects that match the provided name.
    """
    print(f"Clients tool called with {name}")

    lmyc_client = LMYCClient()
    return lmyc_client.get_clients(name)


@agent.tool_plain
def sales(start_date: str, end_date: str, category: Optional[str] = None) -> List[Sale]:
    """
    Returns a list of sales between start_date and end_date.
    Args:
        start_date (str): The start date in the format 'dd/mm/yyyy'.
        end_date (str): The end date in the format 'dd/mm/yyyy'.
        category (Optional[str]): The category of the sale.
    Returns:
        List[Sale]: A list of Sale between the start and end dates.
    """
    print(f"Sales tool called with {start_date}, {end_date} and {category}")

    lmyc_client = LMYCClient()

    return lmyc_client.get_sales(start_date, end_date, category)
