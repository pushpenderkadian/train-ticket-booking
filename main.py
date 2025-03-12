from fastapi import FastAPI
from api import tickets
from db.session import engine, Base
import asyncio

app = FastAPI(title="Train Ticket Booking API")

# Register API routers
app.include_router(tickets.router, prefix="/api/v1/tickets", tags=["Tickets"])

# Create database tables on startup
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to the Train Ticket Booking API"}

if __name__ == "__main__":
    asyncio.run(init_db())