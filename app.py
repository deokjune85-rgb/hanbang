import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random

# -----------------------------------------------------------------------------
# 1. SYSTEM CONFIGURATION (THE BLACK BOX THEME)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="VERITAS AI DIAGNOSIS",
    page_icon="👁‍🗨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# [CSS: 압도적인 몰입감과 긴장감 조성]
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700;900&display=swap');

    .stApp {
        background-color: #000000 !important;
        color: #E0E0E0;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* UI Elements Hiding */
    #MainMenu, footer, header {visibility: hidden;}

    /* Typography */
    h1 { color: #FFF; font-weight: 900; letter-spacing: -1px; }
    .highlight-red { color: #FF0033; font-weight: bold; text-shadow: 0 0 10px #FF0033; }
    .highlight-blue { color: #00BFFF; font-weight: bold; text-shadow: 0 0 10px #00BFFF; }
    
    /* System Logs */
    .sys-msg {
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: #444;
        border-left: 2px solid #333;
        padding-left: 10px;
        margin-bottom: 10px;
    }

    /* Chat Message (AI Persona) */
    .stChatMessage {
        background-color: #0A0A0A !important;
        border: 1px solid #222;
        margin-bottom: 15px;
    }
    
    /* Input Fields (Terminal Style) */
    .stTextArea > div > div > textarea {
        background-color: #050505 !important;
        color: #00FF00 !important;
        border: 1px solid #333 !important;
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 16px;
    }
    .stTextInput > div > div > input {
        background-color: #050505 !important;
        color: #FFF !important;
        border: 1px solid #333 !important;
    }

    /* Action Buttons (Neon Glitch) */
    .stButton > button {
        background-color: #000000 !important;
        color: #00BFFF !important;
        border: 1px solid #00BFFF !important;
        font-weight: bold;
        padding: 15px 0;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #00BFFF !important;
        color: #000 !important;
        box-shadow: 0 0 20px #00BFFF;
    }
    
    /* Critical Alert Box */
    .alert-box {
        border: 1px solid #FF0033;
        background-color: rgba(255, 0, 51, 0.1);
        padding: 20px;
        border-radius: 5px;
        text-align: center;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. LOGIC ENGINE (Simulated AI Intelligence)
# -----------------------------------------------------------------------------
if 'stage' not in st.session_state:
    st.session_state.stage = 'INTRO'
if 'user_context' not in st.session_state:
    st.session_state.user_context = {}

def stream_text(text, speed=0.03):
    """AI가 실시간으로 말하는 듯한 효과"""
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(full_text + "▌")
        time.sleep(speed)
    placeholder.markdown(full_text)

def analyze_keywords(text):
    """키워드 기반의 '콜드 리딩(Cold Reading)' 로직"""
    text = text.lower()
    if any(x in text for x in ['물', '붓기', '부종', '아침', '반지', '신발', '팅팅']):
        return "Edema", "혹시 아침에 일어나면 손이 쥐어지지 않거나, 저녁에 신발이 꽉 끼지 않으십니까? 이건 살이 아니라 '독소 수분'입니다."
    elif any(x in text for x in ['밥', '빵', '면', '단거', '초콜릿', '간식', '식욕', '배고파', '먹고']):
        return "Carb", "식사 후에도 금방 허기가 지고, 스트레스를 받으면 단 것부터 찾게 되시죠? '가짜 배고픔'에 뇌가 속고 있는 상태입니다."
    elif any(x in text for x in ['술', '야식', '회식', '고기', '기름', '맥주', '소주']):
        return "Liver", "단순한 칼로리 문제가 아닙니다. 간의 해독 기능이 마비되어 지방을 태우지 못하고 쌓아두기만 하는 '대사 정체' 상태입니다."
    elif any(x in text for x in ['피곤', '무기력', '잠', '힘들', '우울', '짜증', '스트레스']):
        return "Stress", "아무리 굶어도 안 빠지셨죠? 몸이 '생존 모드'에 들어가서 지방을 꽉 붙들고 있습니다. 이건 의지 문제가 아니라 호르몬 문제입니다."
    else:
        return "General", "체중계의 숫자보다 더 심각한 것은 체내의 '염증 반응'입니다. 현재 대사 시스템이 셧다운 직전입니다."

def generate_danger_chart(score):
    """위협적인 붉은색 레이더 차트"""
    categories = ['식욕 통제력', '림프 순환', '기초 대사량', '호르몬 균형', '염증 수치']
    # 환자에게 충격을 주기 위해 일부러 극단적인 수치 생성
    values = [random.randint(10, 30), random.randint(10, 40), random.randint(20, 50), random.randint(10, 30), random.randint(80, 100)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(255, 0, 51, 0.3)', # 붉은색 채우기
        line=dict(color='#FF0033', width=3), # 붉은색 선
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, linecolor='#333'),
            angularaxis=dict(color='#AAA')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(family='Noto Sans KR', color='#FFF')
    )
    return fig

# -----------------------------------------------------------------------------
# 3. UI FLOW (THE SALES FUNNEL)
# -----------------------------------------------------------------------------

# [HEADER]
st.markdown("<div style='text-align:right; font-size:10px; color:#555;'>VERITAS MED-AI v10.0 ● CONNECTED</div>", unsafe_allow_html=True)
st.divider()

# -----------------------------------------------------------------------------
# STAGE 1: THE INTERROGATION (하소연 유도)
# -----------------------------------------------------------------------------
if st.session_state.
