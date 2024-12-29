from typing import Dict, Any

from pydantic import BaseModel

from utils.date import iso_str_date_to_date


class Client(BaseModel):
    id: int
    name: str
    address: str
    city: str
    postal_code: str
    phone_number: str
    cuit: str
    email: str


def to_client(data: Dict[str, Any]) -> Client:
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
    quantity: float
    price: float
    date: str
    product_id: int
    product_detail: str


def to_sale(data: Dict[str, Any]) -> Sale:
    """
    Converts a dictionary representing sale data coming from
    "Lubricentro M&C" to a Sale object.
    """
    return Sale(
        id=data.get("id"),
        quantity=data.get("cantidad"),
        price=data.get("precio"),
        date=iso_str_date_to_date(data.get("fecha")),
        product_id=data.get("producto", {}).get("codigo"),
        product_detail=data.get("producto", {}).get("detalle"),
    )
