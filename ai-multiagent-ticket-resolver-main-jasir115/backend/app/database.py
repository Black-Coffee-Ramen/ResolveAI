from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

DATABASE_URL = "sqlite:///./data/tickets.db"

Base = declarative_base()

class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
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
    """
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    category = Column(Enum(TicketCategory), default=TicketCategory.GENERAL)
    priority = Column(Enum(TicketPriority), default=TicketPriority.LOW)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN)
    resolution = Column(String, nullable=True)

# Database setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency to get a new database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)
