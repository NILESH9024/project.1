"""
NILESH AI Assistant — Streamlit Web Version
Features:
  1. Code Editor + Review
  2. PDF/Document Chat
  4. Chat History Export
  5. Multi-language Support
  8. Resume Analyzer
"""

import streamlit as st
import os
import re
import json
import base64
from datetime import datetime
from groq import Groq

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🤖 NILESH AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
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
    .stButton > button:hover { background-color: #6a5ae0; color: white; }
    h1, h2, h3 { color: #cdd6f4 !important; }
    .feature-card {
        background: #2a2a3e;
        border-radius: 10px;
        padding: 16px;
        margin: 8px 0;
        border: 1px solid #313150;
    }
</style>
""", unsafe_allow_html=True)

# ── Models ────────────────────────────────────────────────────────────────────
MODELS = {
    "Qwen 3 — 32B (Smart)":       "qwen/qwen3-32b",
    "Llama 3.3 — 70B (Powerful)": "llama-3.3-70b-versatile",
    "Llama 3.1 — 8B (Fast)":      "llama-3.1-8b-instant",
    "Gemma 2 — 9B":                "gemma2-9b-it",
    "DeepSeek R1 — 70B (Coder)":  "deepseek-r1-distill-llama-70b",
    "Mixtral 8x7B":                "mixtral-8x7b-32768",
}

# ── Languages ─────────────────────────────────────────────────────────────────
LANGUAGES = {
    "English": "Respond in English.",
    "Hindi": "हमेशा हिंदी में जवाब दो।",
    "Hinglish": "Respond in Hinglish (mix of Hindi and English).",
    "Spanish": "Responde siempre en español.",
    "French": "Réponds toujours en français.",
    "German": "Antworte immer auf Deutsch.",
}

# ── System prompts ────────────────────────────────────────────────────────────
SYSTEM_PROMPTS = {
    "Default": (
        "You are NILESH AI Assistant — a helpful, smart AI. Answer clearly and concisely. "
        "This app was developed by NILESH PURI GOSWAMI. "
        "If anyone asks who developed or created this app, answer: 'This app was developed by NILESH PURI GOSWAMI.'"
    ),
    "Coder": (
        "You are an expert software engineer. Provide clean, well-commented code. "
        "Always explain your code. Suggest optimizations. "
        "This app was developed by NILESH PURI GOSWAMI. "
        "If asked who built this, say: 'This app was developed by NILESH PURI GOSWAMI.'"
    ),
    "Analyst": (
        "You are a data analyst. Help with data, queries, charts, and findings. "
        "This app was developed by NILESH PURI GOSWAMI."
    ),
    "Teacher": (
        "You are a patient teacher. Explain step by step in simple language. "
        "Use examples. This app was developed by NILESH PURI GOSWAMI."
    ),
    "Resume Expert": (
        "You are an expert HR consultant and resume coach with 10+ years experience. "
        "Analyze resumes thoroughly. Give specific, actionable feedback on: "
        "1) Format & Structure 2) Content & Keywords 3) Achievements 4) ATS compatibility "
        "5) Overall score out of 10. Be constructive and detailed. "
        "This app was developed by NILESH PURI GOSWAMI."
    ),
}

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    "messages": [],
    "groq_client": None,
    "api_key": "",
    "active_tab": "💬 Chat",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Auto-load API key from secrets
if not st.session_state.api_key:
    try:
        st.session_state.api_key = st.secrets["GROQ_API_KEY"]
        st.session_state.groq_client = Groq(api_key=st.session_state.api_key)
    except:
        pass

# ── Helper functions ──────────────────────────────────────────────────────────
def clean(text: str) -> str:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return re.sub(r"\n{3,}", "\n\n", text).strip()

def ask_groq(messages: list, model: str, system: str) -> str:
    if not st.session_state.groq_client:
        return "❌ Please enter your Groq API key in the sidebar."
    try:
        full = [{"role": "system", "content": system}] + messages
        resp = st.session_state.groq_client.chat.completions.create(
            model=model, messages=full, max_tokens=4096, temperature=0.7,
        )
        return clean(resp.choices[0].message.content)
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_download_link(content: str, filename: str, label: str) -> str:
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">{label}</a>'

# ════════════════════════════════════════════════════════════════════════════ #
#  SIDEBAR                                                                     #
# ════════════════════════════════════════════════════════════════════════════ #
with st.sidebar:
    st.title("🤖 NILESH AI Assistant")
    st.markdown("---")

    # API Key
    st.subheader("🔑 API Key")
    if st.session_state.api_key:
        st.success("✅ API Key loaded")
    else:
        key_input = st.text_input("Enter Groq API Key", type="password", placeholder="gsk_...")
        if key_input:
            st.session_state.api_key = key_input
            st.session_state.groq_client = Groq(api_key=key_input)
            st.success("✅ Saved!")
        else:
            st.warning("Get free key: [console.groq.com](https://console.groq.com)")

    st.markdown("---")

    # Model
    st.subheader("⚙️ Model")
    model_name = st.selectbox("Choose Model", list(MODELS.keys()))
    selected_model = MODELS[model_name]
    st.caption(f"`{selected_model}`")

    st.markdown("---")

    # Mode
    st.subheader("🛠️ Mode")
    selected_mode = st.radio("Mode", list(SYSTEM_PROMPTS.keys()))

    st.markdown("---")

    # Language (Feature 5)
    st.subheader("🌐 Language")
    selected_lang = st.selectbox("Response Language", list(LANGUAGES.keys()))

    st.markdown("---")

    # Stats
    msg_count = len([m for m in st.session_state.messages if m["role"] in ("user","assistant")])
    st.metric("Messages", msg_count)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧹 Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("📥 Export", use_container_width=True):
            st.session_state.show_export = True

    st.markdown("---")
    st.caption("Built by **NILESH PURI GOSWAMI**")

# ════════════════════════════════════════════════════════════════════════════ #
#  MAIN AREA — TABS                                                            #
# ════════════════════════════════════════════════════════════════════════════ #
st.title("🤖 NILESH AI Assistant")
st.caption(f"Model: `{selected_model}` | Mode: **{selected_mode}** | Lang: **{selected_lang}**")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Chat",
    "💻 Code Editor",
    "📄 PDF / Doc Chat",
    "📋 Resume Analyzer",
])

# ─── TAB 1: CHAT ─────────────────────────────────────────────────────────────
with tab1:
    # Display chat
    if not st.session_state.messages:
        st.markdown("""
        <div class="system-msg">
        👋 Welcome to <strong>NILESH AI Assistant</strong>!<br>
        Type a message below and press Send to start chatting.
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-msg">👤 You<br><br>{msg["content"]}</div>',
                            unsafe_allow_html=True)
            elif msg["role"] == "assistant":
                st.markdown(f'<div class="bot-msg">🤖 Assistant<br><br>{msg["content"]}</div>',
                            unsafe_allow_html=True)

    st.markdown("---")

    # Input
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_area("Message", placeholder="Type your message here...",
                                      height=80, label_visibility="collapsed")
        with col2:
            submitted = st.form_submit_button("Send ➤", use_container_width=True, type="primary")

    if submitted and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})
        api_msgs = [{"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages if m["role"] in ("user","assistant")]
        system = SYSTEM_PROMPTS[selected_mode] + " " + LANGUAGES[selected_lang]
        with st.spinner("🤔 Thinking..."):
            response = ask_groq(api_msgs, selected_model, system)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    # Export chat (Feature 4)
    if st.session_state.get("show_export"):
        if st.session_state.messages:
            chat_text = f"NILESH AI Assistant — Chat Export\n{'='*50}\n"
            chat_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n{'='*50}\n\n"
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    chat_text += f"You: {msg['content']}\n\n"
                elif msg["role"] == "assistant":
                    chat_text += f"Assistant: {msg['content']}\n\n{'─'*40}\n\n"
            st.markdown(
                get_download_link(chat_text, "chat_export.txt", "📥 Click here to download chat"),
                unsafe_allow_html=True
            )
        st.session_state.show_export = False

# ─── TAB 2: CODE EDITOR ──────────────────────────────────────────────────────
with tab2:
    st.subheader("💻 Code Editor & AI Review")
    st.caption("Paste your code → Get instant AI review, debug help, or optimization tips")

    col1, col2 = st.columns([1, 1])

    with col1:
        code_lang = st.selectbox("Language", [
            "Python", "JavaScript", "C++", "Java", "C", "TypeScript",
            "HTML", "CSS", "SQL", "Go", "Rust", "PHP",
        ])
        code_input = st.text_area("📝 Paste your code here",
                                  height=350,
                                  placeholder="# Paste your code here...",
                                  key="code_input")
        action = st.selectbox("What do you want?", [
            "🔍 Review & Explain",
            "🐛 Debug / Find Errors",
            "⚡ Optimize Performance",
            "📝 Add Comments",
            "🔄 Convert to another language",
            "✅ Write Test Cases",
        ])

        if action == "🔄 Convert to another language":
            target_lang = st.selectbox("Convert to", [
                "Python", "JavaScript", "C++", "Java", "TypeScript", "Go"
            ])

        if st.button("🚀 Analyze Code", use_container_width=True, type="primary"):
            if code_input.strip():
                if action == "🔄 Convert to another language":
                    prompt = f"Convert this {code_lang} code to {target_lang}. Provide clean, working code with comments:\n\n```{code_lang.lower()}\n{code_input}\n```"
                elif action == "🔍 Review & Explain":
                    prompt = f"Review and explain this {code_lang} code in detail:\n\n```{code_lang.lower()}\n{code_input}\n```"
                elif action == "🐛 Debug / Find Errors":
                    prompt = f"Find all bugs and errors in this {code_lang} code. Provide fixed version:\n\n```{code_lang.lower()}\n{code_input}\n```"
                elif action == "⚡ Optimize Performance":
                    prompt = f"Optimize this {code_lang} code for better performance. Explain improvements:\n\n```{code_lang.lower()}\n{code_input}\n```"
                elif action == "📝 Add Comments":
                    prompt = f"Add detailed comments to this {code_lang} code:\n\n```{code_lang.lower()}\n{code_input}\n```"
                elif action == "✅ Write Test Cases":
                    prompt = f"Write comprehensive test cases for this {code_lang} code:\n\n```{code_lang.lower()}\n{code_input}\n```"

                system = SYSTEM_PROMPTS["Coder"] + " " + LANGUAGES[selected_lang]
                with st.spinner("🤔 Analyzing code..."):
                    result = ask_groq([{"role": "user", "content": prompt}], selected_model, system)
                st.session_state["code_result"] = result
            else:
                st.warning("Please paste some code first!")

    with col2:
        st.subheader("🤖 AI Response")
        if "code_result" in st.session_state:
            st.markdown(st.session_state["code_result"])
            st.markdown(
                get_download_link(st.session_state["code_result"], "code_review.txt", "📥 Download Review"),
                unsafe_allow_html=True
            )
        else:
            st.info("👈 Paste code and click **Analyze Code** to get AI feedback")

# ─── TAB 3: PDF / DOC CHAT ───────────────────────────────────────────────────
with tab3:
    st.subheader("📄 PDF / Document Chat")
    st.caption("Upload a document and ask questions about it")

    uploaded_file = st.file_uploader(
        "Upload PDF, TXT, or MD file",
        type=["txt", "md", "py", "js", "csv", "json"],
        help="PDF support coming soon. Currently supports TXT, MD, CSV, JSON, PY, JS"
    )

    if uploaded_file:
        try:
            doc_content = uploaded_file.read().decode("utf-8", errors="ignore")
            st.success(f"✅ File loaded: **{uploaded_file.name}** ({len(doc_content)} chars)")

            with st.expander("👁️ Preview file content"):
                st.text(doc_content[:1000] + ("..." if len(doc_content) > 1000 else ""))

            st.markdown("---")
            st.subheader("💬 Ask about this document")

            if "doc_messages" not in st.session_state:
                st.session_state.doc_messages = []

            # Display doc chat
            for msg in st.session_state.doc_messages:
                if msg["role"] == "user":
                    st.markdown(f'<div class="user-msg">👤 You: {msg["content"]}</div>',
                                unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-msg">🤖 Assistant: {msg["content"]}</div>',
                                unsafe_allow_html=True)

            with st.form("doc_form", clear_on_submit=True):
                doc_q = st.text_input("Ask a question about this document...",
                                      placeholder="e.g. Summarize this document / What are the main points?")
                doc_submit = st.form_submit_button("Ask ➤", type="primary")

            if doc_submit and doc_q.strip():
                prompt = (f"Answer based on this document:\n\n"
                          f"```\n{doc_content[:6000]}\n```\n\n"
                          f"Question: {doc_q}")
                system = (f"You are a document analysis expert. Answer questions accurately "
                          f"based only on the provided document content. "
                          f"This app was developed by NILESH PURI GOSWAMI. "
                          + LANGUAGES[selected_lang])
                st.session_state.doc_messages.append({"role": "user", "content": doc_q})
                with st.spinner("📖 Reading document..."):
                    answer = ask_groq(
                        [{"role": "user", "content": prompt}],
                        selected_model, system
                    )
                st.session_state.doc_messages.append({"role": "assistant", "content": answer})
                st.rerun()

            if st.button("🗑️ Clear Doc Chat"):
                st.session_state.doc_messages = []
                st.rerun()

        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.info("👆 Upload a file to start chatting with your document")
        st.markdown("""
        **What you can do:**
        - 📝 Summarize long documents
        - ❓ Ask specific questions
        - 🔍 Extract key information
        - 📊 Analyze CSV/JSON data
        - 💻 Explain code files
        """)

# ─── TAB 4: RESUME ANALYZER ──────────────────────────────────────────────────
with tab4:
    st.subheader("📋 Resume Analyzer")
    st.caption("Paste your resume → Get professional AI feedback")

    col1, col2 = st.columns([1, 1])

    with col1:
        job_role = st.text_input("🎯 Target Job Role (optional)",
                                  placeholder="e.g. Software Engineer, Data Analyst, ML Engineer")
        resume_text = st.text_area(
            "📄 Paste your Resume here",
            height=400,
            placeholder="Paste your complete resume text here...\n\nName:\nEmail:\nSkills:\nExperience:\nEducation:\n..."
        )

        analyze_type = st.selectbox("Analysis Type", [
            "🔍 Full Review (Recommended)",
            "📊 ATS Score & Keywords",
            "💡 Improvement Suggestions",
            "✍️ Rewrite Summary/Objective",
            "🎯 Match with Job Description",
        ])

        if analyze_type == "🎯 Match with Job Description":
            job_desc = st.text_area("📋 Paste Job Description", height=150,
                                     placeholder="Paste the job description here...")

        if st.button("🚀 Analyze Resume", use_container_width=True, type="primary"):
            if resume_text.strip():
                if analyze_type == "🔍 Full Review (Recommended)":
                    prompt = (f"Analyze this resume for the role of '{job_role or 'General'}'. "
                              f"Give detailed feedback on:\n"
                              f"1. Overall Score (out of 10)\n"
                              f"2. Strengths ✅\n"
                              f"3. Weaknesses ❌\n"
                              f"4. Missing Keywords\n"
                              f"5. Format & Structure\n"
                              f"6. Specific Improvements\n\n"
                              f"Resume:\n{resume_text}")
                elif analyze_type == "📊 ATS Score & Keywords":
                    prompt = (f"Check this resume for ATS (Applicant Tracking System) compatibility "
                              f"for '{job_role or 'Software'}' role. "
                              f"Give ATS score, missing keywords, and fixes:\n\n{resume_text}")
                elif analyze_type == "💡 Improvement Suggestions":
                    prompt = (f"Give 10 specific, actionable improvement suggestions for this resume "
                              f"for '{job_role or 'General'}' role:\n\n{resume_text}")
                elif analyze_type == "✍️ Rewrite Summary/Objective":
                    prompt = (f"Rewrite the professional summary/objective section of this resume "
                              f"for '{job_role or 'General'}' role. Make it impactful and ATS-friendly:\n\n{resume_text}")
                elif analyze_type == "🎯 Match with Job Description":
                    prompt = (f"Compare this resume with the job description. "
                              f"Give match percentage, matched skills, missing skills, and suggestions:\n\n"
                              f"Resume:\n{resume_text}\n\nJob Description:\n{job_desc}")

                system = SYSTEM_PROMPTS["Resume Expert"] + " " + LANGUAGES[selected_lang]
                with st.spinner("📋 Analyzing resume..."):
                    result = ask_groq([{"role": "user", "content": prompt}], selected_model, system)
                st.session_state["resume_result"] = result
            else:
                st.warning("Please paste your resume first!")

    with col2:
        st.subheader("🤖 AI Feedback")
        if "resume_result" in st.session_state:
            st.markdown(st.session_state["resume_result"])
            st.markdown(
                get_download_link(st.session_state["resume_result"],
                                  "resume_feedback.txt", "📥 Download Feedback"),
                unsafe_allow_html=True
            )
        else:
            st.info("👈 Paste your resume and click **Analyze Resume**")
            st.markdown("""
            **Resume Analyzer can:**
            - ⭐ Score your resume out of 10
            - 🔍 Check ATS compatibility
            - 💡 Suggest improvements
            - ✍️ Rewrite your summary
            - 🎯 Match with job descriptions
            """)
