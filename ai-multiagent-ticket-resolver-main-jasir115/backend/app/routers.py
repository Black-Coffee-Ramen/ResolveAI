from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

# Corrected imports to point directly to database.py and agent.py
from .database import Ticket, TicketCategory, TicketPriority, TicketStatus, get_db
from .agent import ClassificationAgent, PriorityAgent, ResolutionAgent

router = APIRouter()

# Pydantic models for request and response
class TicketCreate(BaseModel):
    title: str
    description: str

class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    resolution: str | None

    class Config:
        from_attributes = True

@router.post("/tickets", response_model=TicketResponse, status_code=201)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """
    Endpoint to submit a new ticket.
    The multi-agent system processes it to determine category, priority, and a suggested resolution.
    """
    # 1. Initialize Agents
    classification_agent = ClassificationAgent()
    priority_agent = PriorityAgent()
    resolution_agent = ResolutionAgent()

    # 2. Agent Predictions
    category = classification_agent.predict(ticket.description)
    priority = priority_agent.predict(ticket.description)
    resolution = resolution_agent.predict(ticket.description, category)
    
    # Use the correct Enum from database.py
    status = TicketStatus.RESOLVED if "Suggested Solution" in resolution else TicketStatus.ESCALATED

    # 3. Create Ticket record in DB using the model from database.py
    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        category=category,
        priority=priority,
        resolution=resolution,
        status=status,
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.get("/tickets", response_model=List[TicketResponse])
def get_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all tickets from the database.
    """
    tickets = db.query(Ticket).offset(skip).limit(limit).all()
    return tickets

