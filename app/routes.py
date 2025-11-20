"""Flask routes for the automation intake workflow."""
from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, session, url_for

from .services.workflow import AutomationWorkflow, TurnResponse

bp = Blueprint("main", __name__)
workflow = AutomationWorkflow()


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

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if user_input:
            conversation.append({"role": "user", "content": user_input})
            turn = workflow.next_turn(conversation)
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
    )


def _append_turn(conversation: list[dict[str, str]], turn: TurnResponse) -> None:
    """Append the LLM's reply to the conversation history."""
    conversation.append({"role": "assistant", "content": turn.message})
