import os
import google.generativeai as genai
from .database import TicketCategory, TicketPriority

# --- AI Integration ---
# Configure the Gemini API key
# This will read the GOOGLE_API_KEY you set in your terminal
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("ERROR: GOOGLE_API_KEY environment variable not set.")
    # The application will start, but any attempt to create a ticket will fail.
    pass


class LLMProvider:
    """A simple wrapper for the Gemini model to handle API calls."""
    def __init__(self, model_name="gemini-1.5-flash-latest"):
        self.model = genai.GenerativeModel(model_name)

    def predict(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            # Clean up the response to remove markdown or extra whitespace
            return response.text.strip().replace("`", "").replace("json", "").strip()
        except Exception as e:
            print(f"Error calling LLM: {e}")
            # Provides a default fallback if the API call fails
            return "general" 

# --- AI-Powered Agents ---

class ClassificationAgent:
    """
    Categorizes the ticket by using an LLM to analyze the description.
    """
    def __init__(self):
        self.llm = LLMProvider()

    def predict(self, description: str) -> TicketCategory:
        prompt = f"""
        Classify the following support ticket description into one of these categories: 
        billing, technical, or general.
        
        Return only a single word for the category.
        
        Description: "{description}"
        Category:
        """
        
        predicted_category_str = self.llm.predict(prompt).lower()
        
        if "billing" in predicted_category_str:
            return TicketCategory.BILLING
        elif "technical" in predicted_category_str:
            return TicketCategory.TECHNICAL
        else:
            return TicketCategory.GENERAL

class PriorityAgent:
    """
    Determines the ticket's priority using an LLM to analyze urgency.
    """
    def __init__(self):
        self.llm = LLMProvider()

    def predict(self, description: str) -> TicketPriority:
        prompt = f"""
        Analyze the sentiment and keywords of the following support ticket description
        to determine its priority: low, medium, or high.
        
        Return only a single word for the priority.
        
        Description: "{description}"
        Priority:
        """
        predicted_priority_str = self.llm.predict(prompt).lower()

        if "high" in predicted_priority_str:
            return TicketPriority.HIGH
        elif "medium" in predicted_priority_str:
            return TicketPriority.MEDIUM
        else:
            return TicketPriority.LOW

class ResolutionAgent:
    """
    Suggests a resolution using an LLM, leveraging the output from previous agents.
    """
    def __init__(self):
        self.llm = LLMProvider()

    def predict(self, description: str, category: TicketCategory) -> str:
        # This prompt demonstrates agent collaboration.
        # It uses the 'category' from the ClassificationAgent to generate a better response.
        prompt = f"""
        You are a helpful customer support agent. Based on the ticket description and its classified category,
        provide a concise and helpful first-response.
        
        If a simple solution is possible (like resetting a password), suggest it.
        Otherwise, inform the user that the ticket has been escalated to the appropriate team.
        
        Category: {category.value}
        Description: "{description}"
        
        Suggested Response:
        """
        
        return self.llm.predict(prompt)

