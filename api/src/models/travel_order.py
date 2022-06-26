from pydantic import BaseModel


class TravelOrder(BaseModel):
    travel_order: str
