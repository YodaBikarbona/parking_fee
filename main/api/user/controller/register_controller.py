from fastapi import APIRouter
from starlette import status

from main.api.config import settings
from main.api.exceptions.bad_request import BadRequestException
from main.api.exceptions.internal_server_error import InternalServerErrorException
from main.api.user.serializer.request.register_user import NewUser
from main.api.user.service.user_service import register_new_user
from main.api.utils.response_util import error_response, ok_response

router = APIRouter(
    prefix=f'{settings.route}/register',
    tags=['register'],
)


@router.post('')
async def register(data: NewUser):
    try:
        register_new_user(data)
        return ok_response(message='Successfully registered', status_code=status.HTTP_201_CREATED)
    except (BadRequestException, InternalServerErrorException) as e:
        return error_response(message=e.message, status_code=e.status_code)
