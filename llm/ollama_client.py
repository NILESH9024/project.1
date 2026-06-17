"""
Ollama API Client — wraps local LLM inference.
Supports: DeepSeek, Qwen Coder, CodeLlama (and any model pulled via Ollama).
"""

import requests
import json
from typing import Generator, Optional


OLLAMA_BASE_URL = "http://localhost:11434"

# Available local models (matching the diagram)
AVAILABLE_MODELS = {
    "deepseek-coder": "deepseek-coder",
    "qwen-coder":     "qwen2.5-coder",
    "codellama":      "codellama",
}

DEFAULT_MODEL = "deepseek-coder"


class OllamaClient:
    """
    Handles all communication with the Ollama REST API.
    Provides both blocking and streaming inference.
    """

    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = DEFAULT_MODEL):
        self.base_url = base_url
        self.model = model

    # ------------------------------------------------------------------ #
    #  Model management                                                    #
    # ------------------------------------------------------------------ #

    def list_models(self) -> list[str]:
        """Return names of models currently pulled in Ollama."""
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            resp.raise_for_status()
            return [m["name"] for m in resp.json().get("models", [])]
        except requests.exceptions.ConnectionError:
            return []
        except Exception as e:
            print(f"[OllamaClient] list_models error: {e}")
            return []

    def is_available(self) -> bool:
        """Check whether Ollama is running."""
        try:
            requests.get(f"{self.base_url}/api/tags", timeout=3)
            return True
        except Exception:
            return False

    def set_model(self, model: str):
        self.model = model

    # ------------------------------------------------------------------ #
    #  Inference                                                           #
    # ------------------------------------------------------------------ #

    def chat(
        self,
        messages: list[dict],
        stream: bool = False,
        options: Optional[dict] = None,
    ) -> str | Generator[str, None, None]:
        """
        Send a chat-style request to Ollama.

        Args:
            messages: List of {"role": "user"/"assistant"/"system", "content": "..."}
            stream:   If True, yields token chunks instead of returning full string.
            options:  Ollama model options (temperature, top_p, etc.)

        Returns:
            Full response string (stream=False) or a generator of chunks (stream=True).
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "options": options or {"temperature": 0.7},
        }

        if stream:
            return self._stream_chat(payload)
        return self._blocking_chat(payload)

    def _blocking_chat(self, payload: dict) -> str:
        try:
            resp = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=300,   # 5 min — large models need time to load into RAM
            )
            resp.raise_for_status()
            return resp.json()["message"]["content"]
        except requests.exceptions.ConnectionError:
            return "❌ Cannot connect to Ollama. Make sure it's running (`ollama serve`)."
        except requests.exceptions.ReadTimeout:
            return "❌ Model took too long to respond. Try again — it may still be loading into RAM."
        except Exception as e:
            return f"❌ Ollama error: {e}"

    def _stream_chat(self, payload: dict) -> Generator[str, None, None]:
        try:
            with requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                stream=True,
                timeout=300,   # 5 min for large models
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if line:
                        data = json.loads(line)
                        chunk = data.get("message", {}).get("content", "")
                        if chunk:
                            yield chunk
                        if data.get("done"):
                            break
        except requests.exceptions.ConnectionError:
            yield "❌ Cannot connect to Ollama. Make sure it's running (`ollama serve`)."
        except Exception as e:
            yield f"❌ Ollama error: {e}"
