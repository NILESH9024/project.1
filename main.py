"""
main.py — Entry point for the Local AI Assistant.

Usage:
    python main.py

Requirements:
    pip install -r requirements.txt

Ollama must be running separately:
    ollama serve
    ollama pull deepseek-coder    (or qwen2.5-coder / codellama)
"""

import sys
import os

# Ensure project root is on the path regardless of working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.chat_ui import ChatApp


def main():
    app = ChatApp()
    app.mainloop()


if __name__ == "__main__":
    main()
