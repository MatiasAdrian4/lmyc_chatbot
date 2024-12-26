from typing import Dict, Union

from pydantic import BaseModel


class Client(BaseModel):
    id: int
    name: str
    address: str
    city: str
    postal_code: str
    phone_number: str
    cuit: str
    email: str


def to_client(data: Dict[str, Union[int, str]]) -> Client:
    """
    Converts a dictionary representing client data coming from
    "Lubricentro M&C" to a Client object.
    """
    return Client(
        id=data.get("id"),
        name=data.get("nombre"),
        address=data.get("direccion"),
        city=data.get("localidad"),
        postal_code=data.get("codigo_postal"),
        phone_number=data.get("telefono"),
        cuit=data.get("cuit"),
        email=data.get("email"),
    )


class Sale(BaseModel):
    id: int
    description: str
    date: str
    price: float
