import streamlit as st
import time
import random

# ---------------------------------------
# 0. 시스템 설정: Dark & Neon Green Theme
# ---------------------------------------
st.set_page_config(
    page_title="자연과한의원 AI - Dr.J",
    page_icon="🌿",
    layout="centered"
)

# [CSS: 채팅창 스타일링 & 리얼 블랙 테마]
custom_css = """
<style>
    /* 1. 기본 테마 */
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 2. 헤더 */
    h1, h2, h3 { color: #00E676 !important; font-weight: 800; }
    
    /* 3. 채팅 메시지 스타일 */
    .stChatMessage { background-color: #000 !important; }
    [data-testid="stChatMessageContent"] {
        background-color: #111 !important;
        border: 1px solid #333;
        border-radius: 15px;
        padding: 15px;
        color: #EEE;
    }
    /* 유저 메시지는 색상 다르게 */
    .stChatMessage[data-testid="user"] [data-testid="stChatMessageContent"] {
        background-color: #0A1F0A !important;
        border-color: #00E676;
    }

    /* 4. 입력창 스타일 */
    .stChatInputInput {
        background-color: #1E1E1E !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    
    /* 5. 버튼 (선택지용) */
    div.stButton > button {
        width: 100%;
        background-color: #1E1E1E;
        color: #00E676 !important;
        border: 1px solid #00E676 !important;
        border-radius: 20px;
        margin-bottom: 5px;
    }
    div.stButton > button:hover {
        background-color: #00E676;
        color: #000 !important;
    }

    /* 6. 결과 카드 (Diagnosis Card) */
    .result-card {
        background: linear-gradient(135deg, #0A1F0A 0%, #000 100%);
        border: 2px solid #00E676;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 0 15px rgba(0, 230, 118, 0.2);
    }
    
    /* 7. 비포애프터 라벨 */
    .ba-label {
        background-color: #00E676;
        color: #000;
        font-weight: bold;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 1. 상태 관리 & 헬퍼 함수
# ---------------------------------------
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'step' not in st.session_state:
    st.session_state.step = 0 # 0:인사, 1:기본정보, 2:증상, 3:내성, 4:결과
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

def type_text(text):
    """텍스트가 타이핑되는 듯한 효과 (Streaming)"""
    for char in text:
        yield char
        time.sleep(0.01) # 타이핑 속도 조절

def bot_say(text, image_url=None):
    """봇 메시지 추가"""
    st.session_state.messages.append({"role": "assistant", "content": text, "image": image_url})

def user_say(text):
    """유저 메시지 추가"""
    st.session_state.messages.append({"role": "user", "content": text})

# ---------------------------------------
# 2. 메인 로직 (State Machine)
# ---------------------------------------

# [헤더: 권위 증명]
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://placehold.co/100x100/000000/00E676?text=Dr.J", width=60)
with col2:
    st.markdown("<h3 style='margin:0; padding-top:10px;'>자연과한의원 AI 센터</h3>", unsafe_allow_html=True)
    st.caption("SINCE 2001 · 2억 봉 판매 · 특허 3종 보유")
st.divider()

# [STEP 0: 초기 진입 & 인사]
if st.session_state.step == 0:
    welcome_msg = "안녕하세요. 저는 25년 임상 데이터를 학습한 **AI 닥터 제이(Dr.J)**입니다.\n\n단순히 살을 빼는 게 아니라, **'왜 살이 안 빠지는지'** 그 원인을 찾아 처방해 드립니다.\n\n먼저 분석을 위해 **[성별 / 나이 / 키 / 몸무게]**를 입력해 주세요.\n(예: 여성 32세 160cm 65kg)"
    bot_say(welcome_msg)
    st.session_state.step = 1

# [채팅 히스토리 렌더링]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🌿" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], use_column_width=True)

# [입력 처리 핸들러]
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 1. 유저 메시지 표시
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    user_say(prompt)

    # 2. 봇 응답 로직 (Step별 분기)
    
    # [STEP 1: 기본 정보 수집 -> 증상 질문]
    if st.session_state.step == 1:
        st.session_state.user_data['basic_info'] = prompt
        
        with st.chat_message("assistant", avatar="🌿"):
            response = "정보가 입력되었습니다. BMI와 기초대사량 구간을 계산했습니다.\n\n가장 중요한 질문입니다. **다이어트가 실패하는 가장 큰 이유**가 무엇인가요? 솔직하게 말씀해 주세요."
            st.write_stream(type_text(response))
        bot_say(response)
        
        # 버튼으로 선택지 제공 (입력 편의성)
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🍽️ 배불러도 계속 먹어요 (식욕)"):
                st.session_state.user_data['cause'] = "식욕"
                st.session_state.step = 2
                st.rerun()
            if st.button("💧 물만 먹어도 부어요 (부종)"):
                st.session_state.user_data['cause'] = "부종"
                st.session_state.step = 2
                st.rerun()
        with col_b:
            if st.button("🔥 적게 먹어도 안 빠져요 (대사)"):
                st.session_state.user_data['cause'] = "대사"
                st.session_state.step = 2
                st.rerun()
            if st.button("😰 스트레스 받으면 폭식해요"):
                st.session_state.user_data['cause'] = "스트레스"
                st.session_state.step = 2
                st.rerun()
    
    # [STEP 2: 내성 체크]
    elif st.session_state.step == 2:
        # (버튼 클릭으로 넘어오므로 이 블록은 텍스트 입력 시엔 스킵되거나 처리됨)
        pass 

# [STEP 2 처리: 버튼 클릭 후 자동 실행]
if st.session_state.step == 2 and 'cause' in st.session_state.user_data:
    # 봇이 자동으로 질문을 던짐
    if len(st.session_state.messages) % 2 == 0: # 봇 차례일 때만
        with st.chat_message("assistant", avatar="🌿"):
            cause = st.session_state.user_data['cause']
            if cause == "식욕": msg = "식욕 통제가 안 되시는군요. '위열(위장의 열)'이 원인일 가능성이 높습니다."
            elif cause == "부종": msg = "순환이 막혀 노폐물이 쌓인 '수독' 상태가 의심됩니다."
            elif cause == "대사": msg = "대사 엔진이 꺼진 '냉체질'이시군요. 굶으면 더 안 빠집니다."
            else: msg = "스트레스 호르몬이 지방을 붙잡고 있는 상태입니다."
            
            full_msg = f"{msg}\n\n마지막으로, **다이어트 약물 복용 경험**이나 **카페인 민감도**는 어떠신가요?"
            st.write_stream(type_text(full_msg))
        bot_say(full_msg)
        st.session_state.step = 3

# [STEP 3: 최종 입력 -> 분석 시작]
if st.session_state.step == 3 and prompt:
    st.session_state.user_data['history'] = prompt
    
    # 분석 애니메이션
    with st.chat_message("assistant", avatar="🌿"):
        with st.status("🧬 AI가 고객님의 체질을 분석 중입니다...", expanded=True) as status:
            st.write("데이터 대조 중 (2억 건)...")
            time.sleep(1)
            st.write("부작용 리스크 시뮬레이션 중...")
            time.sleep(1)
            st.write("최적 처방 매칭 완료!")
            status.update(label="분석 완료", state="complete", expanded=False)
        
        # [결과 생성 로직]
        cause = st.session_state.user_data.get('cause', '대사')
        
        if cause == "식욕":
            diag = "위열(Stomach Heat) 과다형"
            drug = "식탐사약"
            desc = "가짜 배고픔을 만드는 위장의 열을 식히고, 포만 중추를 정상화합니다."
            ba_img = "https://placehold.co/600x300/111/00E676?text=Before+After+(Belly)" # 실제 이미지 교체
        elif cause == "부종":
            diag = "수독(Water Poison) 정체형"
            drug = "독소킬 + 지방사약"
            desc = "꽉 막힌 림프를 뚫어 붓기를 배출하고, 라인을 잡습니다."
            ba_img = "https://placehold.co/600x300/111/00E676?text=Before+After+(Legs)"
        elif cause == "대사":
            diag = "대사 기능 저하형"
            drug = "지방사약 (대사촉진형)"
            desc = "심부 체온을 높여 숨만 쉬어도 에너지가 타는 몸을 만듭니다."
            ba_img = "https://placehold.co/600x300/111/00E676?text=Before+After+(FullBody)"
        else:
            diag = "간기 울결(Stress)형"
            drug = "지방사약 + 소요산"
            desc = "스트레스 호르몬을 조절하여 폭식의 고리를 끊습니다."
            ba_img = "https://placehold.co/600x300/111/00E676?text=Before+After+(Stress)"
            
        result_msg = f"""
        ### 📋 분석 결과: <span style='color:#FF5252'>{diag}</span>
        
        고객님은 의지가 약한 게 아닙니다. **몸의 시스템이 고장 난 상태**입니다.
        {desc}
        
        **[처방 솔루션]**
        💊 **{drug}** (맞춤 처방)
        """
        st.markdown(result_msg, unsafe_allow_html=True)
        bot_say(result_msg) # 텍스트 저장
        
        # [비포 애프터 출력]
        st.markdown("---")
        st.markdown("**👁 [증거] 동일 체질 환자의 3개월 변화**")
        st.image(ba_img, caption="자연과한의원 실제 감량 사례", use_column_width=True)
        bot_say("**[증거] 동일 체질 환자의 3개월 변화**", image_url=ba_img) # 이미지 저장
        
        # [CTA 및 가격]
        price_msg = """
        <div class='result-card'>
            <h4 style='color:#00E676; margin:0;'>💰 합리적 비용 제안</h4>
            <p style='color:#DDD; font-size:0.9rem;'>자체 탕전 시스템으로 거품을 뺐습니다.</p>
            <table style='width:100%; color:white; text-align:center;'>
                <tr style='border-bottom:1px solid #333;'>
                    <td>1개월</td>
                    <td style='color:#FF5252; font-weight:bold;'>150,000원</td>
                </tr>
                <tr>
                    <td>6개월 (Best)</td>
                    <td style='color:#00E676; font-weight:bold;'>월 10만원대</td>
                </tr>
            </table>
            <br>
            <p style='text-align:center; margin:0;'>
                지금 신청하시면 <b>비대면 초진</b>이 가능합니다.<br>
                담당 한의사가 10분 내로 연락드립니다.
            </p>
        </div>
        """
        st.markdown(price_msg, unsafe_allow_html=True)
        
        # 상담 신청 폼
        with st.form("final_form"):
            name = st.text_input("성함")
            phone = st.text_input("연락처")
            submitted = st.form_submit_button("👨‍⚕️ 한의사 상담 신청 (무료)")
            if submitted and name and phone:
                st.success("접수되었습니다! 곧 연락드리겠습니다.")
        
    st.session_state.step = 4
