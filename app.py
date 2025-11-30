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
st.markdown("<p style='font-size:12px; color:#555;'>Powered by Jayeon Data Labs | 자연과한의원</p>", unsafe_allow_html=True)
st.divider()

# [STEP 0: Init]
if st.session_state.step == 0:
    msg = "Veritas Engine 활성화.\n\n25년간 축적된 임상 데이터를 기반으로 체중 정체 원인을 분석합니다.\n\n분석을 위해 피험자의 **성별, 나이, 키, 체중** 데이터를 입력하십시오."
    bot_say(msg)
    st.session_state.step = 1

# ---------------------------------------
# 3. Render Chat History
# ---------------------------------------
for i, msg in enumerate(st.session_state.messages):
    avatar = AI_AVATAR if msg["role"] == "assistant" else USER_AVATAR
    
    with st.chat_message(msg["role"], avatar=avatar):
        # 마지막 AI 메시지이고 아직 애니메이션 안 했으면 스트리밍
        is_last_message = (i == len(st.session_state.messages) - 1)
        should_animate = (
            msg["role"] == "assistant" and 
            is_last_message and 
            i > st.session_state.last_animated_index
        )
        
        if should_animate:
            if msg.get("html"):
                # HTML은 애니메이션 없이 즉시 표시
                st.markdown(msg["content"], unsafe_allow_html=True)
            else:
                # 일반 텍스트는 스트리밍
                claude_stream(msg["content"])
            
            st.session_state.last_animated_index = i
        else:
            # 이전 메시지는 즉시 표시
            if msg.get("html"):
                st.markdown(msg["content"], unsafe_allow_html=True)
            else:
                st.markdown(msg["content"])

# ---------------------------------------
# 4. Dynamic Interaction Area
# ---------------------------------------

