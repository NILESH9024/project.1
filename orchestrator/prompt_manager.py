"""
Prompt Management — builds system prompts and injects context.
"""

SYSTEM_PROMPTS = {
    "default": (
        "You are a helpful AI assistant. "
        "Answer clearly and concisely. "
        "If you are unsure, say so."
    ),
    "coder": (
        "You are an expert software engineer. "
        "Provide clean, well-commented code. "
        "Prefer modern best practices and explain your reasoning."
    ),
    "analyst": (
        "You are a data analyst assistant. "
        "Help interpret data, write queries, and explain findings clearly."
    ),
    "rag": (
        "You are a helpful assistant with access to a knowledge base. "
        "Use the provided context to answer questions accurately. "
        "If the context doesn't contain the answer, say so clearly."
    ),
}


class PromptManager:
    """Manages system prompts and injects retrieved RAG context into user messages."""

    def __init__(self, mode: str = "default"):
        self.mode = mode

    def get_system_prompt(self) -> str:
        return SYSTEM_PROMPTS.get(self.mode, SYSTEM_PROMPTS["default"])

    def set_mode(self, mode: str):
        if mode in SYSTEM_PROMPTS:
            self.mode = mode

    def inject_context(self, user_message: str, context_chunks: list[str]) -> str:
        """
        Prepend retrieved RAG context to the user message so the LLM
        can ground its answer in the knowledge base.
        """
        if not context_chunks:
            return user_message

        context_text = "\n\n---\n\n".join(context_chunks)
        return (
            f"Use the following context to answer the question.\n\n"
            f"### Context:\n{context_text}\n\n"
            f"### Question:\n{user_message}"
        )

    @staticmethod
    def available_modes() -> list[str]:
        return list(SYSTEM_PROMPTS.keys())
