import streamlit as st
import time

# ---------------------------------------
# 0. 시스템 설정: Dark & Neon Green Theme (Ultimate Trust)
# ---------------------------------------
st.set_page_config(
    page_title="자연과한의원 - 비대면 정밀 처방",
    page_icon="🌿",
    layout="centered"
)

# [CSS: 리얼 블랙 & 네온 그린 + 이미지/카드 스타일링]
custom_css = """
<style>
    /* 1. 메인 배경 및 폰트 컬러 */
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 2. 헤더 및 강조 텍스트 */
    h1, h2, h3 {
        color: #00E676 !important; /* Neon Green */
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    /* 3. 일반 텍스트 화이트 강제 적용 */
    p, span, div, label, .stMarkdown, .stText {
        color: #E0E0E0 !important;
    }
    
    /* 4. 입력 필드 스타일 */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #333;
    }
    
    /* 5. 정보 박스 (Authority Box) */
    .auth-box {
        background-color: #0A1F0A;
        border: 1px solid #00E676;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        text-align: center;
    }
    .auth-badge {
        display: inline-block;
        background-color: #00E676;
        color: #000;
        font-weight: bold;
        padding: 2px 8px;
        border-radius: 4px;
        margin-right: 5px;
        font-size: 0.8rem;
    }

    /* 6. Before/After 섹션 스타일 */
    .ba-container {
        border: 1px solid #333;
        background-color: #111;
        padding: 10px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .ba-label {
        color: #00E676 !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
        display: block;
    }

    /* 7. 버튼 스타일 */
    .stButton>button {
        width: 100%;
        background-color: #00E676;
        color: #000000 !important;
        font-size: 18px;
        font-weight: 900;
        padding: 15px 0;
        border-radius: 8px;
        border: none;
        margin-top: 10px;
    }
    .stButton>button:hover {
        background-color: #00C853;
        color: #000000 !important;
        transform: scale(1.02);
        transition: 0.2s;
    }
    
    /* 8. 가격 테이블 */
    .price-table {
        width: 100%;
        text-align: center;
        border-collapse: collapse;
        color: #FFFFFF;
        border: 1px solid #333;
    }
    .price-table th {
        background-color: #00E676;
        color: #000000;
        padding: 12px;
        font-weight: bold;
    }
    .price-table td {
        background-color: #121212;
        padding: 12px;
        border-bottom: 1px solid #333;
        color: #FFFFFF;
    }
    .price-best {
        background-color: #0A1F0A !important;
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
    st.image("https://placehold.co/600x150/000000/00E676?text=JAYEON+HANBANG", use_column_width=True)
    
    st.markdown("<h1 style='text-align: center;'>25년 데이터 기반 정밀 처방</h1>", unsafe_allow_html=True)
    
    # [권위 증명 섹션]
    st.markdown("""
    <div class='auth-box'>
        <span class='auth-badge'>SINCE 2001</span>
        <span class='auth-badge'>누적 2억 봉 돌파</span>
        <span class='auth-badge'>특허 3종 보유</span>
        <br><br>
        <p style='margin:0;'>자연과한의원은 검증된 데이터로 증명합니다.<br>
        100% 한약재, 무리한 절식 없는 <b>'지속 가능한 감량'</b>을 시작하세요.</p>
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
    cause = st.radio(
        "가장 해당되는 항목을 하나만 선택하세요.",
        [
            "A. 식욕 통제 불가 (배불러도 계속 먹음) ▶ [위열 과다]",
            "B. 물만 먹어도 붓고 몸이 무거움 ▶ [수독/순환장애]",
            "C. 식사량은 적은데 살이 안 빠짐 ▶ [대사 저하]",
            "D. 스트레스 받으면 폭식 ▶ [간기 울결]"
        ]
    )

    if st.button("다음: 내성 및 안전성 체크"):
        st.session_state.user_data.update({
            'height': height, 'weight': weight, 'age': age, 'gender': gender, 'cause': cause
        })
        st.session_state.step = 2
        st.rerun()

