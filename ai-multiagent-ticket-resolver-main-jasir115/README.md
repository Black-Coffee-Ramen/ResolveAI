🤖 AI Multi-Agent Ticket Resolver
An automated support ticket processing system powered by a multi-agent AI pipeline. This project uses FastAPI for the backend, React for the frontend, and Docker for containerization.


🎯 The Problem: Inefficient Ticket Handling
Customer support teams are often overwhelmed by the sheer volume of incoming tickets. Manually triaging, categorizing, prioritizing, and responding to each ticket is a time-consuming and repetitive process. This leads to:

😠 Delayed response times for customers.

🤷 Inconsistent categorization and prioritization.

💸 High operational costs due to manual labor.

😩 Agent burnout from handling mundane, repetitive tasks.

✨ Solution: A Multi-Agent AI System
Instead of using a single, monolithic AI model, this project employs a multi-agent system. This approach is more effective because it mimics a real-world support team where different specialists handle different tasks.

Specialization: Each agent is an "expert" in its specific task (e.g., classification, priority assessment), leading to more accurate and reliable results.

Modularity: Agents can be updated, improved, or replaced independently without affecting the entire system.

Transparency: It's easier to understand and debug the decision-making process of specialized agents compared to a single black-box model.

🚀 How It Works: The Agent Pipeline
This application provides a full-stack solution for automating the initial stages of support ticket management. A user submits a ticket through a web interface, which is then processed by a pipeline of AI agents in the backend. The system automatically assigns a category, priority, and a suggested resolution, which is then displayed on a dashboard.

When a ticket is submitted, it passes through a sequential pipeline of agents:

Ticket Submission ➔ [Classification Agent] ➔ [Priority Agent] ➔ [Resolution Agent] ➔ Final Output

Classification Agent: Reads the ticket description and categorizes it as Technical, Billing, or General.

Priority Agent: Analyzes the text for keywords and sentiment indicating urgency and assigns a priority level: Low, Medium, or High.

Resolution Agent: Based on the ticket's category and content, it either provides a common solution for simple issues or escalates the ticket for human review.

🧠 LLM Selection
Ideal LLM (Production): Gemini 1.5 Pro. Its large context window and advanced reasoning capabilities are perfect for understanding complex, jargon-heavy tickets and generating nuanced, multi-step solutions.

Free-Tier LLM (Used in this Demo): Gemini 1.5 Flash. This model is extremely fast and cost-effective, making it ideal for the high-volume, focused tasks of classification and prioritization. Its performance is more than sufficient for the defined agent roles in this project.

🛠️ Tech Stack
Area

Technology

Backend

FastAPI, SQLAlchemy (ORM)

Frontend

React, Vite, TailwindCSS

Database

SQLite

AI / LLM

Google Gemini API (google-generativeai)

Deployment

Docker, Docker Compose

Demo

Streamlit

🏁 Getting Started
Prerequisites
Python 3.8+

Node.js 18+ and npm

Docker and Docker Compose

Option 1: Running with Docker (Recommended)
This is the easiest way to get the entire application running.

Clone the repository:

git clone [https://github.com/jasir115/ai-multiagent-ticket-resolver.git](https://github.com/jasir115/ai-multiagent-ticket-resolver.git)
cd ai-ticket-resolver

Create your environment file:
Copy the .env.example to a new file named .env and add your GOOGLE_API_KEY.

Build and run the services:

docker-compose up --build

Access the applications:

Frontend (React App): http://localhost:8080

Backend (FastAPI Docs): http://localhost:8000/docs

Option 2: Running Services Locally
Backend (FastAPI)
Navigate to the backend directory:

cd backend/

Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Run the FastAPI server:

uvicorn app.main:app --reload

The backend will be available at http://localhost:8000.

Frontend (React)
Navigate to the frontend directory:

cd frontend/

Install dependencies:

npm install

Start the Vite development server:

npm run dev

The frontend will be available at http://localhost:5173. It is pre-configured to proxy API requests to the backend.

Running the Streamlit Demo
The standalone demo showcases the agent logic without needing the full backend/frontend stack.

Install dependencies:

pip install streamlit

Run the Streamlit app:

streamlit run streamlit_demo.py