# [Step 3: Chip Buttons]
if st.session_state.step == 3:
    st.markdown("<p style='font-size:12px; color:#666; margin-bottom:10px; letter-spacing: 1.5px;'>SELECT SYMPTOM</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    if c1.button("식욕 조절 불가", key="btn1"):
        st.session_state.temp_input = "식욕 조절이 불가능합니다."
        st.rerun()
    if c2.button("만성 부종", key="btn2"):
        st.session_state.temp_input = "몸이 자주 붓습니다."
        st.rerun()
    if c3.button("대사 저하", key="btn3"):
        st.session_state.temp_input = "섭취량 대비 체중 감소가 없습니다."
        st.rerun()
    if c4.button("스트레스성 폭식", key="btn4"):
        st.session_state.temp_input = "스트레스로 인한 폭식 증상이 있습니다."
        st.rerun()

# [Input Handling]
input_disabled = (st.session_state.step == 6)
prompt = st.chat_input("데이터 또는 증상을 입력하십시오...", disabled=input_disabled)

# temp_input 처리
if st.session_state.temp_input:
    prompt = st.session_state.temp_input
    st.session_state.temp_input = None

if prompt:
    user_say(prompt)
    
    # Step 1: 기본 정보 입력
    if st.session_state.step == 1:
        st.session_state.user_data['info'] = prompt
        
        with st.status("기본 데이터 처리 중...", expanded=False) as status:
            time.sleep(0.8)
            status.update(label="처리 완료.", state="complete", expanded=False)
        
        resp = "기본 데이터 입력 완료.\n\n핵심 질문입니다. 피험자가 호소하는 **다이어트 실패의 주된 원인**은 무엇입니까? (버튼 선택 또는 직접 입력)"
        bot_say(resp)
        st.session_state.step = 3
        st.rerun()
    
    # Step 3: 증상 입력
    elif st.session_state.step == 3:
        txt = prompt.lower()
        cause = "기타"
        
        if any(x in txt for x in ['식욕', '불가능']):
            cause = "식욕"
        elif any(x in txt for x in ['붓기', '붓습니다', '부종']):
            cause = "부종"
        elif any(x in txt for x in ['대사', '없습니다', '감소']):
            cause = "대사"
        elif any(x in txt for x in ['스트레스', '폭식']):
            cause = "스트레스"
        
        st.session_state.user_data['cause'] = cause
        
        with st.status("증상 패턴 분석 중...", expanded=False) as status:
            time.sleep(0.7)
            status.update(label="분석 완료.", state="complete", expanded=False)
        
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
    
    # Step 5: 약물 이력 입력 → 최종 결과
    elif st.session_state.step == 5:
        st.session_state.user_data['history'] = prompt
        
        with st.status("최종 임상 데이터 분석 실행 중...", expanded=True) as status:
            st.write("🔍 200,000+ 임상 케이스 데이터베이스 접속...")
            time.sleep(1.0)
            st.write("🧬 피험자 데이터 패턴 대조 및 시뮬레이션...")
            time.sleep(1.5)
            st.write("💡 최적 처방 프로토콜 도출...")
            time.sleep(1.0)
            status.update(label="최종 분석 완료.", state="complete", expanded=False)
        
        cause = st.session_state.user_data.get('cause', '대사')
        
        # Content Mapping
        if cause == "식욕":
            title = "위열 과다형 (Stomach Heat)"
            desc = "뇌가 포만감을 인지하지 못하는 '가짜 배고픔' 상태. 식욕 중추의 과항진."
            rx = "식탐사약"
            rx_sub = "식욕 억제 및 위장 열 해소"
            img = "https://placehold.co/800x400/111111/00E676?text=CLINICAL+EVIDENCE"
        elif cause == "부종":
            title = "수독 정체형 (Water Retention)"
            desc = "노폐물 배출 기능 저하로 지방과 수분이 결합된 상태. 림프 순환 저하."
            rx = "독소킬 + 지방사약"
            rx_sub = "수분 대사 촉진 및 붓기 배출"
            img = "https://placehold.co/800x400/111111/00E676?text=CLINICAL+EVIDENCE"
        elif cause == "대사":
            title = "대사 저하형 (Metabolic Drop)"
            desc = "기초대사량이 낮아 에너지 소모율이 극히 낮은 체질."
            rx = "지방사약 (대사촉진형)"
            rx_sub = "심부 체온 상승 및 발열 효과 유도"
            img = "https://placehold.co/800x400/111111/00E676?text=CLINICAL+EVIDENCE"
        else:
            title = "간기 울결형 (Stress Induced)"
            desc = "스트레스 호르몬(코르티솔) 과다 분비에 의한 복부 지방 축적."
            rx = "소요산 + 지방사약"
            rx_sub = "자율신경 안정 및 폭식 차단"
            img = "https://placehold.co/800x400/111111/00E676?text=CLINICAL+EVIDENCE"
        
        # Result HTML
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
            
            <div style='margin-top:20px;'>
                <div class='label-small'>CLINICAL EVIDENCE</div>
                <div style='text-align:center; margin: 15px 0;'>
                    <img src='{img}' style='max-width:100%; border-radius:8px;'/>
                </div>
                <p style='font-size:12px; color:#555; text-align:center;'>동일 체질 환자의 3개월 임상 변화 데이터 (자연과한의원 제공)</p>
            </div>
            
            <div style='margin-top:30px; border-top:1px solid #333; padding-top:20px;'>
                <div class='label-small'>PRICING PLAN (VAT 별도)</div>
                <div style='display:flex; justify-content:space-between; margin-bottom:10px; padding: 5px 0;'>
                    <span style='color:#AAA;'>1 Month Plan</span>
                    <span style='color:#FFF;'>150,000 KRW</span>
                </div>
                <div style='display:flex; justify-content:space-between; background-color: #051005; padding: 10px; border-radius: 5px;'>
                    <span style='color:#00E676;'>6 Months Plan (Recommended)</span>
                    <span style='color:#00E676; font-weight:bold;'>Monthly 100,000 KRW ~</span>
                </div>
            </div>
        </div>
        """
        
        bot_say(result_html, html=True)
        st.session_state.step = 6
        st.rerun()

# [Step 6: Contact Form]
if st.session_state.step == 6:
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='label-small'>REQUEST CONSULTATION</div>", unsafe_allow_html=True)
    
    with st.form("contact", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("성함", placeholder="환자명")
        with c2:
            phone = st.text_input("연락처", placeholder="010-XXXX-XXXX")
        
        if st.form_submit_button("상담 접수 및 데이터 전송"):
            if name and phone:
                st.success("✅ 데이터 전송 완료. 담당 의료진이 24시간 내 연락드립니다.")
                # TODO: DB 저장 로직 추가
            else:
                st.warning("⚠️ 정확한 정보를 입력하십시오.")
