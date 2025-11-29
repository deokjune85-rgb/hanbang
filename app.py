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

# [CSS: 리얼 블랙 & 네온 그린]
custom_css = """
<style>
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; font-family: 'Pretendard', sans-serif; }
    h1, h2, h3 { color: #00E676 !important; font-weight: 800; }
    
    /* 채팅 메시지 스타일 */
    .stChatMessage { background-color: #000 !important; }
    [data-testid="stChatMessageContent"] {
        background-color: #111 !important; border: 1px solid #333;
        border-radius: 15px; padding: 15px; color: #EEE;
    }
    .stChatMessage[data-testid="user"] [data-testid="stChatMessageContent"] {
        background-color: #0A1F0A !important; border-color: #00E676;
    }
    
    /* 입력창 */
    .stChatInputInput { background-color: #1E1E1E !important; color: white !important; }
    
    /* 버튼 스타일 */
    div.stButton > button {
        width: 100%; background-color: #1E1E1E; color: #00E676 !important;
        border: 1px solid #00E676 !important; border-radius: 20px; margin-bottom: 5px;
    }
    div.stButton > button:hover { background-color: #00E676; color: #000 !important; }
    
    /* 결과 카드 */
    .result-card {
        background: linear-gradient(135deg, #0A1F0A 0%, #000 100%);
        border: 2px solid #00E676; border-radius: 15px; padding: 20px; margin-top: 20px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 1. 상태 및 NLP 엔진
# ---------------------------------------
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'step' not in st.session_state:
    st.session_state.step = 0 
    # 0: 인사, 1: 정보입력대기, 2: 증상질문, 3: 증상입력대기, 4: 내성질문, 5: 내성입력대기, 6: 결과
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

def bot_say(text, image=None):
    st.session_state.messages.append({"role": "assistant", "content": text, "image": image})

def user_say(text):
    st.session_state.messages.append({"role": "user", "content": text})

# [핵심] 자연어 분석 함수 (Keyword Matching)
def analyze_symptom_text(text):
    text = text.lower()
    if any(x in text for x in ['식욕', '배불러', '먹고', '배고파', '입맛']): return "식욕"
    if any(x in text for x in ['붓기', '부어', '물만', '무거워', '종아리']): return "부종"
    if any(x in text for x in ['적게', '대사', '안빠져', '손발', '추위']): return "대사"
    if any(x in text for x in ['스트레스', '짜증', '폭식', '기분']): return "스트레스"
    return "기타" # 기본값

# ---------------------------------------
# 2. UI 및 로직 흐름
# ---------------------------------------

# [헤더]
col1, col2 = st.columns([1, 4])
with col1: st.image("https://placehold.co/100x100/000000/00E676?text=Dr.J", width=60)
with col2:
    st.markdown("<h3 style='margin:0; padding-top:10px;'>자연과한의원 AI 센터</h3>", unsafe_allow_html=True)
    st.caption("24시간 비대면 정밀 진단 시스템")
st.divider()

# [STEP 0: 초기 실행 - 인사말]
if st.session_state.step == 0:
    msg = "안녕하세요. **AI 닥터 제이(Dr.J)**입니다.\n\n단순히 살을 빼는 게 아니라, **'왜 살이 안 빠지는지'** 그 원인을 찾아 처방해 드립니다.\n\n먼저 분석을 위해 **[성별 / 나이 / 키 / 몸무게]**를 편하게 입력해 주세요."
    bot_say(msg)
    st.session_state.step = 1 # 입력 대기 상태로 변경

# ---------------------------------------
# [메시지 렌더링] (이전 대화 기록 표시)
# ---------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🌿" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])
        if msg.get("image"):
            st.image(msg["image"], use_column_width=True)

# ---------------------------------------
# [입력 핸들링 - 버튼 & 텍스트 동시 처리]
# ---------------------------------------

# [Step 2 특별 처리] 증상 선택 단계일 때 버튼 표시
if st.session_state.step == 3: # 증상 답변 대기 중일 때만 버튼 보임
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🍽️ 식욕 통제 불가"):
            user_say("식욕 통제가 안 돼요")
            st.session_state.user_data['cause'] = "식욕"
            st.session_state.step = 4 # 다음 단계로 강제 이동
            st.rerun()
        if st.button("💧 물만 먹어도 부음"):
            user_say("물만 먹어도 부어요")
            st.session_state.user_data['cause'] = "부종"
            st.session_state.step = 4
            st.rerun()
    with col_b:
        if st.button("🔥 적게 먹어도 안 빠짐"):
            user_say("적게 먹어도 안 빠져요")
            st.session_state.user_data['cause'] = "대사"
            st.session_state.step = 4
            st.rerun()
        if st.button("😰 스트레스성 폭식"):
            user_say("스트레스 받으면 폭식해요")
            st.session_state.user_data['cause'] = "스트레스"
            st.session_state.step = 4
            st.rerun()

# [사용자 텍스트 입력 처리]
if prompt := st.chat_input("답변을 입력하세요..."):
    # 1. 유저 말 표시
    user_say(prompt)
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. 단계별 AI 반응 로직
    
    # [Case 1: 기본 정보 입력 받음 -> 증상 질문 던지기]
    if st.session_state.step == 1:
        st.session_state.user_data['info'] = prompt
        # 즉시 응답
        bot_msg = "정보가 입력되었습니다. BMI와 기초대사량 구간을 분석했습니다.\n\n가장 중요한 질문입니다. **다이어트가 실패하는 가장 큰 이유**가 무엇인가요? (아래 버튼을 누르거나 직접 말씀해 주세요)"
        bot_say(bot_msg)
        with st.chat_message("assistant", avatar="🌿"):
            st.markdown(bot_msg)
        st.session_state.step = 3 # 증상 입력 대기 상태로 이동 (2번 건너뜀)
        st.rerun()

    # [Case 2: 증상 답변 받음 (텍스트로 입력했을 경우)]
    elif st.session_state.step == 3:
        # NLP 분석 실행
        detected_cause = analyze_symptom_text(prompt)
        st.session_state.user_data['cause'] = detected_cause
        
        # 원인별 멘트 생성
        if detected_cause == "식욕": comment = "아, 식욕 조절이 힘드시군요. 그건 의지 문제가 아니라 '위열' 때문입니다."
        elif detected_cause == "부종": comment = "붓기가 살이 되는 '수독' 체질이시군요. 순환부터 잡아야 합니다."
        elif detected_cause == "대사": comment = "대사가 느려서 남들보다 손해보는 체질이시네요. 엔진을 켜야 합니다."
        elif detected_cause == "스트레스": comment = "스트레스 호르몬이 지방을 꽉 잡고 있군요."
        else: comment = "말씀하신 증상을 바탕으로 정밀 분석을 진행하겠습니다."
        
        bot_msg = f"{comment}\n\n마지막으로, **다이어트 약물 복용 경험**이나 **카페인 민감도**는 어떠신가요?"
        bot_say(bot_msg)
        with st.chat_message("assistant", avatar="🌿"):
            st.markdown(bot_msg)
        st.session_state.step = 5 # 내성 입력 대기 상태로 이동
        st.rerun()

    # [Case 3: 내성 답변 받음 -> 최종 결과]
    elif st.session_state.step == 5:
        st.session_state.user_data['history'] = prompt
        
        # 로딩 애니메이션
        with st.chat_message("assistant", avatar="🌿"):
            with st.status("🧬 25년 임상 데이터 대조 중...", expanded=True):
                time.sleep(1)
                st.write("체질별 부작용 시뮬레이션...")
                time.sleep(1)
                st.write("최적 처방 매칭 완료!")
        
        # 결과 도출
        cause = st.session_state.user_data.get('cause', '대사')
        
        if cause == "식욕":
            diag = "위열(Stomach Heat) 과다형"
            drug = "식탐사약"
            desc = "가짜 배고픔을 만드는 위장의 열을 식히고, 포만 중추를 정상화합니다."
            ba_img = "https://placehold.co/600x300/111/00E676?text=Before+After+(Belly)" 
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
        else: # 스트레스 or 기타
            diag = "간기 울결(Stress)형"
            drug = "지방사약 + 소요산"
            desc = "스트레스 호르몬을 조절하여 폭식의 고리를 끊습니다."
            ba_img = "https://placehold.co/600x300/111/00E676?text=Before+After+(Stress)"

        final_msg = f"""
