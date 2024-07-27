from main.api.base.base import Session
from main.api.exceptions.bad_request import BadRequestException
from main.api.exceptions.internal_server_error import InternalServerErrorException
from main.api.exceptions.not_found import NotFoundException
from main.api.logger.logger import logger
from main.api.user.mapper.user_mapper import (
    mapper_new_user_to_user,
    mapper_user_to_login,
)
from main.api.user.repository.user_repository import find_user_by_username
from main.api.user.serializer.request.login_user import LoginUser
from main.api.user.serializer.request.register_user import NewUser
from main.api.utils.jwt_util import generate_token


def register_new_user(new_user: NewUser):
    with Session.begin() as session:
        try:
            user = find_user_by_username(session=session, username=new_user.username)
            if user:
                raise BadRequestException('User already exists!')
            user = mapper_new_user_to_user(new_user=new_user)
            session.add(user)
            logger.info(f'New user registered: ID: {user.id}, username: {new_user.username}')
        except Exception as e:
            session.rollback()
            logger.error(f'The registration of the new user failed, username:{new_user.username}', e)
            raise InternalServerErrorException()


def login_user(user: LoginUser) -> dict:
    with Session.begin() as session:
        try:
            user = find_user_by_username(session=session, username=user.username)
            if not user:
                raise NotFoundException("User doesn't exist!")
            return {
                'access_token': generate_token(user),
                'refresh_token': generate_token(user=user, is_access=False),
                'login': mapper_user_to_login(user=user),
            }
        except Exception as e:
            session.rollback()
            logger.error(f'The login of the new user failed, username:{user.username}', e)
            raise InternalServerErrorException()
