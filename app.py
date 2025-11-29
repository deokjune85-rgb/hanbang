import streamlit as st

st.set_page_config(
    page_title="자연과한의원 - 비대면 정밀 처방",
    page_icon="🌿",
    layout="centered"
)

# 최소한의 CSS (HTML 마크다운 최소화)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    .stApp { background-color: #000; font-family: 'Noto Sans KR', sans-serif; }
    div.stButton > button { 
        width: 100%; background-color: #00E676 !important; 
        color: #000 !important; border: none !important; 
        padding: 14px !important; font-weight: 900 !important; 
        font-size: 1rem !important; border-radius: 25px !important;
    }
    div.stButton > button:hover { background-color: #00C853 !important; }
    div.stButton > button p { color: #000 !important; font-weight: 900 !important; }
    .stRadio > div { gap: 8px; }
    .stRadio label { 
        background: #111 !important; border: 1px solid #333 !important; 
        border-radius: 10px !important; padding: 12px 15px !important; 
        margin: 5px 0 !important;
    }
    .stRadio label:hover { border-color: #00E676 !important; }
    .stFormSubmitButton > button { 
        background-color: #00E676 !important; color: #000 !important; 
        font-weight: 900 !important; border-radius: 25px !important;
    }
    .stFormSubmitButton > button p { color: #000 !important; }
</style>
""", unsafe_allow_html=True)

# 상태 관리
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def add_bot_message(msg):
    st.session_state.chat_history.append({"role": "bot", "content": msg})

def add_user_message(msg):
    st.session_state.chat_history.append({"role": "user", "content": msg})

def render_chat_history():
    """채팅 히스토리 렌더링 (에러 방지: 순수 st 컴포넌트만 사용)"""
    for chat in st.session_state.chat_history:
        if chat["role"] == "bot":
            with st.chat_message("assistant", avatar="🌿"):
                st.write(chat["content"])
        else:
            with st.chat_message("user", avatar="👤"):
                st.write(chat["content"])

# ============================================
# STEP 0: 인트로 (짧게) + 바로 문진 시작
# ============================================
if st.session_state.step == 0:
    st.title("🌿 자연과한의원")
    st.caption("비대면 정밀 처방 시스템")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("연구기간", "25년+")
    with col2:
        st.metric("누적판매", "2억 봉")
    with col3:
        st.metric("특허", "3종")
    
    st.divider()
    
    # 챗봇 시작
    with st.chat_message("assistant", avatar="🌿"):
        st.write("안녕하세요! 자연과한의원 AI 처방 어시스턴트입니다.")
        st.write("25년간 축적된 데이터를 바탕으로 **나에게 딱 맞는 처방**을 찾아드릴게요.")
        st.write("몇 가지 질문에 답해주시면, 왜 살이 안 빠졌는지 원인을 분석하고 맞춤 솔루션을 제안해 드립니다.")
    
    if st.button("💬 맞춤 처방 상담 시작하기"):
        add_bot_message("좋아요! 먼저 기본 정보를 알려주세요.")
        st.session_state.step = 1
        st.rerun()

# ============================================
# STEP 1: 기본 정보 (챗봇 스타일)
# ============================================
elif st.session_state.step == 1:
    st.title("🌿 자연과한의원")
    
    render_chat_history()
    
    with st.chat_message("assistant", avatar="🌿"):
        st.write("**Q1. 기본 정보를 입력해 주세요**")
        
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("성별", ["여성", "남성"], key="gender")
            height = st.number_input("신장 (cm)", 140, 200, 160, key="height")
        with col2:
            age = st.number_input("나이", 18, 70, 30, key="age")
            weight = st.number_input("체중 (kg)", 40, 150, 65, key="weight")
    
    if st.button("다음 →"):
        user_info = f"{gender}, {age}세, {height}cm, {weight}kg"
        add_user_message(user_info)
        add_bot_message("감사합니다! 이제 가장 중요한 질문이에요.")
        st.session_state.user_data.update({
            'gender': gender, 'age': age, 'height': height, 'weight': weight
        })
        st.session_state.step = 2
        st.rerun()

# ============================================
# STEP 2: 비만 원인 (핵심 질문)
# ============================================
elif st.session_state.step == 2:
    st.title("🌿 자연과한의원")
    
    render_chat_history()
    
    with st.chat_message("assistant", avatar="🌿"):
        st.write("**Q2. 다이어트가 실패하는 가장 큰 이유는?**")
        st.write("하나만 골라주세요. 이게 처방의 핵심이에요!")
        
        cause = st.radio(
            "선택",
            [
                "🍽️ 배불러도 계속 먹게 됨 (식욕 통제 불가)",
                "💧 물만 먹어도 붓고 무거움 (부종)",
                "🔥 적게 먹어도 안 빠짐 (대사 저하)",
                "😰 스트레스 받으면 폭식 (감정적 섭식)"
            ],
            key="cause",
            label_visibility="collapsed"
        )
    
    if st.button("다음 →"):
        add_user_message(cause)
        add_bot_message("마지막 질문이에요! 약물 반응성을 체크할게요.")
        st.session_state.user_data['cause'] = cause
        st.session_state.step = 3
        st.rerun()

# ============================================
# STEP 3: 약물 내성 체크
# ============================================
elif st.session_state.step == 3:
    st.title("🌿 자연과한의원")
    
    render_chat_history()
    
    with st.chat_message("assistant", avatar="🌿"):
        st.write("**Q3. 카페인(커피) 반응은?**")
        caffeine = st.radio(
            "카페인",
            ["☕ 하루 3잔 이상 OK", "☕ 1-2잔 적정", "💓 심장 두근, 예민함"],
            key="caffeine",
            label_visibility="collapsed"
        )
        
        st.write("**Q4. 다이어트 약 복용 경험은?**")
        history = st.radio(
            "복용경험",
            ["🆕 처음이에요", "📌 1-2회 있어요", "🔄 여러 번, 효과 미비 (내성 의심)"],
            key="history",
            label_visibility="collapsed"
        )
    
    if st.button("🔍 내 맞춤 처방 확인하기"):
        add_user_message(f"카페인: {caffeine} / 복용경험: {history}")
        st.session_state.user_data['caffeine'] = caffeine
        st.session_state.user_data['history'] = history
        st.session_state.step = 4
        st.rerun()

# ============================================
# STEP 4: 결과 (에러 방지: HTML 마크다운 제거, 순수 st 컴포넌트만)
# ============================================
elif st.session_state.step == 4:
    st.title("🌿 자연과한의원")
    
    data = st.session_state.user_data
    
    # 데이터 추출
    height = data.get('height', 160)
    weight = data.get('weight', 65)
    age = data.get('age', 30)
    gender = data.get('gender', '여성')
    cause = data.get('cause', '')
    caffeine = data.get('caffeine', '')
    history = data.get('history', '')
    
    # BMI 계산
    bmi = round(weight / ((height/100) ** 2), 1)
    
    # 원인별 분석
    if "식욕" in cause or "배불러도" in cause:
        diagnosis_type = "위열(胃熱) 과다형"
        diagnosis_name = "식욕 과항진 비만"
        emoji = "🍽️"
        
        problem_title = "가짜 배고픔에 속고 있어요"
        problem_detail = """위장에 과도한 열이 쌓여 있어요. 이 열기가 뇌의 포만 중추를 마비시켜서, 배가 불러도 '배고프다'는 잘못된 신호를 보내고 있어요. 의지력 문제가 아니에요!"""
        
        why_fail = "단순 절식은 위열을 더 자극해서 폭식→후회→절식의 악순환을 만들어요."
        
        solution_name = "청위사열(清胃瀉熱)"
        solution_steps = [
            "황련, 치자 등으로 위장의 열을 식힘",
            "포만 중추 민감도 회복",
            "식욕 호르몬(그렐린) 억제"
        ]
        expected = "3-5일 후 식욕 감소, 2주 후 폭식 욕구 현저히 감소"
        
    elif "물만" in cause or "붓" in cause:
        diagnosis_type = "수독(水毒) 정체형"
        diagnosis_name = "부종성 비만"
        emoji = "💧"
        
        problem_title = "지방이 아니라 붓기예요"
        problem_detail = """체내 수분 대사가 고장나서 노폐물이 빠져나가지 못하고 있어요. 림프 순환이 막혀 셀룰라이트가 축적되고, 실제 지방보다 붓기가 체중의 상당 부분을 차지해요."""
        
        why_fail = "운동과 식이조절은 지방엔 효과적이지만 수독 정체는 해결 못해요."
        
        solution_name = "이수삼습(利水滲濕)"
        solution_steps = [
            "복령, 택사로 정체된 수분 배출",
            "림프 순환 촉진으로 부종 제거",
            "비장 기능 강화로 재발 방지"
        ]
        expected = "1주일 내 붓기 감소, 2주 후 2-4kg 감량"
        
    elif "적게" in cause or "대사" in cause:
        diagnosis_type = "대사저하(冷體質)형"
        diagnosis_name = "기초대사량 저하 비만"
        emoji = "🔥"
        
        problem_title = "대사 엔진이 꺼져있어요"
        problem_detail = """기초대사량이 현저히 낮아서, 같은 양을 먹어도 남들보다 칼로리 소모가 적어요. 손발이 차고, 쉽게 피로하고, 추위를 많이 타시죠? 신진대사 자체가 슬로우 모드예요."""
        
        why_fail = "절식은 대사량을 더 떨어뜨려서 요요의 원인이 돼요."
        
        solution_name = "온양보기(溫陽補氣)"
        solution_steps = [
            "온열 약재로 심부 체온 0.3-0.5도 상승",
            "교감신경 자극으로 칼로리 소모 체질 전환",
            "갈색 지방(Brown Fat) 활성화"
        ]
        expected = "1주일 후 체온 상승 체감, 2주 후 체중 감소 시작"
        
    else:  # 스트레스
        diagnosis_type = "간기울결(肝氣鬱結)형"
        diagnosis_name = "스트레스성 폭식 비만"
        emoji = "😰"
        
        problem_title = "스트레스 호르몬이 지방을 붙잡고 있어요"
        problem_detail = """코르티솔(스트레스 호르몬)이 만성적으로 높아요. 스트레스→폭식→죄책감→스트레스 악순환에 갇혀 있고, 코르티솔은 특히 복부 지방 축적을 촉진해요."""
        
        why_fail = "의지력으로 억제하면 스트레스가 더 쌓여서 결국 더 큰 폭식으로 터져요."
        
        solution_name = "소간해울(疏肝解鬱)"
        solution_steps = [
            "시호, 향부자로 막힌 기 흐름 소통",
            "가미소요산으로 정서 안정",
            "스트레스 호르몬 분비 정상화"
        ]
        expected = "3-5일 후 심리적 안정, 2주 후 폭식 빈도 현저히 감소"
    
    # 처방 강도
    if "여러" in history or "내성" in history:
        rx_level = "MAX"
        rx_name = "지방사약 MAX"
        rx_reason = "기존 약물 내성 → 강화 처방 필요"
    elif "1-2회" in history:
        rx_level = "STANDARD+"
        rx_name = "지방사약 스탠다드+"
        rx_reason = "약간의 경험 → 표준보다 약간 강화"
    else:
        rx_level = "STANDARD"
        rx_name = "지방사약 스탠다드"
        rx_reason = "첫 복용 → 표준 용량부터 시작"
    
    # 카페인 주의
    caffeine_warning = "민감" in caffeine or "두근" in caffeine
    
    # ============================================
    # 결과 UI (순수 Streamlit 컴포넌트만 사용)
    # ============================================
    
    # 채팅 히스토리
    render_chat_history()
    
    # 결과 메시지
    with st.chat_message("assistant", avatar="🌿"):
        st.write("분석이 완료됐어요! 결과를 보여드릴게요.")
    
    st.divider()
    
    # 진단 결과
    st.subheader(f"{emoji} 진단: {diagnosis_type}")
    st.caption(diagnosis_name)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("BMI", bmi)
    with col2:
        st.metric("처방강도", rx_level)
    with col3:
        st.metric("추천", rx_name)
    
    st.divider()
    
    # 문제 분석
    st.subheader("❓ 왜 살이 안 빠졌나요?")
    st.error(f"**{problem_title}**")
    st.write(problem_detail)
    st.warning(f"⚠️ 일반 다이어트 실패 이유: {why_fail}")
    
    st.divider()
    
    # 솔루션
    st.subheader(f"✅ 해결책: {solution_name}")
    for i, step in enumerate(solution_steps, 1):
        st.success(f"**{i}.** {step}")
    
    st.info(f"📅 예상 효과: {expected}")
    
    if caffeine_warning:
        st.warning("⚠️ 카페인 민감 체질 → 교감신경 자극 성분 최소화 처방")
    
    st.divider()
    
    # 최종 처방
    st.subheader("💊 최종 처방")
    
    st.write(f"**처방명:** {rx_name}")
    st.write(f"**처방 근거:** {rx_reason}")
    st.write(f"**핵심 목표:** {solution_name}")
    
    st.divider()
    
    # 자연과한의원 장점
    st.subheader("🏥 자연과한의원 시스템")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("🧪 **특허 3종 조성물**")
        st.caption("25년 검증된 체중감량 특허")
        st.write("📅 **2주 단위 조절**")
        st.caption("신체 반응 따라 정밀 용량 조정")
    with col2:
        st.write("📱 **90일 밀착 관리**")
        st.caption("카카오톡 1:1 상담")
        st.write("🌿 **100% 청정 한약재**")
        st.caption("부형제 無, 이력추적 약재")
    
    st.divider()
    
    # 가격
    st.subheader("💰 비용")
    
    price_data = {
        "기간": ["1개월", "3개월", "6개월 ⭐"],
        "정상가": ["180,000원", "540,000원", "1,080,000원"],
        "혜택가": ["150,000원", "390,000원", "621,000원"],
        "1일": ["5,000원", "4,330원", "3,450원"]
    }
    st.table(price_data)
    st.caption("※ 2억 봉 돌파 기념 특별 할인")
    
    st.divider()
    
    # 상담 신청
    st.subheader("📞 무료 상담 신청")
    
    with st.form("lead_form"):
        name = st.text_input("성함")
        phone = st.text_input("연락처 (- 없이)")
        submit = st.form_submit_button("한의사 상담 신청")
        
        if submit:
            if name and phone:
                st.success(f"✅ {name}님, 접수 완료!")
                st.write(f"📱 {phone}으로 연락드릴게요.")
                st.write(f"🔬 진단: {diagnosis_type}")
                st.write(f"💊 추천: {rx_name}")
                st.balloons()
            else:
                st.warning("성함과 연락처를 입력해주세요.")
    
    st.divider()
    
    # 지점
    st.subheader("📍 전국 34개 지점")
    st.write("강남본점 · 신촌홍대점 · 명동을지로점 · 신림점 · 노원점 · 목동점 · 상봉점 · 은평연신내점 · 천호점 · 건대점 · 수원점 · 일산점 · 분당점 · 부천점 · 김포점 · 안산점 · 동탄점 · 안양평촌점 · 평택점 · 인천점 · 의정부점 · 부산서면점 · 부산센텀점 · 대구점 · 울산점 · 창원점 · 천안점 · 청주점 · 대전점 · 광주점 · 전주점 · 순천점 · 원주점 · 제주점")
    st.caption("전국 어디서나 동일 처방 가능")
    
    if st.button("🔄 처음부터 다시"):
        st.session_state.step = 0
        st.session_state.user_data = {}
        st.session_state.chat_history = []
        st.rerun()
