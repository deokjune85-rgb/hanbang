import streamlit as st
import time

# ---------------------------------------
# 0. 시스템 설정: Minimal Black Theme
# ---------------------------------------
st.set_page_config(
    page_title="자연과한의원 AI",
    page_icon="▫️",
    layout="centered"
)

# [CSS: Extreme Minimalism & Typography]
custom_css = """
<style>
    /* 1. Main Container & Font */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp {
        background-color: #000000 !important;
        color: #E0E0E0 !important;
        font-family: 'Pretendard', sans-serif;
    }

    /* 2. Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 3. Typography Rules */
    h1, h2, h3 { color: #FFFFFF !important; font-weight: 700; letter-spacing: -0.5px; }
    p, div { line-height: 1.6; color: #CCCCCC; }
    strong { color: #FFFFFF; font-weight: 600; }
    .accent { color: #00E676; } /* Jayeon Green */

    /* 4. Chat Message (Minimal Bubble) */
    .stChatMessage { background-color: #000 !important; padding: 10px 0 !important; }
    [data-testid="stChatMessageContent"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        color: #E0E0E0;
    }
    .stChatMessage[data-testid="user"] {
        flex-direction: row-reverse;
        text-align: right;
    }
    
    /* 5. Input Field (Sleek Line) */
    .stChatInputInput {
        background-color: #111 !important;
        border: 1px solid #333 !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* 6. Chip Buttons (Horizontal & Round) */
    div.stButton > button {
        background-color: #111;
        color: #AAA !important;
        border: 1px solid #333 !important;
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
    
    /* 7. Result Card (Editorial Design) */
    .diagnosis-card {
        border-top: 1px solid #333;
        border-bottom: 1px solid #333;
        padding: 30px 0;
        margin: 20px 0;
    }
    .label-small { font-size: 12px; color: #666; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 5px; }
    .diagnosis-title { font-size: 28px; color: #FFF; font-weight: 700; margin-bottom: 10px; }
    .diagnosis-desc { font-size: 15px; color: #AAA; margin-bottom: 20px; }
    
    /* 8. Pulse Animation (Thinking) */
    @keyframes pulse { 0% { opacity: 0.3; } 50% { opacity: 1; } 100% { opacity: 0.3; } }
    .thinking { color: #00E676; font-size: 12px; animation: pulse 1.5s infinite; letter-spacing: 1px; }

    /* 9. Grid Layout Fix for Chips */
    [data-testid="column"] { padding: 0 5px !important; }
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

def stream_text(text):
    """Gemini-like smooth streaming"""
    for char in text:
        yield char
        time.sleep(0.015)

def bot_say(content, image=None, html=False):
    st.session_state.messages.append({"role": "assistant", "content": content, "image": image, "html": html})

def user_say(content):
    st.session_state.messages.append({"role": "user", "content": content})

def thinking_simulation():
    """AI Thinking Effect"""
    placeholder = st.empty()
    placeholder.markdown("<span class='thinking'>ANALYZING DATA PATTERNS...</span>", unsafe_allow_html=True)
    time.sleep(1.2)
    placeholder.empty()

# ---------------------------------------
# 2. Main Interface
# ---------------------------------------

# [Header: Minimal Text Only]
st.markdown("<h3 style='margin-bottom:0;'>자연과한의원</h3>", unsafe_allow_html=True)
st.markdown("<p style='font-size:12px; color:#555;'>Clinical Data Analysis System v3.0</p>", unsafe_allow_html=True)
st.divider()

# [STEP 0: Init]
if st.session_state.step == 0:
    msg = "안녕하세요. AI 닥터 제이입니다.\n\n25년간 축적된 임상 데이터를 바탕으로 귀하의 **'체중 정체 원인'**을 분석합니다.\n\n먼저 **성별, 나이, 키, 체중**을 입력해 주세요."
    bot_say(msg)
    st.session_state.step = 1

# [Render Chat History]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("html"):
            st.markdown(msg["content"], unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], use_column_width=True)

# ---------------------------------------
# 3. Dynamic Interaction Area (Bottom)
# ---------------------------------------

# [Chip Buttons Area: Appears only when needed]
if st.session_state.step == 3:
    st.markdown("<p style='font-size:12px; color:#444; margin-bottom:10px;'>SUGGESTED INPUTS</p>", unsafe_allow_html=True)
    # 가로형 칩 배치 (Columns)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("식욕 조절"):
        st.session_state.temp_input = "식욕 조절이 안 돼요"
        st.rerun()
    if c2.button("붓기/부종"):
        st.session_state.temp_input = "몸이 자주 부어요"
        st.rerun()
    if c3.button("대사 저하"):
        st.session_state.temp_input = "적게 먹어도 안 빠져요"
        st.rerun()
    if c4.button("스트레스"):
        st.session_state.temp_input = "스트레스 받으면 폭식해요"
        st.rerun()

# [Input Handling]
if prompt := st.chat_input("증상이나 답변을 입력하세요...") or st.session_state.get('temp_input'):
    
    # Reset temp input
    if st.session_state.get('temp_input'):
        prompt = st.session_state.temp_input
        st.session_state.temp_input = None
    
    # 1. User Message
    user_say(prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Logic Controller
    if st.session_state.step == 1:
        st.session_state.user_data['info'] = prompt
        
        thinking_simulation() # Thinking...
        
        resp = "기본 데이터가 입력되었습니다.\n\n가장 핵심적인 질문입니다. **다이어트가 실패하는 주된 원인**은 무엇인가요?"
        with st.chat_message("assistant"):
            st.write_stream(stream_text(resp))
        bot_say(resp)
        st.session_state.step = 3 # Go to Chips Step
        st.rerun()

    elif st.session_state.step == 3:
        # Simple NLP
        txt = prompt.lower()
        cause = "기타"
        if any(x in txt for x in ['식욕', '배불러', '먹고']): cause = "식욕"
        elif any(x in txt for x in ['붓기', '부어', '물만']): cause = "부종"
        elif any(x in txt for x in ['적게', '대사', '안빠져']): cause = "대사"
        elif any(x in txt for x in ['스트레스', '폭식']): cause = "스트레스"
        
        st.session_state.user_data['cause'] = cause
        
        thinking_simulation()
        
        if cause == "식욕": msg = "식욕 통제 중추의 문제입니다. 위장의 열(Heat)을 식히는 것이 급선무입니다."
        elif cause == "부종": msg = "순환계 문제입니다. 림프가 막혀 수분이 지방과 결합된 상태입니다."
        elif cause == "대사": msg = "대사 효율 문제입니다. '엔진'이 꺼져 있어 에너지 소모가 안 되고 있습니다."
        else: msg = "자율신경 문제입니다. 스트레스 호르몬이 지방 분해를 차단하고 있습니다."
        
        full_msg = f"{msg}\n\n마지막으로, **다이어트 약물 복용 경험**이 있으신가요?"
        with st.chat_message("assistant"):
            st.write_stream(stream_text(full_msg))
        bot_say(full_msg)
        st.session_state.step = 5

    elif st.session_state.step == 5:
        st.session_state.user_data['history'] = prompt
        
        # Long Thinking
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("<span class='thinking'>COMPARING 200,000+ CLINICAL CASES...</span>", unsafe_allow_html=True)
            time.sleep(1.5)
            placeholder.markdown("<span class='thinking'>SIMULATING METABOLIC RESPONSE...</span>", unsafe_allow_html=True)
            time.sleep(1.5)
            placeholder.empty()

            # Result Generation
            cause = st.session_state.user_data.get('cause', '대사')
            
            # Content Mapping
            if cause == "식욕":
                title = "위열 과다형 (Stomach Heat)"
                desc = "뇌가 포만감을 느끼지 못하는 '가짜 배고픔' 상태"
                rx = "식탐사약"
                rx_sub = "식욕 억제 및 위장 열 해소"
                img = "https://placehold.co/800x400/111/333?text=BEFORE+vs+AFTER" 
            elif cause == "부종":
                title = "수독 정체형 (Water Retention)"
                desc = "노폐물이 배출되지 못하고 지방과 엉겨 붙은 상태"
                rx = "독소킬 + 지방사약"
                rx_sub = "수분 대사 촉진 및 붓기 배출"
                img = "https://placehold.co/800x400/111/333?text=BEFORE+vs+AFTER"
            elif cause == "대사":
                title = "대사 저하형 (Metabolic Drop)"
                desc = "기초대사량이 낮아 숨만 쉬어도 손해보는 체질"
                rx = "지방사약 (대사촉진형)"
                rx_sub = "심부 체온 상승 및 발열 효과 유도"
                img = "https://placehold.co/800x400/111/333?text=BEFORE+vs+AFTER"
            else:
                title = "간기 울결형 (Stress Induced)"
                desc = "스트레스 호르몬(코르티솔)에 의한 복부 지방 축적"
                rx = "소요산 + 지방사약"
                rx_sub = "자율신경 안정 및 폭식 차단"
                img = "https://placehold.co/800x400/111/333?text=BEFORE+vs+AFTER"

            # Editorial Layout (HTML)
            result_html = f"""
            <div class='diagnosis-card'>
                <div class='label-small'>ANALYSIS RESULT</div>
                <div class='diagnosis-title'>{title}</div>
                <div class='diagnosis-desc'>{desc}</div>
                
                <div style='display:flex; justify-content:space-between; align-items:center; margin-top:30px;'>
                    <div>
                        <div class='label-small' style='color:#00E676;'>PRESCRIPTION</div>
                        <div style='font-size:20px; font-weight:bold; color:#FFF;'>{rx}</div>
                        <div style='font-size:13px; color:#888;'>Target: {rx_sub}</div>
                    </div>
                    <div style='text-align:right;'>
                         <div class='label-small'>PERIOD</div>
                         <div style='color:#FFF;'>3 Months</div>
                    </div>
                </div>
            </div>
            """
            
            # 1. Render Diagnosis
            st.markdown(result_html, unsafe_allow_html=True)
            bot_say(result_html, html=True)
            
            time.sleep(0.5)
            
            # 2. Render Evidence (Text + Image)
            st.markdown("<div class='label-small'>CLINICAL EVIDENCE</div>", unsafe_allow_html=True)
            st.image(img, use_column_width=True)
            st.caption("동일 체질 환자의 3개월 임상 변화 데이터")
            
            # 3. Pricing (Minimal List)
            price_html = """
            <div style='margin-top:30px; border-top:1px solid #333; padding-top:20px;'>
                <div class='label-small'>PRICING PLAN</div>
                <div style='display:flex; justify-content:space-between; margin-bottom:10px;'>
                    <span style='color:#AAA;'>1 Month Plan</span>
                    <span style='color:#FFF;'>150,000 KRW</span>
                </div>
                <div style='display:flex; justify-content:space-between;'>
                    <span style='color:#00E676;'>6 Months Plan (Best)</span>
                    <span style='color:#00E676; font-weight:bold;'>Monthly 100,000 KRW ~</span>
                </div>
            </div>
            """
            st.markdown(price_html, unsafe_allow_html=True)
            
            # Save history
            bot_say(price_html, image=img, html=True)
            
            st.session_state.step = 6

# [Final Step: Simple Input]
if st.session_state.step == 6:
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    with st.form("contact"):
        c1, c2 = st.columns(2)
        with c1: name = st.text_input("NAME", placeholder="성함")
        with c2: phone = st.text_input("CONTACT", placeholder="연락처")
        
        if st.form_submit_button("REQUEST CONSULTATION"):
            if name and phone:
                st.success("접수되었습니다. 담당자가 곧 연락드립니다.")
