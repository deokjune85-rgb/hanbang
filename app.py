import streamlit as st
import time
import pandas as pd
import numpy as np
from datetime import datetime

# ---------------------------------------
# 0. 시스템 설정: Brand Identity (Easy, Fast, Safe)
# ---------------------------------------
st.set_page_config(
    page_title="자연과한의원 - 비대면 정밀 처방 시스템",
    page_icon="🌿",
    layout="centered"
)

# CSS: 브랜드 컬러(Deep Green)와 신뢰감을 주는 'Medical Clean' 테마
custom_css = """
<style>
    /* 전체 폰트 및 배경 */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp {
        background-color: #ffffff; /* Clean White for Trust */
        color: #333333;
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 헤더 스타일 */
    h1 {
        color: #2E7D32 !important; /* Jayeon Green */
        font-weight: 900;
        text-align: center;
        letter-spacing: -1px;
    }
    h2, h3 {
        color: #1B5E20 !important;
        font-weight: 700;
    }
    
    /* 강조 박스 (Info) */
    .info-box {
        background-color: #E8F5E9;
        border-left: 5px solid #2E7D32;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }

    /* 경고 박스 (Warning) */
    .warning-box {
        background-color: #FFEBEE;
        border-left: 5px solid #C62828;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    
    /* 제품 카드 스타일 */
    .product-card {
        border: 2px solid #2E7D32;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #ffffff 0%, #E8F5E9 100%);
    }

    /* 버튼 스타일 */
    .stButton>button {
        width: 100%;
        background-color: #2E7D32;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 15px; 0;
        border-radius: 8px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
        transform: scale(1.02);
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

# [Intro: 다이어트 자연주의 철학 설파]
if st.session_state.step == 0:
    st.image("https://placehold.co/600x150/2E7D32/FFFFFF?text=JAYEON+HANBANG+UNTACT", use_column_width=True)
    st.markdown("### 🌿 다이어트, 이제 '고통'이 아니라 '과학'입니다.")
    st.markdown("""
    <div class='info-box'>
        <b>"살을 빼는 과정이 왜 괴로워야 합니까?"</b><br>
        자연과한의원은 인위적인 식욕 억제가 아닌, 
        <b>신체 대사량을 자연스럽게 끌어올려</b> 
        숨만 쉬어도 에너지가 타는 몸을 만듭니다.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### ✅ 비대면 진료 프로세스 안내")
    st.markdown("""
    1. **AI 사전 문진**: 체질 및 내성(Tolerance) 분석
    2. **한의사 1:1 전화**: 처방 단계(Step) 최종 확정
    3. **익일 택배 발송**: '지방사약' 비대면 수령
    """)
    
    if st.button("내 몸에 맞는 '처방 단계' 확인하기"):
        st.session_state.step = 1
        st.rerun()

# [Phase 1: 결핍의 스캔 - 대사 고장 진단]
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

    st.markdown("---")
    st.markdown("**Q. 귀하의 다이어트가 매번 실패하는 근본 원인은?** (중복 선택 불가)")
    cause = st.radio(
        "가장 해당되는 항목을 하나만 선택하세요.",
        [
            "A. 식욕 통제 불가 (배불러도 계속 먹음) -> [위열]",
            "B. 물만 먹어도 붓고 몸이 무거움 -> [수독/부종]",
            "C. 식사량은 적은데 살이 안 빠짐 -> [대사 저하]",
            "D. 스트레스 받으면 폭식 -> [간기 울결]"
        ]
    )

    if st.button("다음: 내성 및 안전성 체크"):
        st.session_state.user_data.update({
            'height': height, 'weight': weight, 'age': age, 'gender': gender, 'cause': cause
        })
        st.session_state.step = 2
        st.rerun()

# [Phase 2: 리스크 관리 - 마황/카페인 내성 체크]
elif st.session_state.step == 2:
    st.markdown("## 02. 약물 내성 및 민감도 테스트")
    st.info("자연과한의원은 FDA 기준을 준수하며, 개인별 '최적 용량'을 찾기 위해 민감도를 체크합니다.")

    caffeine = st.radio(
        "Q. 평소 카페인(커피) 섭취 시 반응은?",
        ["전혀 영향 없음 (하루 3잔 이상 가능)", 
         "약간의 각성 효과 있음", 
         "심장이 두근거리고 잠을 못 잠 (민감성)"]
    )
    
    history = st.radio(
        "Q. 다이어트 양약/한약 복용 경험",
        ["없음 (Pure Type)", 
         "경험 있음 (약한 내성)", 
         "장기 복용 및 효과 미비 (초고도 내성 - 지방사약 MAX 필요)"]
    )
    
    # [Targeted Boosters] 
    st.markdown("**Q. 다이어트 중 특히 우려되는 증상이 있습니까? (보조 캡슐 매칭)**")
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

