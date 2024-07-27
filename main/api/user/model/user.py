from hashlib import sha512

from sqlalchemy import (
    Column,
    Unicode,
    Boolean,
    # UniqueConstraint,
    Sequence,
)

from main.api.base.base import Base, engine
from main.api.base.model.base_model import BaseModel
from main.api.utils.util import generate_random_string


class User(BaseModel):
    __tablename__ = 'users'

    # Columns
    username = Column(Unicode(32), nullable=False, unique=True)
    password = Column(Unicode(32), nullable=False)
    activated = Column(Boolean, default=False)
    salt = Column(Unicode(255), nullable=False, default=generate_random_string())

    # Constraints
    # UniqueConstraint(username, name="unique_username")

    def __str__(self):
        return f"UserID: {self.id}, username: {self.username}"

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False

    def encrypt_psw(self, password_row: str) -> str:
        password = str(sha512(u'{0}{1}'.format(password_row, self.salt)
                              .encode('utf-8', 'ignore')).hexdigest())
        return password

    def is_password_valid(self, password_row: str) -> bool:
        return self.encrypt_psw(password_row) == self.password


User.__table__.columns['id'].sequence = Sequence('user_id_seq')
Base.metadata.create_all(engine)
