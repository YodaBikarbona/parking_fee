from pydantic.v1 import BaseModel


class Login(BaseModel):
    id: int
    username: str
