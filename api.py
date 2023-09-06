from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from main import main

app = FastAPI()

origins = [
    "http://localhost:3000",  # React
    "http://127.0.0.1:3000",  # React
    "https://rescanpre.netlify.app", # netlify
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HotelBooking(BaseModel):
    arrival_month: int
    arrival_year: int
    avg_price_per_room: float
    lead_time: int
    market_segment_type: int
    no_of_special_requests: int
    no_of_week_nights: int
    no_of_weekend_nights: int
    repeated_guest: int
    required_car_parking_space: int
    room_type_reserved: int
    type_of_meal_plan: int
    no_of_adults: int
    no_of_children: int
    arrival_date: int
    no_of_previous_cancellations: int
    no_of_previous_bookings_not_canceled: int
    
    
 
@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
   
@app.post("/V1/booking_status")
async def book_hotel(booking: HotelBooking):
    booking_status = main(booking)
    return {"booking_status": booking_status}

