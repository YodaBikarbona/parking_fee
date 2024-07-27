from main.api.base.base import Session
from main.api.user.model.user import User


def find_user_by_username(session: Session, username: str) -> User:
    return session.query(User).filter(User.username == username).first()
