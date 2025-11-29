import streamlit as st
import time
import random
import pandas as pd
import numpy as np

# ---------------------------------------
# 0. 시스템 설정: 권위와 공포의 테마
# ---------------------------------------
st.set_page_config(
    page_title="자연과한의원 - AI 체질 정밀 분석",
    page_icon="🧬",
    layout="centered"
)

# CSS: 병원 수술실처럼 차갑고 전문적인 '메디컬 다크' 테마
custom_css = """
<style>
    /* 전체 배경 및 폰트 */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 헤더 스타일 */
    h1, h2, h3 {
        color: #4CAF50 !important; /* Medical Green */
        font-weight: 800;
    }
    
    /* 강조 텍스트 (위험) */
    .warning-text {
        color: #FF4B4B;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    /* 강조 텍스트 (핵심) */
    .highlight-text {
        color: #4CAF50;
        font-weight: bold;
        font-size: 1.1rem;
    }

    /* 버튼 스타일 (권위적) */
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 15px;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }

    /* 박스 스타일 */
    .diagnosis-box {
        border: 2px solid #333;
        background-color: #161B22;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    /* 거절 메시지 박스 */
    .reject-box {
        border: 2px solid #FF4B4B;
        background-color: #2D0E0E;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255, 75, 75, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 1. 상태 관리 (Session State)
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
    st.image("https://placehold.co/600x200/000000/4CAF50?text=Nature+Clinic+AI+Diagnosis", use_column_width=True) # 로고 플레이스홀더
    st.markdown("<h1 style='text-align: center;'>AI 비만 유형 정밀 진단</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <p>본 시스템은 단순한 체중 감량이 아닌,<br>
        <b>'살이 찌는 근본 원인(Root Cause)'</b>을 의학적으로 분석합니다.</p>
        <p class='warning-text'>※ 경고: 분석 결과에 따라 처방이 거절될 수 있습니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("정밀 진단 시작하기 (소요시간 1분)"):
        st.session_state.step = 1
        st.rerun()

# [Phase 1: 생체 데이터 - The Baseline]
elif st.session_state.step == 1:
    st.markdown("### 1. 기본 생체 데이터 분석")
    st.progress(25)
    
    gender_cycle = st.radio(
        "귀하의 현재 생애 주기는?",
        ["남성 (복부/내장지방 집중형)", 
         "여성 - 2030 미혼 (급속 감량 희망)", 
         "여성 - 출산 후 (산후 비만/부종)", 
         "여성 - 갱년기/완경 이후 (나잇살/호르몬성 비만)"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("신장 (cm)", 140, 200, 160)
    with col2:
        weight = st.number_input("현재 체중 (kg)", 40, 150, 60)
        
    goal_weight = st.number_input("목표 체중 (kg)", 35, 100, 48)
    
    if st.button("다음 단계 >"):
        st.session_state.user_data.update({
            'cycle': gender_cycle,
            'height': height,
            'weight': weight,
            'goal': goal_weight
        })
        st.session_state.step = 2
        st.rerun()

# [Phase 2: 원인 규명 - The Trap]
elif st.session_state.step == 2:
    st.markdown("### 2. 체질 및 원인 분석")
    st.progress(50)
    
    cause = st.radio(
        "Q. 귀하가 살이 찌는 가장 큰 원인은? (가장 공감되는 것)",
        ["[식탐형] 배가 불러도 계속 들어간다. (위장 열독)",
         "[부종형] 물만 먹어도 붓고, 저녁에 꽉 낀다. (순환 장애)",
         "[스트레스형] 화가 나면 폭식한다. (간기 울결)",
         "[대사저하형] 적게 먹어도 안 빠진다. (기초대사량 부족)"]
    )
    
    area = st.radio(
        "Q. 가장 시급하게 해결해야 할 '저주받은 부위'는?",
        ["[러브핸들] 바지 위로 튀어나오는 옆구리살",
         "[ET배] 팔다리는 가는데 배만 뽈록 나온 내장지방",
         "[승마살] 허벅지 안쪽과 엉덩이 밑살",
         "[안녕살] 팔뚝이 쳐져서 반팔 입기가 두려움"]
    )
    
    if st.button("다음 단계 >"):
        st.session_state.user_data.update({'cause': cause, 'area': area})
        st.session_state.step = 3
        st.rerun()

# [Phase 3: 자격 검증 - The Kick Out]
elif st.session_state.step == 3:
    st.markdown("### 3. 내성 및 처방 적합도 판정")
    st.progress(75)
    
    history = st.radio(
        "Q. 다이어트 약물(양약/한약) 복용 경험",
        ["없음 (순수 체질)",
         "1~2회 경험 있음 (일반 내성)",
         "수십 번 반복, 효과 없었음 (초고도 내성/정체기)"]
    )
    
    if "수십 번" in history:
        st.warning("⚠️ 경고: 초고도 내성이 의심됩니다. 일반 처방으로는 효과를 보기 어렵습니다.")

    st.markdown("---")
    st.markdown("**Q. 지방사약 처방 전, 귀하의 각오를 확인합니다.**")
    willpower = st.radio(
        "솔직하게 답변하십시오.",
        ["운동/식단 병행하며 확실하게 뺄 것이다. (적합)",
         "노력은 하겠지만, 약의 도움이 절실하다. (적합)",
         "솔직히 아무 노력 없이 약만 먹고 빼고 싶다. (부적합)"]
    )
    
    if st.button("진단 결과 확인"):
        # [KICK-OUT LOGIC] : 3번 선택 시 거절 처리
        if "아무 노력 없이" in willpower:
            st.session_state.step = 999 # 거절 페이지
        else:
            st.session_state.user_data.update({'history': history, 'willpower': willpower})
            st.session_state.step = 4   # 결과 페이지
        st.rerun()

# [Phase 3-B: 거절 페이지 - The Rejection]
elif st.session_state.step == 999:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='reject-box'>
        <h2 style='color: #FF4B4B;'>🚫 처방 불가 판정</h2>
        <p>죄송합니다. 귀하의 답변을 분석한 결과,<br>
        현재 단계에서는 <b>'지방사약'</b> 처방이 불가능합니다.</p>
        <hr style='border-color: #555;'>
        <p style='font-size: 0.9rem;'>
        저희는 고객님의 돈보다 건강한 감량을 최우선으로 생각합니다.<br>
        약물에만 의존하려는 상태에서는 요요현상이 100% 발생합니다.<br>
        최소한의 식단 조절 의지가 생기셨을 때, 다시 방문해 주십시오.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("다시 솔직하게 진단받기"):
        st.session_state.step = 3
        st.rerun()

# [Phase 4: 결과 및 구원 - The Salvation]
elif st.session_state.step == 4:
    # 로딩 애니메이션 (분석하는 척)
    with st.spinner("AI가 귀하의 생체 데이터를 분석 중입니다... (체질/대사량/감량예
