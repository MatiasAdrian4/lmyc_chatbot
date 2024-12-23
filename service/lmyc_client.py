from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from tests.mocks.lmyc_client import MOCK_SALES
from utils.date import str_to_date


class Sale(BaseModel):
    id: int
    description: str
    date: str
    price: float


class LMYCClient:
    def get_sales(
        self, start_date: str, end_date: str, category: Optional[str] = None
    ) -> List[Sale]:
        """
        Retrieve sales data within a specified date range and category.
        Args:
            start_date (str): The start date of the sales period in the format 'dd/mm/yyyy'.
            end_date (str): The end date of the sales period in the format 'dd/mm/yyyy'.
            category (Optional[str]): The category of sales to filter by.
        Returns:
            List[Sale]: A list of Sale objects that match the specified criteria.
        """

        start_date = str_to_date(start_date)
        end_date = str_to_date(end_date)

        sales_data = [
            sale
            for sale in MOCK_SALES
            if start_date <= str_to_date(sale["date"]) <= end_date
        ]

        # TODO: improve it
        if category:
            sales_data = [
                sale for sale in sales_data if sale.get("category") == category
            ]

        return [Sale(**data) for data in sales_data]
