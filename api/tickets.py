from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from utils.ticket_utils import get_available_tickets
from models.tickets import Ticket
from models.passengers import Passenger
from models.child import Child
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi import HTTPException
from schemas import PassengerRequest
import random


router = APIRouter()

# Booking Logic
@router.post("/book")
async def book_ticket(request: PassengerRequest, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        
        confirmed_count, RAC_count, waiting_count = await get_available_tickets(db)
        if waiting_count >= 10:
            raise HTTPException(status_code=400, detail="No tickets available")
        
        lower_berth_priority = request.age >= 60 or (request.gender == "female" and request.with_infant)
        berth_type = "lower" if lower_berth_priority and confirmed_count < 63 else "middle"
        status="confirmed" if confirmed_count < 63 else "RAC" if RAC_count < 18 else "waiting"
        berth_type = "side-lower" if status == "RAC" else berth_type
        
        new_ticket = Ticket(status=status,berth_type=berth_type)
        db.add(new_ticket)
        await db.flush()
        
        passenger = Passenger(name=request.name, age=request.age, gender=request.gender, ticket_id=new_ticket.id,with_infant=request.with_infant)
        db.add(passenger)
        
        if request.with_infant:
            child = Child(name=request.child.name, age=request.child.age,gender=request.child.gender, parent_ticket_id=new_ticket.id)
            db.add(child)
        
        
        await db.commit()
        return {"ticket": new_ticket.id, "message": "Tickets booked successfully"}

# Cancellation Logic
@router.post("/cancel/{ticket_id}")
async def cancel_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        ticket = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
        ticket = ticket.scalars().first()
        
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        if ticket.status == "canceled":
            raise HTTPException(status_code=400, detail="Ticket is already canceled")

        # Cancel the ticket
        ticket.status = "canceled"
        ticket.berth_type = None
        
        # Promote RAC to confirmed (if available)
        rac_ticket = await db.execute(
            select(Ticket).where(Ticket.status == "RAC").order_by(Ticket.id)
        )
        rac_ticket = rac_ticket.scalars().first()
        
        if rac_ticket:
            rac_ticket.status = "confirmed"
            rac_ticket.berth_type = random.choice(["middle", "upper"])
            await db.flush()

            # Promote Waiting list to RAC (if available)
            waiting_ticket = await db.execute(
                select(Ticket).where(Ticket.status == "waiting").order_by(Ticket.id)
            )
            waiting_ticket = waiting_ticket.scalars().first()
            
            if waiting_ticket:
                waiting_ticket.status = "RAC"
                waiting_ticket.berth_type = "side-lower"
        
        await db.commit()
        return {"message": "Ticket canceled successfully"}




# Get Booked Tickets
@router.get("/booked")
async def get_booked_tickets(db: AsyncSession = Depends(get_db)):
    tickets = await db.execute(select(Ticket).where(Ticket.status == "confirmed", Passenger.ticket_id == Ticket.id))
    return {"total_booked":len(tickets),"data":tickets.scalars().all()}

# Get Available Tickets
@router.get("/available")
async def get_available_tickets_summary(db: AsyncSession = Depends(get_db)):
    confirmed,rac,waiting = await get_available_tickets(db)

    confirmed_tickets= (await db.execute(select(Ticket).filter(Ticket.status== "confirmed"))).scalars().all()
    rac_tickets= (await db.execute(select(Ticket).filter(Ticket.status== "RAC"))).scalars().all()
    waiting_tickets= (await db.execute(select(Ticket).filter(Ticket.status== "waiting"))).scalars().all()
    canceled_tickets= (await db.execute(select(Ticket).filter(Ticket.status== "canceled"))).scalars().all()
    return {"confirmed": 63 - confirmed, "RAC": 18 - rac, "waiting": 10 - waiting,"confirmed_ticket": confirmed_tickets, "RAC_ticket": rac_tickets, "waiting_ticket": waiting_tickets, "canceled_ticket": canceled_tickets}


# Get Ticket Details by ID
@router.get("/{ticket_id}")
async def get_ticket_details(ticket_id: int, db: AsyncSession = Depends(get_db)):
    ticket = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = ticket.scalars().first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    passengers = await db.execute(
        select(Passenger)
        .where(Passenger.ticket_id == ticket.id)
    )
    passengers = passengers.scalars().unique().one()
    
    return {"ticket_id": ticket.id, "status": ticket.status, "berth_type": ticket.berth_type, "passengers": passengers}
