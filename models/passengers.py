from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,func
from db.session import Base
from sqlalchemy.orm import relationship

class Passenger(Base):
    __tablename__ = "passengers"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    with_infant = Column(Boolean, nullable=False)
    child = relationship("Child", backref="parent", uselist=False, lazy="joined")
