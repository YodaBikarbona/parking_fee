from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

from main.api.authorization.authorization import get_current_user_id
from main.api.config import settings
from main.api.exceptions.internal_server_error import InternalServerErrorException
from main.api.exceptions.not_found import NotFoundException
from main.api.ticket.serializer.request.new_ticket import NewTicket
from main.api.ticket.service.ticket_service import (
    create_new_ticket,
    get_ticket,
    get_all_tickets,
)
from main.api.utils.response_util import (
    ok_response,
    error_response,
)

router = APIRouter(
    prefix=f'{settings.route}/tickets',
    tags=['tickets'],
)


@router.post('/new')
async def new_ticket(data: NewTicket):
    try:
        response = create_new_ticket(new_ticket=data)
        return ok_response(
            message='Ticket created successfully!',
            data=response.dict(),
            status_code=status.HTTP_201_CREATED,
        )
    except InternalServerErrorException as e:
        return error_response(message=e.message, status_code=e.status_code)


@router.get('/{_id}')
async def get_ticket_by_id(_id: int, user_id: int = Depends(get_current_user_id)):
    try:
        response = get_ticket(ticket_id=_id, user_id=user_id)
        return ok_response(
            message='Ticket',
            **{'data': response.dict()},
            status_code=status.HTTP_201_CREATED,
        )
    except (NotFoundException, InternalServerErrorException) as e:
        return error_response(message=e.message, status_code=e.status_code)


@router.get('')
async def all_tickets(user_id: int = Depends(get_current_user_id)):
    try:
        response = get_all_tickets(user_id=user_id)
        return ok_response(
            message='Ticket',
            **{'data': [r.dict() for r in response]},
            status_code=status.HTTP_201_CREATED,
        )
    except (NotFoundException, InternalServerErrorException) as e:
        return error_response(message=e.message, status_code=e.status_code)
