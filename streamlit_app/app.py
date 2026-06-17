"""NILESH AI — Professional Coding Assistant v4"""
import streamlit as st, re, base64, io
from groq import Groq

st.set_page_config(page_title="NILESH AI", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
html,body,.stApp{font-family:'Inter',sans-serif!important;background:#1a1a2e!important;color:#e2e8f0!important;}
#MainMenu,footer,header,[data-testid="stToolbar"],.stDeployButton,[data-testid="stDecoration"]{display:none!important;}
section[data-testid="stSidebar"]{background:#16213e!important;border-right:1px solid #0f3460;}
section[data-testid="stSidebar"] *{color:#e2e8f0!important;}
/* Tabs */
.stTabs [data-baseweb="tab-list"]{background:#16213e;border-bottom:1px solid #0f3460;gap:0;padding:0;}
.stTabs [data-baseweb="tab"]{background:transparent;color:#94a3b8;border:none;border-radius:0;font-size:13px;font-weight:500;padding:11px 18px;border-bottom:2px solid transparent;transition:all .15s;}
.stTabs [data-baseweb="tab"]:hover{color:#e2e8f0;background:rgba(255,255,255,.03);}
.stTabs [aria-selected="true"]{background:transparent!important;color:#7c3aed!important;border-bottom:2px solid #7c3aed!important;}
.stTabs [data-baseweb="tab-panel"]{background:#1a1a2e;padding:0;}
/* Buttons */
.stButton>button{background:linear-gradient(135deg,#7c3aed,#6d28d9)!important;color:#fff!important;border:none!important;border-radius:8px!important;font-size:13px!important;font-weight:500!important;padding:8px 18px!important;transition:all .2s!important;letter-spacing:.3px;}
.stButton>button:hover{background:linear-gradient(135deg,#6d28d9,#5b21b6)!important;transform:translateY(-1px);box-shadow:0 4px 15px rgba(124,58,237,.3)!important;}
/* Inputs */
.stTextArea textarea{background:#0d1b2a!important;color:#e2e8f0!important;border:1px solid #0f3460!important;border-radius:8px!important;font-family:'Fira Code',monospace!important;font-size:13px!important;line-height:1.6!important;}
.stTextArea textarea:focus{border-color:#7c3aed!important;box-shadow:0 0 0 3px rgba(124,58,237,.15)!important;outline:none!important;}
.stTextInput>div>div>input{background:#0d1b2a!important;color:#e2e8f0!important;border:1px solid #0f3460!important;border-radius:8px!important;font-size:13px!important;padding:8px 12px!important;}
.stTextInput>div>div>input:focus{border-color:#7c3aed!important;box-shadow:0 0 0 3px rgba(124,58,237,.15)!important;}
.stTextInput>div>div>input::placeholder{color:#475569!important;}
/* Selectbox */
.stSelectbox>div>div{background:#0d1b2a!important;border:1px solid #0f3460!important;border-radius:8px!important;color:#e2e8f0!important;font-size:13px!important;}
[data-baseweb="popover"]{background:#16213e!important;border:1px solid #0f3460!important;border-radius:8px!important;}
/* Radio */
.stRadio>div>label{color:#e2e8f0!important;font-size:13px!important;}
/* Chat bubbles */
.u-wrap{display:flex;justify-content:flex-end;padding:10px 0;}
.u-bubble{background:linear-gradient(135deg,#7c3aed,#6d28d9);color:#fff;padding:11px 16px;border-radius:16px 16px 4px 16px;max-width:70%;font-size:14px;line-height:1.65;box-shadow:0 2px 10px rgba(124,58,237,.2);}
.a-wrap{display:flex;gap:10px;padding:10px 0;align-items:flex-start;}
.a-icon{width:32px;height:32px;border-radius:8px;background:linear-gradient(135deg,#0f3460,#533483);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:11px;flex-shrink:0;color:#e2e8f0;border:1px solid #7c3aed;}
.a-body{background:#16213e;border:1px solid #0f3460;border-radius:4px 16px 16px 16px;padding:12px 16px;max-width:87%;font-size:13.5px;line-height:1.75;color:#e2e8f0;}
/* Cards */
.card{background:#16213e;border:1px solid #0f3460;border-radius:12px;padding:18px;transition:border-color .2s;}
.card:hover{border-color:#7c3aed;}
/* Score ring helper */
.score-box{background:#0d1b2a;border:2px solid #7c3aed;border-radius:12px;padding:20px;text-align:center;}
/* Sidebar sections */
.s-header{font-size:10px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:1px;padding:14px 16px 5px;}
/* File uploader */
[data-testid="stFileUploadDropzone"]{background:#0d1b2a!important;border:1px dashed #0f3460!important;border-radius:8px!important;}
[data-testid="stFileUploadDropzone"]:hover{border-color:#7c3aed!important;}
/* Divider */
hr{border:none;border-top:1px solid #0f3460!important;margin:14px 0;}
.stCaption{color:#475569!important;font-size:12px!important;}
/* Alerts */
.stSuccess{background:#0d2b1a!important;border:1px solid #166534!important;border-radius:8px!important;}
.stWarning{background:#2b1a0d!important;border:1px solid #92400e!important;border-radius:8px!important;}
.stError{background:#2b0d0d!important;border:1px solid #7f1d1d!important;border-radius:8px!important;}
.stInfo{background:#0d1b2b!important;border:1px solid #1e3a5f!important;border-radius:8px!important;}
/* Expander */
details>summary{background:#16213e!important;border:1px solid #0f3460!important;border-radius:8px!important;color:#e2e8f0!important;font-size:13px!important;}
/* Scrollbar */
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:#1a1a2e;}
::-webkit-scrollbar-thumb{background:#0f3460;border-radius:3px;}
::-webkit-scrollbar-thumb:hover{background:#7c3aed;}
[data-testid="stForm"]{border:none!important;padding:0!important;background:transparent!important;}
</style>""", unsafe_allow_html=True)

# ── Config ────────────────────────────────────────────────────────────────────
MODELS = {
    "llama-3.1-8b-instant":          "⚡ Llama 3.1 8B — Fastest",
    "llama-3.3-70b-versatile":       "🧠 Llama 3.3 70B — Smartest",
    "qwen/qwen3-32b":                "🔮 Qwen 3 32B — Balanced",
    "deepseek-r1-distill-llama-70b": "💡 DeepSeek R1 — Best for Code",
    "mixtral-8x7b-32768":            "🌀 Mixtral 8x7B — Long Context",
}
LANGS = ["Python","JavaScript","TypeScript","C","C++","C#","Java","Go","Rust",
         "Kotlin","Swift","PHP","SQL","Bash","HTML","CSS","R","Dart"]
RESP_LANGS = {"🇬🇧 English":"Respond in English.",
              "🇮🇳 Hindi":"हमेशा हिंदी में जवाब दो।",
              "🤝 Hinglish":"Respond in Hinglish (Hindi+English mix).",
              "🇪🇸 Spanish":"Responde en español.",
              "🇫🇷 French":"Réponds en français.",}
DEV = "This app was built by NILESH PURI GOSWAMI. If asked who built you, say: 'Built by NILESH PURI GOSWAMI'."
BASE_SYS = f"""You are NILESH AI — an expert coding assistant.
Help with: writing, debugging, reviewing, optimizing, and explaining code.
Always use proper markdown code blocks. Be precise and thorough. {DEV}"""

# ── Session ───────────────────────────────────────────────────────────────────
for k,v in dict(messages=[],api_key="",groq_client=None,code_out="",resume_out="").items():
    if k not in st.session_state: st.session_state[k]=v
if not st.session_state.api_key:
    try:
        st.session_state.api_key=st.secrets["GROQ_API_KEY"]
        st.session_state.groq_client=Groq(api_key=st.session_state.api_key)
    except: pass

# ── Helpers ───────────────────────────────────────────────────────────────────
def _c(t): return re.sub(r"\n{3,}","\n\n",re.sub(r"<think>.*?</think>","",t,flags=re.DOTALL)).strip()
def ask(msgs,model,sys=None):
    if not st.session_state.groq_client: return "❌ Add Groq API key in sidebar."
    try:
        r=st.session_state.groq_client.chat.completions.create(
            model=model,messages=[{"role":"system","content":sys or BASE_SYS}]+msgs,
            max_tokens=4096,temperature=0.2)
        return _c(r.choices[0].message.content)
    except Exception as e: return f"❌ {e}"
def dl(txt,fname,lbl):
    b64=base64.b64encode(txt.encode()).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="{fname}" style="color:#a78bfa;font-size:12px;text-decoration:none;border:1px solid #0f3460;border-radius:6px;padding:4px 12px;">⬇ {lbl}</a>'
def read_file(f):
    try:
        if f.name.lower().endswith(".pdf"):
            try:
                import PyPDF2
                return "\n".join(p.extract_text() or "" for p in PyPDF2.PdfReader(io.BytesIO(f.read())).pages)
            except: return f.read().decode("utf-8","ignore")
        return f.read().decode("utf-8","ignore")
    except: return ""

# ════════════════════════════════════════════════════════════════════════════ #
# SIDEBAR                                                                      #
# ════════════════════════════════════════════════════════════════════════════ #
with st.sidebar:
    st.markdown("""<div style="padding:18px 16px 4px;display:flex;align-items:center;gap:10px;">
      <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#7c3aed,#0f3460);
        display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;color:#fff;flex-shrink:0;">N</div>
      <div><div style="font-size:15px;font-weight:700;color:#e2e8f0;">NILESH AI</div>
        <div style="font-size:11px;color:#475569;">Coding Assistant</div></div></div>""",unsafe_allow_html=True)
    st.markdown("<hr>",unsafe_allow_html=True)

    # API
    st.markdown('<div class="s-header">🔑 API Key</div>',unsafe_allow_html=True)
    if st.session_state.api_key:
        st.markdown('<div style="padding:0 16px 8px;font-size:13px;color:#4ade80;">✦ Connected to Groq</div>',unsafe_allow_html=True)
    else:
        k=st.text_input("",type="password",placeholder="gsk_...",label_visibility="collapsed")
        if k:
            st.session_state.api_key=k; st.session_state.groq_client=Groq(api_key=k); st.rerun()
        st.markdown('<a href="https://console.groq.com" target="_blank" style="color:#a78bfa;font-size:12px;padding:0 16px 8px;display:block;">Get free key →</a>',unsafe_allow_html=True)

    st.markdown("<hr>",unsafe_allow_html=True)
    st.markdown('<div class="s-header">🤖 Model</div>',unsafe_allow_html=True)
    m_key=st.selectbox("",list(MODELS.keys()),format_func=lambda x:MODELS[x],label_visibility="collapsed",key="model_sel")
    st.markdown(f'<div style="padding:2px 16px 8px;font-size:10px;color:#475569;">{m_key}</div>',unsafe_allow_html=True)

    st.markdown("<hr>",unsafe_allow_html=True)
    st.markdown('<div class="s-header">🌐 Response Language</div>',unsafe_allow_html=True)
    rlang=st.selectbox("",list(RESP_LANGS.keys()),label_visibility="collapsed",key="rlang")

    st.markdown("<hr>",unsafe_allow_html=True)
    n=len([m for m in st.session_state.messages if m["role"]=="user"])
    st.markdown(f"""<div style="padding:0 16px 12px;display:flex;gap:10px;">
      <div style="background:#0d1b2a;border:1px solid #0f3460;border-radius:8px;padding:10px;flex:1;text-align:center;">
        <div style="font-size:22px;font-weight:700;color:#a78bfa;">{n}</div>
        <div style="font-size:10px;color:#475569;">Prompts</div></div>
      <div style="background:#0d1b2a;border:1px solid #0f3460;border-radius:8px;padding:10px;flex:1;text-align:center;">
        <div style="font-size:22px;font-weight:700;color:#4ade80;">{len(MODELS)}</div>
        <div style="font-size:10px;color:#475569;">Models</div></div></div>""",unsafe_allow_html=True)

    if st.button("🗑  Clear All",use_container_width=True):
        st.session_state.messages=[]; st.session_state.code_out=""; st.session_state.resume_out=""; st.rerun()
    st.markdown("""<div style="padding:16px;border-top:1px solid #0f3460;margin-top:16px;">
      <div style="font-size:10px;color:#475569;">Built by</div>
      <div style="font-size:12px;color:#94a3b8;font-weight:600;">NILESH PURI GOSWAMI</div></div>""",unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════ #
# HEADER                                                                       #
# ════════════════════════════════════════════════════════════════════════════ #
st.markdown("""<div style="background:#16213e;border-bottom:1px solid #0f3460;
  padding:12px 24px;display:flex;align-items:center;justify-content:space-between;">
  <div style="display:flex;align-items:center;gap:12px;">
    <span style="font-size:14px;font-weight:700;color:#e2e8f0;">⚡ NILESH AI</span>
    <span style="font-size:11px;color:#475569;background:#0d1b2a;border:1px solid #0f3460;
      border-radius:20px;padding:2px 10px;">Coding Assistant</span>
  </div>
  <div style="font-size:11px;color:#475569;">v4.0 · by Nilesh Puri Goswami</div>
</div>""",unsafe_allow_html=True)

# TABS
tab1,tab2,tab3,tab4,tab5=st.tabs([
    "  💬  Chat  ","  💻  Code Tools  ","  🎯  Interview Prep  ",
    "  📋  Resume AI  ","  🔥  Quick Tools  "])

# ════════════════════════════════════════════════════════════════════════════ #
# TAB 1 — CHAT                                                                 #
# ════════════════════════════════════════════════════════════════════════════ #
with tab1:
    SYS1=BASE_SYS+" "+RESP_LANGS[rlang]
    if not st.session_state.messages:
        st.markdown("""<div style="text-align:center;padding:50px 0 36px;">
          <div style="font-size:50px;margin-bottom:14px;">⚡</div>
          <h2 style="font-size:24px;font-weight:700;color:#e2e8f0;margin:0 0 8px;">NILESH AI Coding Assistant</h2>
          <p style="font-size:14px;color:#475569;">Write · Debug · Review · Optimize · Learn</p>
        </div>""",unsafe_allow_html=True)
        SUGS=[("🐛","Debug my code","Find and fix all bugs"),
              ("⚡","Optimize this","Better performance"),
              ("📝","Explain line by line","For beginners"),
              ("✅","Write test cases","Full coverage"),
              ("🔄","Convert to Python","From any language"),
              ("🔒","Security audit","Find vulnerabilities")]
        for row in [SUGS[:3],SUGS[3:]]:
            cols=st.columns(3)
            for i,(ic,t,d) in enumerate(row):
                with cols[i]:
                    if st.button(f"{ic} {t}\n\n{d}",use_container_width=True,key=f"sg_{t}"):
                        q=f"{t} — {d}"
                        st.session_state.messages.append({"role":"user","content":q})
                        with st.spinner(""):
                            r=ask([{"role":"user","content":q}],m_key,SYS1)
                        st.session_state.messages.append({"role":"assistant","content":r}); st.rerun()
    else:
        for msg in st.session_state.messages:
            if msg["role"]=="user":
                st.markdown(f'<div class="u-wrap"><div class="u-bubble">{msg["content"]}</div></div>',unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="a-wrap"><div class="a-icon">AI</div><div class="a-body">{msg["content"]}</div></div>',unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True); st.markdown("<hr>",unsafe_allow_html=True)
    with st.form("cf",clear_on_submit=True):
        cols=st.columns([9,1])
        with cols[0]: inp=st.text_area("",placeholder="Ask anything about code — questions, errors, architecture, best practices...",height=72,label_visibility="collapsed")
        with cols[1]: st.markdown("<div style='height:22px;'></div>",unsafe_allow_html=True); go=st.form_submit_button("➤",type="primary",use_container_width=True)
    if go and inp.strip():
        st.session_state.messages.append({"role":"user","content":inp.strip()})
        api_m=[{"role":m["role"],"content":m["content"]} for m in st.session_state.messages if m["role"] in("user","assistant")]
        with st.spinner(""):
            r=ask(api_m,m_key,SYS1)
        st.session_state.messages.append({"role":"assistant","content":r}); st.rerun()

# ════════════════════════════════════════════════════════════════════════════ #
# TAB 2 — CODE TOOLS                                                           #
# ════════════════════════════════════════════════════════════════════════════ #
with tab2:
    st.markdown("<div style='height:16px;'></div>",unsafe_allow_html=True)
    L,R=st.columns([1,1],gap="medium")
    with L:
        st.markdown("#### 📝 Code Editor")
        c1,c2=st.columns(2)
        with c1: src=st.selectbox("Language",LANGS,key="src")
        with c2:
            act=st.selectbox("Action",["🔍 Review & Explain","🐛 Debug & Fix","⚡ Optimize",
                "📝 Add Comments","🔄 Convert Language","✅ Write Tests",
                "🔒 Security Audit","♻️ Refactor","⏱ Analyze Complexity","📊 Code→Flowchart"],key="act")
        tgt=None
        if act=="🔄 Convert Language": tgt=st.selectbox("Convert to",[l for l in LANGS if l!=src],key="tgt")
        code=st.text_area("",height=320,placeholder=f"# Paste your {src} code here...",label_visibility="collapsed",key="ced")
        if st.button("▶ Run Analysis",type="primary",use_container_width=True,key="run"):
            if not code.strip(): st.warning("Paste some code first.")
            else:
                cb=f"```{src.lower()}\n{code}\n```"
                pm={
                    "🔍 Review & Explain":f"Thorough code review of this {src} code — quality, logic, issues, improvements:\n\n{cb}",
                    "🐛 Debug & Fix":f"Find ALL bugs in this {src} code. Show fixed version with explanations:\n\n{cb}",
                    "⚡ Optimize":f"Optimize this {src} code for performance and readability. Show before/after:\n\n{cb}",
                    "📝 Add Comments":f"Add comprehensive comments and docstrings to this {src} code:\n\n{cb}",
                    "🔄 Convert Language":f"Convert this {src} code to {tgt}. Working, commented code:\n\n{cb}",
                    "✅ Write Tests":f"Write complete unit tests for this {src} code. Cover edge cases:\n\n{cb}",
                    "🔒 Security Audit":f"Security audit this {src} code. Find vulnerabilities, suggest fixes:\n\n{cb}",
                    "♻️ Refactor":f"Refactor this {src} code with clean code principles and design patterns:\n\n{cb}",
                    "⏱ Analyze Complexity":f"Analyze time and space complexity of this {src} code. Show Big O notation for each function, explain, and suggest optimizations:\n\n{cb}",
                    "📊 Code→Flowchart":f"Convert this {src} code into a detailed step-by-step flowchart (text/ASCII format). Explain the logic flow clearly:\n\n{cb}",
                }
                with st.spinner(f"Running {act}..."):
                    st.session_state.code_out=ask([{"role":"user","content":pm[act]}],m_key,BASE_SYS+" "+RESP_LANGS[rlang])
    with R:
        st.markdown("#### 🤖 AI Output")
        if st.session_state.code_out:
            st.markdown(st.session_state.code_out)
            st.markdown("<hr>",unsafe_allow_html=True)
            c1,c2=st.columns(2)
            with c1: st.markdown(dl(st.session_state.code_out,"analysis.txt","Download"),unsafe_allow_html=True)
            with c2:
                if st.button("💬 Add to Chat",key="s2c",use_container_width=True):
                    st.session_state.messages.append({"role":"assistant","content":st.session_state.code_out})
                    st.success("Added to chat!")
        else:
            st.markdown("""<div style="background:#16213e;border:1px solid #0f3460;border-radius:12px;
              padding:60px 24px;text-align:center;min-height:400px;display:flex;flex-direction:column;
              align-items:center;justify-content:center;">
              <div style="font-size:32px;margin-bottom:14px;">💻</div>
              <p style="color:#475569;font-size:13px;">Paste code + choose action<br>then click ▶ Run Analysis</p>
              <div style="margin-top:16px;font-size:12px;color:#334155;line-height:2;">
                🔍 Review · 🐛 Debug · ⚡ Optimize<br>🔄 Convert · ✅ Tests · ⏱ Complexity · 📊 Flowchart</div>
            </div>""",unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════ #
# TAB 3 — INTERVIEW PREP                                                       #
# ════════════════════════════════════════════════════════════════════════════ #
with tab3:
    st.markdown("<div style='height:16px;'></div>",unsafe_allow_html=True)
    st.markdown("### 🎯 Interview Prep Mode")
    st.caption("DSA problems · System Design · HR Questions · Mock Interviews")
    st.markdown("<hr>",unsafe_allow_html=True)

    itype=st.radio("",["🔢 DSA Problem Solver","🏗️ System Design","💼 HR Questions","📝 README Generator","⏱ Complexity Analyzer"],
                   horizontal=True,label_visibility="collapsed",key="itype")
    st.markdown("<br>",unsafe_allow_html=True)

    # DSA
    if itype=="🔢 DSA Problem Solver":
        st.markdown("#### 🔢 DSA Problem Solver")
        c1,c2,c3=st.columns(3)
        with c1: ilang=st.selectbox("Language",["Python","C++","Java","JavaScript"],key="ilang")
        with c2: diff=st.selectbox("Difficulty",["Easy","Medium","Hard"],key="diff")
        with c3: dtype=st.selectbox("Response",["Full Solution","Hints Only","Step-by-step Approach"],key="dtype")
        prob=st.text_area("",height=120,placeholder="Paste DSA problem here...\n\ne.g. Given an array of integers, find two numbers that add up to a target sum.",label_visibility="collapsed",key="prob")
        if st.button("🔢 Solve Problem",type="primary",key="dsa_btn") and prob.strip():
            if dtype=="Hints Only":
                p=f"Give 3 progressive hints for this {diff} DSA problem. Don't give full solution yet:\n\n{prob}"
            elif dtype=="Step-by-step Approach":
                p=f"Explain step-by-step approach for this {diff} DSA problem in {ilang}. Include time/space complexity:\n\n{prob}"
            else:
                p=f"Solve this {diff} DSA problem in {ilang}:\n1. Approach explanation\n2. Clean solution with comments\n3. Time complexity O(?) \n4. Space complexity O(?)\n5. Edge cases\n\nProblem:\n{prob}"
            with st.spinner("Solving..."):
                out=ask([{"role":"user","content":p}],m_key,BASE_SYS+" "+RESP_LANGS[rlang])
            st.markdown("<hr>",unsafe_allow_html=True); st.markdown(out)
            st.markdown(dl(out,"dsa_solution.txt","Download Solution"),unsafe_allow_html=True)

    # System Design
    elif itype=="🏗️ System Design":
        st.markdown("#### 🏗️ System Design")
        sd_q=st.text_input("",placeholder="e.g. Design Twitter / Design a URL shortener / Design WhatsApp...",label_visibility="collapsed",key="sd_q")
        sd_level=st.selectbox("Detail Level",["High-level overview","Detailed with components","Full deep-dive"],key="sd_lvl")
        if st.button("🏗️ Design System",type="primary",key="sd_btn") and sd_q.strip():
            p=(f"System design for: {sd_q}\nDetail: {sd_level}\n\n"
               f"Cover: Requirements, Scale estimation, High-level design, "
               f"Key components, Database choice, API design, Trade-offs")
            with st.spinner("Designing..."):
                out=ask([{"role":"user","content":p}],m_key,BASE_SYS+" "+RESP_LANGS[rlang])
            st.markdown("<hr>",unsafe_allow_html=True); st.markdown(out)

    # HR Questions
    elif itype=="💼 HR Questions":
        st.markdown("#### 💼 HR Interview Questions")
        c1,c2=st.columns(2)
        with c1: role=st.text_input("Target Role",placeholder="e.g. Software Engineer at Google",key="hr_role")
        with c2: hr_type=st.selectbox("Type",["Generate Questions + Answers","Rate my Answer","STAR Method Response"],key="hr_type")
        hr_ans=st.text_area("",height=100,placeholder="Your answer (for rating) or blank for question generation...",label_visibility="collapsed",key="hr_ans")
        if st.button("💼 Get HR Help",type="primary",key="hr_btn"):
            if hr_type=="Generate Questions + Answers":
                p=f"Generate 10 common HR interview questions for '{role or 'Software Engineer'}' with ideal STAR-method answers."
            elif hr_type=="Rate my Answer" and hr_ans.strip():
                p=f"Rate this HR interview answer for '{role}' role. Give score /10, strengths, weaknesses, improved version:\n\n{hr_ans}"
            else:
                p=f"Write a strong STAR method answer for a '{role}' interview:\n\n{hr_ans}"
            with st.spinner(""):
                out=ask([{"role":"user","content":p}],m_key,BASE_SYS+" "+RESP_LANGS[rlang])
            st.markdown("<hr>",unsafe_allow_html=True); st.markdown(out)

    # README Generator
    elif itype=="📝 README Generator":
        st.markdown("#### 📝 README Generator")
        st.caption("Paste your project code or describe it → get a professional README.md")
        c1,c2=st.columns(2)
        with c1: proj_name=st.text_input("Project Name",placeholder="My Awesome Project",key="pname")
        with c2: tech_stack=st.text_input("Tech Stack",placeholder="Python, FastAPI, PostgreSQL",key="pstack")
        proj_desc=st.text_area("",height=120,placeholder="Describe your project or paste main code...",label_visibility="collapsed",key="pdesc")
        if st.button("📝 Generate README",type="primary",key="readme_btn") and proj_desc.strip():
            p=(f"Generate a professional GitHub README.md for:\n"
               f"Project: {proj_name or 'My Project'}\nStack: {tech_stack or 'Not specified'}\n"
               f"Description: {proj_desc}\n\n"
               f"Include: Title, badges, description, features, installation, usage, "
               f"API docs (if applicable), contributing, license. Use proper markdown.")
            with st.spinner("Generating README..."):
                out=ask([{"role":"user","content":p}],m_key,BASE_SYS)
            st.markdown("<hr>",unsafe_allow_html=True); st.markdown(out)
            st.markdown(dl(out,"README.md","Download README.md"),unsafe_allow_html=True)

    # Complexity
    elif itype=="⏱ Complexity Analyzer":
        st.markdown("#### ⏱ Time & Space Complexity Analyzer")
        comp_lang=st.selectbox("Language",LANGS,key="comp_lang")
        comp_code=st.text_area("",height=200,placeholder="Paste your code to analyze complexity...",label_visibility="collapsed",key="comp_code")
        if st.button("⏱ Analyze",type="primary",key="comp_btn") and comp_code.strip():
            p=(f"Analyze time and space complexity of this {comp_lang} code:\n"
               f"```{comp_lang.lower()}\n{comp_code}\n```\n\n"
               f"For each function: Big O notation, explanation, best/worst/average case. "
               f"Then suggest optimizations with improved code.")
            with st.spinner("Analyzing..."):
                out=ask([{"role":"user","content":p}],m_key,BASE_SYS+" "+RESP_LANGS[rlang])
            st.markdown("<hr>",unsafe_allow_html=True); st.markdown(out)

# ════════════════════════════════════════════════════════════════════════════ #
# TAB 4 — RESUME AI                                                            #
# ════════════════════════════════════════════════════════════════════════════ #
with tab4:
    st.markdown("<div style='height:16px;'></div>",unsafe_allow_html=True)
    st.markdown("### 📋 Resume AI Analyzer")
    st.caption("Upload your resume → Get ATS score, detailed feedback, and improvement suggestions")
    st.markdown("<hr>",unsafe_allow_html=True)
    L4,R4=st.columns([1,1],gap="medium")
    with L4:
        st.markdown("#### 📤 Upload Resume")
        res_file=st.file_uploader("",type=["pdf","txt","md"],key="resf",
            help="PDF, TXT, or MD supported",label_visibility="collapsed")
        res_text=""
        if res_file:
            res_text=read_file(res_file)
            st.success(f"✅ **{res_file.name}** uploaded ({len(res_text):,} chars)")
            with st.expander("👁 Preview"):
                st.text(res_text[:600]+("..." if len(res_text)>600 else ""))

        st.markdown("**— or paste text —**")
        res_paste=st.text_area("",height=180,placeholder="Paste your resume here...",label_visibility="collapsed",key="resp")
        final_res=res_text if res_text.strip() else res_paste

        st.markdown("<br>",unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1: res_role=st.text_input("🎯 Target Role",placeholder="e.g. Software Engineer",key="rrole")
        with c2: res_act=st.selectbox("Analysis",["🔍 Full Review + Score","📊 ATS Score","💡 10 Tips","✍️ Rewrite Summary","🎯 Job Match"],key="ract")

        jd=""
        if res_act=="🎯 Job Match":
            jd=st.text_area("Paste Job Description",height=100,key="jdesc")

        if st.button("🚀 Analyze Resume",type="primary",use_container_width=True,key="res_btn"):
            if not final_res.strip():
                st.warning("Upload or paste your resume first!")
            else:
                role=res_role or "General"
                if res_act=="🔍 Full Review + Score":
                    p=(f"Analyze this resume for '{role}'. Provide:\n"
                       f"## 📊 Overall Score: X/10\n"
                       f"## ✅ Strengths (3-5 points)\n"
                       f"## ❌ Weaknesses (3-5 points)\n"
                       f"## 🔑 Missing Keywords for '{role}'\n"
                       f"## 📐 Format & Structure (bullet points)\n"
                       f"## 💡 Top 5 Specific Improvements\n"
                       f"## 🏆 Final Verdict\n\nResume:\n{final_res}")
                elif res_act=="📊 ATS Score":
                    p=f"ATS analysis for '{role}'. Give ATS score %, missing keywords, format issues, and fixes:\n\n{final_res}"
                elif res_act=="💡 10 Tips":
                    p=f"Give exactly 10 specific, actionable improvement tips for this resume for '{role}':\n\n{final_res}"
                elif res_act=="✍️ Rewrite Summary":
                    p=f"Rewrite the professional summary for '{role}'. 3-4 lines, impactful, ATS-friendly, results-focused:\n\n{final_res}"
                elif res_act=="🎯 Job Match":
                    p=(f"Compare resume vs job description. Give:\n"
                       f"- Match percentage\n- Matched skills ✅\n- Missing skills ❌\n"
                       f"- Suggestions to improve match\n\n"
                       f"Resume:\n{final_res}\n\nJob Description:\n{jd}")
                RES_SYS=f"You are an expert HR consultant and resume coach. {DEV} {RESP_LANGS[rlang]}"
                with st.spinner("📋 Analyzing resume..."):
                    st.session_state.resume_out=ask([{"role":"user","content":p}],m_key,RES_SYS)

    with R4:
        st.markdown("#### 🤖 AI Feedback")
        if st.session_state.resume_out:
            st.markdown(st.session_state.resume_out)
            st.markdown("<hr>",unsafe_allow_html=True)
            st.markdown(dl(st.session_state.resume_out,"resume_feedback.txt","Download Feedback"),unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#16213e;border:1px solid #0f3460;border-radius:12px;
              padding:50px 24px;text-align:center;min-height:420px;display:flex;flex-direction:column;
              align-items:center;justify-content:center;">
              <div style="font-size:32px;margin-bottom:14px;">📋</div>
              <h3 style="color:#e2e8f0;font-size:15px;margin:0 0 8px;">Resume AI Analyzer</h3>
              <p style="color:#475569;font-size:13px;">Upload or paste your resume and click Analyze</p>
              <div style="margin-top:16px;font-size:12px;color:#334155;line-height:2;">
                ✅ ATS Score<br>✅ Keyword Analysis<br>✅ Improvement Tips<br>✅ Job Description Match</div>
            </div>""",unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════ #
# TAB 5 — QUICK TOOLS                                                          #
# ════════════════════════════════════════════════════════════════════════════ #
with tab5:
    st.markdown("<div style='height:16px;'></div>",unsafe_allow_html=True)
    tool=st.radio("",["🚨 Error Explainer","📋 Code Generator","🔀 Git Helper","🔍 Regex Builder","📖 Concept Explainer"],
                  horizontal=True,label_visibility="collapsed",key="qtool")
    st.markdown("<hr>",unsafe_allow_html=True)

    SYS5=BASE_SYS+" "+RESP_LANGS[rlang]

    if tool=="🚨 Error Explainer":
        st.markdown("#### 🚨 Error Explainer")
        st.caption("Paste any error or stack trace → get cause + fix instantly")
        c1,c2=st.columns([1,3])
        with c1: elang=st.selectbox("Language",LANGS,key="elang")
        with c2: st.markdown("<div style='height:28px;'></div>",unsafe_allow_html=True)
        err=st.text_area("",height=150,placeholder="Paste your error or stack trace here...\n\nTraceback (most recent call last):\n  File 'app.py', line 12\nTypeError: unsupported operand...",label_visibility="collapsed",key="err")
        if st.button("🔍 Explain & Fix",type="primary",key="eb") and err.strip():
            p=(f"This {elang} error:\n```\n{err}\n```\n\n"
               f"Explain: 1) Root cause 2) What it means 3) Fixed code 4) Prevention tip")
            with st.spinner("Analyzing error..."):
                out=ask([{"role":"user","content":p}],m_key,SYS5)
            st.markdown("<hr>",unsafe_allow_html=True); st.markdown(out)

    elif tool=="📋 Code Generator":
        st.markdown("#### 📋 Code Generator")
        st.caption("Describe what you want → get clean, production-ready code")
        c1,c2=st.columns(2)
        with c1: glang=st.selectbox("Language",LANGS,key="glang")
        with c2: gstyle=st.selectbox("Style",["Clean & Commented","With Error Handling","With Tests","Minimal"],key="gstyle")
        gdesc=st.text_area("",height=100,placeholder="Describe what you want to build...\ne.g. A REST API endpoint that accepts a JSON body with name and email, validates them, and saves to a database",label_visibility="collapsed",key="gdesc")
        if st.button("⚡ Generate Code",type="primary",key="gb") and gdesc.strip():
            p=f"Write {glang} code: {gdesc}\nStyle: {gstyle}, production-ready, best practices."
            with st.spinner("Generating..."):
                out=ask([{"role":"user","content":p}],m_key,SYS5)
            st.markdown("<hr>",unsafe_allow_html=True); st.markdown(out)
            st.markdown(dl(out,"generated.txt","Download Code"),unsafe_allow_html=True)

    elif tool=="🔀 Git Helper":
        st.markdown("#### 🔀 Git Helper")
        st.caption("Git commands, problems, workflows — all explained")
        gtype=st.selectbox("What do you need?",["Explain a git command","Fix a git problem",
            "Generate commit message","Git workflow guide","Undo/revert changes"],key="gtype")
        gin=st.text_area("",height=100,placeholder="Describe your git question or problem...",label_visibility="collapsed",key="gin")
        if st.button("🔀 Get Git Help",type="primary",key="git_b") and gin.strip():
            p=f"Git help — {gtype}:\n\n{gin}\n\nProvide exact commands with clear explanation."
            with st.spinner(""):
                out=ask([{"role":"user","content":p}],m_key,SYS5)
            st.markdown("<hr>",unsafe_allow_html=True); st.markdown(out)

    elif tool=="🔍 Regex Builder":
        st.markdown("#### 🔍 Regex Builder")
        st.caption("Describe in plain English → get the regex pattern + explanation")
        c1,c2=st.columns(2)
        with c1: rlang2=st.selectbox("Language",["Python","JavaScript","Java","PHP","Go"],key="rlang2")
        with c2: st.markdown("")
        rdesc=st.text_input("",placeholder="e.g. Match all email addresses / Extract phone numbers / Validate Indian PIN code",label_visibility="collapsed",key="rdesc")
        rtest=st.text_area("",height=80,placeholder="Optional: paste test strings to validate the regex...",label_visibility="collapsed",key="rtest")
        if st.button("🔍 Build Regex",type="primary",key="rb") and rdesc.strip():
            p=(f"Build a {rlang2} regex for: {rdesc}\n"
               f"Provide: 1) The regex pattern 2) Explanation of each part 3) Code example"
               +(f"\n4) Test against these strings:\n{rtest}" if rtest.strip() else ""))
            with st.spinner("Building regex..."):
                out=ask([{"role":"user","content":p}],m_key,SYS5)
            st.markdown("<hr>",unsafe_allow_html=True); st.markdown(out)

    elif tool=="📖 Concept Explainer":
        st.markdown("#### 📖 Concept Explainer")
        st.caption("Any programming concept → clear explanation with examples")
        c1,c2=st.columns([3,1])
        with c1: con=st.text_input("",placeholder="e.g. recursion, Big O notation, async/await, REST API, pointers, closures...",label_visibility="collapsed",key="con")
        with c2: lvl=st.selectbox("",["Beginner","Intermediate","Advanced"],label_visibility="collapsed",key="clvl")
        if st.button("📖 Explain",type="primary",key="conb") and con.strip():
            p=(f"Explain '{con}' for a {lvl} programmer.\n"
               f"Include: definition, how it works, real-world analogy, "
               f"code example in Python, common mistakes, when to use it.")
            with st.spinner("Explaining..."):
                out=ask([{"role":"user","content":p}],m_key,SYS5)
            st.markdown("<hr>",unsafe_allow_html=True); st.markdown(out)
