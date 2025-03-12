# Train Ticket Booking API

## Overview
The Train Ticket Booking API is a FastAPI-based backend service that allows users to book, cancel, and check ticket availability for train journeys. It uses asynchronous SQLAlchemy for database interactions and follows a structured modular approach.

## Features
- **Book Tickets**: Supports passenger booking with seat allocation logic.
- **Cancel Tickets**: Allows users to cancel booked tickets.
- **Check Available Tickets**: Provides details of available confirmed, RAC, and waiting tickets.
- **Retrieve Ticket Details**: Fetches ticket and passenger information.

## Technologies Used
- **FastAPI**: Web framework for the API.
- **SQLAlchemy**: ORM for database interactions.
- **MySQL / SQLite**: Database support (configurable via environment variables).
- **Python Asyncio**: Ensures non-blocking database operations.

## Installation
### Prerequisites
- Python 3.9+
- MySQL or SQLite
- Virtual environment (recommended)

### Setup Instructions
1. **Clone the repository**
   ```sh
   git clone https://github.com/pushpenderkadian/train-ticket-booking.git
   cd train-ticket-booking
   ```

2. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate     # For Windows
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update `DATABASE_URL` with your database credentials

5. **Run the application**
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

### For swagger UI visit : /docs

### Ticket Booking
- **`POST /api/v1/tickets/book`**
  - Request Body:
    ```json
    {
      "name": "John Doe",
      "age": 30,
      "gender": "male",
      "with_infant": false
    }
    ```
  - Response:
    ```json
    {
      "ticket": 1,
      "message": "Tickets booked successfully"
    }
    ```

### Ticket Cancellation
- **`POST /api/v1/tickets/cancel/{ticket_id}`**
  - Cancels the ticket with the given ID.
  - Response:
    ```json
    {
      "message": "Ticket canceled successfully"
    }
    ```

### Check Available Tickets
- **`GET /api/v1/tickets/available`**
  - Response:
    ```json
    {
      "confirmed": 50,
      "RAC": 10,
      "waiting": 5
    }
    ```

### Get Ticket Details
- **`GET /api/v1/tickets/{ticket_id}`**
  - Response:
    ```json
    {
      "ticket_id": 1,
      "status": "confirmed",
      "berth_type": "lower",
      "passengers": {
        "name": "John Doe",
        "age": 30,
        "gender": "male"
      }
    }
    ```

## Project Structure
```
train-ticket-booking/
│-- api/
│   ├── tickets.py      # API routes for booking and managing tickets
│-- db/
│   ├── session.py      # Database connection and session management
│-- models/
│   ├── tickets.py      # Ticket model
│   ├── passengers.py   # Passenger model
│   ├── child.py        # Child passenger model
│-- schemas.py          # Pydantic models for request validation
│-- utils/
│   ├── ticket_utils.py # Utility functions for ticket management
│-- config.py           # Environment variable configuration
│-- main.py             # Application entry point
│-- requirements.txt    # Required dependencies
│-- .env.example        # Example environment variables file
```