# [Phase 3: 처방 및 구원 - 가격 정책 및 솔루션]
elif st.session_state.step == 3:
    data = st.session_state.user_data
    
    # 로딩: 권위 부여
    msg_list = ["기초 대사량 분석 중...", "교감 신경 민감도 시뮬레이션...", "최적 처방 단계 매칭 중..."]
    bar = st.progress(0)
    status_text = st.empty()
    
    for i, msg in enumerate(msg_list):
        status_text.text(msg)
        time.sleep(0.8)
        bar.progress((i + 1) * 33)
    
    # 분석 로직
    is_max = "초고도 내성" in data['history']
    drug_name = "지방사약 MAX" if is_max else "지방사약 (Standard)"
    drug_level = "8단계 이상" if is_max else "3~5단계 (Standard)"
    
    # 진단명 매핑
    diagnosis_title = "대사 기능 저하형 비만"
    if "식욕" in data['cause']: diagnosis_title = "위열(Stomach Heat) 과다형 비만"
    if "스트레스" in data['cause']: diagnosis_title = "스트레스성 간기 울결형 비만"
    
    # 결과 화면
    st.markdown(f"## 📋 귀하의 비만 유형: [{diagnosis_title}]")
    st.markdown(f"""
    <div class='info-box'>
        귀하는 일반적인 운동으로는 체지방 분해가 어려운 상태입니다.<br>
        강제로 굶는 것이 아니라, <b>'대사 스위치'</b>를 켜야 합니다.
    </div>
    """, unsafe_allow_html=True)
    
    # 메인 처방 카드
    st.markdown("### 💊 1:1 맞춤 처방 솔루션")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("https://placehold.co/400x400/2E7D32/FFFFFF?text=Jibang+Sayak", caption=drug_name)
    with col2:
        st.markdown(f"#### **{drug_name}**")
        st.markdown(f"- **처방 강도**: {drug_level}")
        st.markdown(f"- **핵심 기전**: {data['cause'].split('->')[1] if '->' in data['cause'] else '대사 촉진'} 집중 케어")
        st.markdown("- **예상 반응**: 복용 30분 후 가벼운 열감과 심박수 증가 (운동 효과)")
        
        # 부스터 추천 (Upselling)
        if data['symptoms'] and "해당" not in data['symptoms'][0]:
            st.markdown("---")
            st.markdown("**➕ 추가 처방 (Option)**")
            for sym in data['symptoms']:
                if "수면" in sym: st.markdown("- **수면킬**: 수면 중 대사 유지 및 불면 완화")
                if "변비" in sym: st.markdown("- **독소킬**: 노폐물 배출 및 변비 해결")
                if "회식" in sym: st.markdown("- **지방킬**: 탄수화물 컷팅 방어 기제")

    # 가격 정책 (Volume Strategy)
    st.markdown("---")
    st.markdown("### 💰 합리적 비용 제안 (박리다매 정책)")
    st.info("💡 '지방사약'은 장기 복용 시 할인율이 급격히 높아집니다.")
    
    # 가격 테이블 구성
    price_html = """
    <table style="width:100%; text-align:center; border-collapse: collapse;">
      <tr style="background-color: #2E7D32; color: white;">
        <th style="padding: 10px;">기간</th>
        <th>정상가</th>
        <th>할인가 (Event)</th>
        <th>1일 비용</th>
      </tr>
      <tr>
        <td style="padding: 10px; border-bottom: 1px solid #ddd;">1개월</td>
        <td style="border-bottom: 1px solid #ddd; text-decoration: line-through; color: #999;">180,000원</td>
        <td style="border-bottom: 1px solid #ddd; font-weight: bold;">150,000원</td>
        <td style="border-bottom: 1px solid #ddd;">5,000원</td>
      </tr>
      <tr>
        <td style="padding: 10px; border-bottom: 1px solid #ddd;">3개월</td>
        <td style="border-bottom: 1px solid #ddd; text-decoration: line-through; color: #999;">540,000원</td>
        <td style="border-bottom: 1px solid #ddd; font-weight: bold; color: #C62828;">420,000원</td>
        <td style="border-bottom: 1px solid #ddd;">4,600원</td>
      </tr>
      <tr style="background-color: #E8F5E9; font-weight: bold;">
        <td style="padding: 10px;">6개월 (Best)</td>
        <td style="text-decoration: line-through; color: #999;">1,260,000원</td>
        <td style="color: #C62828;">621,000원</td>
        <td>3,450원 ✨</td>
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
                <div class='info-box'>
                    담당 한의사가 <b>{phone}</b>으로 10분 내에 연락드립니다.<br>
                    비대면 진료 후, 오늘 오후에 택배가 발송됩니다.
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.warning("성함과 연락처를 입력해주세요.")
