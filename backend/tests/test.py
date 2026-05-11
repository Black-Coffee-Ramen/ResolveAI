import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Add the parent directory to the path to allow imports from app
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.models import Base, get_db

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the test database
Base.metadata.create_all(bind=engine)

def override_get_db():
    """
    Dependency override to use the test database session.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def cleanup_db():
    """
    Fixture to clean up the test database after tests are done.
    """
    yield
    if os.path.exists("./test.db"):
        os.remove("./test.db")

def test_create_and_get_ticket():
    """
    Test creating a ticket and then retrieving it to ensure correctness.
    """
    # Test POST request to create a ticket
    response_create = client.post(
        "/tickets",
        json={"title": "Urgent Billing Issue", "description": "I have an urgent problem with my recent invoice payment."},
    )
    assert response_create.status_code == 201
    data = response_create.json()
    assert data["title"] == "Urgent Billing Issue"
    assert data["category"] == "billing"
    assert data["priority"] == "high"
    assert data["status"] == "escalated" # The agent will escalate this
    assert "escalated" in data["resolution"]

    # Test GET request to retrieve tickets
    response_get = client.get("/tickets")
    assert response_get.status_code == 200
    tickets = response_get.json()
    assert len(tickets) > 0
    assert tickets[0]["title"] == "Urgent Billing Issue"

def test_root_endpoint():
    """
    Test the root endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AI Multi-Agent Ticket Resolver API!"}
