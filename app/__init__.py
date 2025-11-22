"""Application factory for the Automation Intake Flask app."""
from __future__ import annotations
import os
from flask import Flask
from dotenv import load_dotenv

from app.services.workflow import AutomationWorkflow
from app.services.llm import GeminiLLM

def create_app() -> Flask:
    """Create and configure the Flask application."""
    load_dotenv()

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        GEMINI_API_KEY=os.environ.get("GEMINI_API_KEY"),
        TEMPLATES_AUTO_RELOAD=True,
    )

    # Initialize the workflow with the GeminiLLM
    llm = GeminiLLM()
    app.workflow = AutomationWorkflow(llm)

    from .routes import bp as routes_bp

    app.register_blueprint(routes_bp)
    return app
