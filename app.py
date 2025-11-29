import streamlit as st

# ---------------------------------------
# 0. 시스템 설정
# ---------------------------------------
st.set_page_config(
    page_title="자연과한의원 - 비대면 정밀 처방",
    page_icon="🌿",
    layout="centered"
)

# [CSS: 모든 형광 배경 내 글자 → 검은색 강제]
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    
    /* 메인 배경 */
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 헤더 */
    h1, h2, h3 {
        color: #00E676 !important;
        font-weight: 800;
    }
    
    /* 일반 텍스트 */
    p, span, div, label, .stMarkdown, .stText, li {
        color: #E0E0E0 !important;
        line-height: 1.7;
    }
    
    /* 입력 필드 */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #333;
    }
    
    /* [핵심 수정] 권위 뱃지 - 검은 글씨 강제 */
    .auth-badge {
        display: inline-block;
        background-color: #00E676 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        padding: 6px 12px;
        border-radius: 4px;
        margin: 3px;
        font-size: 0.9rem;
    }
    
    /* 권위 박스 */
    .auth-box {
        background-color: #0A1F0A;
        border: 1px solid #00E676;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        text-align: center;
    }

    /* [핵심 수정] 버튼 - 검은 글씨 강제 */
    div.stButton > button {
        width: 100%;
        background-color: #00E676 !important;
        color: #000000 !important;
        border: none !important;
        padding: 16px 0 !important;
        margin-top: 15px !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
    }
    div.stButton > button * {
        color: #000000 !important;
    }
    div.stButton > button p {
        color: #000000 !important; 
        font-size: 18px !important;
        font-weight: 900 !important;
    }
    div.stButton > button:hover {
        background-color: #00C853 !important;
        transform: scale(1.01);
    }
    
    /* 분석 리포트 박스 */
    .report-box {
        background-color: #0D1F0D;
        border-left: 4px solid #00E676;
        padding: 25px;
        margin: 20px 0;
        border-radius: 0 12px 12px 0;
    }
    .report-title {
        color: #00E676 !important;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 15px;
        display: block;
    }
    
    /* 진단 카드 */
    .diagnosis-card {
        background: linear-gradient(135deg, #1a2f1a 0%, #0a1f0a 100%);
        border: 2px solid #00E676;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
    }
    .diagnosis-title {
        color: #FF5252 !important;
        font-size: 1.5rem;
        font-weight: 900;
        margin-bottom: 10px;
    }
    
    /* 처방 근거 상세 */
    .reasoning-section {
        background-color: #111;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
    }
    .reasoning-header {
        color: #00E676 !important;
        font-weight: bold;
        font-size: 1.1rem;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    
    /* 솔루션 박스 */
    .solution-box {
        background: linear-gradient(135deg, #002200 0%, #001a00 100%);
        border: 2px solid #00E676;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
    }
    
    /* 가격 테이블 */
    .price-table {
        width: 100%;
        text-align: center;
        border-collapse: collapse;
        color: #FFFFFF;
        border: 1px solid #333;
        margin-top: 10px;
    }
    .price-table th {
        background-color: #00E676 !important;
        color: #000000 !important;
        padding: 12px;
        font-weight: bold;
    }
    .price-table td {
        background-color: #121212;
        padding: 12px;
        border-bottom: 1px solid #333;
        color: #FFFFFF !important;
    }
    
    /* 체크리스트 */
    .check-item {
        background-color: #0a1a0a;
        border-left: 3px solid #00E676;
        padding: 12px 15px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
    }
    
    /* Form 버튼도 검은 글씨 */
    .stFormSubmitButton > button {
        background-color: #00E676 !important;
        color: #000000 !important;
        font-weight: 900 !important;
    }
    .stFormSubmitButton > button * {
        color: #000000 !important;
    }
    
    /* 특징 카드 (4개 그리드) */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
        margin: 20px 0;
    }
    .feature-card {
        background: linear-gradient(135deg, #0a1a0a 0%, #111 100%);
        border: 1px solid #00E676;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    .feature-title {
        color: #00E676 !important;
        font-weight: 800;
        font-size: 1rem;
        margin-bottom: 8px;
    }
    .feature-desc {
        color: #AAA !important;
        font-size: 0.85rem;
        line-height: 1.5;
    }
    
    /* 시스템 카드 (세로 리스트) */
    .system-card {
        background-color: #0a1a0a;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 18px;
        margin: 10px 0;
        display: flex;
        align-items: flex-start;
        gap: 15px;
    }
    .system-icon {
        font-size: 1.8rem;
        min-width: 40px;
        text-align: center;
    }
    .system-content {
        flex: 1;
    }
    .system-title {
        color: #00E676 !important;
        font-weight: 800;
        font-size: 1rem;
        margin-bottom: 5px;
    }
    .system-desc {
        color: #CCC !important;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* 검증 수치 박스 */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin: 20px 0;
    }
    .stat-box {
        background-color: #111;
        border: 1px solid #00E676;
        border-radius: 10px;
        padding: 15px 10px;
        text-align: center;
    }
    .stat-number {
        color: #00E676 !important;
        font-size: 1.4rem;
        font-weight: 900;
        display: block;
    }
    .stat-label {
        color: #888 !important;
        font-size: 0.8rem;
        margin-top: 5px;
    }
    
    /* 지점 태그 */
    .branch-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
        margin: 15px 0;
    }
    .branch-tag {
        background-color: #1a1a1a;
        border: 1px solid #333;
        color: #CCC !important;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
    }
    
    /* 한약 특징 카드 */
    .medicine-card {
        background: linear-gradient(135deg, #0f1f0f 0%, #0a150a 100%);
        border: 1px solid #00E676;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    .medicine-title {
        color: #00E676 !important;
        font-weight: 800;
        font-size: 1.1rem;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 1. 상태 관리
# ---------------------------------------
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# ---------------------------------------
# 2. 메인 로직
# ---------------------------------------

def render_intro():
    """Step 0: 인트로 화면 - 강점 콘텐츠 통합"""
    
    # 메인 헤더
    st.markdown("<h1 style='text-align: center; font-size: 2.8rem; margin-bottom: 5px;'>🌿 자연과한의원</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #00E676 !important; font-weight: bold; font-size: 1.1rem;'>비대면 정밀 처방 시스템</p>", unsafe_allow_html=True)
    
    # 핵심 메시지
    st.markdown("""
    <div class='auth-box'>
        <p style='font-size: 1.05rem; margin: 0; line-height: 1.8;'>
        25년 이상의 다이어트 연구를 바탕으로,<br>
        <b style='color:#00E676;'>검증된 개인 맞춤형 처방</b>과 <b style='color:#00E676;'>스트레스 없는 감량법</b>으로<br>
        고객님의 건강하고 성공적인 변화를 함께합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 4대 특징 (그리드)
    st.markdown("### 💊 쉽고 편리한 다이어트")
    st.markdown("""
    <div class='feature-grid'>
        <div class='feature-card'>
            <div class='feature-icon'>💯</div>
            <div class='feature-title'>100% 한약재</div>
            <div class='feature-desc'>부형제 없이<br>순수 한약재로만 채워<br>높은 효과</div>
        </div>
        <div class='feature-card'>
            <div class='feature-icon'>💊</div>
            <div class='feature-title'>복용이 쉬운 한약</div>
            <div class='feature-desc'>한약의 쓴맛을 잡고<br>휴대와 복용의<br>편의성을 높임</div>
        </div>
        <div class='feature-card'>
            <div class='feature-icon'>🍽️</div>
            <div class='feature-title'>굶지 않는 다이어트</div>
            <div class='feature-desc'>무리한 절식 없이<br>일상생활 중<br>자연스럽게 감량</div>
        </div>
        <div class='feature-card'>
            <div class='feature-icon'>✅</div>
            <div class='feature-title'>검증된 다이어트</div>
            <div class='feature-desc'>Since 2001<br>25년 이상 연구<br>특허 3종 보유</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 검증 수치
    st.markdown("""
    <div class='stats-grid'>
        <div class='stat-box'>
            <span class='stat-number'>25년+</span>
            <span class='stat-label'>연구 기간</span>
        </div>
        <div class='stat-box'>
            <span class='stat-number'>2억 봉</span>
            <span class='stat-label'>누적 판매</span>
        </div>
        <div class='stat-box'>
            <span class='stat-number'>특허 3종</span>
            <span class='stat-label'>체중감량 조성물</span>
        </div>
    </div>
    <p style='text-align: center; color: #666 !important; font-size: 0.8rem;'>* 2024년 11월 기준</p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 자연과한의원 시스템
    st.markdown("### 🏥 자연과한의원 시스템")
    st.markdown("<p style='color:#AAA !important;'>25년 이상 경험으로 검증된 체계적인 시스템과 신뢰성 높은 서비스</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='system-card'>
        <div class='system-icon'>🧪</div>
        <div class='system-content'>
            <div class='system-title'>프리미엄 청정 한약</div>
            <div class='system-desc'>보건복지부 인증 한약 규격품 사용, 대한한의사협회 '한약재 이력추적 관리제도' 도입 업체에서 공급</div>
        </div>
    </div>
    
    <div class='system-card'>
        <div class='system-icon'>🎯</div>
        <div class='system-content'>
            <div class='system-title'>1:1 체질 맞춤 솔루션</div>
            <div class='system-desc'>개인의 체질과 생활 습관을 반영한 맞춤 처방, 2주 단위로 부작용 최소화하며 단계별 조절</div>
        </div>
    </div>
    
    <div class='system-card'>
        <div class='system-icon'>🌐</div>
        <div class='system-content'>
            <div class='system-title'>전국 네트워크 통합</div>
            <div class='system-desc'>전국 34개 지점 어디서나 이전 진료 기록 기반 연속 처방 가능</div>
        </div>
    </div>
    
    <div class='system-card'>
        <div class='system-icon'>📱</div>
        <div class='system-content'>
            <div class='system-title'>90일 밀착 가이드</div>
            <div class='system-desc'>카카오톡으로 식단, 레시피, 감량 팁 등 다이어트 정보 제공 및 지속적 동기 부여</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 한약 연구 및 조제
    st.markdown("### 🔬 한약 연구 및 조제")
    
    st.markdown("""
    <div class='medicine-card'>
        <div class='medicine-title'>🏆 체중감량용 특허 조성물</div>
        <p style='color:#CCC !important; margin:0;'>효과가 입증된 체중감량용 특허 조성물 3종을 활용하여 처방합니다.<br>건강하고 효과적인 다이어트를 경험해 보세요.</p>
    </div>
    
    <div class='medicine-card'>
        <div class='medicine-title'>🌿 우수한 품질의 청정 한약재</div>
        <p style='color:#CCC !important; margin:0;'>보건복지부가 인증한 한약 규격품과 직접 엄선한 우수 한약재를 사용하며,<br>대한한의사협회의 '한약재 이력추적 관리제도'를 도입한 업체에서 공급받아 믿고 드실 수 있습니다.</p>
    </div>
    
    <div class='medicine-card'>
        <div class='medicine-title'>💰 합리적 가격의 프리미엄 한약</div>
        <p style='color:#CCC !important; margin:0;'>자체 탕전 설비를 갖춤으로써 유통경로를 단순화하고,<br>조제와 품질을 직접 관리해 합리적인 가격에 프리미엄 한약을 제공합니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 전국 지점
    st.markdown("### 📍 전국 34개 지점")
    
    branches = [
        "강남본점", "신촌홍대점", "명동을지로점", "신림점", "노원점", "목동점", "상봉점", 
        "은평연신내점", "천호점", "건대점", "수원점", "일산점", "분당점", "부천점", 
        "김포점", "안산점", "동탄점", "안양평촌점", "평택점", "인천점", "의정부점",
        "부산서면점", "부산센텀점", "대구점", "울산점", "창원점", "천안점", "청주점", 
        "대전점", "광주점", "전주점", "순천점", "원주점", "제주점"
    ]
    
    branch_html = "<div class='branch-container'>"
    for branch in branches:
        branch_html += f"<span class='branch-tag'>{branch}</span>"
    branch_html += "</div>"
    st.markdown(branch_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # CTA
    st.markdown("### 🚀 지금 바로 시작하세요")
    st.info("**비대면 진료 프로세스:** 체질 분석 문진 → 한의사 맞춤 처방 (2주 단위) → 익일 택배 배송")
    
    if st.button("내 체질에 맞는 처방 확인하기"):
        st.session_state.step = 1
        st.rerun()


def render_step1():
    """Step 1: 신체 정보 & 비만 원인 분석"""
    st.markdown("## 01. 체질 및 대사 분석")
    st.markdown("단순히 체중이 문제가 아닙니다. **'왜 살이 안 빠지는가'**의 근본 원인을 찾습니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("신장 (cm)", 140, 200, 160)
        age = st.number_input("나이 (세)", 18, 70, 30)
    with col2:
        weight = st.number_input("체중 (kg)", 40, 150, 65)
        gender = st.selectbox("성별", ["여성", "남성"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔍 비만 원인 자가 진단")
    st.markdown("**Q. 다이어트가 번번이 실패하는 가장 큰 이유는?**")
    
    cause_options = [
        "A. 식욕 통제 불가 (배불러도 계속 먹게 됨)",
        "B. 물만 먹어도 붓고 몸이 무거움",
        "C. 식사량은 적은데 살이 안 빠짐 (대사 저하)",
        "D. 스트레스 받으면 폭식함 (감정적 섭식)"
    ]
    cause = st.radio("가장 해당되는 항목을 선택하세요.", cause_options, label_visibility="collapsed")

    if st.button("다음 단계: 약물 반응성 체크"):
        st.session_state.user_data.update({
            'height': height, 'weight': weight, 'age': age, 'gender': gender, 'cause': cause
        })
        st.session_state.step = 2
        st.rerun()


def render_step2():
    """Step 2: 약물 내성 체크"""
    st.markdown("## 02. 약물 민감도 및 내성 테스트")
    
    st.markdown("""
    <div style='background-color:#0a1a0a; padding:18px; border-radius:10px; border:1px solid #00E676;'>
        <b style='color:#00E676; font-size:1.1rem;'>💊 2주 단위 정밀 용량 조절 시스템</b><br><br>
        자연과한의원은 한 번에 강한 처방을 하지 않습니다.<br>
        <b>2주마다 신체 반응(대사량, 수면, 식욕 변화)을 체크</b>하여<br>
        단계적으로 용량을 조절하는 <b>'Titration(적정) 방식'</b>을 사용합니다.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    caffeine = st.radio(
        "**Q1. 카페인(커피) 섭취 시 반응은?**",
        ["전혀 영향 없음 (하루 3잔 이상 가능)", 
         "약간의 각성 효과 있음 (1-2잔 적정)", 
         "심장이 두근거리고 수면에 영향 (민감 체질)"]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    history = st.radio(
        "**Q2. 다이어트 약(양약/한약) 복용 경험**",
        ["없음 (처음입니다)", 
         "1-2회 복용 경험 있음", 
         "여러 차례 복용했으나 효과 미비 (내성 의심)"]
    )
    
    if st.button("맞춤 처방 결과 확인하기"):
        st.session_state.user_data.update({
            'caffeine': caffeine, 'history': history
        })
        st.session_state.step = 3
        st.rerun()


def render_result():
    """Step 3: 처방 결과 (상세 분석 포함)"""
    data = st.session_state.user_data
    
    # ============================================
    # [핵심] 상세 분석 로직
    # ============================================
    cause_input = data.get('cause', '')
    height = data.get('height', 160)
    weight = data.get('weight', 65)
    age = data.get('age', 30)
    gender = data.get('gender', '여성')
    caffeine = data.get('caffeine', '')
    history = data.get('history', '')
    
    # BMI 계산
    bmi = round(weight / ((height/100) ** 2), 1)
    if bmi < 23:
        bmi_status = "정상~과체중 경계"
    elif bmi < 25:
        bmi_status = "과체중"
    elif bmi < 30:
        bmi_status = "비만 1단계"
    else:
        bmi_status = "비만 2단계 이상"
    
    # 원인별 진단 및 상세 설명
    if "식욕" in cause_input:
        diagnosis_type = "위열(胃熱) 과다형"
        diagnosis_name = "식욕 과항진 비만"
        color_code = "#FF6B6B"
        
        problem_analysis = """
        <b style='color:#FF5252; font-size:1.1rem;'>📌 문제의 핵심: 가짜 배고픔</b><br><br>
        귀하의 위장에는 <b>과도한 열(胃熱)</b>이 축적되어 있습니다. 
        이 열기는 시상하부의 포만 중추를 교란시켜, <b>실제로 배가 부른 상태에서도 
        뇌가 '배고프다'는 잘못된 신호</b>를 보내게 만듭니다.<br><br>
        
        <b style='color:#00E676;'>▶ 한의학적 해석:</b><br>
        위장에 열이 많으면 소화가 지나치게 빨라지고, 음식이 빠르게 분해되면서 
        허기 신호가 과도하게 발생합니다. 이는 의지력의 문제가 아닌 
        <b>생리적 불균형</b>입니다.<br><br>
        
        <b style='color:#00E676;'>▶ 일반 다이어트가 실패하는 이유:</b><br>
        단순 절식은 위열을 더 자극하여 폭식 → 후회 → 절식의 악순환을 만듭니다.
        """
        
        solution_detail = """
        <b style='color:#00E676; font-size:1.1rem;'>🎯 처방 전략: 청위사열(清胃瀉熱)</b><br><br>
        
        <div class='check-item'>
        <b>1. 위열 제거</b><br>
        황련, 치자 등 청열 약재로 위장의 과도한 열을 식힙니다.
        </div>
        
        <div class='check-item'>
        <b>2. 포만감 정상화</b><br>
        식탐사약(食貪瀉藥) 조성으로 포만 중추 민감도를 회복시킵니다.
        </div>
        
        <div class='check-item'>
        <b>3. 식욕 호르몬 조절</b><br>
        그렐린(식욕 호르몬) 분비를 억제하고 렙틴(포만 호르몬) 반응성을 높입니다.
        </div>
        """
        solution_focus = "식욕 정상화 + 포만감 회복"
        expected_result = "복용 3-5일 후 식욕 감소 체감, 2주 후 폭식 욕구 현저히 감소"
        
    elif "물만 먹어도" in cause_input:
        diagnosis_type = "수독(水毒) 정체형"
        diagnosis_name = "부종성 비만"
        color_code = "#64B5F6"
        
        problem_analysis = """
        <b style='color:#64B5F6; font-size:1.1rem;'>📌 문제의 핵심: 수분 대사 장애</b><br><br>
        귀하의 체내에는 <b>수독(水毒)</b>이 정체되어 있습니다. 
        정상적으로 배출되어야 할 수분과 노폐물이 조직에 고여 
        <b>붓기, 무거움, 피로감</b>을 유발합니다.<br><br>
        
        <b style='color:#00E676;'>▶ 한의학적 해석:</b><br>
        비장(脾臟)의 운화 기능이 저하되면 수습(水濕)이 정체됩니다. 
        이 상태에서는 림프 순환이 막히고, 셀룰라이트가 축적되며, 
        <b>실제 지방보다 붓기가 체중의 상당 부분</b>을 차지합니다.<br><br>
        
        <b style='color:#00E676;'>▶ 일반 다이어트가 실패하는 이유:</b><br>
        운동과 식이조절은 지방 감량에는 효과적이나, 수독 정체는 해결하지 못합니다.
        오히려 무리한 운동은 피로를 가중시킵니다.
        """
        
        solution_detail = """
        <b style='color:#00E676; font-size:1.1rem;'>🎯 처방 전략: 이수삼습(利水滲濕)</b><br><br>
        
        <div class='check-item'>
        <b>1. 수독 배출</b><br>
        복령, 택사, 의이인 등으로 정체된 수분과 노폐물을 소변으로 배출합니다.
        </div>
        
        <div class='check-item'>
        <b>2. 림프 순환 촉진</b><br>
        독소킬(毒素-) 조성으로 막힌 림프관을 열어 부종을 제거합니다.
        </div>
        
        <div class='check-item'>
        <b>3. 비장 기능 강화</b><br>
        백출, 창출로 비장의 운화 기능을 회복시켜 재발을 방지합니다.
        </div>
        """
        solution_focus = "부종 제거 + 림프 순환 개선"
        expected_result = "복용 1주일 내 붓기 감소 체감, 2주 후 체중 2-4kg 감량 (수분)"
        
    elif "식사량은 적은데" in cause_input:
        diagnosis_type = "대사 저하(冷體質)형"
        diagnosis_name = "기초대사량 저하 비만"
        color_code = "#FFB74D"
        
        problem_analysis = """
        <b style='color:#FFB74D; font-size:1.1rem;'>📌 문제의 핵심: 꺼진 대사 엔진</b><br><br>
        귀하의 <b>기초대사량(BMR)</b>이 현저히 낮은 상태입니다. 
        같은 양을 먹어도 남들보다 칼로리 소모가 적어 
        <b>먹는 것 대비 살이 쉽게 찌는 체질</b>이 된 것입니다.<br><br>
        
        <b style='color:#00E676;'>▶ 한의학적 해석:</b><br>
        양기(陽氣) 부족으로 인해 체온 유지와 에너지 연소 기능이 저하되었습니다. 
        손발이 차고, 쉽게 피로하며, 추위를 많이 타는 증상이 동반됩니다.
        <b>신진대사 자체가 슬로우 모드</b>인 상태입니다.<br><br>
        
        <b style='color:#00E676;'>▶ 일반 다이어트가 실패하는 이유:</b><br>
        절식은 대사량을 더욱 떨어뜨려 요요의 원인이 됩니다. 
        근본적으로 '태우는 능력'을 키워야 합니다.
        """
        
        solution_detail = """
        <b style='color:#00E676; font-size:1.1rem;'>🎯 처방 전략: 온양보기(溫陽補氣)</b><br><br>
        
        <div class='check-item'>
        <b>1. 체온 상승 (Thermogenesis)</b><br>
        부자, 건강 등 온열 약재로 심부 체온을 0.3-0.5도 높여 기초대사량을 증가시킵니다.
        </div>
        
        <div class='check-item'>
        <b>2. 교감신경 활성화</b><br>
        지방사약의 특허 조성으로 교감신경을 자극, 가만히 있어도 칼로리를 소모하는 체질로 전환합니다.
        </div>
        
        <div class='check-item'>
        <b>3. 갈색 지방 활성화</b><br>
        열을 발생시키는 갈색 지방(Brown Fat)의 활성도를 높입니다.
        </div>
        """
        solution_focus = "기초대사량 상승 + 체온 상승"
        expected_result = "복용 1주일 후 체온 상승 체감, 2주 후 에너지 레벨 향상 및 체중 감소 시작"
        
    else:  # 스트레스 폭식
        diagnosis_type = "간기울결(肝氣鬱結)형"
        diagnosis_name = "스트레스성 폭식 비만"
        color_code = "#BA68C8"
        
        problem_analysis = """
        <b style='color:#BA68C8; font-size:1.1rem;'>📌 문제의 핵심: 스트레스 호르몬</b><br><br>
        귀하는 <b>코르티솔(스트레스 호르몬)</b>이 만성적으로 높은 상태입니다. 
        스트레스 → 폭식 → 죄책감 → 스트레스의 <b>악순환 고리</b>에 갇혀 있으며, 
        코르티솔은 특히 <b>복부 지방 축적</b>을 촉진합니다.<br><br>
        
        <b style='color:#00E676;'>▶ 한의학적 해석:</b><br>
        간(肝)의 소설(疏泄) 기능이 막혀 기(氣)가 울체된 상태입니다. 
        이로 인해 감정 기복이 심하고, 스트레스 상황에서 음식으로 
        위안을 찾게 됩니다. 이는 <b>정서적 허기(Emotional Hunger)</b>입니다.<br><br>
        
        <b style='color:#00E676;'>▶ 일반 다이어트가 실패하는 이유:</b><br>
        의지력으로 억제하면 스트레스가 더 쌓여 결국 더 큰 폭식으로 터집니다. 
        스트레스 자체를 다스려야 합니다.
        """
        
        solution_detail = """
        <b style='color:#00E676; font-size:1.1rem;'>🎯 처방 전략: 소간해울(疏肝解鬱)</b><br><br>
        
        <div class='check-item'>
        <b>1. 간기 소통</b><br>
        시호, 향부자 등 소간(疏肝) 약재로 막힌 기의 흐름을 풀어줍니다.
        </div>
        
        <div class='check-item'>
        <b>2. 정서 안정</b><br>
        가미소요산 가감방으로 불안, 초조, 감정 기복을 안정시킵니다.
        </div>
        
        <div class='check-item'>
        <b>3. 코르티솔 조절</b><br>
        아답토겐(Adaptogen) 약재로 스트레스 호르몬 분비를 정상화합니다.
        </div>
        """
        solution_focus = "정서 안정 + 폭식 충동 제어"
        expected_result = "복용 3-5일 후 심리적 안정감, 2주 후 폭식 빈도 현저히 감소"

    # 내성 여부에 따른 처방 강도
    if "여러 차례" in history or "내성" in history:
        prescription_level = "MAX"
        prescription_name = "지방사약 MAX 처방"
        prescription_reason = "기존 약물에 내성이 생긴 상태이므로, 강화된 용량과 특수 조성이 필요합니다."
    elif "1-2회" in history:
        prescription_level = "STANDARD PLUS"
        prescription_name = "지방사약 스탠다드 플러스"
        prescription_reason = "약물 경험이 있으나 내성은 낮은 상태로, 표준보다 약간 강화된 처방이 적합합니다."
    else:
        prescription_level = "STANDARD"
        prescription_name = "지방사약 스탠다드"
        prescription_reason = "약물 복용 경험이 없어 표준 용량부터 시작하여 점진적으로 조절합니다."
    
    # 카페인 민감도에 따른 주의사항
    if "민감" in caffeine or "두근" in caffeine:
        caffeine_note = "⚠️ 카페인 민감 체질로 확인되어, 교감신경 자극 성분을 최소화한 처방으로 조정합니다."
    else:
        caffeine_note = ""
    
    # ============================================
    # [UI 렌더링]
    # ============================================
    
    st.markdown("## 📋 맞춤 처방 분석 결과")
    
    # 기본 정보 요약
    st.markdown(f"""
    <div style='background-color:#111; padding:15px; border-radius:10px; border:1px solid #333; margin-bottom:20px;'>
        <b style='color:#00E676;'>📊 입력 정보 요약</b><br><br>
        <b>기본:</b> {gender} / {age}세 / {height}cm / {weight}kg<br>
        <b>BMI:</b> {bmi} ({bmi_status})<br>
        <b>주요 증상:</b> {cause_input.split('.')[0].replace('A', '').replace('B', '').replace('C', '').replace('D', '').strip()}
    </div>
    """, unsafe_allow_html=True)
    
    # 진단 결과
    st.markdown(f"""
    <div class='diagnosis-card'>
        <div class='diagnosis-title'>🔬 진단: {diagnosis_type} - {diagnosis_name}</div>
        <p style='color:#CCC !important; margin:0;'>귀하의 비만 원인을 25년 임상 데이터 기반으로 정밀 분석한 결과입니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 문제 분석
    st.markdown(f"""
    <div class='reasoning-section'>
        <div class='reasoning-header'>1️⃣ 왜 살이 안 빠졌는가? - 문제 분석</div>
        {problem_analysis}
    </div>
    """, unsafe_allow_html=True)
    
    # 솔루션 상세
    st.markdown(f"""
    <div class='reasoning-section'>
        <div class='reasoning-header'>2️⃣ 어떻게 해결하는가? - 처방 전략</div>
        {solution_detail}
    </div>
    """, unsafe_allow_html=True)
    
    # 최종 처방
    st.markdown(f"""
    <div class='solution-box'>
        <b style='color:#00E676; font-size:1.3rem;'>💊 최종 처방: {prescription_name}</b><br><br>
        
        <table style='width:100%; color:#FFF;'>
            <tr>
                <td style='padding:8px 0; color:#888;'>처방 강도</td>
                <td style='padding:8px 0;'><b style='color:#00E676;'>{prescription_level}</b></td>
            </tr>
            <tr>
                <td style='padding:8px 0; color:#888;'>처방 근거</td>
                <td style='padding:8px 0;'>{prescription_reason}</td>
            </tr>
            <tr>
                <td style='padding:8px 0; color:#888;'>핵심 목표</td>
                <td style='padding:8px 0;'><b style='color:#00E676;'>{solution_focus}</b></td>
            </tr>
            <tr>
                <td style='padding:8px 0; color:#888;'>예상 효과</td>
                <td style='padding:8px 0;'>{expected_result}</td>
            </tr>
        </table>
        {"<br><div style='background:#1a0a0a; padding:10px; border-radius:5px; border:1px solid #FF5252;'>" + caffeine_note + "</div>" if caffeine_note else ""}
    </div>
    """, unsafe_allow_html=True)
    
    # 자연과한의원 시스템 장점 (결과 페이지에서 다시 강조)
    st.markdown("""
    <div class='auth-box' style='text-align:left;'>
        <b style='color:#00E676; font-size:1.1rem;'>✅ 자연과한의원만의 차별화된 시스템</b><br><br>
        
        <div style='display:grid; grid-template-columns: 1fr 1fr; gap:15px;'>
            <div>
                <b style='color:#FFF;'>🧪 특허 3종 조성물</b><br>
                <span style='color:#AAA; font-size:0.9rem;'>25년간 검증된 체중감량 특허 처방</span>
            </div>
            <div>
                <b style='color:#FFF;'>📅 2주 단위 조절</b><br>
                <span style='color:#AAA; font-size:0.9rem;'>신체 반응에 따른 정밀 용량 조정</span>
            </div>
            <div>
                <b style='color:#FFF;'>📱 90일 밀착 관리</b><br>
                <span style='color:#AAA; font-size:0.9rem;'>카카오톡 1:1 상담 + 요요 방지</span>
            </div>
            <div>
                <b style='color:#FFF;'>🌿 100% 청정 한약재</b><br>
                <span style='color:#AAA; font-size:0.9rem;'>부형제 無, 이력추적 관리 약재</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 가격
    st.markdown("---")
    st.markdown("### 💰 비용 안내")
    st.markdown("<p style='color:#888 !important;'>자체 탕전 설비로 유통 단순화 → 합리적 가격의 프리미엄 한약</p>", unsafe_allow_html=True)
    
    price_html = """
    <table class="price-table">
      <tr>
        <th>기간</th>
        <th>정상가</th>
        <th>혜택가</th>
        <th>1일 비용</th>
      </tr>
      <tr>
        <td>1개월 (2주×2)</td>
        <td style="text-decoration: line-through; color: #666 !important;">180,000원</td>
        <td style="color:#FF5252 !important; font-weight:bold;">150,000원</td>
        <td>5,000원</td>
      </tr>
      <tr>
        <td>3개월</td>
        <td style="text-decoration: line-through; color: #666 !important;">540,000원</td>
        <td style="color:#FF5252 !important; font-weight:bold;">390,000원</td>
        <td>4,330원</td>
      </tr>
      <tr>
        <td><b>6개월 (추천)</b></td>
        <td style="text-decoration: line-through; color: #666 !important;">1,080,000원</td>
        <td style="color:#FF5252 !important; font-weight:bold;">621,000원</td>
        <td style="color:#00E676 !important; font-weight:bold;">3,450원 ✨</td>
      </tr>
    </table>
    """
    st.markdown(price_html, unsafe_allow_html=True)
    st.caption("※ 2억 봉 돌파 기념 특별 할인 적용 중 (2024년 11월 기준)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 리드 폼
    st.markdown("### 📞 비대면 상담 신청")
    st.markdown(f"**'{diagnosis_name}'** 맞춤 처방 상담을 신청해 주세요.")
    
    with st.form("lead_form"):
        name = st.text_input("성함")
        phone = st.text_input("연락처 (- 없이)")
        
        submit = st.form_submit_button("한의사 무료 상담 신청하기")
        
        if submit:
            if name and phone:
                st.success(f"✅ {name}님, 상담 신청이 완료되었습니다!")
                st.markdown(f"""
                <div style='background-color:#0a1a0a; padding:18px; border:2px solid #00E676; border-radius:10px; margin-top:15px;'>
                    <b style='color:#00E676; font-size:1.1rem;'>🎉 접수 완료</b><br><br>
                    담당 한의사가 <b>{phone}</b>으로 연락드립니다.<br><br>
                    <b>진단 결과:</b> {diagnosis_type} - {diagnosis_name}<br>
                    <b>추천 처방:</b> {prescription_name}<br><br>
                    <span style='color:#888;'>상담 시 위 결과를 말씀해주시면 더 빠른 진료가 가능합니다.</span>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.warning("성함과 연락처를 모두 입력해주세요.")
    
    # 전국 지점 안내
    st.markdown("---")
    st.markdown("### 📍 가까운 지점에서도 동일한 처방을 받으실 수 있습니다")
    
    branches = [
        "강남본점", "신촌홍대점", "명동을지로점", "신림점", "노원점", "목동점", "상봉점", 
        "은평연신내점", "천호점", "건대점", "수원점", "일산점", "분당점", "부천점", 
        "김포점", "안산점", "동탄점", "안양평촌점", "평택점", "인천점", "의정부점",
        "부산서면점", "부산센텀점", "대구점", "울산점", "창원점", "천안점", "청주점", 
        "대전점", "광주점", "전주점", "순천점", "원주점", "제주점"
    ]
    
    branch_html = "<div class='branch-container'>"
    for branch in branches:
        branch_html += f"<span class='branch-tag'>{branch}</span>"
    branch_html += "</div>"
    st.markdown(branch_html, unsafe_allow_html=True)
    st.caption("전국 네트워크 통합 시스템으로 어느 지점에서나 동일한 진료 기록 기반 처방 가능")
    
    # 처음으로 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("처음부터 다시 분석하기"):
        st.session_state.step = 0
        st.session_state.user_data = {}
        st.rerun()


# ---------------------------------------
# 3. 메인 실행
# ---------------------------------------
if st.session_state.step == 0:
    render_intro()
elif st.session_state.step == 1:
    render_step1()
elif st.session_state.step == 2:
    render_step2()
elif st.session_state.step == 3:
    render_result()
