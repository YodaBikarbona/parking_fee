from typing import List

from main.api.base.base import Session
from main.api.ticket.model.ticketentity import TicketEntity


def get_ticket_by_id(session: Session, ticket_id: int, user_id: int) -> TicketEntity:
    return session.query(TicketEntity).filter(
        TicketEntity.id == ticket_id,
        TicketEntity.user_id == user_id
    ).first()


def fetch_all_tickets(session: Session, user_id: int) -> List[TicketEntity]:
    return session.query(TicketEntity).filter(
        TicketEntity.user_id == user_id
    ).all()
