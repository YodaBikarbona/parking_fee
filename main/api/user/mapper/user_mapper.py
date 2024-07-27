from main.api.user.model.user import User
from main.api.user.serializer.request.register_user import NewUser
from main.api.user.serializer.response.login import Login


def mapper_new_user_to_user(new_user: NewUser) -> User:
    user = User()
    user.username = new_user.username
    user.password = user.encrypt_psw(new_user.password)
    return user


def mapper_user_to_login(user: User) -> Login:
    return Login(id=user.id, username=user.username)
