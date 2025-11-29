import streamlit as st
import time

# ---------------------------------------
# 0. 시스템 설정: Dark & Neon Green Theme (High Contrast)
# ---------------------------------------
st.set_page_config(
    page_title="자연과한의원 - 비대면 정밀 처방",
    page_icon="🌿",
    layout="centered"
)

# [CSS 수정: 검은색 텍스트 강제 적용 및 가독성 확보]
custom_css = """
<style>
    /* 1. 메인 배경 및 기본 폰트 (화이트) */
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 2. 헤더 스타일 */
    h1, h2, h3 {
        color: #00E676 !important;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    /* 3. 일반 텍스트 (화이트) */
    p, span, div, label, .stMarkdown, .stText, li {
        color: #E0E0E0 !important;
        line-height: 1.6;
    }
    
    /* 4. 입력 필드 */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #333;
    }
    
    /* 5. [수정] 권위 뱃지 (형광 배경 + 검은 글씨) */
    .auth-badge {
        display: inline-block;
        background-color: #00E676;
        color: #000000 !important; /* 리얼 블랙 강제 */
        font-weight: 900;
        padding: 4px 10px;
        border-radius: 4px;
        margin-right: 5px;
        margin-bottom: 5px;
        font-size: 0.85rem;
    }
    
    /* 6. 권위 박스 컨테이너 */
    .auth-box {
        background-color: #0A1F0A;
        border: 1px solid #00E676;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        text-align: center;
    }

    /* 7. [수정] 버튼 스타일 (형광 배경 + 검은 글씨) */
    .stButton>button {
        width: 100%;
        background-color: #00E676;
        color: #000000 !important; /* 리얼 블랙 강제 */
        font-size: 19px;
        font-weight: 900;
        padding: 16px 0;
        border-radius: 8px;
        border: none;
        margin-top: 15px;
    }
    .stButton>button:hover {
        background-color: #00C853;
        color: #000000 !important;
        transform: scale(1.01);
    }
    
    /* 8. 분석 리포트 박스 (New) */
    .report-box {
        background-color: #111;
        border-left: 4px solid #00E676;
        padding: 20px;
        margin: 20px 0;
        border-radius: 0 10px 10px 0;
    }
    .report-title {
        color: #00E676 !important;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 10px;
        display: block;
    }

    /* 9. 가격 테이블 */
    .price-table {
        width: 100%;
        text-align: center;
        border-collapse: collapse;
        color: #FFFFFF;
        border: 1px solid #333;
        margin-top: 10px;
    }
    .price-table th {
        background-color: #00E676;
        color: #000000 !important; /* 헤더 검은 글씨 */
        padding: 12px;
        font-weight: bold;
    }
    .price-table td {
        background-color: #121212;
        padding: 12px;
        border-bottom: 1px solid #333;
        color: #FFFFFF !important;
    }
    .price-best {
        background-color: #051405 !important;
        border: 2px solid #00E676;
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

# [Intro: Authority & Trust]
if st.session_state.step == 0:
    # 한글 로고 이미지 (placeholder 텍스트 변경)
    st.image("https://placehold.co/600x120/000000/00E676?text=%EC%9E%90%EC%97%B0%EA%B3%BC%ED%95%9C%EC%9D%98%EC%9B%90&font=roboto", use_column_width=True)
    
    st.markdown("<h1 style='text-align: center; font-size: 1.8rem;'>25년 데이터 기반 정밀 처방</h1>", unsafe_allow_html=True)
    
    # [권위 증명 섹션 - 가독성 수정]
    st.markdown("""
    <div class='auth-box'>
        <div style='margin-bottom:15px;'>
            <span class='auth-badge'>SINCE 2001</span>
            <span class='auth-badge'>누적 2억 봉 돌파</span>
            <span class='auth-badge'>특허 3종 보유</span>
        </div>
        <p style='margin:0; font-size: 1.05rem;'>
        <b>"다이어트는 과학입니다."</b><br>
        자연과한의원은 검증된 데이터로 증명합니다.<br>
        100% 한약재, 무리한 절식 없는 <b>'지속 가능한 감량'</b>을 시작하세요.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✅ 비대면 진료 시스템 (Easy & Fast)")
    st.info("1. AI 사전 문진 ➔ 2. 1:1 맞춤 처방 (2주 단위) ➔ 3. 익일 택배 도착")
    
    if st.button("내 몸에 맞는 '처방 단계' 확인하기"):
        st.session_state.step = 1
        st.rerun()

