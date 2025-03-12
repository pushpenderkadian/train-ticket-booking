from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.tickets import Ticket,func

async def get_available_tickets(db: AsyncSession):
    confirmed = (await db.execute(select(func.count()).where(Ticket.status == "confirmed"))).scalar()
    rac = (await db.execute(select(func.count()).where(Ticket.status == "RAC"))).scalar()
    waiting = (await db.execute(select(func.count()).where(Ticket.status == "waiting"))).scalar()

    return [confirmed, rac, waiting]
