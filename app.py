import streamlit as st
import time
import pandas as pd
import numpy as np

# ---------------------------------------
# 0. 시스템 설정: Dark & Neon Green Theme
# ---------------------------------------
st.set_page_config(
    page_title="자연과한의원 - 비대면 정밀 처방",
    page_icon="🌿",
    layout="centered"
)

# [CSS: 완벽한 블랙 & 화이트 가독성 최적화]
custom_css = """
<style>
    /* 1. 메인 배경 및 폰트 컬러 강제 적용 */
    .stApp {
        background-color: #000000 !important; /* 리얼 블랙 */
        color: #FFFFFF !important; /* 리얼 화이트 */
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 2. 헤더 스타일 (형광 그린으로 권위 강조) */
    h1, h2, h3 {
        color: #00E676 !important; /* Neon Green */
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    /* 3. 일반 텍스트 및 라벨 강제 화이트 */
    p, span, div, label, .stMarkdown, .stText {
        color: #E0E0E0 !important;
    }
    
    /* 4. 입력 필드 스타일 (어두운 배경에 흰 글씨) */
    .stTextInput > div > div > input, 
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #333;
    }
    
    /* 5. 라디오/체크박스 선택 항목 스타일 */
    .stRadio label {
        color: #FFFFFF !important;
        font-size: 16px;
    }

    /* 6. 정보 박스 (다크 모드 전용) */
    .info-box {
        background-color: #111111;
        border: 1px solid #333;
        border-left: 5px solid #00E676; /* 포인트 컬러 */
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        color: #FFFFFF !important;
    }

    /* 7. 버튼 스타일 (네온 그린) */
    .stButton>button {
        width: 100%;
        background-color: #00E676; /* 버튼 색상 */
        color: #000000 !important; /* 버튼 글씨는 검정 */
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
    }
    
    /* 8. 가격 테이블 스타일 */
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
    .price-strike {
        text-decoration: line-through;
        color: #666 !important;
    }
    .price-discount {
        color: #FF5252 !important; /* 형광 레드 */
        font-weight: bold;
    }
    .price-best {
        background-color: #0A1F0A !important; /* 아주 어두운 그린 배경 */
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

# [Intro]
if st.session_state.step == 0:
    st.image("https://placehold.co/600x150/000000/00E676?text=JAYEON+HANBANG", use_column_width=True)
    
    st.markdown("<h1 style='text-align: center;'>비대면 처방 정밀 진단</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    <div class='info-box'>
        <h4 style='color: #00E676; margin:0;'>🌿 다이어트 자연주의 (Diet Naturalism)</h4>
        <br>
        <p>인위적인 식욕 억제제는 뇌를 망가뜨립니다.<br>
        자연과한의원은 <b>'순수 한약재'</b>를 통해 대사량을 높여<br>
        숨만 쉬어도 에너지가 소비되는 <b>'살이 안 찌는 체질'</b>로 변화시킵니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✅ 비대면 진료 프로세스")
    st.info("1. AI 사전 문진 ➔ 2. 한의사 전화 진료 ➔ 3. 익일 택배 도착")
    
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
            "A. 식욕 통제 불가 (배불러도 계속 먹음) ▶ [위열]",
            "B. 물만 먹어도 붓고 몸이 무거움 ▶ [수독/부종]",
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

# [Phase 2: 리스크 관리]
elif st.session_state.step == 2:
    st.markdown("## 02. 약물 내성 및 민감도 테스트")
    st.markdown("""
    <div class='info-box'>
        FDA 기준을 준수하며, 개인별 <b>'최적 용량'</b>을 찾기 위해 민감도를 체크합니다.
    </div>
    """, unsafe_allow_html=True)

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
         "장기 복용 및 효과 미비 (초고도 내성 ➔ MAX 필요)"]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Q. 다이어트 중 우려되는 증상 (보조 캡슐 매칭)**")
    symptoms = st.multiselect(
        "해당되는 증상을 모두 선택하세요.",
        ["수면 장애/불면증 (수면킬 필요)", 
         "심한 변비 (독소킬 필요)", 
         "잦은 회식/음주 (지방킬 필요)", 
         "해당 사항 없음"]
    )

    if st.button("AI 정밀 처방 결과 보기"):
        st.session_state.user_data.update({
            'caffeine': caffeine, 'history': history, 'symptoms': symptoms
        })
        st.session_state.step = 3
        st.rerun()

# [Phase 3: 처방 및 구원 - 안정화 버전]
elif st.session_state.step == 3:
    data = st.session_state.user_data
    
    # [FIX]: DOM 충돌 방지를 위해 반복문 애니메이션 제거하고 안전한 spinner 사용
    with st.spinner("AI가 교감 신경 민감도와 대사량을 분석 중입니다..."):
        time.sleep(2.0)
    
    # 분석 로직
    is_max = "초고도 내성" in data.get('history', '')
    drug_name = "지방사약 MAX" if is_max else "지방사약 (Standard)"
    drug_level = "8단계 이상" if is_max else "3~5단계 (Standard)"
    
    cause_val = data.get('cause', '대사 저하')
    diagnosis_title = "대사 기능 저하형 비만"
    if "식욕" in cause_val: diagnosis_title = "위열(Stomach Heat) 과다형 비만"
    elif "스트레스" in cause_val: diagnosis_title = "스트레스성 간기 울결형 비만"
    elif "부종" in cause_val: diagnosis_title = "수독(Water Poison) 정체형 비만"
    
    # 결과 화면
    st.markdown(f"## 📋 비만 유형: <span style='color:#FF5252'>{diagnosis_title}</span>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='info-box'>
        <p>귀하는 일반적인 운동으로는 체지방 분해가 어려운 상태입니다.<br>
        강제로 굶는 것이 아니라, <b>'대사 스위치'</b>를 켜야 합니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 메인 처방 카드
    st.markdown("### 💊 1:1 맞춤 처방 솔루션")
    
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image("https://placehold.co/400x400/111111/00E676?text=FAT+KILLER", caption=drug_name)
    with col2:
        st.markdown(f"<h3 style='color:#00E676'>{drug_name}</h3>", unsafe_allow_html=True)
        st.markdown(f"- **처방 강도**: {drug_level}")
        st.markdown(f"- **핵심 기전**: {cause_val.split('▶')[0][:10]}... 집중 케어")
        st.markdown("- **예상 반응**: 복용 30분 후 가벼운 열감 (운동 효과)")
        
        # 보조제 추천
        if data.get('symptoms') and "해당" not in data['symptoms'][0]:
            st.markdown("<hr style='border-top: 1px solid #333;'>", unsafe_allow_html=True)
            st.markdown("**➕ 추가 처방 (Option)**")
            for sym in data['symptoms']:
                if "수면" in sym: st.markdown("- <span style='color:#AAA'>수면킬: 수면 중 대사 유지</span>", unsafe_allow_html=True)
                if "변비" in sym: st.markdown("- <span style='color:#AAA'>독소킬: 노폐물 배출</span>", unsafe_allow_html=True)
                if "회식" in sym: st.markdown("- <span style='color:#AAA'>지방킬: 탄수화물 컷팅</span>", unsafe_allow_html=True)

    # 가격 정책 (HTML Table - Dark Mode)
    st.markdown("---")
    st.markdown("### 💰 합리적 비용 제안 (박리다매 정책)")
    
    price_html = """
    <table class="price-table">
      <tr>
        <th>기간</th>
        <th>정상가</th>
        <th>할인가 (Event)</th>
        <th>1일 비용</th>
      </tr>
      <tr>
        <td>1개월</td>
        <td class="price-strike">180,000원</td>
        <td class="price-discount">150,000원</td>
        <td>5,000원</td>
      </tr>
      <tr>
        <td>3개월</td>
        <td class="price-strike">540,000원</td>
        <td class="price-discount">420,000원</td>
        <td>4,600원</td>
      </tr>
      <tr class="price-best">
        <td>6개월 (Best)</td>
        <td class="price-strike">1,260,000원</td>
        <td class="price-discount">621,000원</td>
        <td style="color:#00E676; font-weight:bold;">3,450원 ✨</td>
      </tr>
    </table>
    """
    st.markdown(price_html, unsafe_allow_html=True)
    st.caption("※ 6개월 패키지 선택 시 커피 한 잔 값(3,450원)으로 관리가 가능합니다.")
    
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
                <div class='info-box' style='border-color:#00E676;'>
                    담당 한의사가 <b>{phone}</b>으로 10분 내에 연락드립니다.<br>
                    비대면 진료 후, 오늘 오후에 택배가 발송됩니다.
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.warning("성함과 연락처를 입력해주세요.")