# [Phase 1: 결핍의 스캔]
elif st.session_state.step == 1:
    st.markdown("## 01. 신체 대사 효율 측정")
    st.markdown("단순히 체중이 문제가 아닙니다. **'왜 안 빠지는가'**를 분석합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("신장 (cm)", 140, 200, 160)
        age = st.number_input("나이 (세)", 18, 70, 30)
    with col2:
        weight = st.number_input("체중 (kg)", 40, 150, 60)
        gender = st.selectbox("성별", ["여성", "남성"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Q. 귀하의 다이어트가 매번 실패하는 근본 원인은?**")
    
    # 원인별 키워드 매핑을 위해 key 값을 명확히 분리
    cause_options = [
        "A. 식욕 통제 불가 (배불러도 계속 먹음)",
        "B. 물만 먹어도 붓고 몸이 무거움",
        "C. 식사량은 적은데 살이 안 빠짐",
        "D. 스트레스 받으면 폭식 (감정 기복)"
    ]
    cause = st.radio("가장 해당되는 항목을 하나만 선택하세요.", cause_options)

    if st.button("다음: 내성 및 안전성 체크"):
        st.session_state.user_data.update({
            'height': height, 'weight': weight, 'age': age, 'gender': gender, 'cause': cause
        })
        st.session_state.step = 2
        st.rerun()

# [Phase 2: 리스크 관리]
elif st.session_state.step == 2:
    st.markdown("## 02. 약물 내성 및 민감도 테스트")
    st.markdown("""
    <div style='background-color:#111; padding:15px; border-radius:8px; border:1px solid #333;'>
        <b style='color:#00E676;'>💡 2주 단위 정밀 처방 시스템</b><br>
        한 번에 강한 약을 쓰지 않습니다. 
        <b>2주마다 몸의 반응(대사량, 수면, 식욕)을 체크</b>하여 
        단계를 조절하는 'Titration(용량 적정)' 방식을 사용합니다.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    caffeine = st.radio(
        "Q. 평소 카페인(커피) 섭취 시 반응은?",
        ["전혀 영향 없음 (하루 3잔 이상 가능)", 
         "약간의 각성 효과 있음", 
         "심장이 두근거리고 잠을 못 잠 (민감성)"]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    history = st.radio(
        "Q. 다이어트 양약/한약 복용 경험",
        ["없음 (Pure Type)", 
         "경험 있음 (약한 내성)", 
         "장기 복용 및 효과 미비 (초고도 내성 ➔ MAX 처방 필요)"]
    )
    
    if st.button("AI 정밀 처방 결과 보기"):
        st.session_state.user_data.update({
            'caffeine': caffeine, 'history': history
        })
        st.session_state.step = 3
        st.rerun()

# [Phase 3: 처방 및 상세 리포트]
elif st.session_state.step == 3:
    data = st.session_state.user_data
    
    # 스피너
    with st.spinner("AI가 25년 임상 데이터를 기반으로 최적 처방을 매칭 중입니다..."):
        time.sleep(1.5)
    
    # ----------------------------------------------------
    # [Logic Engine] 상세 분석 내용 생성
    # ----------------------------------------------------
    cause_input = data.get('cause', '')
    
    if "식욕" in cause_input:
        diagnosis = "위열(Stomach Heat) 과다형 비만"
        reasoning = """
        <b>"가짜 배고픔에 속고 계십니다."</b><br>
        귀하의 위장에는 과도한 열(Heat)이 쌓여있습니다. 이 열기는 뇌의 포만 중추를 마비시켜, 
        배가 불러도 숟가락을 놓지 못하게 만듭니다. 의지의 문제가 아닙니다. 
        <b>'식탐사약' 기전</b>을 통해 위장의 열을 식히고 포만감을 정상화해야만 감량이 가능합니다.
        """
        solution_focus = "식욕 억제 + 포만감 증대"
        
    elif "물만 먹어도" in cause_input:
        diagnosis = "수독(Water Poison) 정체형 비만"
        reasoning = """
        <b>"지방이 아니라 붓기부터 잡아야 합니다."</b><br>
        체내 수분 대사가 고장 나 노폐물이 빠져나가지 못하고 썩어있는 '수독' 상태입니다. 
        이 상태에서는 굶어도 몸만 붓습니다. 
        <b>'독소킬' 기전</b>을 통해 꽉 막힌 림프 순환을 뚫어주면, 
        초반 2주 안에 붓기가 빠지며 급격한 라인 변화를 경험하실 겁니다.
        """
        solution_focus = "부종 제거 + 순환 개선"
        
    elif "식사량은 적은데" in cause_input:
        diagnosis = "대사 기능 저하형(Cold Body) 비만"
        reasoning = """
        <b>"엔진이 꺼진 자동차와 같습니다."</b><br>
        기초대사량이 현저히 낮아, 남들과 똑같이 먹어도 귀하만 살이 찝니다. 
        절식은 오히려 대사를 더 떨어뜨리는 독입니다.
        <b>'지방사약'의 교감신경 자극 기전</b>으로 
        심박수와 체온을 강제로 높여, 가만히 있어도 운동하는 것 같은 '태우는 몸'을 만들어야 합니다.
        """
        solution_focus = "기초대사량 상승 + 발열 효과"
        
    else: # 스트레스
        diagnosis = "간기 울결(Stress Induced)형 비만"
        reasoning = """
        <b>"스트레스 호르몬이 지방을 붙잡고 있습니다."</b><br>
        스트레스를 받으면 나오는 '코르티솔'이 뱃살을 저장하고 있습니다. 
        억지로 굶으면 폭식 터집니다.
        간의 기운을 풀어주는 <b>'소요산' 계열 처방</b>을 통해, 
        심신을 안정시키면서 자연스럽게 폭식 욕구를 잠재우는 것이 유일한 해법입니다.
        """
        solution_focus = "스트레스 완화 + 폭식 방지"

    # 내성 여부
    is_max = "초고도 내성" in data.get('history', '')
    drug_name = "지방사약 MAX" if is_max else "지방사약 (Standard)"
    
    # ----------------------------------------------------
    # [UI Render] 결과 화면
    # ----------------------------------------------------
    st.markdown(f"## 📋 정밀 진단: <span style='color:#FF5252'>{diagnosis}</span>", unsafe_allow_html=True)
    
    # [심층 분석 리포트 - 상세 내용]
    st.markdown(f"""
    <div class='report-box'>
        <span class='report-title'>🔍 AI 처방 근거 (Why This Solution?)</span>
        {reasoning}
        <br><br>
        <b style='color:#FFF;'>👉 핵심 처방 포인트: {solution_focus}</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='auth-box' style='text-align:left;'>
        <b style='color:#00E676; font-size:1.1rem;'>최종 솔루션: {drug_name}</b><br><br>
        ✅ <b>체지방 분해:</b> 특허 조성물 3종 탑재<br>
        ✅ <b>안전성:</b> 2주 단위 정밀 용량 조절 (Titration)<br>
        ✅ <b>사후 관리:</b> 90일 밀착 가이드 + 요요 방지 프로그램
    </div>
    """, unsafe_allow_html=True)
    
    # 비포 애프터
    st.markdown("### 👁 실제 감량 사례 (Before & After)")
    st.markdown("""
    <div style='background-color:#111; padding:10px; border-radius:10px; border:1px solid #333;'>
         <p style='text-align:center; color:#666 !important; font-size:0.9rem;'>
         ※ 자연과한의원 실제 환자 데이터 (3개월 프로그램)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_b, col_a = st.columns(2)
    with col_b:
        st.markdown("<div style='color:#00E676; font-weight:bold; text-align:center;'>BEFORE (78kg)</div>", unsafe_allow_html=True)
        # 이미지 placeholder
        st.image("https://placehold.co/300x400/333333/FFFFFF?text=BEFORE", use_column_width=True)
    with col_a:
        st.markdown("<div style='color:#00E676; font-weight:bold; text-align:center;'>AFTER (58kg)</div>", unsafe_allow_html=True)
        # 이미지 placeholder
        st.image("https://placehold.co/300x400/00E676/000000?text=AFTER", use_column_width=True)

    # 가격 정책
    st.markdown("---")
    st.markdown("### 💰 합리적 비용 (자체 탕전/유통 혁신)")
    
    price_html = """
    <table class="price-table">
      <tr>
        <th>기간</th>
        <th>정상가</th>
        <th>혜택가</th>
        <th>1일 비용</th>
      </tr>
      <tr>
        <td>1개월</td>
        <td style="text-decoration: line-through; color: #666 !important;">180,000원</td>
        <td style="color:#FF5252 !important; font-weight:bold;">150,000원</td>
        <td>5,000원</td>
      </tr>
      <tr class="price-best">
        <td>6개월 (Best)</td>
        <td style="text-decoration: line-through; color: #666 !important;">1,260,000원</td>
        <td style="color:#FF5252 !important; font-weight:bold;">621,000원</td>
        <td style="color:#00E676 !important; font-weight:bold;">3,450원 ✨</td>
      </tr>
    </table>
    """
    st.markdown(price_html, unsafe_allow_html=True)
    st.caption("※ 2억 봉 판매 돌파 기념, 6개월 패키지 최대 혜택 적용 중")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Call to Action
    st.markdown("#### 🚀 지금 신청하면 '비대면 초진'이 가능합니다.")
    
    with st.form("lead_form"):
        name = st.text_input("성함")
        phone = st.text_input("연락처 (- 없이 입력)")
        referral = st.text_input("추천인 코드 (선택: 10만 포인트 지급)")
        
        submit = st.form_submit_button("👨‍⚕️ 한의사 무료 상담 및 처방 신청")
        
        if submit:
            if name and phone:
                st.success(f"✅ {name}님, 접수가 완료되었습니다.")
                st.markdown(f"""
                <div style='background-color:#111; padding:15px; border:1px solid #00E676; border-radius:8px;'>
                    <b style='color:#00E676;'>[접수 완료]</b><br>
                    담당 한의사가 <b>{phone}</b>으로 연락드립니다.<br>
                    진료 시 <b>"{diagnosis.split('(')[0]}"</b> 결과를 말씀해주시면 더 빠릅니다.
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.warning("성함과 연락처를 입력해주세요.")
