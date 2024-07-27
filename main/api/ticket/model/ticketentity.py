from sqlalchemy import Integer, Column, String, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship

from main.api.base.model.base_model import BaseModel
from main.api.user.model.user import User


class TicketEntity(BaseModel):
    __tablename__ = 'tickets'

    # Columns
    duration = Column(Integer, nullable=False, default=30)
    registration_plate = Column(String, nullable=False)
    location = Column(String, nullable=False)
    extended_minutes = Column(Integer, nullable=False, default=0)

    # Foreign keys
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)

    # Relationships
    user = relationship(User)

    # Constraints
    CheckConstraint('duration >= 30 AND duration <= 180', name='check_duration_range'),

    def extend_ticket_for_30_minutes(self):
        self.extended_minutes += 30
        self.check_duration_range()

    def extend_ticket_for_one_hour(self):
        self.extended_minutes += 60
        self.check_duration_range()

    def extent_ticket_for_2_hours(self):
        self.extended_minutes += 120
        self.check_duration_range()

    def check_duration_range(self):
        if not (30 <= self.duration + self.extended_minutes <= 180):
            raise ValueError('The duration must be between 30 and 180 minutes!')
