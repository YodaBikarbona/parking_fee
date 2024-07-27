from pydantic.v1 import (
    BaseModel,
    validator,
)


class NewTicket(BaseModel):
    registration_plate: str
    duration: int
    location: str

    @validator('duration')
    def validate_duration(cls, value):
        if not (30 <= value <= 180):
            raise ValueError('The duration must be between 30 and 180 minutes!')
        return value
