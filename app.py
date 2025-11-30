import streamlit as st
import time
import random

# ---------------------------------------
# 0. 시스템 설정: Veritas Clinical Engine
# ---------------------------------------
st.set_page_config(
    page_title="Veritas Clinical Engine v4.1 | 자연과한의원",
    page_icon="🧬",
    layout="centered"
)

# [CSS: High-End Editorial Design]
custom_css = """
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp {
        background-color: #0C0C0C !important;
        color: #E0E0E0 !important;
        font-family: 'Pretendard', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    p, div { line-height: 1.7; color: #CCCCCC; font-weight: 300; }
    .accent { color: #00E676; }

    .stChatMessage { 
        background-color: #0C0C0C !important; 
        padding: 15px 0 !important; 
        border-bottom: 1px solid #1A1A1A; 
    }
    [data-testid="stChatMessageContent"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        color: #E0E0E0;
    }
    .stChatMessage img { border-radius: 0 !important; }

    .stChatInputContainer {
        border-top: 1px solid #333;
        padding-top: 10px;
    }
    .stChatInputInput {
        background-color: #1A1A1A !important;
        border: 1px solid #444 !important;
        color: white !important;
        border-radius: 8px !important;
    }

    div.stButton > button {
        background-color: #1A1A1A;
        color: #AAA !important;
        border: 1px solid #444 !important;
        border-radius: 20px !important;
        font-size: 14px !important;
        padding: 8px 16px !important;
        margin-right: 5px;
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        border-color: #00E676 !important;
        color: #00E676 !important;
        background-color: #051005 !important;
    }
    
    .diagnosis-card {
        border-left: 2px solid #00E676;
        padding: 30px 20px;
        margin: 20px 0;
        background-color: #111111;
    }
    .label-small { 
        font-size: 11px; 
        color: #888; 
        letter-spacing: 1.5px; 
        text-transform: uppercase; 
        margin-bottom: 5px; 
    }
    .diagnosis-title { 
        font-size: 32px; 
        color: #FFF; 
        font-weight: 800; 
        margin-bottom: 15px; 
        font-family: serif; 
    }
    .diagnosis-desc { 
        font-size: 16px; 
        color: #AAA; 
        margin-bottom: 20px; 
    }
    
    [data-testid="stStatusWidget"] {
        background-color: #1A1A1A;
        border-radius: 8px;
        padding: 10px;
    }

    [data-testid="column"] { padding: 0 5px !important; }

    div[data-testid="stForm"] button[type="submit"] {
        width: 100%;
        background-color: #00E676 !important;
        color: #000000 !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px;
        border: none;
        font-size: 16px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 1. State & Helper Functions
# ---------------------------------------
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'temp_input' not in st.session_state:
    st.session_state.temp_input = None
if 'last_animated_index' not in st.session_state:
    st.session_state.last_animated_index = -1

AI_AVATAR = "🧬"
USER_AVATAR = "👤"

def claude_stream(text, speed=0.02):
    """Claude/Gemini 스타일 스트리밍"""
    placeholder = st.empty()
    words = text.split(' ')
    display_text = ""
    
    for word in words:
        display_text += word + " "
        placeholder.markdown(display_text + "●")
        time.sleep(speed)
    
    placeholder.markdown(display_text.strip())
    return display_text.strip()

def bot_say(content, html=False):
    """AI 메시지 추가"""
    st.session_state.messages.append({
        "role": "assistant", 
        "content": content, 
        "html": html
    })

def user_say(content):
    """사용자 메시지 추가"""
    st.session_state.messages.append({
        "role": "user", 
        "content": content
    })

# ---------------------------------------
# 2. Main Interface
# ---------------------------------------
st.markdown("<h3 style='margin-bottom:0; font-family: serif;'>Veritas Clinical Engine v4.1</h3>", unsafe_allow_html=True)
st.markdown("<p style='font-size:12px; color:#555;'>Powered by Jayeon Data Labs | 자연과한의원</p>", unsafe