# [Phase 2: 리스크 관리 & 안전 장치]
elif st.session_state.step == 2:
    st.markdown("## 02. 약물 내성 및 민감도 테스트")
    st.markdown("""
    <div style='background-color:#111; padding:15px; border-radius:8px;'>
        <b style='color:#00E676;'>💡 2주 단위 처방 시스템</b><br>
        자연과한의원은 한 번에 많은 약을 주지 않습니다.<br>
        몸의 반응을 보고 <b>2주마다 단계를 조절</b>하여 부작용을 최소화합니다.
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

# [Phase 3: 처방 및 증명 - The Proof]
elif st.session_state.step == 3:
    data = st.session_state.user_data
    
    # 안전한 로딩
    with st.spinner("AI가 25년 임상 데이터를 기반으로 최적 처방을 매칭 중입니다..."):
        time.sleep(2.0)
    
    # 로직 설정
    is_max = "초고도 내성" in data.get('history', '')
    drug_name = "지방사약 MAX" if is_max else "지방사약 (Standard)"
    drug_level = "8단계 이상" if is_max else "3~5단계 (Standard)"
    
    cause_val = data.get('cause', '대사 저하')
    diagnosis_title = "대사 기능 저하형 비만"
    if "식욕" in cause_val: diagnosis_title = "위열(Stomach Heat) 과다형 비만"
    elif "스트레스" in cause_val: diagnosis_title = "스트레스성 간기 울결형"
    elif "부종" in cause_val: diagnosis_title = "수독(Water Poison) 정체형"
    
    # 1. 결과 요약
    st.markdown(f"## 📋 진단: <span style='color:#FF5252'>{diagnosis_title}</span>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='auth-box' style='text-align:left;'>
        <b>처방 솔루션: {drug_name}</b><br>
        • 특허받은 감량 조성물 3종 적용<br>
        • 2주 단위 정밀 용량 조절 (Titration)<br>
        • 90일 밀착 관리 가이드 제공
    </div>
    """, unsafe_allow_html=True)
    
    # 2. 비포 애프터 (NEW SECTION)
    st.markdown("### 👁 실제 감량 사례 (Before & After)")
    st.markdown("<div class='ba-container'>", unsafe_allow_html=True)
    col_b, col_a = st.columns(2)
    
    with col_b:
        st.markdown("<span class='ba-label'>BEFORE</span>", unsafe_allow_html=True)
        # 실제 사용 시 아래 URL을 실제 비포 사진으로 교체
        st.image("https://placehold.co/300x400/333333/FFFFFF?text=BEFORE", use_column_width=True)
        st.caption("체중: 78kg / 복부비만 심각")
        
    with col_a:
        st.markdown("<span class='ba-label'>AFTER (3개월)</span>", unsafe_allow_html=True)
        # 실제 사용 시 아래 URL을 실제 애프터 사진으로 교체
        st.image("https://placehold.co/300x400/00E676/000000?text=AFTER", use_column_width=True)
        st.caption("체중: 58kg (-20kg 감량)")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("※ 위 사례는 개인차가 있을 수 있으며, 자연과한의원 실제 환자 데이터입니다.")

    # 3. 가격 정책
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
        <td class="price-strike">180,000원</td>
        <td style="color:#FF5252; font-weight:bold;">150,000원</td>
        <td>5,000원</td>
      </tr>
      <tr class="price-best">
        <td>6개월 (Best)</td>
        <td class="price-strike">1,260,000원</td>
        <td style="color:#FF5252; font-weight:bold;">621,000원</td>
        <td style="color:#00E676; font-weight:bold;">3,450원 ✨</td>
      </tr>
    </table>
    """
    st.markdown(price_html, unsafe_allow_html=True)
    st.caption("※ 2억 봉 판매 돌파 기념, 6개월 패키지 최대 혜택 적용 중")
    
    # 4. 네트워크 (Scale Authority)
    with st.expander("🏥 전국 34개 지점 찾기 (네트워크 통합 관리)"):
        st.markdown("""
        **어느 지점에서나 동일한 프리미엄 서비스를 받으실 수 있습니다.**
        
        강남본점 | 신촌홍대점 | 명동을지로점 | 신림점 | 노원점 | 목동점 | 상봉점 | 은평연신내점 | 천호점 | 건대점 | 수원점 | 일산점 | 분당점 | 부천점 | 김포점 | 안산점 | 동탄점 | 안양평촌점 | 평택점 | 인천점 | 의정부점 | 부산서면점 | 부산센텀점 | 대구점 | 울산점 | 창원점 | 천안점 | 청주점 | 대전점 | 광주점 | 전주점 | 순천점 | 원주점 | 제주점
        """)

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
                    담당 한의사가 <b>{phone}</b>으로 연락드립니다.<br>
                    <b>[90일 가이드]</b>와 <b>[1:1 식단 팁]</b>도 함께 제공됩니다.
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.warning("성함과 연락처를 입력해주세요.")
