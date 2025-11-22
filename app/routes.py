"""Flask routes for the automation intake workflow."""
from __future__ import annotations

from flask import Blueprint, current_app, redirect, render_template, request, session, url_for

from .services.workflow import TurnResponse

bp = Blueprint("main", __name__)


@bp.route("/auth/login", methods=["GET", "POST"])
def login() -> str:
    """Render a simple login form and validate credentials."""
    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            error = "Email and password are required to sign in."
        else:
            session["user"] = {"email": email}
            return redirect(url_for("main.intake"))

    return render_template("login.html", error=error), (400 if error else 200)


@bp.route("/", methods=["GET", "POST"])
def intake() -> str:
    """Render the intake conversation and process user submissions."""
    conversation = session.get(
        "conversation",
        [
            {
                "role": "assistant",
                "content": "Describe a process you'd like to automate, and I'll gather the details.",
            }
        ],
    )
    assessment = session.get("assessment")
    process_logic = session.get("process_logic", {})

    if request.method == "POST":
        # Update process logic from form
        process_logic = {
            "decision_logic": request.form.get("decision_logic"),
            "exception_rate": request.form.get("exception_rate"),
            "standardization": request.form.get("standardization"),
            "process_stability": request.form.get("process_stability"),
            "input_data_format": request.form.get("input_data_format"),
            "data_sensitivity": request.form.get("data_sensitivity"),
            "error_impact": request.form.get("error_impact"),
            "volume": request.form.get("volume"),
            "processing_time": request.form.get("processing_time"),
            "frequency": request.form.get("frequency"),
            "current_backlog": request.form.get("current_backlog"),
        }
        session["process_logic"] = process_logic

        user_input = request.form.get("user_input", "").strip()
        if user_input:
            conversation.append({"role": "user", "content": user_input})
            turn = current_app.workflow.next_turn(conversation, process_logic)
            _append_turn(conversation, turn)
            if turn.assessment:
                assessment = turn.assessment
        session["conversation"] = conversation
        session["assessment"] = assessment
        return redirect(url_for("main.intake"))

    return render_template(
        "intake.html",
        conversation=conversation,
        assessment=assessment,
        process_logic=process_logic,
    )


@bp.route("/reset", methods=["POST"])
def reset() -> str:
    """Clear the conversation history and restart."""
    session.clear()
    return redirect(url_for("main.intake"))


def _append_turn(conversation: list[dict[str, str]], turn: TurnResponse) -> None:
    """Append the LLM's reply to the conversation history."""
    conversation.append({"role": "assistant", "content": turn.message})
