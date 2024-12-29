import requests
from typing import List, Optional

from settings import LUBRICENTRO_MYC_URL
from services.lmyc_client.models import Sale, Client, to_client, to_sale


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

    def get_sales(self, start_date: str, end_date: str) -> List[Sale]:
        response = requests.post(
            f"{LUBRICENTRO_MYC_URL}/sales/",
            json={"start_date": start_date, "end_date": end_date},
        )
        if response.status_code == 200:
            data = response.json()
            return [to_sale(sale) for sale in data.get("sales", [])]
        else:
            return []
