from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_tables
from . import routers

app = FastAPI(title="AI Multi-Agent Ticket Resolver")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This function correctly sets up your database tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()

# All the agent logic you have in the Canvas will now be used.
app.include_router(routers.router, prefix="/api")

# Optional: A simple root endpoint to check if the API is running
@app.get("/")
def read_root():
    return {"status": "API is running"}

