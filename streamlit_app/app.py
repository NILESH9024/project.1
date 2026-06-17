"""
NILESH AI — Coding Assistant
Professional AI-powered coding assistant built by NILESH PURI GOSWAMI
"""
import streamlit as st
import re, base64
from groq import Groq

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NILESH AI — Coding Assistant",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }
.stApp { background: #0d1117; color: #e6edf3; }
section[data-testid="stSidebar"] {
    background: #161b22 !important;
    border-right: 1px solid #21262d;
}
#MainMenu, footer, header { visibility: hidden; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #161b22;
    border-bottom: 1px solid #21262d;
    gap: 0; padding: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #7d8590;
    border-radius: 0;
    font-size: 14px;
    font-weight: 500;
    padding: 12px 20px;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: #e6edf3 !important;
    border-bottom: 2px solid #f78166 !important;
}

/* Buttons */
.stButton > button {
    background: #238636 !important;
    color: #ffffff !important;
    border: 1px solid #2ea043 !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 6px 16px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #2ea043 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(46,160,67,0.3) !important;
}

/* Text areas */
.stTextArea textarea {
    background: #0d1117 !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: #388bfd !important;
    box-shadow: 0 0 0 3px rgba(56,139,253,0.15) !important;
}

/* Text inputs */
.stTextInput input {
    background: #0d1117 !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    font-size: 14px !important;
}
.stTextInput input:focus {
    border-color: #388bfd !important;
    box-shadow: 0 0 0 3px rgba(56,139,253,0.15) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #161b22 !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
}

