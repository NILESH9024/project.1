"""
Chat UI — Tkinter-based desktop interface.

Panels (matching the diagram):
  - Chat Interface   (main area)
  - Model Manager    (sidebar dropdown)
  - Project Explorer (load files / knowledge base)
  - Settings         (mode, RAG toggle)
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import os
import sys

# Allow running from any working directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.orchestrator import AIOrchestrator
from rag.rag_engine import RAGEngine


# ── Colour palette ──────────────────────────────────────────────────────────
BG_DARK   = "#1e1e2e"
BG_MID    = "#2a2a3e"
BG_LIGHT  = "#313150"
ACCENT    = "#7c6af7"
ACCENT2   = "#56cfbf"
FG        = "#cdd6f4"
FG_DIM    = "#6c7086"
USER_CLR  = "#89dceb"
BOT_CLR   = "#a6e3a1"
ERR_CLR   = "#f38ba8"
FONT_MAIN = ("Segoe UI", 11)
FONT_MONO = ("Consolas", 10)
FONT_BIG  = ("Segoe UI", 13, "bold")


class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🤖 Local AI Assistant")
        self.geometry("1100x720")
        self.minsize(800, 550)
        self.configure(bg=BG_DARK)

        # ── Backend ──────────────────────────────────────────────────────
        self.rag_engine   = RAGEngine(persist_dir="./chroma_db")
        self.orchestrator = AIOrchestrator(
            model="qwen3:4b",
            mode="default",
            rag_engine=self.rag_engine,
        )

        self._build_ui()
        self._check_ollama_status()

    # ================================================================== #
    #  UI Construction                                                     #
    # ================================================================== #

    def _build_ui(self):
        # Top bar
        self._build_topbar()

        # Main content: sidebar | chat
        content = tk.Frame(self, bg=BG_DARK)
        content.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        self._build_sidebar(content)
        self._build_chat_area(content)

    # ── Top bar ──────────────────────────────────────────────────────────
    def _build_topbar(self):
        bar = tk.Frame(self, bg=BG_MID, height=50)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)

        tk.Label(
            bar, text="🤖  Local AI Assistant",
            bg=BG_MID, fg=FG, font=FONT_BIG,
        ).pack(side=tk.LEFT, padx=16)

        self.status_lbl = tk.Label(
            bar, text="⚙ Checking Ollama…",
            bg=BG_MID, fg=FG_DIM, font=FONT_MAIN,
        )
        self.status_lbl.pack(side=tk.RIGHT, padx=16)

    # ── Sidebar ──────────────────────────────────────────────────────────
    def _build_sidebar(self, parent):
        side = tk.Frame(parent, bg=BG_MID, width=230)
        side.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8), pady=4)
        side.pack_propagate(False)

        def section(title):
            tk.Label(
                side, text=title, bg=BG_MID, fg=ACCENT,
                font=("Segoe UI", 10, "bold"),
            ).pack(anchor=tk.W, padx=10, pady=(12, 2))

        # ── Model Manager ──
        section("⚙ Model Manager")
        self.model_var = tk.StringVar(value="qwen3:4b")
        self.model_combo = ttk.Combobox(
            side, textvariable=self.model_var,
            values=["qwen3:4b", "gemma3:4b", "deepseek-coder", "qwen2.5-coder", "codellama"],
            state="readonly", width=24,
        )
        self.model_combo.pack(padx=10, pady=2, fill=tk.X)
        self.model_combo.bind("<<ComboboxSelected>>", self._on_model_change)

        tk.Button(
            side, text="🔄 Refresh Models",
            bg=BG_LIGHT, fg=FG, relief=tk.FLAT, cursor="hand2",
            command=self._refresh_models,
        ).pack(padx=10, pady=4, fill=tk.X)

        # ── Mode / Settings ──
        section("🛠 Settings")
        self.mode_var = tk.StringVar(value="default")
        for mode in ["default", "coder", "analyst", "rag"]:
            tk.Radiobutton(
                side, text=mode.capitalize(),
                variable=self.mode_var, value=mode,
                bg=BG_MID, fg=FG, selectcolor=BG_LIGHT,
                activebackground=BG_MID, font=FONT_MAIN,
                command=self._on_mode_change,
            ).pack(anchor=tk.W, padx=14)

        tk.Label(side, text="RAG (Knowledge Base)", bg=BG_MID, fg=FG_DIM,
                 font=("Segoe UI", 9)).pack(anchor=tk.W, padx=10, pady=(8, 0))

        self.rag_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            side, text="Enable RAG",
            variable=self.rag_var,
            command=self._on_rag_toggle,
        ).pack(anchor=tk.W, padx=10)

        # ── Project Explorer ──
        section("📁 Project Explorer")
        tk.Button(
            side, text="📂 Load Project Folder",
            bg=ACCENT, fg="white", relief=tk.FLAT, cursor="hand2",
            command=self._load_project_folder,
        ).pack(padx=10, pady=3, fill=tk.X)

        tk.Button(
            side, text="📄 Load Single File",
            bg=BG_LIGHT, fg=FG, relief=tk.FLAT, cursor="hand2",
            command=self._load_single_file,
        ).pack(padx=10, pady=3, fill=tk.X)

        tk.Button(
            side, text="🗑 Clear Knowledge Base",
            bg=BG_LIGHT, fg=ERR_CLR, relief=tk.FLAT, cursor="hand2",
            command=self._clear_kb,
        ).pack(padx=10, pady=3, fill=tk.X)

        self.kb_lbl = tk.Label(
            side, text=f"📚 {self.rag_engine.document_count()} chunks stored",
            bg=BG_MID, fg=FG_DIM, font=("Segoe UI", 9),
        )
        self.kb_lbl.pack(padx=10, pady=(2, 0))

        # ── Actions ──
        section("💬 Chat")
        tk.Button(
            side, text="🧹 Clear Chat",
            bg=BG_LIGHT, fg=FG, relief=tk.FLAT, cursor="hand2",
            command=self._clear_chat,
        ).pack(padx=10, pady=3, fill=tk.X)

        tk.Button(
            side, text="🗑 Clear Memory",
            bg=BG_LIGHT, fg=FG, relief=tk.FLAT, cursor="hand2",
            command=self._clear_memory,
        ).pack(padx=10, pady=3, fill=tk.X)

    # ── Chat area ────────────────────────────────────────────────────────
    def _build_chat_area(self, parent):
        chat_frame = tk.Frame(parent, bg=BG_DARK)
        chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            bg=BG_MID, fg=FG,
            font=FONT_MONO,
            wrap=tk.WORD,
            state=tk.DISABLED,
            relief=tk.FLAT,
            padx=10, pady=10,
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        # Configure text tags for coloured messages
        self.chat_display.tag_config("user",      foreground=USER_CLR, font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_config("assistant", foreground=BOT_CLR,  font=FONT_MONO)
        self.chat_display.tag_config("system",    foreground=FG_DIM,   font=("Segoe UI", 9, "italic"))
        self.chat_display.tag_config("error",     foreground=ERR_CLR)

        # Input area
        input_frame = tk.Frame(chat_frame, bg=BG_DARK)
        input_frame.pack(fill=tk.X, pady=(6, 0))

        self.input_box = tk.Text(
            input_frame,
            bg=BG_MID, fg=FG,
            font=FONT_MAIN,
            height=3,
            relief=tk.FLAT,
            padx=8, pady=6,
            wrap=tk.WORD,
        )
        self.input_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        self.input_box.bind("<Return>",       self._on_enter)
        self.input_box.bind("<Shift-Return>", lambda e: None)  # allow newline with Shift+Enter

        send_btn = tk.Button(
            input_frame, text="Send ➤",
            bg=ACCENT, fg="white",
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT, cursor="hand2",
            padx=16,
            command=self._send_message,
        )
        send_btn.pack(side=tk.RIGHT, fill=tk.Y)

        hint = tk.Label(
            chat_frame,
            text="Enter → Send   |   Shift+Enter → New line",
            bg=BG_DARK, fg=FG_DIM,
            font=("Segoe UI", 8),
        )
        hint.pack(anchor=tk.E, pady=(2, 0))

        # Welcome message
        self._append_message(
            "system",
            "Welcome! Type a message below and press Enter to chat.\n"
            "Use the sidebar to load a project folder into the knowledge base.\n",
        )

    # ================================================================== #
    #  Event Handlers                                                      #
    # ================================================================== #

    def _on_enter(self, event):
        """Send on plain Enter; Shift+Enter inserts a newline."""
        if not event.state & 0x1:   # Shift not held
            self._send_message()
            return "break"          # prevent default newline

    def _send_message(self):
        text = self.input_box.get("1.0", tk.END).strip()
        if not text:
            return

        self.input_box.delete("1.0", tk.END)
        self._append_message("user", f"You: {text}\n")

        # Run inference in background thread to keep UI responsive
        threading.Thread(
            target=self._run_inference,
            args=(text,),
            daemon=True,
        ).start()

    def _run_inference(self, text: str):
        self._append_message("system", "⏳ Assistant is thinking… (first response may take 30-60s while model loads)\n")
        try:
            response = self.orchestrator.chat(text, stream=False)
        except Exception as e:
            response = f"❌ Error: {e}"
            self._remove_last_system()
            self._append_message("error", f"{response}\n")
            return

        self._remove_last_system()
        self._append_message("assistant", f"Assistant: {response}\n\n")

    def _on_model_change(self, _event=None):
        model = self.model_var.get()
        self.orchestrator.set_model(model)
        self._append_message("system", f"[Model changed to: {model}]\n")

    def _on_mode_change(self):
        mode = self.mode_var.get()
        self.orchestrator.set_mode(mode)
        self._append_message("system", f"[Mode changed to: {mode}]\n")

    def _on_rag_toggle(self):
        self.orchestrator.use_rag = self.rag_var.get()
        state = "enabled" if self.rag_var.get() else "disabled"
        self._append_message("system", f"[RAG {state}]\n")

    def _refresh_models(self):
        models = self.orchestrator.list_models()
        if models:
            self.model_combo["values"] = models
            self._append_message("system", f"[Found models: {', '.join(models)}]\n")
        else:
            self._append_message("error", "[Could not fetch models — is Ollama running?]\n")

    def _load_project_folder(self):
        folder = filedialog.askdirectory(title="Select Project Folder")
        if not folder:
            return
        self._append_message("system", f"[Ingesting '{folder}'… this may take a moment]\n")
        threading.Thread(
            target=self._ingest_folder,
            args=(folder,),
            daemon=True,
        ).start()

    def _ingest_folder(self, folder: str):
        try:
            self.rag_engine.ingest_directory(folder)
            count = self.rag_engine.document_count()
            self._update_kb_label(count)
            self._append_message("system", f"[Ingestion complete — {count} chunks stored]\n")
        except Exception as e:
            self._append_message("error", f"[Ingestion error: {e}]\n")

    def _load_single_file(self):
        path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[
                ("Text/Code files", "*.py *.txt *.md *.js *.ts *.json *.yaml *.toml"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return
        try:
            content = open(path, encoding="utf-8", errors="ignore").read()
            self.orchestrator.add_file_context(os.path.basename(path), content)
            self._append_message("system", f"[File loaded into context: {os.path.basename(path)}]\n")
        except Exception as e:
            self._append_message("error", f"[Could not load file: {e}]\n")

    def _clear_kb(self):
        if messagebox.askyesno("Clear Knowledge Base", "Delete all stored embeddings?"):
            self.rag_engine.clear()
            self._update_kb_label(0)
            self._append_message("system", "[Knowledge base cleared]\n")

    def _clear_chat(self):
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.configure(state=tk.DISABLED)

    def _clear_memory(self):
        self.orchestrator.clear_memory()
        self._append_message("system", "[Conversation memory cleared]\n")

    # ================================================================== #
    #  Helpers                                                             #
    # ================================================================== #

    def _append_message(self, tag: str, text: str):
        """Thread-safe append to the chat display."""
        def _do():
            self.chat_display.configure(state=tk.NORMAL)
            self.chat_display.insert(tk.END, text, tag)
            self.chat_display.see(tk.END)
            self.chat_display.configure(state=tk.DISABLED)
        self.after(0, _do)

    def _remove_last_system(self):
        """Remove the last 'thinking…' system line."""
        def _do():
            self.chat_display.configure(state=tk.NORMAL)
            content = self.chat_display.get("1.0", tk.END)
            thinking_line = "⏳ Assistant is thinking… (first response may take 30-60s while model loads)\n"
            idx = content.rfind(thinking_line)
            if idx != -1:
                start = f"1.0 + {idx} chars"
                end   = f"1.0 + {idx + len(thinking_line)} chars"
                self.chat_display.delete(start, end)
            self.chat_display.configure(state=tk.DISABLED)
        self.after(0, _do)

    def _update_kb_label(self, count: int):
        self.after(0, lambda: self.kb_lbl.configure(
            text=f"📚 {count} chunks stored"
        ))

    def _check_ollama_status(self):
        def _check():
            ok = self.orchestrator.is_ollama_available()
            if ok:
                models = self.orchestrator.list_models()
                label  = f"✅ Ollama running  |  {len(models)} model(s)"
                color  = ACCENT2
                if models:
                    self.after(0, lambda: self.model_combo.configure(values=models))
            else:
                label = "❌ Ollama offline — run `ollama serve`"
                color = ERR_CLR
            self.after(0, lambda: self.status_lbl.configure(text=label, fg=color))

        threading.Thread(target=_check, daemon=True).start()
