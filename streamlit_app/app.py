"""
NILESH AI — Professional Coding Assistant
Built by NILESH PURI GOSWAMI
"""
import streamlit as st
import re, base64
from groq import Groq

st.set_page_config(
    page_title="NILESH AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp { font-family: 'Inter', sans-serif !important; background: #1e1e1e !important; color: #d4d4d4 !important; }

/* Hide Streamlit chrome */
#MainMenu, footer, header, [data-testid="stToolbar"], .stDeployButton { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* Sidebar */
section[data-testid="stSidebar"] { background: #252526 !important; border-right: 1px solid #3c3c3c; min-width: 240px !important; max-width: 280px !important; }
section[data-testid="stSidebar"] > div { padding: 0 !important; }
section[data-testid="stSidebar"] * { color: #cccccc !important; }

/* Tabs — VSCode style */
.stTabs [data-baseweb="tab-list"] { background: #2d2d2d; border-bottom: 1px solid #3c3c3c; gap: 0; padding: 0; margin: 0; }
.stTabs [data-baseweb="tab"] { background: #2d2d2d; color: #969696; border: none; border-radius: 0; font-size: 13px; font-weight: 400; padding: 10px 20px; border-right: 1px solid #3c3c3c; transition: all 0.15s; min-width: 120px; }
.stTabs [data-baseweb="tab"]:hover { background: #1e1e1e; color: #cccccc; }
.stTabs [aria-selected="true"] { background: #1e1e1e !important; color: #ffffff !important; border-bottom: 2px solid #007acc !important; font-weight: 500 !important; }
.stTabs [data-baseweb="tab-panel"] { background: #1e1e1e; padding: 0; }

/* Buttons */
.stButton > button { background: #0e639c !important; color: #ffffff !important; border: none !important; border-radius: 2px !important; font-size: 13px !important; font-weight: 400 !important; padding: 6px 14px !important; font-family: 'Inter', sans-serif !important; letter-spacing: 0.3px; transition: background 0.15s !important; }
.stButton > button:hover { background: #1177bb !important; }
.stButton > button:active { background: #0d5c8f !important; }

/* Secondary button style */
div[data-testid="column"] .stButton > button { background: #3c3c3c !important; color: #cccccc !important; border: 1px solid #555 !important; }
div[data-testid="column"] .stButton > button:hover { background: #4c4c4c !important; }

/* Inputs */
.stTextArea textarea { background: #1e1e1e !important; color: #d4d4d4 !important; border: 1px solid #3c3c3c !important; border-radius: 2px !important; font-family: 'Fira Code', monospace !important; font-size: 13px !important; line-height: 1.6 !important; resize: vertical; }
.stTextArea textarea:focus { border-color: #007acc !important; outline: none !important; box-shadow: none !important; }
.stTextInput > div > div > input { background: #3c3c3c !important; color: #cccccc !important; border: 1px solid #555 !important; border-radius: 2px !important; font-size: 13px !important; padding: 6px 10px !important; }
.stTextInput > div > div > input:focus { border-color: #007acc !important; box-shadow: none !important; }
.stTextInput > div > div > input::placeholder { color: #666 !important; }

/* Selectbox */
.stSelectbox > div > div { background: #3c3c3c !important; border: 1px solid #555 !important; border-radius: 2px !important; color: #cccccc !important; font-size: 13px !important; }
[data-baseweb="select"] { background: #3c3c3c !important; }
[data-baseweb="popover"] { background: #252526 !important; border: 1px solid #3c3c3c !important; }

/* Radio */
.stRadio > div > label { color: #cccccc !important; font-size: 13px !important; }
.stRadio [data-baseweb="radio"] { background: #007acc; }

/* Chat messages */
.msg-user-wrap { display: flex; justify-content: flex-end; padding: 8px 0; }
.msg-user { background: #264f78; color: #d4d4d4; padding: 10px 14px; border-radius: 8px 8px 2px 8px; max-width: 72%; font-size: 13px; line-height: 1.65; }
.msg-ai-wrap { display: flex; gap: 10px; padding: 8px 0; align-items: flex-start; }
.msg-ai-icon { width: 28px; height: 28px; border-radius: 4px; background: #007acc; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0; margin-top: 1px; color: white; font-weight: 700; }
.msg-ai-body { background: #252526; border: 1px solid #3c3c3c; border-radius: 2px 8px 8px 8px; padding: 10px 14px; max-width: 88%; font-size: 13px; line-height: 1.7; color: #d4d4d4; }

/* Code output panel */
.output-panel { background: #252526; border: 1px solid #3c3c3c; border-radius: 4px; padding: 0; overflow: hidden; }
.output-header { background: #2d2d2d; border-bottom: 1px solid #3c3c3c; padding: 8px 14px; display: flex; align-items: center; justify-content: space-between; }
.output-title { font-size: 12px; color: #858585; font-weight: 500; text-transform: uppercase; letter-spacing: 0.8px; }
.output-body { padding: 16px; }

/* Status dots */
.status-ok { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #4ec9b0; margin-right: 6px; }
.status-off { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #f44747; margin-right: 6px; }

/* Section labels */
.section-label { font-size: 11px; font-weight: 600; color: #858585; text-transform: uppercase; letter-spacing: 0.8px; padding: 12px 16px 6px; }

/* Sidebar nav item */
.nav-item { display: flex; align-items: center; gap: 8px; padding: 7px 16px; font-size: 13px; color: #cccccc; cursor: pointer; transition: background 0.1s; }
.nav-item:hover { background: #2a2d2e; }
.nav-item.active { background: #094771; color: #ffffff; }

/* Kbd shortcut */
.kbd { background: #3c3c3c; border: 1px solid #555; border-radius: 3px; padding: 1px 5px; font-size: 11px; font-family: 'Fira Code', monospace; color: #969696; }

/* Divider */
hr { border: none; border-top: 1px solid #3c3c3c !important; margin: 12px 0; }

/* Scrollbar */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #1e1e1e; }
::-webkit-scrollbar-thumb { background: #424242; border-radius: 0; }
::-webkit-scrollbar-thumb:hover { background: #555; }

/* Alerts */
.stSuccess, .stInfo, .stWarning, .stError { border-radius: 2px !important; font-size: 13px !important; }

/* Expander */
details > summary { background: #2d2d2d !important; color: #cccccc !important; border: 1px solid #3c3c3c !important; border-radius: 2px !important; font-size: 13px !important; padding: 8px 12px !important; }
details[open] > summary { border-bottom-color: transparent !important; }

/* Metric */
[data-testid="metric-container"] { background: #252526; border: 1px solid #3c3c3c; border-radius: 2px; padding: 10px 14px; }
[data-testid="metric-container"] label { color: #858585 !important; font-size: 11px !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #4fc1ff !important; font-size: 22px !important; font-weight: 700 !important; }

/* Caption */
.stCaption, small { color: #666 !important; font-size: 12px !important; }

/* Welcome suggestions */
.sug-btn { background: #252526; border: 1px solid #3c3c3c; border-radius: 4px; padding: 12px 14px; cursor: pointer; transition: border-color 0.15s, background 0.15s; }
.sug-btn:hover { border-color: #007acc; background: #2a2d2e; }
.sug-title { font-size: 13px; font-weight: 500; color: #cccccc; }
.sug-desc { font-size: 12px; color: #666; margin-top: 3px; }

/* File uploader */
[data-testid="stFileUploadDropzone"] { background: #252526 !important; border: 1px dashed #3c3c3c !important; border-radius: 4px !important; }
[data-testid="stFileUploadDropzone"]:hover { border-color: #007acc !important; }

/* Form */
[data-testid="stForm"] { border: none !important; padding: 0 !important; background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── Config ────────────────────────────────────────────────────────────────────
MODELS = {
    "llama-3.1-8b-instant":            "⚡ Llama 3.1 8B — Fastest",
    "llama-3.3-70b-versatile":         "🧠 Llama 3.3 70B — Smart",
    "qwen/qwen3-32b":                  "🔮 Qwen 3 32B — Balanced",
    "deepseek-r1-distill-llama-70b":   "💡 DeepSeek R1 — Reasoning",
    "mixtral-8x7b-32768":              "🌀 Mixtral 8x7B — Long context",
}

LANGS = [
    "Python","JavaScript","TypeScript","C","C++","C#",
    "Java","Go","Rust","Kotlin","Swift","PHP","SQL",
    "Bash","HTML","CSS","R","Dart",
]

SYSTEM = """You are NILESH AI, a professional coding assistant built by NILESH PURI GOSWAMI.

You help developers with:
- Writing clean, production-ready code
- Debugging errors and fixing bugs
- Code review and optimization
- Explaining complex concepts clearly
- Best practices and design patterns

Rules:
- Always use proper markdown code blocks with language tags
- Be concise but complete
- For code: add brief inline comments
- If asked who built you: "I was built by NILESH PURI GOSWAMI"
- Temperature is low — be precise and accurate"""

# ── Session ───────────────────────────────────────────────────────────────────
_defaults = dict(messages=[], api_key="", groq_client=None, code_out="")
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state.api_key:
    try:
        st.session_state.api_key = st.secrets["GROQ_API_KEY"]
        st.session_state.groq_client = Groq(api_key=st.session_state.api_key)
    except: pass

# ── Helpers ───────────────────────────────────────────────────────────────────
def _clean(t):
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"<think>.*?</think>", "", t, flags=re.DOTALL)).strip()

def chat(msgs, model):
    if not st.session_state.groq_client:
        return "❌ Add your Groq API key in the sidebar to start."
    try:
        r = st.session_state.groq_client.chat.completions.create(
            model=model,
            messages=[{"role":"system","content":SYSTEM}]+msgs,
            max_tokens=4096, temperature=0.2,
        )
        return _clean(r.choices[0].message.content)
    except Exception as e:
        return f"❌ {e}"

def dl(content, fname, label):
    b64 = base64.b64encode(content.encode()).decode()
    return (f'<a href="data:text/plain;base64,{b64}" download="{fname}" '
            f'style="color:#4fc1ff;font-size:12px;text-decoration:none;'
            f'border:1px solid #3c3c3c;border-radius:2px;padding:4px 10px;">'
            f'⬇ {label}</a>')

# ════════════════════════════════════════════════════════════════════════════ #
#  SIDEBAR                                                                     #
# ════════════════════════════════════════════════════════════════════════════ #
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="padding:16px 16px 0;display:flex;align-items:center;gap:10px;">
      <div style="width:32px;height:32px;border-radius:4px;background:#007acc;
                  display:flex;align-items:center;justify-content:center;
                  font-weight:800;font-size:14px;color:white;flex-shrink:0;">N</div>
      <div>
        <div style="font-size:14px;font-weight:600;color:#cccccc;line-height:1.2;">NILESH AI</div>
        <div style="font-size:11px;color:#666;">Coding Assistant</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:12px 0;'>", unsafe_allow_html=True)

    # API Status
    st.markdown('<div class="section-label">Connection</div>', unsafe_allow_html=True)
    if st.session_state.api_key:
        st.markdown('<div style="padding:0 16px 8px;font-size:13px;"><span class="status-ok"></span>Connected to Groq</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding:0 16px;">', unsafe_allow_html=True)
        k = st.text_input("API Key", type="password", placeholder="gsk_...", label_visibility="collapsed")
        if k:
            st.session_state.api_key = k
            st.session_state.groq_client = Groq(api_key=k)
            st.rerun()
        st.markdown('<a href="https://console.groq.com" target="_blank" style="color:#4fc1ff;font-size:12px;padding:0 0 8px;display:block;">Get free key →</a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

    # Model
    st.markdown('<div class="section-label">Model</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div style="padding:0 16px 8px;">', unsafe_allow_html=True)
        m_key = st.selectbox("", list(MODELS.keys()),
                              format_func=lambda x: MODELS[x],
                              label_visibility="collapsed", key="model")
        st.markdown(f'<div style="font-size:11px;color:#666;padding:2px 0 4px;">{m_key}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

    # Stats
    st.markdown('<div class="section-label">Session</div>', unsafe_allow_html=True)
    n = len([m for m in st.session_state.messages if m["role"]=="user"])
    st.markdown(f"""
    <div style="padding:0 16px 12px;display:flex;gap:12px;">
      <div style="background:#1e1e1e;border:1px solid #3c3c3c;border-radius:2px;
                  padding:8px 14px;flex:1;text-align:center;">
        <div style="font-size:20px;font-weight:700;color:#4fc1ff;">{n}</div>
        <div style="font-size:11px;color:#666;">Prompts</div>
      </div>
      <div style="background:#1e1e1e;border:1px solid #3c3c3c;border-radius:2px;
                  padding:8px 14px;flex:1;text-align:center;">
        <div style="font-size:20px;font-weight:700;color:#4ec9b0;">{len(MODELS)}</div>
        <div style="font-size:11px;color:#666;">Models</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

    # Actions
    st.markdown('<div class="section-label">Actions</div>', unsafe_allow_html=True)
    st.markdown('<div style="padding:4px 16px 12px;">', unsafe_allow_html=True)
    if st.button("🗑  Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.code_out = ""
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="position:absolute;bottom:16px;left:0;right:0;padding:0 16px;
                border-top:1px solid #3c3c3c;padding-top:12px;">
      <div style="font-size:11px;color:#555;">Built by</div>
      <div style="font-size:12px;color:#858585;font-weight:500;">NILESH PURI GOSWAMI</div>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════ #
#  MAIN                                                                        #
# ════════════════════════════════════════════════════════════════════════════ #

# Top bar
st.markdown("""
<div style="background:#2d2d2d;border-bottom:1px solid #3c3c3c;
            padding:10px 20px;display:flex;align-items:center;
            justify-content:space-between;">
  <div style="display:flex;align-items:center;gap:12px;">
    <span style="font-size:13px;font-weight:600;color:#cccccc;">⚡ NILESH AI</span>
    <span style="font-size:11px;color:#555;background:#1e1e1e;border:1px solid #3c3c3c;
                 border-radius:2px;padding:2px 8px;">Coding Assistant</span>
  </div>
  <div style="font-size:11px;color:#555;">v2.0 · by Nilesh Puri Goswami</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["  💬  Chat  ", "  💻  Code Tools  ", "  🔥  Quick Tools  "])

# ════════════════════════════════════════════════════════════════════════════ #
# TAB 1 — CHAT                                                                 #
# ════════════════════════════════════════════════════════════════════════════ #
with tab1:
    chat_area = st.container()

    with chat_area:
        if not st.session_state.messages:
            # Welcome
            st.markdown("""
            <div style="text-align:center;padding:52px 0 36px;">
              <div style="font-size:44px;margin-bottom:14px;">⚡</div>
              <h2 style="font-size:22px;font-weight:600;color:#cccccc;margin:0 0 6px;">
                NILESH AI — Coding Assistant
              </h2>
              <p style="font-size:14px;color:#666;margin:0;">
                Ask me to write, debug, review or explain any code
              </p>
            </div>
            """, unsafe_allow_html=True)

            # Suggestion cards
            SUGS = [
                ("🐛", "Debug my code",        "Find & fix all bugs"),
                ("⚡", "Optimize this",         "Better performance"),
                ("📝", "Explain line by line",  "For beginners"),
                ("✅", "Write test cases",       "Full coverage"),
                ("🔄", "Convert to Python",      "From any language"),
                ("🔒", "Security audit",          "Find vulnerabilities"),
            ]
            rows = [SUGS[:3], SUGS[3:]]
            for row in rows:
                cols = st.columns(3)
                for i, (icon, title, desc) in enumerate(row):
                    with cols[i]:
                        if st.button(
                            f"{icon} {title}\n\n{desc}",
                            use_container_width=True,
                            key=f"s_{title}"
                        ):
                            q = f"{title} — {desc}"
                            st.session_state.messages.append({"role":"user","content":q})
                            with st.spinner(""):
                                r = chat([{"role":"user","content":q}], m_key)
                            st.session_state.messages.append({"role":"assistant","content":r})
                            st.rerun()
        else:
            # Messages
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(
                        f'<div class="msg-user-wrap"><div class="msg-user">{msg["content"]}</div></div>',
                        unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div class="msg-ai-wrap"><div class="msg-ai-icon">AI</div>'
                        f'<div class="msg-ai-body">{msg["content"]}</div></div>',
                        unsafe_allow_html=True)

    # Input bar
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    with st.form("chat_f", clear_on_submit=True):
        cols = st.columns([9, 1])
        with cols[0]:
            inp = st.text_area("",
                placeholder="Ask a coding question, paste an error, or describe what you want to build...",
                height=72, label_visibility="collapsed")
        with cols[1]:
            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
            go = st.form_submit_button("Send", type="primary", use_container_width=True)

    if go and inp.strip():
        st.session_state.messages.append({"role":"user","content":inp.strip()})
        api_m = [{"role":m["role"],"content":m["content"]}
                 for m in st.session_state.messages if m["role"] in ("user","assistant")]
        with st.spinner(""):
            r = chat(api_m, m_key)
        st.session_state.messages.append({"role":"assistant","content":r})
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════ #
# TAB 2 — CODE TOOLS                                                           #
# ════════════════════════════════════════════════════════════════════════════ #
with tab2:
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    left, right = st.columns([1, 1], gap="medium")

    with left:
        st.markdown("""
        <div style="background:#2d2d2d;border:1px solid #3c3c3c;border-radius:4px 4px 0 0;
                    padding:8px 12px;display:flex;align-items:center;gap:8px;">
          <span style="font-size:11px;color:#858585;text-transform:uppercase;
                       letter-spacing:0.8px;font-weight:600;">Editor</span>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            src = st.selectbox("", LANGS, key="src", label_visibility="collapsed")
        with c2:
            action = st.selectbox("", [
                "🔍 Review & Explain",
                "🐛 Debug & Fix",
                "⚡ Optimize",
                "📝 Add Comments",
                "🔄 Convert Language",
                "✅ Write Tests",
                "🔒 Security Audit",
                "♻️ Refactor",
                "📚 Explain to Beginner",
            ], key="action", label_visibility="collapsed")

        tgt = None
        if action == "🔄 Convert Language":
            tgt = st.selectbox("Target", [l for l in LANGS if l != src], key="tgt")

        code = st.text_area("",
            height=320,
            placeholder=f"# Paste your {src} code here...",
            label_visibility="collapsed",
            key="code_editor")

        run = st.button("▶  Run Analysis", type="primary", use_container_width=True, key="run")

        if run:
            if not code.strip():
                st.warning("Paste some code first.")
            else:
                cb = f"```{src.lower()}\n{code}\n```"
                p = {
                    "🔍 Review & Explain":    f"Review this {src} code thoroughly — quality, logic, issues:\n\n{cb}",
                    "🐛 Debug & Fix":         f"Find ALL bugs in this {src} code. Show fixed version:\n\n{cb}",
                    "⚡ Optimize":             f"Optimize this {src} code for speed and readability:\n\n{cb}",
                    "📝 Add Comments":         f"Add comprehensive comments/docstrings to this {src} code:\n\n{cb}",
                    "🔄 Convert Language":     f"Convert this {src} code to {tgt}. Working code with comments:\n\n{cb}",
                    "✅ Write Tests":           f"Write complete unit tests for this {src} code:\n\n{cb}",
                    "🔒 Security Audit":        f"Security audit this {src} code. Find vulnerabilities, suggest fixes:\n\n{cb}",
                    "♻️ Refactor":             f"Refactor this {src} code with best practices and clean code principles:\n\n{cb}",
                    "📚 Explain to Beginner":  f"Explain this {src} code line by line for a complete beginner:\n\n{cb}",
                }
                with st.spinner(f"Running {action}..."):
                    st.session_state.code_out = chat([{"role":"user","content":p[action]}], m_key)

    with right:
        st.markdown("""
        <div style="background:#2d2d2d;border:1px solid #3c3c3c;border-radius:4px 4px 0 0;
                    padding:8px 12px;display:flex;align-items:center;justify-content:space-between;">
          <span style="font-size:11px;color:#858585;text-transform:uppercase;
                       letter-spacing:0.8px;font-weight:600;">Output</span>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.code_out:
            st.markdown(st.session_state.code_out)
            st.markdown("<hr>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(dl(st.session_state.code_out, "analysis.txt", "Download"), unsafe_allow_html=True)
            with c2:
                if st.button("💬 Send to Chat", key="s2c", use_container_width=True):
                    st.session_state.messages.append({"role":"assistant","content":st.session_state.code_out})
                    st.info("Added to chat! Switch to 💬 tab.")
        else:
            st.markdown("""
            <div style="border:1px solid #3c3c3c;border-top:none;border-radius:0 0 4px 4px;
                        padding:60px 24px;text-align:center;min-height:420px;
                        display:flex;flex-direction:column;align-items:center;justify-content:center;">
              <div style="font-size:28px;margin-bottom:12px;">💻</div>
              <div style="font-size:13px;color:#666;">Paste code + choose action</div>
              <div style="font-size:12px;color:#555;margin-top:6px;">then click ▶ Run Analysis</div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════ #
# TAB 3 — QUICK TOOLS                                                          #
# ════════════════════════════════════════════════════════════════════════════ #
with tab3:
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    tool = st.radio("", [
        "🚨 Error Explainer",
        "📋 Code Generator",
        "📖 Concept Explainer",
        "🔀 Git Helper",
    ], horizontal=True, label_visibility="collapsed", key="tool")

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Error Explainer ──────────────────────────────────────────────────────
    if tool == "🚨 Error Explainer":
        st.markdown("#### 🚨 Error Explainer")
        st.caption("Paste any error/stack trace → get cause, explanation, and fix")

        err_lang = st.selectbox("Language", LANGS, key="err_lang")
        err_in = st.text_area("", height=160,
            placeholder="Paste your error or stack trace here...\n\nTypeError: unsupported operand type(s) for +: 'int' and 'str'",
            label_visibility="collapsed", key="err_in")

        if st.button("🔍 Explain & Fix", type="primary", key="err_btn") and err_in.strip():
            p = (f"This is a {err_lang} error. Explain:\n"
                 f"1. What caused this error\n"
                 f"2. What it means\n"
                 f"3. How to fix it (show code)\n"
                 f"4. How to prevent it\n\n"
                 f"Error:\n```\n{err_in}\n```")
            with st.spinner("Analyzing error..."):
                out = chat([{"role":"user","content":p}], m_key)
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(out)

    # ── Code Generator ───────────────────────────────────────────────────────
    elif tool == "📋 Code Generator":
        st.markdown("#### 📋 Code Generator")
        st.caption("Describe what you want → get clean, production-ready code")

        c1, c2 = st.columns(2)
        with c1:
            gen_lang = st.selectbox("Language", LANGS, key="gen_lang")
        with c2:
            gen_style = st.selectbox("Style", ["Clean & Commented", "Minimal", "With Error Handling", "With Tests"], key="gen_style")

        desc = st.text_area("", height=100,
            placeholder="Describe what you want...\n\ne.g. A function that reads a CSV file, filters rows where age > 18, and returns a sorted list",
            label_visibility="collapsed", key="gen_desc")

        if st.button("⚡ Generate Code", type="primary", key="gen_btn") and desc.strip():
            p = (f"Write {gen_lang} code for: {desc}\n\n"
                 f"Style: {gen_style}\n"
                 f"Requirements: production-ready, {gen_style.lower()}, best practices")
            with st.spinner("Generating..."):
                out = chat([{"role":"user","content":p}], m_key)
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(out)
            st.markdown(dl(out, "generated_code.txt", "Download Code"), unsafe_allow_html=True)

    # ── Concept Explainer ────────────────────────────────────────────────────
    elif tool == "📖 Concept Explainer":
        st.markdown("#### 📖 Concept Explainer")
        st.caption("Any programming concept → clear explanation with code examples")

        c1, c2 = st.columns([3,1])
        with c1:
            concept = st.text_input("", placeholder="e.g. recursion, Big O notation, async/await, REST APIs, pointers...",
                                     label_visibility="collapsed", key="concept")
        with c2:
            level = st.selectbox("", ["Beginner","Intermediate","Advanced"],
                                  label_visibility="collapsed", key="level")

        if st.button("📖 Explain", type="primary", key="con_btn") and concept.strip():
            p = (f"Explain '{concept}' for a {level} programmer.\n"
                 f"Include: definition, how it works, real-world analogy, "
                 f"code example in Python, common mistakes, when to use it.")
            with st.spinner("Explaining..."):
                out = chat([{"role":"user","content":p}], m_key)
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(out)

    # ── Git Helper ───────────────────────────────────────────────────────────
    elif tool == "🔀 Git Helper":
        st.markdown("#### 🔀 Git Helper")
        st.caption("Git questions, commands, and workflows explained")

        git_type = st.selectbox("What do you need?", [
            "Explain a git command",
            "Fix a git problem",
            "Generate commit message",
            "Git workflow for my project",
            "Undo / revert changes",
        ], key="git_type")

        git_in = st.text_area("", height=100,
            placeholder="Describe your git question or problem...",
            label_visibility="collapsed", key="git_in")

        if st.button("🔀 Get Git Help", type="primary", key="git_btn") and git_in.strip():
            p = f"Git help — {git_type}:\n\n{git_in}\n\nProvide exact commands with explanation."
            with st.spinner(""):
                out = chat([{"role":"user","content":p}], m_key)
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(out)
