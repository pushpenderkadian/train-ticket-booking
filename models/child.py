from sqlalchemy import Column, Integer, String, ForeignKey,func
from db.session import Base

class Child(Base):
    __tablename__ = "children"
    id = Column(Integer, primary_key=True, index=True)
    parent_ticket_id = Column(Integer, ForeignKey("passengers.ticket_id"), nullable=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
