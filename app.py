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

# [CSS: 애니메이션 및 리얼 블랙 테마]
custom_css = """
<style>
    /* 1. 메인 테마 */
    .stApp { background-color: #000000 !important; color: #FFFFFF !important; font-family: 'Pretendard', sans-serif; }
    h1, h2, h3 { color: #00E676 !important; font-weight: 800; }
    
    /* 2. 채팅 메시지 스타일 & 애니메이션 */
    .stChatMessage { background-color: #000 !important; }
    
    /* 메시지 등장 애니메이션 (Fade In + Slide Up) */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translate3d(0, 20px, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }
    
    [data-testid="stChatMessageContent"] {
        background-color: #111 !important; 
        border: 1px solid #333;
        border-radius: 15px; 
        padding: 15px; 
        color: #EEE;
        animation: fadeInUp 0.5s ease-out; /* 애니메이션 적용 */
    }
    
    .stChatMessage[data-testid="user"] [data-testid="stChatMessageContent"] {
        background-color: #0A1F0A !important; 
        border-color: #00E676;
    }
    
    /* 3. 입력창 스타일 */
    .stChatInputInput { background-color: #1E1E1E !important; color: white !important; }
    
    /* 4. 버튼 스타일 */
    div.stButton > button {
        width: 100%; background-color: #1E1E1E; color: #00E676 !important;
        border: 1px solid #00E676 !important; border-radius: 20px; margin-bottom: 5px;
    }
    div.stButton > button:hover { background-color: #00E676; color: #000 !important; }
    
    /* 5. 생각하는 로딩 애니메이션 (Pulsing) */
    @keyframes pulse {
        0% { opacity: 0.5; }
        50% { opacity: 1; }
        100% { opacity: 0.5; }
    }
    .thinking-text {
        color: #00E676;
        font-style: italic;
        animation: pulse 1.5s infinite;
        font-size: 0.9rem;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 1. 상태 및 헬퍼 함수
# ---------------------------------------
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'step' not in st.session_state:
    st.session_state.step = 0 
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# [핵심] 제미나이 느낌의 스트리밍 생성기
def stream_data(text):
    """텍스트를 한 글자씩 쪼개서 제너레이터로 반환 (타이핑 효과)"""
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.04) # 타이핑 속도 (낮을수록 빠름)

def add_message(role, content, save=True):
    if save:
        st.session_state.messages.append({"role": role, "content": content})

# 자연어 분석 함수
def analyze_symptom_text(text):
    text = text.lower()
    if any(x in text for x in ['식욕', '배불러', '먹고', '배고파', '입맛', '못참']): return "식욕"
    if any(x in text for x in ['붓기', '부어', '물만', '무거워', '종아리']): return "부종"
    if any(x in text for x in ['적게', '대사', '안빠져', '손발', '추위']): return "대사"
    if any(x in text for x in ['스트레스', '짜증', '폭식', '기분', '우울']): return "스트레스"
    return "기타" 

# ---------------------------------------
# 2. UI 및 로직 흐름
# ---------------------------------------

# [헤더]
col1, col2 = st.columns([1, 4])
with col1: st.image("https://placehold.co/100x100/000000/00E676?text=Dr.J", width=60)
with col2:
    st.markdown("<h3 style='margin:0; padding-top:10px;'>자연과한의원 AI</h3>", unsafe_allow_html=True)
    st.caption("Neural Diagnosis System v2.4")
st.divider()

# [STEP 0: 초기 인사 (한 번만 실행)]
if st.session_state.step == 0:
    welcome_text = "안녕하세요. **AI 닥터 제이(Dr.J)**입니다.\n\n단순히 살을 빼는 게 아니라, **'왜 살이 안 빠지는지'** 그 원인을 찾아 처방해 드립니다.\n\n먼저 분석을 위해 **[성별 / 나이 / 키 / 몸무게]**를 입력해 주세요."
    st.session_state.messages.append({"role": "assistant", "content": welcome_text})
    st.session_state.step = 1

# ---------------------------------------
# [메시지 렌더링 (히스토리)]
# ---------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🌿" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"], unsafe_allow_html=True)

# ---------------------------------------
# [입력 핸들링 (Main Loop)]
# ---------------------------------------

# [Step 3 증상 선택 버튼]
if st.session_state.step == 3:
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🍽️ 식욕 통제 불가"):
            prompt = "식욕 통제가 안 돼요" # 버튼 눌러도 텍스트 입력처럼 처리
            # 버튼 클릭 시 즉시 처리가 안 되므로, session_state에 임시 저장 후 rerun 패턴 사용
            st.session_state.temp_input = prompt
            st.rerun()
        if st.button("💧 물만 먹어도 부음"):
            st.session_state.temp_input = "물만 먹어도 부어요"
            st.rerun()
    with col_b:
        if st.button("🔥 적게 먹어도 안 빠짐"):
            st.session_state.temp_input = "적게 먹어도 안 빠져요"
            st.rerun()
        if st.button("😰 스트레스성 폭식"):
            st.session_state.temp_input = "스트레스 받으면 폭식해요"
            st.rerun()

# [입력 감지: 텍스트 입력창 OR 버튼 클릭으로 인한 임시 값]
if prompt := st.chat_input("답변을 입력하세요...") or st.session_state.get('temp_input'):
    
    # 임시 값 초기화 (버튼 클릭 처리용)
    if st.session_state.get('temp_input'):
        prompt = st.session_state.temp_input
        st.session_state.temp_input = None
        
    # 1. 유저 메시지 즉시 표시 (저장)
    add_message("user", prompt)
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2. AI "생각하는 척" 연출 (Thinking Phase)
    with st.chat_message("assistant", avatar="🌿"):
        placeholder = st.empty()
        with placeholder.container():
             st.markdown("<div class='thinking-text'>AI가 분석 중입니다...</div>", unsafe_allow_html=True)
             time.sleep(1.2) # 일부러 1.2초 딜레이 (생각하는 느낌)

        # 3. 로직 처리 및 스트리밍 답변
        response_text = ""
        
        # [Case 1: 기본 정보 입력 받음 -> 증상 질문]
        if st.session_state.step == 1:
            st.session_state.user_data['info'] = prompt
            response_text = "정보가 입력되었습니다. BMI와 기초대사량 구간 분석을 완료했습니다.\n\n가장 중요한 질문입니다. **다이어트가 실패하는 가장 큰 이유**가 무엇인가요? 솔직하게 말씀해 주세요."
            
            # 스트리밍 출력
            placeholder.empty() # Thinking 텍스트 지움
            st.write_stream(stream_data(response_text)) # 타다닥 효과
            
            add_message("assistant", response_text) # 히스토리 저장
            st.session_state.step = 3
            st.rerun() # 버튼 표시 위해 리런

        # [Case 2: 증상 답변 받음]
        elif st.session_state.step == 3:
            detected_cause = analyze_symptom_text(prompt)
            st.session_state.user_data['cause'] = detected_cause
            
            if detected_cause == "식욕": comment = "식욕 조절이 힘드시군요. 의지 문제가 아니라 '위열' 때문입니다."
            elif detected_cause == "부종": comment = "붓기가 살이 되는 '수독' 체질이시군요. 순환부터 잡아야 합니다."
            elif detected_cause == "대사": comment = "대사가 느려서 남들보다 손해 보는 체질이시네요. 엔진을 켜야 합니다."
            else: comment = "스트레스 호르몬이 지방을 꽉 잡고 있군요."
            
            response_text = f"{comment}\n\n마지막으로, **다이어트 약물 복용 경험**이나 **카페인 민감도**는 어떠신가요?"
            
            placeholder.empty()
            st.write_stream(stream_data(response_text))
            
            add_message("assistant", response_text)
            st.session_state.step = 5
            # 내성 입력은 버튼 없이 텍스트로만 받음 (자연스럽게)

        # [Case 3: 최종 결과 출력 (HTML 카드 + 스트리밍)]
        elif st.session_state.step == 5:
            st.session_state.user_data['history'] = prompt
            
            # 여기서 한 번 더 Thinking... (길게)
            placeholder.markdown("<div class='thinking-text'>25년 임상 데이터 대조 중 (2억 건)...<br>부작용 시뮬레이션 실행 중...</div>", unsafe_allow_html=True)
            time.sleep(2.0)
            
            # 결과 내용 생성
            cause = st.session_state.user_data.get('cause', '대사')
            
            if cause == "식욕":
                diag_title = "위열(Stomach Heat) 과다형"
                sub_desc = "가짜 배고픔 / 포만 중추 마비"
                reasoning = "위장에 과도한 열이 쌓여, 뇌가 배부름을 인지하지 못하는 상태입니다."
                drug_name = "식탐사약"
                drug_desc = "위장의 열을 내리고 식욕 억제 호르몬 활성화"
                ba_img = "https://placehold.co/600x300/111/00E676?text=Before+After+(Belly)" 
            elif cause == "부종":
                diag_title = "수독(Water Poison) 정체형"
                sub_desc = "림프 순환 장애 / 만성 부종"
                reasoning = "체내 수분 대사가 고장 나, 노폐물이 지방과 엉겨 붙은 상태입니다."
                drug_name = "독소킬 + 지방사약"
                drug_desc = "수분 길을 열어 부종 배출 및 라인 정리"
                ba_img = "https://placehold.co/600x300/111/00E676?text=Before+After+(Legs)"
            elif cause == "대사":
                diag_title = "대사 기능 저하형 (Cold Body)"
                sub_desc = "기초대사량 부족 / 수족냉증"
                reasoning = "엔진이 꺼진 차와 같습니다. 남들과 똑같이 먹어도 고객님만 살이 찝니다."
                drug_name = "지방사약 (대사촉진형)"
                drug_desc = "심부 체온을 높여 숨만 쉬어도 칼로리 소모 유도"
                ba_img = "https://placehold.co/600x300/111/00E676?text=Before+After+(Body)"
            else:
                diag_title = "간기 울결형 (Stress Induced)"
                sub_desc = "코르티솔 과다 / 감정적 폭식"
                reasoning = "스트레스 호르몬(코르티솔)이 뱃살을 붙잡고 있습니다. 굶으면 폭식합니다."
                drug_name = "지방사약 + 소요산"
                drug_desc = "자율신경을 안정시켜 폭식 충동을 원천 차단"
                ba_img = "https://placehold.co/600x300/111/00E676?text=Before+After+(Stress)"

            # 결과 카드 HTML (스트리밍 하지 않고, Thinking 끝난 후 '짠' 하고 등장)
            result_html = f"""
            <div style="background-color: #0A1F0A; border: 1px solid #00E676; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                <div style="color: #00E676; font-size: 0.9rem; font-weight: bold; margin-bottom: 5px;">DIAGNOSIS REPORT</div>
                <h3 style="color: #fff; margin: 0 0 5px 0;">{diag_title}</h3>
                <div style="color: #FF5252; font-size: 0.9rem; margin-bottom: 15px;">⚠️ {sub_desc}</div>
                <hr style="border-color: #333; margin-bottom: 15px;">
                <p style="color: #ddd; font-size: 0.95rem; line-height: 1.5;">
                    <b>"의지가 약한 게 아닙니다."</b><br>
                    {reasoning}
                </p>
                <div style="background-color: #1E1E1E; border-left: 4px solid #00E676; padding: 15px; margin-top: 15px;">
                    <div style="color: #888; font-size: 0.8rem;">FINAL PRESCRIPTION</div>
                    <div style="color: #00E676; font-size: 1.2rem; font-weight: bold;">💊 {drug_name}</div>
                    <div style="color: #fff; font-size: 0.9rem; margin-top: 5px;">: {drug_desc}</div>
                </div>
            </div>
            """
            
            placeholder.empty() # Thinking 제거
            st.markdown(result_html, unsafe_allow_html=True) # 리포트 표시
            add_message("assistant", result_html)
            
            # 비포 애프터 & 가격
            time.sleep(0.5)
            st.write("**👁 [증거] 동일 체질 환자의 3개월 변화**")
            st.image(ba_img, use_column_width=True)
            
            price_html = """
            <div style="background: linear-gradient(135deg, #111 0%, #000 100%); border: 1px solid #333; border-radius: 10px; padding: 15px; margin-top: 15px;">
                <h4 style='color:#00E676; margin:0; font-size:1rem;'>💰 합리적 비용 제안</h4>
                <table style='width:100%; color:white; text-align:center; margin-top:10px;'>
                    <tr style='border-bottom:1px solid #333;'>
                        <td style='padding:8px; color:#aaa;'>1개월</td>
                        <td style='color:#FF5252; font-weight:bold;'>150,000원</td>
                    </tr>
                    <tr>
                        <td style='padding:8px; color:#fff;'>6개월 (Best)</td>
                        <td style='color:#00E676; font-weight:bold;'>월 10만원대</td>
                    </tr>
                </table>
            </div>
            """
            st.markdown(price_html, unsafe_allow_html=True)
            add_message("assistant", price_html) # 히스토리 저장
            
            st.session_state.step = 6

# [Case 4: 완료 후 상담 신청]
if st.session_state.step == 6:
    st.markdown("### 🚀 비대면 초진 신청")
    with st.form("final_lead"):
        name = st.text_input("성함")
        phone = st.text_input("연락처")
        sub = st.form_submit_button("👨‍⚕️ 한의사 상담 연결")
        if sub and name and phone:
            st.success("접수 완료! 담당자가 곧 연락드립니다.")
