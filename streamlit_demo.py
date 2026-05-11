import streamlit as st
import enum
import os
import google.generativeai as genai

# --- Secure API Key Configuration ---

# This function securely gets the API key.
# 1. It first tries to get the key from Streamlit's secrets management.
# 2. If not found (i.e., when running locally), it falls back to an environment variable.
def get_api_key():
    if "GOOGLE_API_KEY" in st.secrets:
        return st.secrets["GOOGLE_API_KEY"]
    else:
        return os.environ.get("GOOGLE_API_KEY")

api_key = get_api_key()

# Configure the Gemini API only if the key is available
if api_key:
    genai.configure(api_key=api_key)
else:
    # Display a warning on the Streamlit page if the key is missing
    st.warning("Google API Key not configured. Please set it in your Streamlit secrets or environment variables.")


# --- Agent and Model Definitions (Self-contained for standalone deployment) ---
class LLMProvider:
    """A simple wrapper for the Gemini model."""
    def __init__(self, model_name="gemini-1.5-flash-latest"):
        if not api_key:
            self.model = None
            return
        self.model = genai.GenerativeModel(model_name)

    def predict(self, prompt: str) -> str:
        if not self.model:
            return "API Key not configured."
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip().replace("`", "").replace("json", "").strip()
        except Exception as e:
            return f"Error calling LLM: {e}"


class TicketCategory(str, enum.Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    GENERAL = "general"

class TicketPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    ESCALATED = "escalated"

class ClassificationAgent:
    def __init__(self):
        self.llm = LLMProvider()

    def predict(self, description: str) -> TicketCategory:
        prompt = f"Classify the following ticket description into one of these categories: billing, technical, or general. Return only a single word.\n\nDescription: \"{description}\"\nCategory:"
        predicted_category_str = self.llm.predict(prompt).lower()
        if "billing" in predicted_category_str: return TicketCategory.BILLING
        elif "technical" in predicted_category_str: return TicketCategory.TECHNICAL
        else: return TicketCategory.GENERAL

class PriorityAgent:
    def __init__(self):
        self.llm = LLMProvider()

    def predict(self, description: str) -> TicketPriority:
        prompt = f"Analyze the urgency of the following ticket description and classify its priority as: low, medium, or high. Return only a single word.\n\nDescription: \"{description}\"\nPriority:"
        predicted_priority_str = self.llm.predict(prompt).lower()
        if "high" in predicted_priority_str: return TicketPriority.HIGH
        elif "medium" in predicted_priority_str: return TicketPriority.MEDIUM
        else: return TicketPriority.LOW

class ResolutionAgent:
    def __init__(self):
        self.llm = LLMProvider()
    
    def predict(self, description: str, category: TicketCategory) -> str:
        prompt = f"You are a support agent. Based on the ticket description and its category ('{category.value}'), provide a concise suggested solution or state that it has been escalated.\n\nDescription: \"{description}\"\nResponse:"
        return self.llm.predict(prompt)

# --- Streamlit UI ---

st.set_page_config(layout="wide")
st.title("🤖 AI Multi-Agent Ticket Resolver Demo")
st.write("Enter the details of your support issue below, and our AI agents will automatically process and categorize it.")

# User Input Form
with st.form(key='ticket_form'):
    title = st.text_input("Ticket Title", placeholder="e.g., Unable to access my account")
    description = st.text_area("Ticket Description", height=200, placeholder="Describe your issue in detail...")
    submit_button = st.form_submit_button(label='Process Ticket')

# Agent Processing and Output
if submit_button and title and description:
    if not api_key:
        st.error("Cannot process ticket: Google API Key is not configured.")
    else:
        with st.spinner('AI agents are analyzing your ticket...'):
            classification_agent = ClassificationAgent()
            priority_agent = PriorityAgent()
            resolution_agent = ResolutionAgent()

            category = classification_agent.predict(description)
            priority = priority_agent.predict(description)
            resolution = resolution_agent.predict(description, category)
            
            status = TicketStatus.RESOLVED if "suggested solution" in resolution.lower() else TicketStatus.ESCALATED

        st.success("Ticket processed successfully!")
        
        st.subheader("Agent Analysis Dashboard")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Category", category.value.capitalize())
        col2.metric("Assigned Priority", priority.value.capitalize())
        col3.metric("Ticket Status", status.value.replace('_', ' ').capitalize())

        st.markdown("---")
        
        st.subheader("Proposed Resolution / Action")
        if status == TicketStatus.RESOLVED:
            st.info(resolution)
        else:
            st.warning(resolution)
else:
    if submit_button:
        st.error("Please fill in both the title and description fields.")

