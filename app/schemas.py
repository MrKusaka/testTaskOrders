from pydantic import BaseModel


class CreateOrder(BaseModel):
    name: str
    description: str
    price: int
    image_url: str
    quantity: int
    status: str

