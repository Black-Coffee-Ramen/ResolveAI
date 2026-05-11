import os
import enum
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Enum, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/tickets.db")

Base = declarative_base()

class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING_APPROVAL = "pending_approval"
    RESOLVED = "resolved"
    REJECTED = "rejected"
    ESCALATED = "escalated"

class TicketCategory(str, enum.Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    GENERAL = "general"

class TicketPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Ticket(Base):
    """
    Represents a support ticket in the database.
    Includes timestamps and RAG context for HITL workflow and metrics.
    """
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    category = Column(Enum(TicketCategory), default=TicketCategory.GENERAL)
    priority = Column(Enum(TicketPriority), default=TicketPriority.LOW)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN)
    # AI-generated draft response
    resolution = Column(Text, nullable=True)
    # The RAG context retrieved, stored for the analyst to review
    rag_context = Column(Text, nullable=True)
    # Whether the analyst edited the AI draft (True = edited, False = approved as-is)
    was_edited = Column(String, nullable=True)  # "true" or "false"

    # Timestamps for flow metrics
    created_at = Column(DateTime, default=datetime.utcnow)
    triaged_at = Column(DateTime, nullable=True)   # when status -> PENDING_APPROVAL
    resolved_at = Column(DateTime, nullable=True)  # when status -> RESOLVED

# Database setup — uses PostgreSQL in Docker, falls back to SQLite locally
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get a new database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
