"""
Context Builder — assembles the final context sent to the LLM.
Combines conversation history, RAG results, and file contents.
"""

from typing import Optional


class ContextBuilder:
    """
    Builds an enriched context dict that the orchestrator feeds
    to the prompt manager and memory system.
    """

    def __init__(self):
        self._file_snippets: list[str] = []
        self._extra_context: list[str] = []

    def add_file_snippet(self, filename: str, content: str, max_chars: int = 2000):
        """Attach a code/file snippet (truncated) to the context."""
        snippet = content[:max_chars]
        if len(content) > max_chars:
            snippet += "\n... [truncated]"
        self._file_snippets.append(f"### File: {filename}\n```\n{snippet}\n```")

    def add_extra(self, text: str):
        """Add any free-form extra context."""
        self._extra_context.append(text)

    def build(self) -> Optional[str]:
        """Return assembled context string, or None if nothing was added."""
        parts = self._file_snippets + self._extra_context
        if not parts:
            return None
        return "\n\n".join(parts)

    def clear(self):
        self._file_snippets.clear()
        self._extra_context.clear()
