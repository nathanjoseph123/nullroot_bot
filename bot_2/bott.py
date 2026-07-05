

import streamlit as st
import time
from datetime import datetime

from streamlit.runtime.state import session_state
from bot import bot
import threading
from streamlit_local_storage import LocalStorage

localS = LocalStorage()

saved_server = localS.getItem("server_input") or ""
saved_auth = localS.getItem("auth_input") or ""
saved_message = localS.getItem("message_input") or ""
if "bot_" not in st.session_state:
# near the top of the file, outside any function
    _bot_instance = {"bot": None, "running": False}

def on_start(mode, server_input, auth_input):
    if _bot_instance["running"]:
        push_log("Already running — ignoring duplicate start.")
        return
    if _bot_instance["bot"] is not None:
        try:
            _bot_instance["bot"].scrap.site.quit()
        except Exception:
            pass
    _bot_instance["bot"] = bot(server_input, auth_input)
    _bot_instance["running"] = True
    _bot_instance["bot"].scrap.scrap()
    threading.Thread(target=_bot_instance["bot"].command).start()
    push_log(f"[stub] on_start called — mode={mode}")

def on_stop():
    if _bot_instance["bot"] is not None:
        try:
            _bot_instance["bot"].scrap.site.quit()
        except Exception:
            pass
    _bot_instance["bot"] = None
    _bot_instance["running"] = False
    push_log("Stopped.")

def push_log(msg: str):
    st.session_state.logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
st.set_page_config(page_title="NULLROOT BOT", page_icon="🛰️", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #1a1a2e 0%, #0f0f1a 55%, #06060c 100%);
        color: #e6e6f0;
    }
    section[data-testid="stSidebar"] { display: none; }
    h1, h2, h3 { color: #f5f5ff !important; letter-spacing: 0.4px; }

    .hero {
        text-align: center;
        padding: 18px 0 6px 0;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #7c4dff, #448aff, #00e5c8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }
    .hero-sub { color: #9a9ab8; font-size: 0.95rem; }

    div[data-testid="stTextInput"] input {
        background-color: #14142280;
        border: 1px solid #3a3a5c;
        border-radius: 10px;
        color: #eaeaff;
    }

    .status-pill {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }
    .status-running { background: linear-gradient(90deg,#00c9a7,#00b09b); color: #04231d; }
    .status-idle { background: #2c2c40; color: #9a9ab8; }

    .log-box {
        background: #0b0b14;
        border: 1px solid #2c2c40;
        border-radius: 12px;
        padding: 14px;
        font-family: "JetBrains Mono", monospace;
        font-size: 0.82rem;
        max-height: 240px;
        overflow-y: auto;
        white-space: pre-wrap;
    }

    div.stButton > button {
        border-radius: 10px;
        border: 1px solid #3a3a5c;
        background: linear-gradient(180deg, #23233a, #17172a);
        color: #eaeaff;
        font-weight: 600;
        transition: 0.15s ease;
    }
    div.stButton > button:hover {
        border-color: #7c7cff;
        color: #ffffff;
        transform: translateY(-1px);
    }

    .dev-card {
        background: linear-gradient(160deg, #14142499, #0b0b1499);
        border: 1px solid #2c2c40;
        border-radius: 16px;
        padding: 20px 22px;
        margin-top: 10px;
    }
    .dev-avatar {
        width: 54px; height: 54px;
        border-radius: 50%;
        background: linear-gradient(135deg, #7c4dff, #00e5c8);
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: 1.2rem; color: #06060c;
        float: left; margin-right: 14px;
    }
    .dev-name { font-weight: 700; font-size: 1.05rem; color: #f5f5ff; }
    .dev-tag { color: #9a9ab8; font-size: 0.85rem; }
    .dev-links a {
        display: inline-block;
        margin: 10px 8px 0 0;
        padding: 5px 14px;
        border-radius: 999px;
        border: 1px solid #3a3a5c;
        color: #cfcfff !important;
        text-decoration: none;
        font-size: 0.8rem;
    }
    .dev-links a:hover { border-color: #7c7cff; color: #fff !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

for key, val in {
    "running": False,
    "mode": "recent",
    "logs": [],
    "downloads": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🛰️ MINTER CONTROL PANEL</div>
        <div class="hero-sub">scrape · deliver · repeat</div>
    </div>
    """,
    unsafe_allow_html=True,
)


col1, col2 = st.columns(2)
with col1:
    server_input = st.text_input(
        "Discord Webhook URL / Channel ID",
        key="server_input",
        value=saved_server,
        placeholder="https://discord.com/api/webhooks/...  or channel ID",

    )
with col2:
    auth_input = st.text_input(
        "Discord Auth (Bot Token)",
        key="auth_input",
        value=saved_auth,
        type="password",
        placeholder="leave blank if using a webhook URL",
    )

message_input = st.text_input(
    "Message",
    key="message_input",
    value=saved_message,
    placeholder="Custom message to send along with the CSV",
)
if  st.session_state.bot_:
    st.session_state.bot_.mess_to_send=message_input
    
st.write("")
st.subheader("Mode")
m1, m2 = st.columns(2)
with m1:
    if st.button("🏆 Top Minters", use_container_width=True,
                  type="primary" if st.session_state.mode == "top" else "secondary"):
        if st.session_state.bot_:
            st.session_state.bot_.mints=1
            st.session_state.mode = "top"
with m2:
    if st.button("🆕 Recent Minters", use_container_width=True,
                  type="primary" if st.session_state.mode == "recent" else "secondary"):
        if st.session_state.bot_:
            st.session_state.bot_.mints=0
    
            st.session_state.mode = "recent"
       

st.write("")
status_class = "status-running" if st.session_state.running else "status-idle"
status_text = "RUNNING" if st.session_state.running else "IDLE"
st.markdown(
    f'<span class="status-pill {status_class}">● {status_text}</span> '
    f'&nbsp; mode: <b>{st.session_state.mode.upper()}</b>',
    unsafe_allow_html=True,
)

st.write("")
c1, c2 = st.columns(2)
with c1:
    if st.button("▶ Start", use_container_width=True, disabled=st.session_state.running):
        if not server_input:
            st.warning("Add a Discord webhook URL or channel ID first.")
        else:
            st.session_state.running = True
            on_start(st.session_state.mode, server_input, auth_input)
            st.rerun()
with c2:
    if st.button("■ Stop", use_container_width=True, disabled=not st.session_state.running):
        st.session_state.running = False
        on_stop()
        st.rerun()

st.write("")
st.subheader("Logs")
st.markdown(
    f'<div class="log-box">{"<br>".join(st.session_state.logs) or "No activity yet."}</div>',
    unsafe_allow_html=True,
)


st.write("")
st.write("")
with st.expander("👤 About the Dev", expanded=False):
    st.markdown(
        """
        <div class="dev-card">
            <div class="dev-avatar">N</div>
            <div class="dev-name">Nathan joseph (nullroot)</div>
            <div class="dev-tag">builder · systems &amp; graphics</div>
            <div style="clear:both;"></div>
            <div style="margin-top:10px; color:#c8c8dd; font-size:0.88rem;">
                This project was made by nathan in a fucking day ,\nso might not be perfect , but come on " i am nullroot"
            </div>
            <div class="dev-links">
                <a href="https://github.com/nathanjoseph123" target="_blank">GitHub</a> 
                <a href="https://nullroot1.itch.io/" target="_blank">itch.io</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
