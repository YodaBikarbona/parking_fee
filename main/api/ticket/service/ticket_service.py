from typing import List

from main.api.base.base import Session
from main.api.exceptions.internal_server_error import InternalServerErrorException
from main.api.exceptions.not_found import NotFoundException
from main.api.logger.logger import logger
from main.api.ticket.mapper.ticket_mapper import (
    mapper_new_ticket_to_ticket_entity,
    mapper_ticket_entity_to_ticket, mapper_ticket_entities_to_tickets,
)
from main.api.ticket.repository.ticket_repository import get_ticket_by_id, fetch_all_tickets
from main.api.ticket.serializer.request.new_ticket import NewTicket
from main.api.ticket.serializer.response.ticket import Ticket


def create_new_ticket(new_ticket: NewTicket) -> Ticket:
    with Session.begin() as session:
        try:
            ticket = mapper_new_ticket_to_ticket_entity(new_ticket=new_ticket)
            session.add(ticket)
            return mapper_ticket_entity_to_ticket(ticket_entity=ticket)
        except Exception as e:
            session.rollback()
            logger.error('Failed to create new ticket!', e)
            raise InternalServerErrorException()


def get_ticket(ticket_id: int, user_id: int) -> Ticket:
    with Session.begin() as session:
        try:
            ticket = get_ticket_by_id(session=session, ticket_id=ticket_id, user_id=user_id)
            if not ticket:
                raise NotFoundException("The ticket doesn't exist!")
            return mapper_ticket_entity_to_ticket(ticket_entity=ticket)
        except Exception as e:
            session.rollback()
            logger.error('Failed to get ticket!', e)
            raise InternalServerErrorException()


def get_all_tickets(user_id: int) -> List[Ticket]:
    with Session.begin() as session:
        try:
            tickets = fetch_all_tickets(session=session, user_id=user_id)
            if not tickets:
                raise NotFoundException("The tickets don't exist!")
            return mapper_ticket_entities_to_tickets(tickets)
        except Exception as e:
            session.rollback()
            logger.error('Failed to get tickets!', e)
            raise InternalServerErrorException()