/* Radio */
.stRadio label { color: #e6edf3 !important; font-size: 14px !important; }

/* Chat bubbles */
.user-bubble {
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 12px 12px 2px 12px;
    padding: 12px 16px;
    margin: 8px 0 8px auto;
    max-width: 75%;
    color: #e6edf3;
    font-size: 14px;
    line-height: 1.6;
}
.ai-row { display: flex; gap: 12px; margin: 8px 0; align-items: flex-start; }
.ai-avatar {
    width: 32px; height: 32px; border-radius: 6px;
    background: linear-gradient(135deg, #388bfd, #56cfbf);
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; flex-shrink: 0; margin-top: 2px;
}
.ai-bubble {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 2px 12px 12px 12px;
    padding: 12px 16px;
    max-width: 85%;
    color: #e6edf3;
    font-size: 14px;
    line-height: 1.7;
}

/* Code output card */
.code-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 20px;
}

/* Stat badge */
.badge {
    display: inline-block;
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 12px;
    color: #7d8590;
    margin: 2px;
}

/* Sidebar section headers */
.sidebar-header {
    font-size: 11px;
    font-weight: 600;
    color: #7d8590;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin: 16px 0 6px;
}

/* Welcome area */
.welcome-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 24px; }
.suggestion-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 14px;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
}
.suggestion-card:hover { border-color: #388bfd; background: #1c2128; }
.suggestion-title { font-size: 14px; font-weight: 500; color: #e6edf3; }
.suggestion-sub { font-size: 12px; color: #7d8590; margin-top: 2px; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #388bfd; }

/* Alerts */
div[data-testid="stAlert"] { border-radius: 6px !important; }

/* Expander */
.streamlit-expanderHeader {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 6px !important;
    color: #e6edf3 !important;
}

/* Divider */
hr { border-color: #21262d !important; }
.stCaption { color: #7d8590 !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
MODELS = {
    "⚡ Llama 3.1 — 8B (Fastest)":  "llama-3.1-8b-instant",
    "🧠 Llama 3.3 — 70B (Smart)":   "llama-3.3-70b-versatile",
    "🔮 Qwen 3 — 32B":               "qwen/qwen3-32b",
    "💎 DeepSeek R1 — 70B (Coder)":  "deepseek-r1-distill-llama-70b",
    "🌀 Mixtral 8x7B":               "mixtral-8x7b-32768",
}

LANGUAGES = [
    "Python","JavaScript","TypeScript","C","C++","C#","Java",
    "Go","Rust","Kotlin","Swift","PHP","Ruby","SQL","HTML/CSS",
    "Bash","R","MATLAB",
]

DEV_NOTE = (
    "This coding assistant was developed by NILESH PURI GOSWAMI. "
    "If asked who built or created this app, always say: "
    "'This app was developed by NILESH PURI GOSWAMI.'"
)

SYSTEM_CODING = f"""You are NILESH AI — an expert coding assistant.
You help with: writing code, debugging, code review, optimization, explaining code, and all programming questions.
Always provide clean, well-commented, production-ready code.
When showing code, use proper markdown code blocks with language tags.
Be concise but thorough. {DEV_NOTE}"""

ACTIONS = [
    "🔍 Review & Explain",
    "🐛 Debug & Fix Bugs",
    "⚡ Optimize Code",
    "📝 Add Comments & Docs",
    "🔄 Convert Language",
    "✅ Generate Test Cases",
    "📚 Explain Line by Line",
    "🔒 Security Audit",
    "♻️  Refactor Code",
]

SUGGESTIONS = [
    ("🐛", "Debug this code", "Find and fix all errors"),
    ("⚡", "Optimize my function", "Make it faster and cleaner"),
    ("✅", "Write test cases", "for my Python code"),
    ("📝", "Explain this code", "line by line for beginners"),
    ("🔄", "Convert Python to JS", "Keep same functionality"),
    ("🔒", "Security audit", "Find vulnerabilities in my code"),
]

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "messages": [],
    "groq_client": None,
    "api_key": "",
    "code_result": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Auto-load key from secrets
if not st.session_state.api_key:
    try:
        st.session_state.api_key = st.secrets["GROQ_API_KEY"]
        st.session_state.groq_client = Groq(api_key=st.session_state.api_key)
    except:
        pass

# ── Helpers ───────────────────────────────────────────────────────────────────
def clean(text: str) -> str:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return re.sub(r"\n{3,}", "\n\n", text).strip()

def ask(messages: list, model: str) -> str:
    if not st.session_state.groq_client:
        return "❌ Please enter your Groq API key in the sidebar."
    try:
        full = [{"role": "system", "content": SYSTEM_CODING}] + messages
        resp = st.session_state.groq_client.chat.completions.create(
            model=model, messages=full, max_tokens=4096, temperature=0.3,
        )
        return clean(resp.choices[0].message.content)
    except Exception as e:
        return f"❌ Error: {e}"

def dl_link(content: str, fname: str, label: str) -> str:
    b64 = base64.b64encode(content.encode()).decode()
    return (f'<a href="data:file/txt;base64,{b64}" download="{fname}" '
            f'style="color:#388bfd;font-size:13px;text-decoration:none;">'
            f'⬇️ {label}</a>')

def render_chat():
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div style="display:flex;justify-content:flex-end;">'
                f'<div class="user-bubble">{msg["content"]}</div></div>',
                unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            st.markdown(
                f'<div class="ai-row">'
                f'<div class="ai-avatar">👨‍💻</div>'
                f'<div class="ai-bubble">{msg["content"]}</div></div>',
                unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════ #
#  SIDEBAR                                                                     #
# ════════════════════════════════════════════════════════════════════════════ #
with st.sidebar:
    # Brand
    st.markdown("""
    <div style='padding:12px 0 20px;'>
        <div style='display:flex;align-items:center;gap:10px;'>
            <div style='width:36px;height:36px;border-radius:8px;
                background:linear-gradient(135deg,#388bfd,#56cfbf);
                display:flex;align-items:center;justify-content:center;
                font-size:18px;flex-shrink:0;'>👨‍💻</div>
            <div>
                <div style='font-weight:700;font-size:15px;color:#e6edf3;'>NILESH AI</div>
                <div style='font-size:11px;color:#7d8590;'>Coding Assistant</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # API Key
    st.markdown('<div class="sidebar-header">🔑 API Key</div>', unsafe_allow_html=True)
    if st.session_state.api_key:
        st.markdown(
            '<div style="background:#0d2118;border:1px solid #2ea043;border-radius:6px;'
            'padding:8px 12px;font-size:13px;color:#3fb950;">✅ Connected</div>',
            unsafe_allow_html=True)
    else:
        key_in = st.text_input("", type="password", placeholder="gsk_...",
                                label_visibility="collapsed", key="key_input")
        if key_in:
            st.session_state.api_key = key_in
            st.session_state.groq_client = Groq(api_key=key_in)
            st.rerun()
        st.markdown(
            '<a href="https://console.groq.com" target="_blank" '
            'style="color:#388bfd;font-size:12px;">Get free key →</a>',
            unsafe_allow_html=True)

    st.divider()

    # Model
    st.markdown('<div class="sidebar-header">🤖 Model</div>', unsafe_allow_html=True)
    model_label = st.selectbox("", list(MODELS.keys()), label_visibility="collapsed", key="model_sel")
    selected_model = MODELS[model_label]
    st.caption(f"`{selected_model}`")

    st.divider()

    # Stats
    st.markdown('<div class="sidebar-header">📊 Session Stats</div>', unsafe_allow_html=True)
    msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style='background:#21262d;border:1px solid #30363d;border-radius:6px;
                    padding:10px;text-align:center;'>
            <div style='font-size:22px;font-weight:700;color:#388bfd;'>{msgs}</div>
            <div style='font-size:11px;color:#7d8590;'>Questions</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='background:#21262d;border:1px solid #30363d;border-radius:6px;
                    padding:10px;text-align:center;'>
            <div style='font-size:22px;font-weight:700;color:#3fb950;'>{len(MODELS)}</div>
            <div style='font-size:11px;color:#7d8590;'>Models</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.code_result = ""
        st.rerun()

    st.divider()
    st.markdown(
        '<div style="font-size:11px;color:#7d8590;text-align:center;">'
        'Built by <strong style="color:#e6edf3;">NILESH PURI GOSWAMI</strong></div>',
        unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════ #
#  MAIN — HEADER                                                               #
# ════════════════════════════════════════════════════════════════════════════ #
st.markdown("""
<div style='padding:20px 0 8px;'>
    <h1 style='font-size:24px;font-weight:700;color:#e6edf3;margin:0;'>
        👨‍💻 NILESH AI — Coding Assistant
    </h1>
    <p style='color:#7d8590;font-size:14px;margin:4px 0 0;'>
        Your AI-powered coding companion — Debug · Review · Optimize · Learn
    </p>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["💬  Ask AI", "💻  Code Tools", "📚  Learn & Explain"])

# ════════════════════════════════════════════════════════════════════════════ #
# TAB 1 — ASK AI (Chat)                                                        #
# ════════════════════════════════════════════════════════════════════════════ #
with tab1:
    # Welcome screen
    if not st.session_state.messages:
        st.markdown("""
        <div style='text-align:center;padding:40px 0 32px;'>
            <div style='font-size:52px;'>👨‍💻</div>
            <h2 style='font-size:26px;font-weight:700;color:#e6edf3;margin:12px 0 6px;'>
                How can I help you code today?
            </h2>
            <p style='color:#7d8590;font-size:15px;'>
                Ask me anything about coding — debugging, algorithms, architecture, best practices
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Suggestion grid
        cols = st.columns(3)
        for i, (icon, title, sub) in enumerate(SUGGESTIONS):
            with cols[i % 3]:
                if st.button(f"{icon} **{title}**\n\n_{sub}_",
                             use_container_width=True, key=f"sug_{i}"):
                    q = f"{title} — {sub}"
                    st.session_state.messages.append({"role": "user", "content": q})
                    with st.spinner("Thinking..."):
                        r = ask([{"role": "user", "content": q}], selected_model)
                    st.session_state.messages.append({"role": "assistant", "content": r})
                    st.rerun()
    else:
        render_chat()

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # Input
    with st.form("chat_form", clear_on_submit=True):
        user_in = st.text_area(
            "",
            placeholder="Ask a coding question, paste an error, describe what you want to build...",
            height=80,
            label_visibility="collapsed",
        )
        c1, c2, c3 = st.columns([5, 1, 1])
        with c2:
            send = st.form_submit_button("Send ➤", type="primary", use_container_width=True)
        with c3:
            st.form_submit_button("Clear", use_container_width=True)

    if send and user_in.strip():
        st.session_state.messages.append({"role": "user", "content": user_in.strip()})
        api_msgs = [{"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                    if m["role"] in ("user", "assistant")]
        with st.spinner("💭 Thinking..."):
            resp = ask(api_msgs, selected_model)
        st.session_state.messages.append({"role": "assistant", "content": resp})
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════ #
# TAB 2 — CODE TOOLS                                                           #
# ════════════════════════════════════════════════════════════════════════════ #
with tab2:
    st.markdown("### 💻 Code Tools")
    st.caption("Paste your code and choose an action — review, debug, optimize, convert and more")
    st.divider()

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown("#### 📝 Your Code")

        t1, t2 = st.columns(2)
        with t1:
            src_lang = st.selectbox("Language", LANGUAGES, key="src_lang")
        with t2:
            action = st.selectbox("Action", ACTIONS, key="action_sel")

        # Target language for conversion
        tgt_lang = None
        if action == "🔄 Convert Language":
            tgt_lang = st.selectbox("Convert to", [l for l in LANGUAGES if l != src_lang], key="tgt_lang")

        code_in = st.text_area(
            "",
            height=340,
            placeholder=f"# Paste your {src_lang} code here...",
            label_visibility="collapsed",
            key="code_in",
        )

        if st.button("🚀 Run Analysis", use_container_width=True, type="primary", key="run_btn"):
            if not code_in.strip():
                st.warning("⚠️ Please paste your code first!")
            else:
                code_block = f"```{src_lang.lower()}\n{code_in}\n```"
                prompt_map = {
                    "🔍 Review & Explain":       f"Do a thorough code review of this {src_lang} code. Explain what it does, identify issues, and rate quality:\n\n{code_block}",
                    "🐛 Debug & Fix Bugs":        f"Find ALL bugs and errors in this {src_lang} code. Show the fixed version with explanations:\n\n{code_block}",
                    "⚡ Optimize Code":            f"Optimize this {src_lang} code for performance, readability, and best practices. Show before/after:\n\n{code_block}",
                    "📝 Add Comments & Docs":     f"Add comprehensive comments and docstrings to this {src_lang} code:\n\n{code_block}",
                    "🔄 Convert Language":        f"Convert this {src_lang} code to {tgt_lang}. Keep same logic, add comments:\n\n{code_block}",
                    "✅ Generate Test Cases":      f"Write comprehensive unit tests for this {src_lang} code. Cover edge cases:\n\n{code_block}",
                    "📚 Explain Line by Line":    f"Explain this {src_lang} code line by line for a beginner:\n\n{code_block}",
                    "🔒 Security Audit":          f"Do a security audit of this {src_lang} code. Find vulnerabilities and suggest fixes:\n\n{code_block}",
                    "♻️  Refactor Code":           f"Refactor this {src_lang} code using best practices and design patterns:\n\n{code_block}",
                }
                with st.spinner(f"🔍 Running {action}..."):
                    st.session_state.code_result = ask(
                        [{"role": "user", "content": prompt_map[action]}],
                        selected_model
                    )

    with col_right:
        st.markdown("#### 🤖 AI Analysis")
        if st.session_state.code_result:
            result_container = st.container()
            with result_container:
                st.markdown(st.session_state.code_result)

            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(
                    dl_link(st.session_state.code_result, "analysis.txt", "Download Result"),
                    unsafe_allow_html=True)
            with c2:
                if st.button("💬 Continue in Chat", key="to_chat"):
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": st.session_state.code_result
                    })
                    st.info("Result added to chat! Switch to 💬 Ask AI tab.")
        else:
            st.markdown("""
            <div style='background:#161b22;border:1px solid #21262d;border-radius:8px;
                        padding:48px 24px;text-align:center;height:420px;
                        display:flex;flex-direction:column;align-items:center;justify-content:center;'>
                <div style='font-size:36px;margin-bottom:16px;'>💻</div>
                <h3 style='color:#e6edf3;font-size:16px;margin:0 0 8px;'>Ready to analyze your code</h3>
                <p style='color:#7d8590;font-size:13px;margin:0;'>
                    Paste code on the left and choose an action
                </p>
                <br>
                <div style='color:#7d8590;font-size:12px;text-align:left;'>
                    <p>🔍 Review · 🐛 Debug · ⚡ Optimize</p>
                    <p>🔄 Convert · ✅ Test · 🔒 Security</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════ #
# TAB 3 — LEARN & EXPLAIN                                                      #
# ════════════════════════════════════════════════════════════════════════════ #
with tab3:
    st.markdown("### 📚 Learn & Explain")
    st.caption("Learn concepts, get explanations, explore algorithms")
    st.divider()

    learn_type = st.radio(
        "What do you want?",
        ["📖 Explain a Concept", "🔢 Algorithm Visualizer",
         "⚖️  Compare Technologies", "📋 Cheat Sheet Generator"],
        horizontal=True,
        key="learn_type"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if learn_type == "📖 Explain a Concept":
        col1, col2 = st.columns([3, 1])
        with col1:
            concept = st.text_input("", placeholder="e.g. recursion, binary search, REST APIs, async/await, Big O notation...",
                                     label_visibility="collapsed", key="concept_in")
        with col2:
            level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"], key="level_sel")

        if st.button("📖 Explain", type="primary", key="explain_btn") and concept.strip():
            prompt = f"Explain '{concept}' for a {level} programmer. Include: definition, how it works, real-world use case, and a code example in Python."
            with st.spinner("📖 Generating explanation..."):
                result = ask([{"role": "user", "content": prompt}], selected_model)
            st.divider()
            st.markdown(result)

    elif learn_type == "🔢 Algorithm Visualizer":
        algo = st.selectbox("Choose Algorithm", [
            "Binary Search", "Bubble Sort", "Quick Sort", "Merge Sort",
            "BFS (Breadth First Search)", "DFS (Depth First Search)",
            "Dijkstra's Algorithm", "Dynamic Programming (Fibonacci)",
        ], key="algo_sel")
        algo_lang = st.selectbox("Language", ["Python", "JavaScript", "C++", "Java"], key="algo_lang")

        if st.button("🔢 Show Algorithm", type="primary", key="algo_btn"):
            prompt = (f"Explain {algo} with:\n"
                      f"1. Step-by-step explanation\n"
                      f"2. Time & Space complexity\n"
                      f"3. Working code in {algo_lang} with comments\n"
                      f"4. Example walkthrough")
            with st.spinner("🔢 Preparing..."):
                result = ask([{"role": "user", "content": prompt}], selected_model)
            st.divider()
            st.markdown(result)

    elif learn_type == "⚖️  Compare Technologies":
        col1, col2 = st.columns(2)
        with col1:
            tech1 = st.text_input("Technology 1", placeholder="e.g. React", key="t1")
        with col2:
            tech2 = st.text_input("Technology 2", placeholder="e.g. Vue", key="t2")

        if st.button("⚖️ Compare", type="primary", key="compare_btn") and tech1 and tech2:
            prompt = (f"Compare {tech1} vs {tech2} for developers:\n"
                      f"1. Key differences\n2. Pros & Cons of each\n"
                      f"3. When to use which\n4. Performance\n5. Community & Jobs\n"
                      f"6. Final recommendation")
            with st.spinner("⚖️ Comparing..."):
                result = ask([{"role": "user", "content": prompt}], selected_model)
            st.divider()
            st.markdown(result)

    elif learn_type == "📋 Cheat Sheet Generator":
        sheet_topic = st.text_input("", placeholder="e.g. Python list methods, Git commands, SQL queries, CSS flexbox...",
                                     label_visibility="collapsed", key="sheet_in")
        if st.button("📋 Generate Cheat Sheet", type="primary", key="sheet_btn") and sheet_topic.strip():
            prompt = f"Create a comprehensive cheat sheet for '{sheet_topic}'. Format with clear sections, code examples, and tips. Make it practical and easy to reference."
            with st.spinner("📋 Generating cheat sheet..."):
                result = ask([{"role": "user", "content": prompt}], selected_model)
            st.divider()
            st.markdown(result)
            st.markdown(dl_link(result, "cheatsheet.txt", "Download Cheat Sheet"), unsafe_allow_html=True)
