"""
Conversation Memory — stores and retrieves chat history.
Keeps a rolling window to stay within context limits.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Message:
    role: str       # "system" | "user" | "assistant"
    content: str


class ConversationMemory:
    """
    Maintains conversation history with a configurable rolling window.
    Optionally prepends a persistent system prompt.
    """

    def __init__(self, max_turns: int = 20, system_prompt: Optional[str] = None):
        self.max_turns = max_turns          # max user+assistant pairs to keep
        self.system_prompt = system_prompt
        self._history: list[Message] = []

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def add_user(self, content: str):
        self._history.append(Message(role="user", content=content))
        self._trim()

    def add_assistant(self, content: str):
        self._history.append(Message(role="assistant", content=content))

    def get_messages(self) -> list[dict]:
        """Return messages formatted for the Ollama chat API."""
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        for msg in self._history:
            messages.append({"role": msg.role, "content": msg.content})
        return messages

    def clear(self):
        self._history.clear()

    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt

    def __len__(self):
        return len(self._history)

    # ------------------------------------------------------------------ #
    #  Internal                                                            #
    # ------------------------------------------------------------------ #

    def _trim(self):
        """Keep only the last max_turns * 2 messages (user + assistant pairs)."""
        max_messages = self.max_turns * 2
        if len(self._history) > max_messages:
            self._history = self._history[-max_messages:]
