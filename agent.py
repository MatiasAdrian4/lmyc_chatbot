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
        "Actúa como un asistente virtual para un lubricentro. Responde a las preguntas "
        "de los usuarios de manera clara, específica y breve. No incluyas explicaciones "
        "ni detalles adicionales a menos que te los soliciten explícitamente. Si el "
        "usuario pregunta por cifras, proporciona únicamente el dato solicitado."
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

    print(f"clients tool called with {name}")

    lmyc_client = LMYCClient()
    return lmyc_client.get_clients(name)


@agent.tool_plain()
def amount_of_sales(start_date: str, end_date: str) -> int:
    """
    Calculate the amount of sales between two dates.

    Args:
        start_date (str): The start date in the format "dd/mm/yyyy".
        end_date (str): The end date in the format "dd/mm/yyyy".

    Returns:
        int: The number of sales between the start and end dates.
    """

    print(f"amount_of_sales tool called with {start_date} and {end_date}")

    lmyc_client = LMYCClient()
    sales_in_period = lmyc_client.get_sales(start_date, end_date)
    return len(sales_in_period)


@agent.tool_plain()
def total_price_of_sales(start_date: str, end_date: str) -> float:
    """
    Calculate the total price of sales within a specified date range.

    Args:
        start_date (str): The start date of the period in "dd/mm/yyyy" format.
        end_date (str): The end date of the period in "dd/mm/yyyy" format.

    Returns:
        float: The total price of all sales within the specified date range.
    """

    print(f"total_price_of_sales tool called with {start_date} and {end_date}")

    lmyc_client = LMYCClient()
    sales_in_period = lmyc_client.get_sales(start_date, end_date)
    return sum(sale.price for sale in sales_in_period)
