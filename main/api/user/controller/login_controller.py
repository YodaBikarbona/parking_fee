from fastapi import APIRouter
from starlette import status

from main.api.config import settings
from main.api.exceptions.internal_server_error import InternalServerErrorException
from main.api.exceptions.not_found import NotFoundException
from main.api.user.serializer.request.login_user import LoginUser
from main.api.user.service.user_service import login_user
from main.api.utils.response_util import (
    ok_response,
    error_response,
)

router = APIRouter(
    prefix=f'{settings.route}/login',
    tags=['login'],
)


@router.post('')
async def login(data: LoginUser):
    try:
        response = login_user(data)
        return ok_response(
            message='Successfully logged in!',
            **{'data': response.get('login').dict()},
            cookies={
                "Authorization": f"Bearer {response.get('access_token')}",
                "refresh_token": f"Bearer {response.get('refresh_token')}",
            },
            status_code=status.HTTP_200_OK,
        )
    except (NotFoundException, InternalServerErrorException) as e:
        return error_response(message=e.message, status_code=e.status_code)
