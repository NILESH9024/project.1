# 🤖 Local AI Assistant

A fully local AI assistant desktop app built with Python — no cloud, no API keys, complete privacy.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLMs-green)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-orange)

---

## ✨ Features

- 💬 **Chat Interface** — Dark-themed Tkinter UI
- 🧠 **Local LLMs** via Ollama (DeepSeek, Qwen, Gemma, CodeLlama, etc.)
- 📚 **RAG Engine** — Load project folders/files into a ChromaDB knowledge base
- 🔀 **AI Orchestrator** — Prompt management, conversation memory, context builder, response post-processing
- 🛠 **Mode Selector** — Default / Coder / Analyst / RAG
- 📁 **Project Explorer** — Ingest entire folders or single files
- 🔄 **Model Manager** — Switch models on the fly

---

## 🏗 Architecture

```
Desktop UI (Tkinter)
        │
   AI Orchestrator
   ┌────┴────┐
Ollama API  RAG Engine
(Local LLMs) (ChromaDB)
   │              │
qwen3, gemma,  Project Files
deepseek, etc. & Embeddings
```

---

## 🚀 Quick Start

### 1. Install Ollama
Download from [ollama.com](https://ollama.com) and run:
```bash
ollama serve
ollama pull qwen3:4b        # recommended
# or
ollama pull gemma3:4b
ollama pull deepseek-coder
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python main.py
```

---

## 📦 Project Structure

```
ai_assistant/
├── main.py                        # Entry point
├── requirements.txt
├── llm/
│   └── ollama_client.py           # Ollama API (streaming + blocking)
├── orchestrator/
│   ├── orchestrator.py            # Central coordinator
│   ├── prompt_manager.py          # System prompts
│   ├── context_builder.py         # File snippet injection
│   ├── memory.py                  # Rolling conversation memory
│   └── postprocessor.py          # Output cleaning
├── rag/
│   ├── rag_engine.py              # ChromaDB + sentence-transformers
│   └── ingestion.py               # File loading & text chunking
└── ui/
    └── chat_ui.py                 # Tkinter dark UI
```

---

## 📋 Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally
- At least one model pulled via `ollama pull <model>`

---

## 🔧 Dependencies

```
ollama
chromadb
sentence-transformers
requests
```

---

## 📝 Usage Tips

- **First response** may take 30-60s as the model loads into RAM
- Use **"Load Project Folder"** to ingest your codebase into the knowledge base
- Enable **RAG mode** to get context-aware answers from your documents
- **Shift+Enter** for new line, **Enter** to send

---

## 📄 License

MIT License — free to use and modify.
