from sqlalchemy import Column, Integer, String, func
from db.session import Base
from sqlalchemy.orm import relationship

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(20),nullable=True)  # confirmed, RAC, waiting, canceled
    berth_type = Column(String(20), nullable=True)  # lower, middle, upper, side-lower

    passengers = relationship("Passenger", backref="ticket", lazy="joined", uselist=False)
