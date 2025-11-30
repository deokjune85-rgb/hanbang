import streamlit as st
import time
import random

# ---------------------------------------
# 0. 시스템 설정: Veritas Clinical Engine v4.3 (Final Fix)
# ---------------------------------------
st.set_page_config(
    page_title="Veritas Clinical Engine v4.3 | 자연과한의원",
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
st.markdown("<h3 style='margin-bottom:0; font-family: serif; color: white;'>Veritas Clinical Engine v4.3</h3>", unsafe_allow_html=True)
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
            time.sleep(0.5)

        # [수정 완료: 한 줄로 정리하여 에러 방지]
        if cause == "식욕":
            msg = "분석 결과: 식욕 통제 중추의 문제입니다. 위장의 열(Heat)을 제어해야 합니다."
        elif cause == "부종":
            msg = "분석 결과: 순환계 문제입니다. 림프 정체로 인해 수분이 지방과 결합된 상태입니다."
        elif cause == "대사":
            msg = "분석 결과: 대사 효율 문제입니다. 에너지 소모 기능이 저하되어 있습니다."
        else:
            msg = "분석 결과: 자율신경 문제입니다. 스트레스 호르몬(코르티솔)이 지방 분해를 차단하고 있습니다."
        
        full_msg = f"{msg}\n\n마지막 질문입니다. 피험자의 **다이어트 약물(양약/한약) 복용 이력**이 있습니까?"
        bot_say(full_msg)
        st.session_state.step = 5
        st.rerun()

    elif st.session_state.step == 5:
        st.session_state.user_data['history'] = current_input
        
        # Thinking Visualization (Expanded)
        with st.status("최종 임상 데이터 분석 실행 중...", expanded=True) as status:
            st.write("🔍 200,000+ 임상 케이스 데이터베이스 접속...")
            time.sleep(0.8)
            st.write("🧬 피험자 데이터 패턴 대조 및 시뮬레이션...")
            time.sleep(1.2)
            st.write("💡 최적 처방 프로토콜 도출...")
            time.sleep(0.8)
            status.update(label="최종 분석 완료.", state="complete", expanded=False)
            time.sleep(1.0) # 중요: 완료 상태를 보여주고 넘어가야 함

        cause = st.session_state.user_data.get('cause', '대사')
        
        # Data Mapping
        if cause == "식욕":
            title, desc, rx = "위열 과다형 (Stomach Heat)", "뇌가 포만감을 인지하지 못하는 '가짜 배고픔' 상태. 식욕 중추의 과항진.", "식탐사약"
            rx_sub, img = "식욕 억제 및 위장 열 해소", "https://placehold.co/800x400/111/333?text=CLINICAL+EVIDENCE+(BELLY)"
        elif cause == "부종":
            title, desc, rx = "수독 정체형 (Water Retention)", "노폐물 배출 기능 저하로 지방과 수분이 결합된 상태. 림프 순환 저하.", "독소킬 + 지방사약"
            rx_sub, img = "수분 대사 촉진 및 붓기 배출", "https://placehold.co/800x400/111/333?text=CLINICAL+EVIDENCE+(BODY)"
        elif cause == "대사":
            title, desc, rx = "대사 저하형 (Metabolic Drop)", "기초대사량이 낮아 에너지 소모율이 극히 낮은 체질.", "지방사약 (대사촉진형)"
            rx_sub, img = "심부 체온 상승 및 발열 효과 유도", "https://placehold.co/800x400/111/333?text=CLINICAL+EVIDENCE+(FULLBODY)"
        else:
            title, desc, rx = "간기 울결형 (Stress Induced)", "스트레스 호르몬(코르티솔) 과다 분비에 의한 복부 지방 축적.", "소요산 + 지방사약"
            rx_sub, img = "자율신경 안정 및 폭식 차단", "https://placehold.co/800x400/111/333?text=CLINICAL+EVIDENCE+(STRESS)"

        # Result HTML (Same Design)
        result_html = f"""
        <div class='diagnosis-card'>
            <div class='label-small'>ANALYSIS REPORT</div>
            <div class='diagnosis-title'>{title}</div>
            <div class='diagnosis-desc'>{desc}</div>
            <div style='display:flex; justify-content:space-between; align-items:center; margin-top:30px; border-top: 1px solid #333; padding-top: 20px;'>
                <div>
                    <div class='label-small' style='color:#00E676;'>OPTIMAL PRESCRIPTION</div>
                    <div style='font-size:22px; font-weight:bold; color:#FFF;'>{rx}</div>
                    <div style='font-size:14px; color:#AAA;'>Target: {rx_sub}</div>
                </div>
                <div style='text-align:right;'>
                    <div class='label-small'>EST. PERIOD</div>
                    <div style='color:#FFF; font-size:18px;'>3 Months</div>
                </div>
            </div>
        </div>
        <div class='label-small' style='margin-top: 20px;'>CLINICAL EVIDENCE</div>
        <div style='text-align:center; margin: 15px 0;'><img src='{img}' style='max-width:100%; border-radius:8px;'/></div>
        <p style='font-size:12px; color:#555; text-align:center; margin-top: 5px;'>동일 체질 환자의 3개월 임상 변화 데이터 (자연과한의원 제공)</p>
        <div style='margin-top:30px; border-top:1px solid #333; padding-top:20px;'>
            <div class='label-small'>PRICING PLAN (VAT 별도)</div>
            <div style='display:flex; justify-content:space-between; margin-bottom:10px; padding: 5px 0;'>
                <span style='color:#AAA;'>1 Month Plan</span><span style='color:#FFF;'>150,000 KRW</span>
            </div>
            <div style='display:flex; justify-content:space-between; background-color: #051005; padding: 10px; border-radius: 5px;'>
                <span style='color:#00E676;'>6 Months Plan (Recommended)</span>
                <span style='color:#00E676; font-weight:bold;'>Monthly 100,000 KRW ~</span>
            </div>
        </div>
        """
        
        bot_say(result_html, html=True)
        st.session_state.step = 6
        st.rerun()

# [Final Form]
if st.session_state.step == 6:
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='label-small'>REQUEST CONSULTATION</div>", unsafe_allow_html=True)
    with st.form("contact"):
        c1, c2 = st.columns(2)
        with c1: name = st.text_input("성함", placeholder="환자명")
        with c2: phone = st.text_input("연락처", placeholder="010-XXXX-XXXX")
        
        if st.form_submit_button("상담 접수 및 데이터 전송"):
            if name and phone:
                st.success("데이터 전송 완료. 담당 의료진이 배정됩니다.")
            else:
                st.warning("정확한 정보를 입력하십시오.")
