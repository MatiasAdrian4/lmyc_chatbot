import requests
from typing import List, Optional

from settings import LUBRICENTRO_MYC_URL
from services.lmyc_client.models import Sale, Client, to_client
from tests.mocks.lmyc_client import MOCK_SALES
from utils.date import str_to_date


class LMYCClient:
    def get_clients(self, name: str) -> List[Client]:
        response = requests.post(
            f"{LUBRICENTRO_MYC_URL}/clients/",
            json={"name": name},
        )
        if response.status_code == 200:
            data = response.json()
            return [to_client(client) for client in data.get("clients", [])]
        else:
            return []

    def get_sales(
        self, start_date: str, end_date: str, category: Optional[str] = None
    ) -> List[Sale]:
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
