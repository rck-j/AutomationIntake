"""Workflow orchestration and placeholder LLM adapter."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol


@dataclass
class TurnResponse:
    """LLM turn output and optional assessment."""

    message: str
    assessment: str | None = None


class AutomationLLM(Protocol):
    """Interface for generating LLM replies for the intake flow."""

    def respond(self, history: Iterable[dict[str, str]], context: dict | None = None) -> TurnResponse:  # pragma: no cover - protocol
        ...


class RuleBasedLLM:
    """A deterministic stand-in for OpenAI that keeps the conversation moving."""

    def __init__(self) -> None:
        self.prompts = [
            "Thanks! What systems or tools are involved in this process?",
            "Who performs each step today, and how often does it run?",
            "Do you have any constraints or compliance considerations I should know about?",
        ]

    def respond(self, history: Iterable[dict[str, str]], context: dict | None = None) -> TurnResponse:
        """Return a clarifying prompt or a lightweight assessment."""
        user_messages = [entry for entry in history if entry.get("role") == "user"]
        if len(user_messages) < len(self.prompts):
            return TurnResponse(message=self.prompts[len(user_messages) - 1])

        summary_points = [
            "Document the current process with owners and frequencies.",
            "Identify repetitive steps suitable for scripting or RPA.",
            "Map data inputs/outputs to gauge integration needs.",
        ]
        assessment = "\n".join(f"- {point}" for point in summary_points)
        return TurnResponse(
            message="Thanks for the details. Here's an initial automation assessment:",
            assessment=assessment,
        )


class AutomationWorkflow:
    """Manage the conversational intake loop for automation requests."""

    def __init__(self, llm: AutomationLLM | None = None) -> None:
        self.llm = llm or RuleBasedLLM()

    def next_turn(self, history: list[dict[str, str]], context: dict | None = None) -> TurnResponse:
        """Send the conversation to the LLM client and return its reply."""
        return self.llm.respond(history, context)
