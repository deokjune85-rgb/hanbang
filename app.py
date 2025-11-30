import streamlit as st
import time
import random

# ---------------------------------------
# 0. 시스템 설정: Veritas Clinical Engine v4.2 (Logic Fix)
# ---------------------------------------
st.set_page_config(
    page_title="Veritas Clinical Engine v4.2 | 자연과한의원",
    page_icon="🧬",
    layout="centered"
)

# [CSS: High-End Editorial Design - 유지하되 일부 최적화]
custom_css = """
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp {
        background-color: #0C0C0C !important;
        color: #E0E0E0 !important;
        font-family: 'Pretendard', sans-serif;
    }
    #MainMenu, footer, header {visibility: hidden;}

    /* Typography */
    p, div { line-height: 1.7; color: #CCCCCC; font-weight: 300; }
    
    /* Chat Message */
    .stChatMessage { background-color: #0C0C0C !important; padding: 15px 0 !important; border-bottom: 1px solid #1A1A1A; }
    [data-testid="stChatMessageContent"] { background-color: transparent !important; color: #E0E0E0; }
    .stChatMessage img { border-radius: 0 !important; } 

    /* Input & Buttons */
    .stChatInputContainer { border-top: 1px solid #333; padding-top: 10px; }
    .stChatInputInput { background-color: #1A1A1A !important; border: 1px solid #444 !important; color: white !important; }
    
    /* Chips */
    div.stButton > button {
        background-color: #1A1A1A;
        color: #AAA !important;
        border: 1px solid #444 !important;
        border-radius: 20px !important;
        font-size: 13px !important;
        padding: 8px 16px !important;
        transition: all 0.2s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        border-color: #00E676 !important;
        color: #00E676 !important;
        background-color: #051005 !important;
    }
    
    /* Diagnosis Card */
    .diagnosis-card {
        border-left: 2px solid #00E676;
        padding: 30px 20px;
        margin: 20px 0;
        background-color: #111111;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .label-small { font-size: 11px; color: #888; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 5px; }
    .diagnosis-title { font-size: 28px; color: #FFF; font-weight: 800; margin-bottom: 15px; font-family: serif; }
    .diagnosis-desc { font-size: 15px; color: #AAA; margin-bottom: 20px; }

    /* Submit Button */
    div[data-testid="stForm"] button[type="submit"] {
        width: 100%;
        background-color: #00E676 !important;
        color: #000000 !important;
        font-weight: bold;
        border-radius: 8px;
        border: none;
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

AI_AVATAR = "🧬"
USER_AVATAR = "👤"

def claude_stream(text, speed=0.01):
    """글자 단위 스트리밍으로 변경하여 더 부드럽게 표현"""
    placeholder = st.empty()
    display_text = ""
    # 한글은 글자 단위가 자연스러움
    for char in text:
        display_text += char
        placeholder.markdown(display_text + "●") # 커서 효과
        time.sleep(speed)
    placeholder.markdown(display_text)
    return display_text

def bot_say(content, image=None, html=False):
    st.session_state.messages.append({
        "role": "assistant", 
        "content": content, 
        "image": image, 
        "html": html, 
        "animated": False
    })

def user_say(content):
    st.session_state.messages.append({
        "role": "user", 
        "content": content, 
        "animated": True
    })

# ---------------------------------------
# 2. Render Chat History
# ---------------------------------------
# [Header]
st.markdown("<h3 style='margin-bottom:0; font-family: serif; color: white;'>Veritas Clinical Engine v4.2</h3>", unsafe_allow_html=True)
st.markdown("<p style='font-size:12px; color:#555;'>Powered by Jayeon Data Labs | 자연과한의원</p>", unsafe_allow_html=True)
st.divider()

# [Init Prompt]
if st.session_state.step == 0:
    msg = "Veritas Engine 활성화.\n\n25년간 축적된 임상 데이터를 기반으로 체중 정체 원인을 분석합니다.\n\n분석을 위해 피험자의 **성별, 나이, 키, 체중** 데이터를 입력하십시오."
    bot_say(msg)
    st.session_state.step = 1

# [Render Messages]
for i, msg in enumerate(st.session_state.messages):
    avatar = AI_AVATAR if msg["role"] == "assistant" else USER_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        # 마지막 메시지이고, 아직 애니메이션 안됐고, AI인 경우
        if msg["role"] == "assistant" and not msg.get("animated") and i == len(st.session_state.messages) - 1:
            if msg.get("html"):
                st.markdown(msg["content"], unsafe_allow_html=True)
            else:
                claude_stream(msg["content"])
            
            if msg.get("image"):
                st.image(msg["image"], use_column_width=True)
            
            msg["animated"] = True # 애니메이션 완료 처리
        else:
            # 과거 메시지 or 유저 메시지 (즉시 렌더링)
            if msg.get("html"):
                st.markdown(msg["content"], unsafe_allow_html=True)
            else:
                st.markdown(msg["content"])
            
            if msg.get("image"):
                st.image(msg["image"], use_column_width=True)

# ---------------------------------------
# 3. Dynamic Interaction Controller
# ---------------------------------------
# 입력 변수 초기화
current_input = None

# [Step 3: Chips Area - 입력창 바로 위에 배치]
if st.session_state.step == 3:
    st.markdown("<p style='font-size:12px; color:#666; margin-bottom:10px; letter-spacing: 1px;'>SELECT SYMPTOM</p>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    # 버튼 클릭 시 rerun 없이 current_input에 할당 -> 하단 로직으로 흐름 연결
    if col1.button("식욕 조절 불가"): current_input = "식욕 조절이 불가능합니다."
    if col2.button("만성 부종"): current_input = "몸이 자주 붓습니다."
    if col3.button("대사 저하"): current_input = "섭취량 대비 체중 감소가 없습니다."
    if col4.button("스트레스성 폭식"): current_input = "스트레스로 인한 폭식 증상이 있습니다."

# [Main Input]
input_disabled = (st.session_state.step == 6)
chat_input_val = st.chat_input("데이터 또는 증상을 입력하십시오...", disabled=input_disabled)

# 버튼 값 혹은 채팅 입력 값 중 하나라도 있으면 진행
if chat_input_val:
    current_input = chat_input_val

# ---------------------------------------
# 4. Logic Processing (Core)
# ---------------------------------------
if current_input:
    # 1. User Message 기록
    user_say(current_input)
    
    # 2. Logic Handler
    if st.session_state.step == 1:
        st.session_state.user_data['info'] = current_input
        
        with st.status("기본 데이터 처리 중...", expanded=False) as status:
            time.sleep(1.0) # UX를 위한 의도적 지연
            status.update(label="처리 완료.", state="complete", expanded=False)
        
        bot_say("기본 데이터 입력 완료.\n\n핵심 질문입니다. 피험자가 호소하는 **다이어트 실패의 주된 원인**은 무엇입니까? (상단 버튼 선택 또는 직접 입력)")
        st.session_state.step = 3
        st.rerun()

    elif st.session_state.step == 3:
        txt = current_input.lower()
        cause = "기타"
        if any(x in txt for x in ['식욕', '불가능합니다', '먹고']): cause = "식욕"
        elif any(x in txt for x in ['붓기', '붓습', '부종']): cause = "부종"
        elif any(x in txt for x in ['대사', '없습', '적게']): cause = "대사"
        elif any(x in txt for x in ['스트레스', '폭식']): cause = "스트레스"
        
        st.session_state.user_data['cause'] = cause
        
        with st.status("증상 패턴 분석 중...", expanded=False) as status:
            time.sleep(1.2)
            status.update(label="분석 완료.", state="complete", expanded=False)
            time.sleep(0.5) # 사용자가 완료 메시지를 볼 시간 부여

        if cause == "식욕": msg = "분석 결과: 식욕 통제 중추의 문제입니다. 위장의 열(Heat)을 제어해야 합니다."
        elif cause == "부종": msg = "분석 결과: 순환계 문제입니다. 림프 정체로 인해 수분이 지방과 결합된 상태입니다."
        elif cause == "대사": msg = "분석 결과: 대사 효율 문제입니다. 에너지 소모 기능이 저하되어 있습니다."
        else: msg = "분석 결과: 자율신경 문제입니다. 스트레스