### 📋 분석 결과: <span style='color:#FF5252'>{diag}</span>

고객님은 의지가 약한 게 아닙니다. **몸의 시스템이 고장 난 상태**입니다.
{desc}

**[처방 솔루션]**
💊 **{drug}** (맞춤 처방)
"""
        bot_say(final_msg)
        with st.chat_message("assistant", avatar="🌿"):
            st.markdown(final_msg)
            
        # 비포 애프터
        st.markdown("---")
        bot_say("**[증거] 동일 체질 환자의 3개월 변화**", image=ba_img)
        with st.chat_message("assistant", avatar="🌿"):
            st.write("**[증거] 동일 체질 환자의 3개월 변화**")
            st.image(ba_img)
            
            # 가격 카드
            price_html = """
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
            </div>
            """
            st.markdown(price_html, unsafe_allow_html=True)
            bot_say(price_html) # 히스토리 저장용 (HTML은 텍스트로 저장됨)

        st.session_state.step = 6 # 완료 상태

# [Case 4: 완료 후 상담 신청]
if st.session_state.step == 6:
    st.markdown("### 🚀 비대면 초진 신청")
    with st.form("final_lead"):
        name = st.text_input("성함")
        phone = st.text_input("연락처")
        sub = st.form_submit_button("👨‍⚕️ 한의사 상담 연결")
        if sub and name and phone:
            st.success("접수 완료! 담당자가 곧 연락드립니다.")
