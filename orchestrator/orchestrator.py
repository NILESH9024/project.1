"""
AI Orchestrator — the central coordinator.

Wires together:
  - PromptManager   (system prompts & context injection)
  - ContextBuilder  (file snippets, extra context)
  - ConversationMemory (rolling history)
  - ResponsePostProcessor (output cleaning)
  - OllamaClient    (LLM inference)
  - RAGEngine       (optional knowledge base retrieval)
"""

from typing import Generator, Optional

from orchestrator.prompt_manager  import PromptManager
from orchestrator.context_builder import ContextBuilder
from orchestrator.memory          import ConversationMemory
from orchestrator.postprocessor   import ResponsePostProcessor
from llm.ollama_client            import OllamaClient


class AIOrchestrator:
    def __init__(
        self,
        model: str = "deepseek-coder",
        mode: str = "default",
        rag_engine=None,          # optional RAGEngine instance
        max_turns: int = 20,
    ):
        self.prompt_manager  = PromptManager(mode=mode)
        self.context_builder = ContextBuilder()
        self.memory          = ConversationMemory(
            max_turns=max_turns,
            system_prompt=self.prompt_manager.get_system_prompt(),
        )
        self.postprocessor   = ResponsePostProcessor()
        self.llm             = OllamaClient(model=model)
        self.rag             = rag_engine
        self.use_rag         = rag_engine is not None

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def chat(self, user_input: str, stream: bool = False) -> str | Generator[str, None, None]:
        """
        Main entry point for a user message.
        Returns full response string or a streaming generator.
        """
        # 1. RAG retrieval
        rag_chunks: list[str] = []
        if self.use_rag and self.rag:
            try:
                rag_chunks = self.rag.query(user_input, n_results=3)
            except Exception as e:
                print(f"[Orchestrator] RAG query failed: {e}")

        # 2. Build enriched user message
        enriched_input = self.prompt_manager.inject_context(user_input, rag_chunks)

        # 3. Add to memory
        self.memory.add_user(enriched_input)

        # 4. Get messages for LLM
        messages = self.memory.get_messages()

        # 5. Inference
        if stream:
            return self._stream_response(user_input, messages)

        raw = self.llm.chat(messages, stream=False)
        response = self.postprocessor.process(raw)

        # 6. Store assistant reply
        self.memory.add_assistant(response)
        return response

    def set_model(self, model: str):
        self.llm.set_model(model)

    def set_mode(self, mode: str):
        self.prompt_manager.set_mode(mode)
        self.memory.set_system_prompt(self.prompt_manager.get_system_prompt())

    def clear_memory(self):
        self.memory.clear()
        # Re-inject system prompt after clearing
        self.memory.set_system_prompt(self.prompt_manager.get_system_prompt())

    def add_file_context(self, filename: str, content: str):
        self.context_builder.add_file_snippet(filename, content)

    def is_ollama_available(self) -> bool:
        return self.llm.is_available()

    def list_models(self) -> list[str]:
        return self.llm.list_models()

    # ------------------------------------------------------------------ #
    #  Streaming helper                                                    #
    # ------------------------------------------------------------------ #

    def _stream_response(
        self, original_input: str, messages: list[dict]
    ) -> Generator[str, None, None]:
        """Yield chunks and accumulate the full reply for memory storage."""
        full_response = ""
        for chunk in self.llm.chat(messages, stream=True):
            processed = self.postprocessor.process(chunk)
            full_response += chunk
            yield processed
        self.memory.add_assistant(self.postprocessor.process(full_response))
