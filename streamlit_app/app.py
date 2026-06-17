"""
Local AI Assistant — Streamlit Web Version
Uses Groq API for fast cloud-based LLM inference.
"""

import streamlit as st
import os
import re
from groq import Groq

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🤖 AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS (dark theme) ───────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #1e1e2e; color: #cdd6f4; }
    .stSidebar { background-color: #2a2a3e; }
    .stTextInput > div > div > input { background-color: #313150; color: #cdd6f4; }
    .stTextArea > div > div > textarea { background-color: #313150; color: #cdd6f4; }
    .stSelectbox > div > div { background-color: #313150; color: #cdd6f4; }
    .user-msg {
        background: #313150;
        border-left: 4px solid #89dceb;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
        color: #89dceb;
        font-weight: bold;
    }
    .bot-msg {
        background: #2a2a3e;
        border-left: 4px solid #a6e3a1;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
        color: #cdd6f4;
    }
    .system-msg {
        background: #1e1e2e;
        border-left: 4px solid #6c7086;
        padding: 8px 16px;
        border-radius: 8px;
        margin: 4px 0;
        color: #6c7086;
        font-size: 0.85em;
        font-style: italic;
    }
    .stButton > button {
        background-color: #7c6af7;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #6a5ae0;
        color: white;
    }
    h1, h2, h3 { color: #cdd6f4 !important; }
</style>
""", unsafe_allow_html=True)

# ── Available models on Groq ──────────────────────────────────────────────────
MODELS = {
    "Qwen 3 — 32B (Smart)":        "qwen/qwen3-32b",
    "Llama 3.3 — 70B (Powerful)":  "llama-3.3-70b-versatile",
    "Llama 3.1 — 8B (Fast)":       "llama-3.1-8b-instant",
    "Gemma 2 — 9B":                 "gemma2-9b-it",
    "DeepSeek R1 — 70B (Coder)":   "deepseek-r1-distill-llama-70b",
    "Mixtral 8x7B":                 "mixtral-8x7b-32768",
}

SYSTEM_PROMPTS = {
    "Default":  "You are a helpful AI assistant. Answer clearly and concisely.",
    "Coder":    "You are an expert software engineer. Provide clean, well-commented code and explain your reasoning.",
    "Analyst":  "You are a data analyst. Help interpret data, write queries, and explain findings clearly.",
    "Teacher":  "You are a patient teacher. Explain concepts step by step in simple language.",
}

# ── Session state init ────────────────────────────────────────────────────────
if "messages"    not in st.session_state: st.session_state.messages    = []
if "groq_client" not in st.session_state: st.session_state.groq_client = None
if "api_key"     not in st.session_state:
    # Auto-load from Streamlit secrets if available
    try:
        st.session_state.api_key = st.secrets["GROQ_API_KEY"]
        st.session_state.groq_client = Groq(api_key=st.session_state.api_key)
    except:
        st.session_state.api_key = ""

# ── Helper: clean LLM output ──────────────────────────────────────────────────
def clean_response(text: str) -> str:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return re.sub(r"\n{3,}", "\n\n", text).strip()

# ── Helper: call Groq API ─────────────────────────────────────────────────────
def get_response(messages: list, model: str, system_prompt: str) -> str:
    if not st.session_state.groq_client:
        return "❌ Please enter your Groq API key in the sidebar."
    try:
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        resp = st.session_state.groq_client.chat.completions.create(
            model=model,
            messages=full_messages,
            max_tokens=4096,
            temperature=0.7,
            stream=False,
        )
        return clean_response(resp.choices[0].message.content)
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ════════════════════════════════════════════════════════════════════════════ #
#  SIDEBAR                                                                     #
# ════════════════════════════════════════════════════════════════════════════ #
with st.sidebar:
    st.title("🤖 AI Assistant")
    st.markdown("---")

    # API Key — only show if not already loaded from secrets
    st.subheader("🔑 Groq API Key")
    if st.session_state.api_key:
        st.success("✅ API Key loaded")
    else:
        api_key_input = st.text_input(
            "Enter API Key",
            type="password",
            value=st.session_state.api_key,
            placeholder="gsk_...",
            help="Get free key at console.groq.com",
        )
        if api_key_input and api_key_input != st.session_state.api_key:
            st.session_state.api_key     = api_key_input
            st.session_state.groq_client = Groq(api_key=api_key_input)
            st.success("✅ API Key saved!")

        if not st.session_state.api_key:
            st.warning("⚠️ Get free key at [console.groq.com](https://console.groq.com)")

    st.markdown("---")

    # Model selector
    st.subheader("⚙️ Model Manager")
    selected_model_name = st.selectbox(
        "Choose Model",
        list(MODELS.keys()),
        index=0,
    )
    selected_model = MODELS[selected_model_name]
    st.caption(f"`{selected_model}`")

    st.markdown("---")

    # Mode selector
    st.subheader("🛠️ Mode")
    selected_mode = st.radio(
        "Assistant Mode",
        list(SYSTEM_PROMPTS.keys()),
        index=0,
    )

    st.markdown("---")

    # File context
    st.subheader("📁 File Context")
    uploaded_file = st.file_uploader(
        "Upload a file",
        type=["py", "txt", "md", "js", "ts", "json", "csv", "yaml", "toml"],
        help="File content will be added to the conversation context",
    )
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8", errors="ignore")[:3000]
        file_context = f"### File: {uploaded_file.name}\n```\n{file_content}\n```"
        # Add file context to messages only once
        if not any(uploaded_file.name in m.get("content", "") for m in st.session_state.messages):
            st.session_state.messages.append({
                "role": "system",
                "content": file_context,
                "_is_file": True,
                "_filename": uploaded_file.name,
            })
            st.success(f"✅ {uploaded_file.name} loaded!")

    st.markdown("---")

    # Stats
    st.subheader("📊 Stats")
    st.metric("Messages in memory", len([m for m in st.session_state.messages if m["role"] in ("user", "assistant")]))

    st.markdown("---")

    # Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🗑️ Clear Memory", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════ #
#  MAIN CHAT AREA                                                              #
# ════════════════════════════════════════════════════════════════════════════ #
st.title("🤖 Local AI Assistant")
st.caption(f"Model: `{selected_model}` | Mode: **{selected_mode}**")
st.markdown("---")

# Display chat history
chat_container = st.container()
with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div class="system-msg">
        👋 Welcome! Enter your Groq API key in the sidebar and start chatting.<br>
        Get a <strong>free API key</strong> at <a href="https://console.groq.com" target="_blank">console.groq.com</a>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            role = msg["role"]
            content = msg["content"]

            # Skip hidden system/file messages in display
            if role == "system" and msg.get("_is_file"):
                st.markdown(f"""
                <div class="system-msg">📄 File loaded: <strong>{msg.get('_filename', 'file')}</strong></div>
                """, unsafe_allow_html=True)
                continue
            if role == "system":
                continue

            if role == "user":
                st.markdown(f"""
                <div class="user-msg">👤 You<br><br>{content}</div>
                """, unsafe_allow_html=True)
            elif role == "assistant":
                st.markdown(f"""
                <div class="bot-msg">🤖 Assistant<br><br>{content}</div>
                """, unsafe_allow_html=True)

st.markdown("---")

# Input area
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_area(
            "Message",
            placeholder="Type your message here... (Ctrl+Enter to send)",
            height=80,
            label_visibility="collapsed",
        )
    with col2:
        submitted = st.form_submit_button(
            "Send ➤",
            use_container_width=True,
            type="primary",
        )

if submitted and user_input.strip():
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    # Get only user/assistant messages for API (no internal system messages)
    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
        if m["role"] in ("user", "assistant")
    ]

    # Add file contexts if any
    file_contexts = [
        m["content"] for m in st.session_state.messages
        if m.get("_is_file")
    ]
    system_prompt = SYSTEM_PROMPTS[selected_mode]
    if file_contexts:
        system_prompt += "\n\n" + "\n\n".join(file_contexts)

    # Get response with spinner
    with st.spinner("🤔 Thinking..."):
        response = get_response(api_messages, selected_model, system_prompt)

    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
