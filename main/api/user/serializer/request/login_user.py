from pydantic.v1 import (
    BaseModel,
    Field,
)


class LoginUser(BaseModel):
    username: str = Field(min_length=6)
    password: str
