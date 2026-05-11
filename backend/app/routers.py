from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timezone

from .database import Ticket, TicketCategory, TicketPriority, TicketStatus, get_db
from .agent import ClassificationAgent, PriorityAgent, ResolutionAgent
from .safety import precheck
from .corpus import build_corpus
from .retriever import SupportRetriever

router = APIRouter()

# Build retriever once at module load (singleton)
_corpus = build_corpus()
_retriever = SupportRetriever(_corpus) if _corpus else None


# ==============================================================================
# Pydantic Schemas
# ==============================================================================

class TicketCreate(BaseModel):
    title: str
    description: str

class ApproveRequest(BaseModel):
    final_resolution: Optional[str] = None  # If provided, analyst edited the draft

class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    resolution: Optional[str]
    rag_context: Optional[str]
    was_edited: Optional[str]
    created_at: datetime
    triaged_at: Optional[datetime]
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True

class MetricsResponse(BaseModel):
    total_tickets: int
    pending_approval: int
    resolved: int
    escalated: int
    rejected: int
    avg_time_to_triage_seconds: Optional[float]
    approval_without_edit_rate: Optional[float]  # 0.0 - 1.0
    escalation_rate: Optional[float]              # 0.0 - 1.0


# ==============================================================================
# Endpoints
# ==============================================================================

@router.post("/tickets", response_model=TicketResponse, status_code=201)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    """
    Submit a support ticket through the full multi-agent pipeline:
    Safety Precheck → RAG Retrieval → Classification → Priority → Resolution Draft
    Ticket lands in PENDING_APPROVAL (or ESCALATED if safety precheck fires).
    """
    # 1. Safety Precheck — runs BEFORE any LLM call
    safety_result = precheck(ticket.description)

    if safety_result:
        db_ticket = Ticket(
            title=ticket.title,
            description=ticket.description,
            category=TicketCategory.GENERAL,
            priority=TicketPriority.HIGH,
            status=TicketStatus.ESCALATED,
            resolution=f"[AUTO-ESCALATED] {safety_result['justification']}\n\n{safety_result['response']}",
            rag_context=None,
            triaged_at=datetime.utcnow(),
        )
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        return db_ticket

    # 2. Hybrid RAG Retrieval
    rag_context = "No relevant documentation found."
    if _retriever:
        docs = _retriever.retrieve(ticket.description, top_k=3)
        rag_context = _retriever.format_context(docs)

    # 3. Multi-Agent Pipeline
    classification_agent = ClassificationAgent()
    priority_agent = PriorityAgent()
    resolution_agent = ResolutionAgent()

    category = classification_agent.predict(ticket.description)
    priority = priority_agent.predict(ticket.description)
    resolution = resolution_agent.predict(ticket.description, category, priority, rag_context)

    # 4. Save with PENDING_APPROVAL — human must review before it's sent
    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        category=category,
        priority=priority,
        status=TicketStatus.PENDING_APPROVAL,
        resolution=resolution,
        rag_context=rag_context,
        triaged_at=datetime.utcnow(),
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


@router.post("/tickets/{ticket_id}/approve", response_model=TicketResponse)
def approve_ticket(ticket_id: int, body: ApproveRequest, db: Session = Depends(get_db)):
    """
    Human-in-the-Loop: Approve (and optionally edit) the AI's draft resolution.
    If final_resolution is provided, the draft was edited before approval.
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.status not in (TicketStatus.PENDING_APPROVAL, TicketStatus.OPEN):
        raise HTTPException(status_code=400, detail=f"Ticket is in '{ticket.status}' state and cannot be approved")

    was_edited = body.final_resolution is not None and body.final_resolution.strip() != (ticket.resolution or "").strip()
    if was_edited:
        ticket.resolution = body.final_resolution

    ticket.status = TicketStatus.RESOLVED
    ticket.was_edited = "true" if was_edited else "false"
    ticket.resolved_at = datetime.utcnow()

    db.commit()
    db.refresh(ticket)
    return ticket


@router.post("/tickets/{ticket_id}/reject", response_model=TicketResponse)
def reject_ticket(ticket_id: int, db: Session = Depends(get_db)):
    """
    Human-in-the-Loop: Reject the AI draft and mark for manual handling.
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.status = TicketStatus.REJECTED
    ticket.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/tickets", response_model=List[TicketResponse])
def get_tickets(status: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List tickets, optionally filtered by status.
    """
    query = db.query(Ticket)
    if status:
        try:
            query = query.filter(Ticket.status == TicketStatus(status))
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    return query.order_by(Ticket.id.desc()).offset(skip).limit(limit).all()


@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.get("/metrics", response_model=MetricsResponse)
def get_metrics(db: Session = Depends(get_db)):
    """
    Flow Metrics endpoint:
    - Total tickets, by status
    - Average time to triage (created_at → triaged_at)
    - Approval-without-edit rate (proxy for AI accuracy)
    - Escalation rate
    """
    total = db.query(func.count(Ticket.id)).scalar()
    pending = db.query(func.count(Ticket.id)).filter(Ticket.status == TicketStatus.PENDING_APPROVAL).scalar()
    resolved = db.query(func.count(Ticket.id)).filter(Ticket.status == TicketStatus.RESOLVED).scalar()
    escalated = db.query(func.count(Ticket.id)).filter(Ticket.status == TicketStatus.ESCALATED).scalar()
    rejected = db.query(func.count(Ticket.id)).filter(Ticket.status == TicketStatus.REJECTED).scalar()

    # Avg time to triage: only tickets that have been triaged
    triaged_tickets = db.query(Ticket).filter(Ticket.triaged_at != None).all()
    avg_triage_seconds = None
    if triaged_tickets:
        deltas = [(t.triaged_at - t.created_at).total_seconds() for t in triaged_tickets if t.created_at and t.triaged_at]
        if deltas:
            avg_triage_seconds = sum(deltas) / len(deltas)

    # Approval-without-edit rate
    reviewed = db.query(Ticket).filter(Ticket.was_edited != None).all()
    approval_rate = None
    if reviewed:
        no_edit = sum(1 for t in reviewed if t.was_edited == "false")
        approval_rate = round(no_edit / len(reviewed), 2)

    # Escalation rate
    escalation_rate = round(escalated / total, 2) if total > 0 else None

    return MetricsResponse(
        total_tickets=total,
        pending_approval=pending,
        resolved=resolved,
        escalated=escalated,
        rejected=rejected,
        avg_time_to_triage_seconds=avg_triage_seconds,
        approval_without_edit_rate=approval_rate,
        escalation_rate=escalation_rate,
    )
