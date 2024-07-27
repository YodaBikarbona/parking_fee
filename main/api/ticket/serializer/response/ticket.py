from pydantic.v1 import BaseModel


class Ticket(BaseModel):
    id: int
    created_at: str
    registration_plate: str
    duration: int
    location: str
    extended: str
