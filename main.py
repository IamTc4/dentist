from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

from database import engine, Base, get_db, DemoRequest, Appointment

# Create DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DentaFlow AI Backend", version="1.0")

# -----------------
# HTML Routes
# -----------------

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("code.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: code.html not found</h1>", status_code=404)

@app.get("/booking", response_class=HTMLResponse)
async def read_booking():
    try:
        with open("booking.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: booking.html not found</h1>", status_code=404)

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard():
    try:
        with open("dashboard.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: dashboard.html not found</h1>", status_code=404)

# -----------------
# Pydantic Schemas
# -----------------

class DemoBookingRequestModel(BaseModel):
    name: str
    email: str
    phone: str
    clinicName: str
    message: Optional[str] = ""

class AppointmentModel(BaseModel):
    patient_name: str
    patient_phone: str
    service_type: str
    appointment_time: str

class AppointmentResponse(AppointmentModel):
    id: int
    status: str
    created_at: str

    class Config:
        from_attributes = True

class DemoResponse(BaseModel):
    id: int
    name: str
    email: str
    clinic_name: str
    message: Optional[str] = ""
    created_at: str

    class Config:
        from_attributes = True

# -----------------
# API Routes
# -----------------

@app.post("/api/book-demo")
async def book_demo(booking: DemoBookingRequestModel, db: Session = Depends(get_db)):
    new_request = DemoRequest(
        name=booking.name,
        email=booking.email,
        phone=booking.phone,
        clinic_name=booking.clinicName,
        message=booking.message
    )
    db.add(new_request)
    db.commit()
    print(f"Received demo request from {booking.name} for clinic {booking.clinicName}")
    return {"status": "success", "message": "Demo request received successfully!"}

@app.get("/api/demos", response_model=List[DemoResponse])
async def get_demos(db: Session = Depends(get_db)):
    demos = db.query(DemoRequest).order_by(DemoRequest.created_at.desc()).all()
    # Manual serialization since datetime needs string conversion for Pydantic in simple setup
    return [{
        "id": d.id,
        "name": d.name,
        "email": d.email,
        "clinic_name": d.clinic_name,
        "message": d.message,
        "created_at": d.created_at.isoformat()
    } for d in demos]


@app.post("/api/appointments")
async def book_appointment(apt: AppointmentModel, db: Session = Depends(get_db)):
    new_apt = Appointment(
        patient_name=apt.patient_name,
        patient_phone=apt.patient_phone,
        service_type=apt.service_type,
        appointment_time=apt.appointment_time
    )
    db.add(new_apt)
    db.commit()
    return {"status": "success", "message": "Appointment booked successfully!"}

@app.get("/api/appointments", response_model=List[AppointmentResponse])
async def get_appointments(db: Session = Depends(get_db)):
    apts = db.query(Appointment).order_by(Appointment.appointment_time.asc()).all()
    return [{
        "id": a.id,
        "patient_name": a.patient_name,
        "patient_phone": a.patient_phone,
        "service_type": a.service_type,
        "appointment_time": a.appointment_time,
        "status": a.status,
        "created_at": a.created_at.isoformat()
    } for a in apts]


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
