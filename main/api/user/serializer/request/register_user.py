from pydantic import Field
from pydantic.v1 import (
    BaseModel,
    root_validator,
)


class NewUser(BaseModel):
    username: str = Field(min_length=6)
    password: str
    confirm_password: str

    @root_validator
    def check_passwords_match(cls, values):
        if values.get('password') != values.get('confirm_password'):
            raise ValueError("Password and confirm password don't match")
        return values
