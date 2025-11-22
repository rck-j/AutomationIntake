
import os
import google.generativeai as genai
from typing import Iterable
from app.services.workflow import TurnResponse, AutomationLLM

# Configure the Gemini API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class GeminiLLM:
    """A wrapper for the Gemini API that adheres to the AutomationLLM protocol."""

    def __init__(self) -> None:
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.system_prompt = (
            "You are an expert Automation Consultant. Your goal is to gather requirements "
            "for a potential automation project. Ask clarifying questions to understand the "
            "process, inputs, outputs, volume, and pain points. Be concise and professional."
        )

    def respond(self, history: Iterable[dict[str, str]], context: dict | None = None) -> TurnResponse:
        """Generate a response using the Gemini API."""
        user_messages = [entry for entry in history if entry.get("role") == "user"]
        
        # If we have enough turns, generate the assessment
        if len(user_messages) >= 4:
            return self._generate_assessment(history, context)

        # Otherwise, continue the conversation
        prompt = f"{self.system_prompt}\n\n"
        if context:
            prompt += "Process Context:\n"
            prompt += f"- Decision Logic: {context.get('decision_logic')}\n"
            prompt += f"- Exception Rate: {context.get('exception_rate')}%\n"
            prompt += f"- Standardization: {context.get('standardization')}\n"
            prompt += f"- Process Stability: {context.get('process_stability')}\n"
            prompt += f"- Input Data Format: {context.get('input_data_format')}\n"
            prompt += f"- Data Sensitivity: {context.get('data_sensitivity')}\n"
            prompt += f"- Error Impact: {context.get('error_impact')}\n"
            prompt += f"- Volume: {context.get('volume')}\n"
            prompt += f"- Processing Time: {context.get('processing_time')} minutes\n"
            prompt += f"- Frequency: {context.get('frequency')}\n"
            prompt += f"- Current Backlog: {context.get('current_backlog')}\n\n"
        
        prompt += "Conversation History:\n"
        for entry in history:
            prompt += f"{entry['role']}: {entry['content']}\n"
        prompt += "\nAssistant:"

        response = self.model.generate_content(prompt)
        return TurnResponse(message=response.text)

    def _calculate_metrics(self, context: dict) -> dict:
        """Calculate automation score and time savings."""
        score = 0
        
        # Scoring Logic
        if context.get("decision_logic") == "Rule Based":
            score += 20
        
        exception_rate = int(context.get("exception_rate") or 0)
        if exception_rate < 10:
            score += 20
        elif exception_rate < 30:
            score += 10
            
        if context.get("standardization") == "Fully documented/Up-to-date":
            score += 20
        elif context.get("standardization") == "Outdated documentation":
            score += 10
            
        if context.get("process_stability") == "Stable":
            score += 20
            
        if context.get("input_data_format") == "Structured":
            score += 20
        elif context.get("input_data_format") == "Semi-Structured":
            score += 10

        # Time Savings Calculation
        volume = int(context.get("volume") or 0)
        processing_time = int(context.get("processing_time") or 0)
        frequency = context.get("frequency")
        
        multiplier = 0
        if frequency == "Daily":
            multiplier = 260
        elif frequency == "Weekly":
            multiplier = 52
        elif frequency == "Monthly":
            multiplier = 12
            
        yearly_savings_hours = (volume * processing_time * multiplier) / 60
        
        return {
            "score": score,
            "yearly_savings_hours": round(yearly_savings_hours, 1)
        }

    def _generate_assessment(self, history: Iterable[dict[str, str]], context: dict | None = None) -> TurnResponse:
        """Generate the final automation assessment."""
        prompt = (
            "Based on the following conversation and process context, provide a comprehensive automation assessment. "
            "Include: 1. Process Summary, 2. Automation Potential (High/Medium/Low), "
            "3. Recommended Approach (RPA, API, Custom Script), 4. Estimated Effort.\n"
        )
        
        if context:
            metrics = self._calculate_metrics(context)
            prompt += f"\nCALCULATED METRICS (Please include these in your report):\n"
            prompt += f"- Automation Suitability Score: {metrics['score']}/100\n"
            prompt += f"- Estimated Yearly Time Savings: {metrics['yearly_savings_hours']} Hours\n\n"

            prompt += "Process Context:\n"
            prompt += f"- Decision Logic: {context.get('decision_logic')}\n"
            prompt += f"- Exception Rate: {context.get('exception_rate')}%\n"
            prompt += f"- Standardization: {context.get('standardization')}\n"
            prompt += f"- Process Stability: {context.get('process_stability')}\n"
            prompt += f"- Input Data Format: {context.get('input_data_format')}\n"
            prompt += f"- Data Sensitivity: {context.get('data_sensitivity')}\n"
            prompt += f"- Error Impact: {context.get('error_impact')}\n"
            prompt += f"- Volume: {context.get('volume')}\n"
            prompt += f"- Processing Time: {context.get('processing_time')} minutes\n"
            prompt += f"- Frequency: {context.get('frequency')}\n"
            prompt += f"- Current Backlog: {context.get('current_backlog')}\n\n"
        
        prompt += "Conversation History:\n"
        for entry in history:
            prompt += f"{entry['role']}: {entry['content']}\n"
        
        response = self.model.generate_content(prompt)
        
        return TurnResponse(
            message="I have gathered enough information. Here is your automation assessment:",
            assessment=response.text,
        )
