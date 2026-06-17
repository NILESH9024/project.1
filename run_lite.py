"""
run_lite.py — Lite version (no RAG/ChromaDB needed).
Runs immediately with just the requests library.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import threading
import requests
import json
import re

OLLAMA_URL = "http://localhost:11434"

BG_DARK  = "#1e1e2e"
BG_MID   = "#2a2a3e"
BG_LIGHT = "#313150"
ACCENT   = "#7c6af7"
ACCENT2  = "#56cfbf"
FG       = "#cdd6f4"
FG_DIM   = "#6c7086"
USER_CLR = "#89dceb"
BOT_CLR  = "#a6e3a1"
ERR_CLR  = "#f38ba8"
FONT     = ("Segoe UI", 11)
MONO     = ("Consolas", 10)
BOLD     = ("Segoe UI", 13, "bold")

history = []
MAX_TURNS = 20

SYSTEM_PROMPTS = {
    "Default":  "You are a helpful AI assistant. Answer clearly and concisely.",
    "Coder":    "You are an expert software engineer. Provide clean, well-commented code.",
    "Analyst":  "You are a data analyst. Help with data, queries, and findings.",
}

def ollama_available():
    try:
        requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        return True
    except:
        return False

def list_models():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return [m["name"] for m in r.json().get("models", [])]
    except:
        return []

def chat_ollama(messages, model):
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": model, "messages": messages, "stream": False,
                  "options": {"temperature": 0.7}},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        return "❌ Ollama offline. Run:  ollama serve"
    except Exception as e:
        return f"❌ Error: {e}"

def clean(text):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🤖 Local AI Assistant")
        self.geometry("1050x680")
        self.minsize(750, 500)
        self.configure(bg=BG_DARK)
        self._build()
        self._status_check()

    def _build(self):
        bar = tk.Frame(self, bg=BG_MID, height=48)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)
        tk.Label(bar, text="🤖  Local AI Assistant", bg=BG_MID, fg=FG,
                 font=BOLD).pack(side=tk.LEFT, padx=14)
        self.status_lbl = tk.Label(bar, text="⚙ Checking Ollama…",
                                   bg=BG_MID, fg=FG_DIM, font=FONT)
        self.status_lbl.pack(side=tk.RIGHT, padx=14)

        content = tk.Frame(self, bg=BG_DARK)
        content.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        self._sidebar(content)
        self._chat_area(content)

    def _sidebar(self, parent):
        side = tk.Frame(parent, bg=BG_MID, width=220)
        side.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8), pady=4)
        side.pack_propagate(False)

        def hdr(t):
            tk.Label(side, text=t, bg=BG_MID, fg=ACCENT,
                     font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(12, 2))

        hdr("⚙ Model Manager")
        self.model_var = tk.StringVar(value="deepseek-coder")
        self.model_cb = ttk.Combobox(side, textvariable=self.model_var,
                                     values=["deepseek-coder", "qwen2.5-coder", "codellama"],
                                     state="readonly", width=22)
        self.model_cb.pack(padx=10, pady=2, fill=tk.X)
        tk.Button(side, text="🔄 Refresh Models", bg=BG_LIGHT, fg=FG,
                  relief=tk.FLAT, cursor="hand2",
                  command=self._refresh_models).pack(padx=10, pady=3, fill=tk.X)

        hdr("🛠 Mode")
        self.mode_var = tk.StringVar(value="Default")
        for m in SYSTEM_PROMPTS:
            tk.Radiobutton(side, text=m, variable=self.mode_var, value=m,
                           bg=BG_MID, fg=FG, selectcolor=BG_LIGHT,
                           activebackground=BG_MID, font=FONT).pack(anchor=tk.W, padx=14)

        hdr("📁 File Context")
        tk.Button(side, text="📄 Load File", bg=BG_LIGHT, fg=FG,
                  relief=tk.FLAT, cursor="hand2",
                  command=self._load_file).pack(padx=10, pady=3, fill=tk.X)
        self.file_lbl = tk.Label(side, text="No file loaded",
                                 bg=BG_MID, fg=FG_DIM, font=("Segoe UI", 9), wraplength=190)
        self.file_lbl.pack(padx=10)

        hdr("💬 Chat")
        tk.Button(side, text="🧹 Clear Chat", bg=BG_LIGHT, fg=FG,
                  relief=tk.FLAT, cursor="hand2",
                  command=self._clear_chat).pack(padx=10, pady=3, fill=tk.X)
        tk.Button(side, text="🗑 Clear Memory", bg=BG_LIGHT, fg=FG,
                  relief=tk.FLAT, cursor="hand2",
                  command=self._clear_memory).pack(padx=10, pady=3, fill=tk.X)

    def _chat_area(self, parent):
        frame = tk.Frame(parent, bg=BG_DARK)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.display = scrolledtext.ScrolledText(
            frame, bg=BG_MID, fg=FG, font=MONO, wrap=tk.WORD,
            state=tk.DISABLED, relief=tk.FLAT, padx=10, pady=10)
        self.display.pack(fill=tk.BOTH, expand=True)
        self.display.tag_config("user",      foreground=USER_CLR, font=("Segoe UI", 11, "bold"))
        self.display.tag_config("assistant", foreground=BOT_CLR,  font=MONO)
        self.display.tag_config("system",    foreground=FG_DIM,   font=("Segoe UI", 9, "italic"))
        self.display.tag_config("error",     foreground=ERR_CLR)

        inp_frame = tk.Frame(frame, bg=BG_DARK)
        inp_frame.pack(fill=tk.X, pady=(6, 0))

        self.inp = tk.Text(inp_frame, bg=BG_MID, fg=FG, font=FONT,
                           height=3, relief=tk.FLAT, padx=8, pady=6, wrap=tk.WORD)
        self.inp.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        self.inp.bind("<Return>", self._on_enter)

        tk.Button(inp_frame, text="Send ➤", bg=ACCENT, fg="white",
                  font=("Segoe UI", 11, "bold"), relief=tk.FLAT,
                  cursor="hand2", padx=16,
                  command=self._send).pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(frame, text="Enter → Send   |   Shift+Enter → New line",
                 bg=BG_DARK, fg=FG_DIM, font=("Segoe UI", 8)).pack(anchor=tk.E, pady=(2, 0))

        self._append("system", "Welcome to Local AI Assistant! 🤖\n"
                               "Type a message and press Enter.\n"
                               "Make sure Ollama is running: ollama serve\n\n")

    def _append(self, tag, text):
        def _do():
            self.display.configure(state=tk.NORMAL)
            self.display.insert(tk.END, text, tag)
            self.display.see(tk.END)
            self.display.configure(state=tk.DISABLED)
        self.after(0, _do)

    def _remove_thinking(self):
        def _do():
            self.display.configure(state=tk.NORMAL)
            content = self.display.get("1.0", tk.END)
            line = "Assistant is thinking…\n"
            idx = content.rfind(line)
            if idx != -1:
                self.display.delete(f"1.0+{idx}c", f"1.0+{idx+len(line)}c")
            self.display.configure(state=tk.DISABLED)
        self.after(0, _do)

    def _on_enter(self, event):
        if not (event.state & 0x1):
            self._send()
            return "break"

    def _send(self):
        text = self.inp.get("1.0", tk.END).strip()
        if not text:
            return
        self.inp.delete("1.0", tk.END)
        self._append("user", f"You: {text}\n")
        threading.Thread(target=self._infer, args=(text,), daemon=True).start()

    def _infer(self, text):
        global history
        system = SYSTEM_PROMPTS.get(self.mode_var.get(), SYSTEM_PROMPTS["Default"])
        messages = [{"role": "system", "content": system}]
        messages += history[-MAX_TURNS * 2:]
        messages.append({"role": "user", "content": text})

        self._append("system", "Assistant is thinking…\n")
        raw = chat_ollama(messages, self.model_var.get())
        response = clean(raw)

        history.append({"role": "user",      "content": text})
        history.append({"role": "assistant", "content": response})
        if len(history) > MAX_TURNS * 2:
            history = history[-MAX_TURNS * 2:]

        self._remove_thinking()
        self._append("assistant", f"Assistant: {response}\n\n")

    def _refresh_models(self):
        models = list_models()
        if models:
            self.model_cb["values"] = models
            self._append("system", f"[Models: {', '.join(models)}]\n")
        else:
            self._append("error", "[Cannot reach Ollama — is it running?]\n")

    def _load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Code/Text", "*.py *.txt *.md *.js *.ts *.json"), ("All", "*.*")])
        if not path:
            return
        try:
            content = open(path, encoding="utf-8", errors="ignore").read()[:3000]
            history.append({
                "role": "system",
                "content": f"### File context: {os.path.basename(path)}\n```\n{content}\n```"
            })
            self.file_lbl.configure(text=f"✅ {os.path.basename(path)}")
            self._append("system", f"[File loaded: {os.path.basename(path)}]\n")
        except Exception as e:
            self._append("error", f"[File error: {e}]\n")

    def _clear_chat(self):
        self.display.configure(state=tk.NORMAL)
        self.display.delete("1.0", tk.END)
        self.display.configure(state=tk.DISABLED)

    def _clear_memory(self):
        global history
        history = []
        self._append("system", "[Memory cleared]\n")

    def _status_check(self):
        def _check():
            if ollama_available():
                models = list_models()
                txt   = f"✅ Ollama running  |  {len(models)} model(s)"
                color = ACCENT2
                if models:
                    self.after(0, lambda: self.model_cb.configure(values=models))
            else:
                txt   = "❌ Ollama offline — run `ollama serve`"
                color = ERR_CLR
            self.after(0, lambda: self.status_lbl.configure(text=txt, fg=color))
        threading.Thread(target=_check, daemon=True).start()


if __name__ == "__main__":
    App().mainloop()
