"""
Response Post-processing — cleans and formats LLM output.
"""

import re


class ResponsePostProcessor:
    """
    Applies a pipeline of transformations to the raw LLM response
    before it reaches the UI.
    """

    def process(self, text: str) -> str:
        text = self._strip_think_tags(text)
        text = self._normalize_whitespace(text)
        return text.strip()

    # ------------------------------------------------------------------ #
    #  Pipeline steps                                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _strip_think_tags(text: str) -> str:
        """Remove <think>...</think> blocks (used by some reasoning models)."""
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        """Collapse 3+ consecutive blank lines into 2."""
        return re.sub(r"\n{3,}", "\n\n", text)
