import os
from google import genai
from google.genai import types
from .database import TicketCategory, TicketPriority


# ==============================================================================
# LLM Factory — swap providers with a single ENV variable
# ==============================================================================

def get_llm_provider():
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    if provider == "gemini":
        return GeminiProvider()
    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")


class GeminiProvider:
    """Gemini LLM backend using the new google-genai SDK."""
    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest")
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            print("WARNING: GOOGLE_API_KEY not set. LLM calls will fail.")
            self.client = None

    def predict(self, prompt: str) -> str:
        if self.client is None:
            return "error: llm_not_configured"
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.1),
            )
            return response.text.strip()
        except Exception as e:
            print(f"[LLM ERROR] {e}")
            return "error"


# ==============================================================================
# AI-Powered Agents
# ==============================================================================

class ClassificationAgent:
    """
    Agent 1: Categorizes the ticket into billing / technical / general.
    """
    def __init__(self):
        self.llm = get_llm_provider()

    def predict(self, description: str) -> TicketCategory:
        prompt = f"""
        Classify the following support ticket description into exactly one of these categories: 
        billing, technical, or general.
        
        Return ONLY a single word. No explanation.
        
        Description: "{description}"
        Category:
        """
        result = self.llm.predict(prompt).lower()
        if "billing" in result:
            return TicketCategory.BILLING
        elif "technical" in result:
            return TicketCategory.TECHNICAL
        return TicketCategory.GENERAL


class PriorityAgent:
    """
    Agent 2: Determines ticket urgency from sentiment and keywords.
    """
    def __init__(self):
        self.llm = get_llm_provider()

    def predict(self, description: str) -> TicketPriority:
        prompt = f"""
        Analyze the urgency of the following support ticket.
        Consider keywords like "urgent", "broken", "can't access", "data loss" as high priority.
        
        Return ONLY one word: low, medium, or high.
        
        Description: "{description}"
        Priority:
        """
        result = self.llm.predict(prompt).lower()
        if "high" in result:
            return TicketPriority.HIGH
        elif "medium" in result:
            return TicketPriority.MEDIUM
        return TicketPriority.LOW


class ResolutionAgent:
    """
    Agent 3: Drafts a grounded response using RAG context.
    Uses category and priority from previous agents to tailor the response.
    """
    def __init__(self):
        self.llm = get_llm_provider()

    def predict(self, description: str, category: TicketCategory, priority: TicketPriority, context: str) -> str:
        prompt = f"""
        You are a helpful customer support agent. Draft a professional first-response to this support ticket.
        
        STRICT RULES:
        1. Ground your response ONLY in the Documentation provided below.
        2. If the documentation does not cover the issue, say: "I don't have specific information on this topic. A specialist will follow up shortly."
        3. Never invent policies, phone numbers, URLs, or procedures not in the documentation.
        4. If priority is "high", open with acknowledgment of urgency.
        5. Keep the response concise (2-4 sentences max).
        
        Ticket Category: {category.value}
        Priority: {priority.value}
        Description: "{description}"
        
        Relevant Documentation:
        ---
        {context}
        ---
        
        Draft Response:
        """
        return self.llm.predict(prompt)
