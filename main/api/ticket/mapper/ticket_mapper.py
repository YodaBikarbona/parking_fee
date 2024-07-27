from typing import List

from main.api.ticket.model.ticketentity import TicketEntity
from main.api.ticket.serializer.request.new_ticket import NewTicket
from main.api.ticket.serializer.response.ticket import Ticket


def mapper_new_ticket_to_ticket_entity(new_ticket: NewTicket) -> TicketEntity:
    ticket = TicketEntity()
    ticket.duration = new_ticket.duration
    ticket.registration_plate = new_ticket.registration_plate
    ticket.location = new_ticket.location
    return ticket


def mapper_ticket_entity_to_ticket(ticket_entity: TicketEntity) -> Ticket:
    ticket = Ticket()
    ticket.id = ticket_entity.id
    ticket.created_at = ticket_entity.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f%Z")
    ticket.registration_plate = ticket_entity.registration_plate
    ticket.location = ticket_entity.location
    ticket.duration = ticket_entity.duration
    return ticket


def mapper_ticket_entities_to_tickets(ticket_entities: List[TicketEntity]) -> List[Ticket]:
    tickets = []
    for ticket_entity in ticket_entities:
        tickets.append(mapper_ticket_entity_to_ticket(ticket_entity))
    return tickets
