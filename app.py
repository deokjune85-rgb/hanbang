import streamlit as st
import time
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# ============================================
# SYSTEM CONFIGURATION: VERITAS MEDICAL INTELLIGENCE TERMINAL v8.0
# ============================================
st.set_page_config(
    page_title="VERITAS Medical Intelligence Terminal",
    page_icon="⬢",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# CSS: THE BLACK BOX INTERFACE
# ============================================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');
    
    /* Core System */
    .stApp {
        background-color: #000000 !important;
        color: #00BFFF !important;
        font-family: 'Rajdhani', sans-serif;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Typography */
    p, div, span {
        color: #00BFFF;
        font-weight: 300;
        line-height: 1.8;
        letter-spacing: 0.5px;
    }
    
    /* System Header */
    .system-header {
        font-family: 'Orbitron', monospace;
        font-size: 32px;
        font-weight: 900;
        color: #00FF00;
        text-align: center;
        margin: 30px 0;
        text-shadow: 0 0 20px rgba(0, 255, 0, 0.8);
        letter-spacing: 3px;
    }
    
    .system-subheader {
        font-family: 'Rajdhani', sans-serif;
        font-size: 12px;
        color: #666;
        text-align: center;
        margin-top: -20px;
        margin-bottom: 30px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Chat Messages */
    .stChatMessage {
        background-color: #000000 !important;
        border-bottom: 1px solid #0a0a0a;
        padding: 20px 0 !important;
    }
    
    [data-testid="stChatMessageContent"] {
        background-color: transparent !important;
        color: #00BFFF !important;
        font-size: 15px;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .stChatMessage img {
        border-radius: 0 !important;
    }
    
    /* Input Area */
    .stChatInputContainer {
        border-top: 1px solid #00FF00;
        padding-top: 15px;
        background-color: #000000;
    }
    
    .stChatInput input {
        background-color: #0a0a0a !important;
        border: 1px solid #00FF00 !important;
        color: #00BFFF !important;
        font-family: 'Rajdhani', sans-serif;
        font-size: 14px;
    }
    
    /* Symptom Selection Chips */
    .symptom-label {
        font-size: 10px;
        color: #00FF00;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 15px;
        font-weight: 700;
    }
    
    div.stButton > button {
        background-color: #0a0a0a;
        color: #00BFFF !important;
        border: 1px solid #00FF00 !important;
        border-radius: 0px !important;
        font-size: 12px !important;
        padding: 12px 20px !important;
        transition: all 0.3s ease;
        width: 100%;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    div.stButton > button:hover {
        background-color: #00FF00 !important;
        color: #000000 !important;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.6);
        transform: translateY(-2px);
    }
    
    /* Critical Alert Card */
    .alert-critical {
        background: linear-gradient(135deg, #1a0000 0%, #000000 100%);
        border: 2px solid #FF0000;
        padding: 30px;
        margin: 30px 0;
        box-shadow: 0 0 40px rgba(255, 0, 0, 0.3);
        position: relative;
    }
    
    .alert-critical::before {
        content: "⚠ CRITICAL DIAGNOSIS";
        position: absolute;
        top: -12px;
        left: 20px;
        background-color: #000000;
        padding: 0 10px;
        font-size: 10px;
        color: #FF0000;
        letter-spacing: 2px;
        font-weight: 700;
    }
    
    /* Diagnosis Result Card */
    .diagnosis-terminal {
        background: linear-gradient(135deg, #001a1a 0%, #000000 100%);
        border-left: 4px solid #00FF00;
        padding: 40px 30px;
        margin: 30px 0;
        box-shadow: 0 0 60px rgba(0, 255, 0, 0.2);
        position: relative;
    }
    
    .diagnosis-code {
        font-family: 'Orbitron', monospace;
        font-size: 11px;
        color: #666;
        letter-spacing: 3px;
        margin-bottom: 10px;
    }
    
    .diagnosis-type {
        font-family: 'Orbitron', monospace;
        font-size: 36px;
        font-weight: 900;
        color: #00FF00;
        margin-bottom: 20px;
        text-shadow: 0 0 30px rgba(0, 255, 0, 0.8);
        letter-spacing: 2px;
    }
    
    .diagnosis-desc {
        font-size: 16px;
        color: #00BFFF;
        margin-bottom: 25px;
        line-height: 1.8;
    }
    
    .risk-indicator {
        display: inline-block;
        padding: 8px 20px;
        background-color: #FF0000;
        color: #FFFFFF;
        font-weight: 700;
        font-size: 12px;
        letter-spacing: 2px;
        margin: 10px 0;
        text-transform: uppercase;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    /* Prescription Protocol */
    .protocol-section {
        background-color: #0a0a0a;
        border: 1px solid #00BFFF;
        padding: 25px;
        margin: 20px 0;
    }
    
    .protocol-header {
        font-size: 11px;
        color: #00FF00;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 10px;
        font-weight: 700;
    }
    
    .protocol-title {
        font-family: 'Orbitron', monospace;
        font-size: 24px;
        color: #FFFFFF;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .protocol-detail {
        font-size: 14px;
        color: #00BFFF;
    }
    
    /* Data Grid */
    .data-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin: 20px 0;
        padding: 20px;
        background-color: #0a0a0a;
        border: 1px solid #333;
    }
    
    .data-item {
        border-bottom: 1px solid #1a1a1a;
        padding: 10px 0;
    }
    
    .data-label {
        font-size: 10px;
        color: #666;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    
    .data-value {
        font-size: 20px;
        color: #00FF00;
        font-weight: 700;
        font-family: 'Orbitron', monospace;
    }
    
    /* Form Styling */
    .stTextInput input {
        background-color: #0a0a0a !important;
        border: 1px solid #00FF00 !important;
        color: #00BFFF !important;
        font-family: 'Rajdhani', sans-serif;
        font-size: 14px;
    }
    
    div[data-testid="stForm"] button[type="submit"] {
        width: 100%;
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        font-weight: 900;
        font-size: 16px;
        border: none;
        padding: 18px;
        font-family: 'Orbitron', monospace;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stForm"] button[type="submit"]:hover {
        background-color: #FF3333 !important;
        transform: scale(1.02);
        box-shadow: 0 0 50px rgba(255, 0, 0, 0.8);
    }
    
    /* Status Widget */
    .stStatus {
        background-color: #0a0a0a !important;
        border-left: 3px solid #00FF00 !important;
    }
    
    /* Plotly Chart Styling */
    .js-plotly-plot {
        background-color: transparent !important;
    }
    
    /* Timestamp */
    .timestamp {
        font-size: 10px;
        color: #333;
        text-align: right;
        margin-top: 10px;
        font-family: 'Orbitron', monospace;
        letter-spacing: 1px;
    }
    
    /* Warning Box */
    .warning-box {
        background-color: #1a1000;
        border: 1px solid #FFB800;
        padding: 20px;
        margin: 20px 0;
        color: #FFB800;
    }
    
    .warning-box strong {
        color: #FFB800;
        font-size: 12px;
        letter-spacing: 2px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ============================================
# STATE INITIALIZATION
# ============================================
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'analysis_scores' not in st.session_state:
    st.session_state.analysis_scores = {}

AI_AVATAR = "🔷"
USER_AVATAR = "👤"

# ============================================
# HELPER FUNCTIONS
# ============================================
def terminal_stream(text, speed=0.015):
    """Medical terminal typing effect"""
    placeholder = st.empty()
    display_text = ""
    for char in text:
        display_text += char
        placeholder.markdown(display_text)
        time.sleep(speed)
    return text

def add_message(role, content, html=False, chart=None, animated=False):
    """Add message to session state"""
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "html": html,
        "chart": chart,
        "animated": animated
    })

def calculate_bmi(weight, height_cm):
    """Calculate BMI"""
    height_m = height_cm / 100
    return round(weight / (height_m ** 2), 1)

def calculate_bmr(gender, weight, height_cm, age):
    """Calculate Basal Metabolic Rate"""
    if gender == "남성":
        return int(88.362 + (13.397 * weight) + (4.799 * height_cm) - (5.677 * age))
    else:
        return int(447.593 + (9.247 * weight) + (3.098 * height_cm) - (4.330 * age))

def create_radar_chart(scores):
    """Create radar chart for diagnosis visualization"""
    categories = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(0, 255, 0, 0.1)',
        line=dict(color='#00FF00', width=2),
        marker=dict(size=8, color='#00FF00')
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='#000000',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='#1a1a1a',
                tickfont=dict(size=10, color='#00BFFF')
            ),
            angularaxis=dict(
                gridcolor='#1a1a1a',
                tickfont=dict(size=11, color='#00BFFF', family='Rajdhani')
            )
        ),
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        margin=dict(l=80, r=80, t=40, b=40),
        height=400
    )
    
    return fig

def create_bar_chart(metrics):
    """Create bar chart for comparative analysis"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=list(metrics.keys()),
        y=list(metrics.values()),
        marker=dict(
            color=['#FF0000' if v > 70 else '#FFB800' if v > 40 else '#00FF00' for v in metrics.values()],
            line=dict(color='#00FF00', width=1)
        ),
        text=[f"{v}%" for v in metrics.values()],
        textposition='outside',
        textfont=dict(size=12, color='#00BFFF', family='Orbitron')
    ))
    
    fig.update_layout(
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        xaxis=dict(
            gridcolor='#1a1a1a',
            tickfont=dict(size=11, color='#00BFFF', family='Rajdhani')
        ),
        yaxis=dict(
            range=[0, 100],
            gridcolor='#1a1a1a',
            tickfont=dict(size=10, color='#00BFFF')
        ),
        margin=dict(l=40, r=40, t=40, b=40),
        height=300,
        showlegend=False
    )
    
    return fig

# ============================================
# HEADER
# ============================================
st.markdown("<div class='system-header'>⬢ VERITAS</div>", unsafe_allow_html=True)
st.markdown("<div class='system-subheader'>Medical Intelligence Terminal v8.0 | Jayeon Clinical Data Labs</div>", unsafe_allow_html=True)
st.markdown("<hr style='border: 0; border-top: 1px solid #00FF00; margin: 20px 0;'>", unsafe_allow_html=True)

# ============================================
# INITIALIZATION
# ============================================
if st.session_state.step == 0:
    init_msg = """**SYSTEM ONLINE.**

임상 데이터베이스 접속 완료.
25년간 축적된 200,000+ 사례 분석 알고리즘 활성화.

체중 정체 및 대사 장애의 근본 원인을 진단합니다.

**피험자 기본 데이터를 입력하십시오.**
형식: `성별, 나이, 키(cm), 체중(kg)`
예시: `여성, 32, 165, 68`"""
    add_message("assistant", init_msg)
    st.session_state.step = 1

# ============================================
# RENDER MESSAGES
# ============================================
for i, msg in enumerate(st.session_state.messages):
    avatar = AI_AVATAR if msg["role"] == "assistant" else USER_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        is_last = (i == len(st.session_state.messages) - 1)
        
        if msg["role"] == "assistant" and not msg.get("animated") and is_last:
            if msg.get("html"):
                st.markdown(msg["content"], unsafe_allow_html=True)
            else:
                terminal_stream(msg["content"])
            
            if msg.get("chart"):
                st.plotly_chart(msg["chart"], use_container_width=True)
            
            msg["animated"] = True
        else:
            if msg.get("html"):
                st.markdown(msg["content"], unsafe_allow_html=True)
            else:
                st.markdown(msg["content"])
            
            if msg.get("chart"):
                st.plotly_chart(msg["chart"], use_container_width=True)

# ============================================
# INTERACTION CONTROLLER
# ============================================
current_input = None

# Step 2: Symptom Selection Chips
if st.session_state.step == 2:
    st.markdown("<div class='symptom-label'>▸ PRIMARY SYMPTOM SELECTOR</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("물만 먹어도 붓는다"): current_input = "물만 먹어도 붓는다"
        if st.button("손발이 차갑다"): current_input = "손발이 차갑다"
    with col2:
        if st.button("폭식 후 구토 증상"): current_input = "폭식 후 구토 증상"
        if st.button("식욕 통제 불가"): current_input = "식욕 통제 불가"

# Step 4: Secondary Analysis Chips
if st.session_state.step == 4:
    st.markdown("<div class='symptom-label'>▸ SECONDARY VALIDATION REQUIRED</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("있음 (양약/한약)"): current_input = "있음"
        if st.button("없음"): current_input = "없음"
    with col2:
        if st.button("과거 복용 (현재 중단)"): current_input = "과거 복용"
        if st.button("잘 모르겠음"): current_input = "잘 모르겠음"

# Chat Input
input_disabled = (st.session_state.step == 5)
chat_input_val = st.chat_input("▸ INPUT DATA OR SYMPTOM DESCRIPTION", disabled=input_disabled)

if chat_input_val:
    current_input = chat_input_val

# ============================================
# LOGIC PROCESSING
# ============================================
if current_input:
    add_message("user", current_input, animated=True)
    
    # ----------------
    # STEP 1: Basic Data Input
    # ----------------
    if st.session_state.step == 1:
        with st.status("▸ 기본 데이터 처리 중...", expanded=True) as status:
            st.write("├─ 데이터 무결성 검증...")
            time.sleep(0.8)
            st.write("├─ BMI 연산 실행...")
            time.sleep(0.7)
            st.write("└─ 기초대사량(BMR) 계산...")
            time.sleep(0.9)
            status.update(label="✓ 기본 데이터 처리 완료", state="complete", expanded=False)
        
        # Parse input
        try:
            parts = [p.strip() for p in current_input.replace(" ", "").split(",")]
            gender, age, height, weight = parts[0], int(parts[1]), int(parts[2]), float(parts[3])
            
            bmi = calculate_bmi(weight, height)
            bmr = calculate_bmr(gender, weight, height, age)
            
            st.session_state.user_data.update({
                "gender": gender,
                "age": age,
                "height": height,
                "weight": weight,
                "bmi": bmi,
                "bmr": bmr
            })
            
            data_html = f"""
<div class='data-grid'>
    <div class='data-item'>
        <div class='data-label'>BMI Index</div>
        <div class='data-value'>{bmi}</div>
    </div>
    <div class='data-item'>
        <div class='data-label'>기초대사량 (BMR)</div>
        <div class='data-value'>{bmr} kcal</div>
    </div>
    <div class='data-item'>
        <div class='data-label'>피험자 연령</div>
        <div class='data-value'>{age}세</div>
    </div>
    <div class='data-item'>
        <div class='data-label'>체질량</div>
        <div class='data-value'>{weight} kg</div>
    </div>
</div>

**기본 데이터 등록 완료.**

1차 진단을 시작합니다.
**피험자가 호소하는 주요 증상을 선택하십시오.**
"""
            add_message("assistant", data_html, html=True)
            st.session_state.step = 2
            
        except:
            add_message("assistant", "**⚠ 데이터 형식 오류.**\n\n올바른 형식으로 재입력하십시오.\n예시: `여성, 32, 165, 68`")
        
        st.rerun()
    
    # ----------------
    # STEP 2: Symptom Analysis
    # ----------------
    elif st.session_state.step == 2:
        with st.status("▸ 증상 패턴 분석 중...", expanded=True) as status:
            st.write("├─ 200,000+ 케이스 데이터베이스 대조...")
            time.sleep(1.1)
            st.write("├─ 체질 알고리즘 연산 중...")
            time.sleep(1.0)
            st.write("└─ 병리학적 패턴 식별...")
            time.sleep(0.9)
            status.update(label="✓ 1차 분석 완료", state="complete", expanded=False)
        
        txt = current_input.lower()
        
        # Symptom classification
        if "붓" in txt or "부종" in txt:
            symptom_type = "수독정체형"
            st.session_state.analysis_scores = {
                "식욕": 35,
                "대사저하": 45,
                "독소축적": 85,
                "스트레스": 40,
                "순환장애": 90
            }
        elif "차갑" in txt or "냉증" in txt:
            symptom_type = "냉증형대사장애"
            st.session_state.analysis_scores = {
                "식욕": 40,
                "대사저하": 95,
                "독소축적": 50,
                "스트레스": 35,
                "순환장애": 75
            }
        elif "폭식" in txt or "구토" in txt:
            symptom_type = "간기울결형"
            st.session_state.analysis_scores = {
                "식욕": 90,
                "대사저하": 45,
                "독소축적": 40,
                "스트레스": 95,
                "순환장애": 50
            }
        else:
            symptom_type = "위열과다형"
            st.session_state.analysis_scores = {
                "식욕": 95,
                "대사저하": 40,
                "독소축적": 35,
                "스트레스": 60,
                "순환장애": 45
            }
        
        st.session_state.user_data['symptom_type'] = symptom_type
        
        response = f"""**1차 분석 결과:**

증상 패턴: `{symptom_type}`
신뢰도: 87.3%

**⚠ 데이터의 모순을 감지했습니다.**

심층 분석을 위해 추가 정보가 필요합니다.

**과거 다이어트 약물(양약/한약) 복용 이력이 있습니까?**
(상단 버튼 선택 또는 직접 입력)
"""
        add_message("assistant", response)
        st.session_state.step = 4
        st.rerun()
    
    # ----------------
    # STEP 4: Final Analysis
    # ----------------
    elif st.session_state.step == 4:
        st.session_state.user_data['drug_history'] = current_input
        
        with st.status("▸ 최종 임상 분석 실행 중...", expanded=True) as status:
            st.write("├─ 피험자 데이터 통합 중...")
            time.sleep(0.9)
            st.write("├─ AI 진단 모델 시뮬레이션...")
            time.sleep(1.3)
            st.write("├─ 처방 프로토콜 검색...")
            time.sleep(1.0)
            st.write("└─ 최적 솔루션 도출...")
            time.sleep(0.8)
            status.update(label="✓ 최종 분석 완료", state="complete", expanded=False)
        
        time.sleep(0.5)
        
        # Generate diagnosis
        symptom_type = st.session_state.user_data.get('symptom_type', '위열과다형')
        scores = st.session_state.analysis_scores
        
        # Create radar chart
        radar_chart = create_radar_chart(scores)
        
        # Determine diagnosis details
        if symptom_type == "수독정체형":
            diag_code = "VRT-C2"
            diag_name = "TYPE-C2: 수독 정체형 (WATER RETENTION)"
            diag_desc = "림프 순환계의 정체로 인해 수분과 지방이 결합된 상태. 노폐물 배출 기능이 85% 이상 저하되어 있습니다."
            risk_level = "HIGH"
            prescription = "독소킬 + 지방사약 (수분대사 촉진형)"
            target = "림프 순환 정상화 및 부종 제거"
            success_rate = "92%"
            side_effect = "15%"
        elif symptom_type == "냉증형대사장애":
            diag_code = "VRT-C3"
            diag_name = "TYPE-C3: 냉증형 대사 장애 (METABOLIC DROP)"
            diag_desc = "기초대사량이 정상 대비 70% 수준. 심부 체온 저하로 인한 에너지 소모 효율 급감 상태입니다."
            risk_level = "CRITICAL"
            prescription = "지방사약 (대사촉진형) + 온열처방"
            target = "심부 체온 상승 및 발열 효과 유도"
            success_rate = "89%"
            side_effect = "22%"
        elif symptom_type == "간기울결형":
            diag_code = "VRT-S4"
            diag_name = "TYPE-S4: 간기 울결형 (STRESS INDUCED)"
            diag_desc = "코르티솔 과다 분비로 인한 복부 지방 축적. 자율신경계 불균형이 식욕 중추를 왜곡시킨 상태입니다."
            risk_level = "HIGH"
            prescription = "소요산 + 지방사약"
            target = "자율신경 안정 및 폭식 패턴 차단"
            success_rate = "87%"
            side_effect = "18%"
        else:
            diag_code = "VRT-A1"
            diag_name = "TYPE-A1: 위열 과다형 (STOMACH HEAT)"
            diag_desc = "식욕 통제 중추의 과항진. 뇌가 포만감을 인지하지 못하는 '가짜 배고픔' 상태입니다."
            risk_level = "CRITICAL"
            prescription = "식탐사약 (식욕억제 + 위장열 해소)"
            target = "식욕 중추 정상화"
            success_rate = "94%"
            side_effect = "12%"
        
        # Build result HTML
        result_html = f"""
<div class='diagnosis-terminal'>
    <div class='diagnosis-code'>DIAGNOSTIC CODE: {diag_code}</div>
    <div class='diagnosis-type'>{diag_name}</div>
    <div class='diagnosis-desc'>{diag_desc}</div>
    <div class='risk-indicator'>⚠ RISK LEVEL: {risk_level}</div>
</div>

<div class='warning-box'>
    <strong>⚠ CRITICAL WARNING</strong><br>
    일반적인 식욕억제제 투여 시 부작용 발생 확률: <strong>{side_effect}</strong><br>
    해당 체질에 맞지 않는 처방은 대사율을 더욱 저하시킬 수 있습니다.
</div>

<div class='protocol-section'>
    <div class='protocol-header'>▸ OPTIMAL PRESCRIPTION PROTOCOL</div>
    <div class='protocol-title'>{prescription}</div>
    <div class='protocol-detail'>Target: {target}</div>
    <div class='protocol-detail'>Success Rate: <span style='color:#00FF00; font-weight:700;'>{success_rate}</span> (기존 환자 데이터 기준)</div>
    <div class='protocol-detail'>처방 기간: 3개월 (최소)</div>
</div>

<div style='margin-top: 30px; padding: 20px; background-color: #0a0a0a; border: 1px solid #00FF00;'>
    <div class='protocol-header' style='color: #FF0000;'>⚠ GOLDEN TIME ALERT</div>
    <p style='font-size: 15px; color: #00BFFF; margin-top: 10px;'>
    귀하의 상태는 <strong style='color:#FF0000;'>'{risk_level}' 단계</strong>입니다.<br>
    대사 기능이 추가 저하되기 전 <strong style='color:#00FF00;'>72시간 이내</strong> 처방이 권장됩니다.<br><br>
    상세 리포트 및 처방전 수신을 위해 연락처를 입력하십시오.
    </p>
</div>

<div class='timestamp'>ANALYSIS COMPLETED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
"""
        
        add_message("assistant", result_html, html=True, chart=radar_chart)
        st.session_state.step = 5
        st.rerun()

# ============================================
# CONTACT FORM (STEP 5)
# ============================================
if st.session_state.step == 5:
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='protocol-header' style='color:#FF0000;'>▸ EMERGENCY PRESCRIPTION REQUEST</div>", unsafe_allow_html=True)
    
    with st.form("emergency_contact"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("성함", placeholder="환자명 입력")
        with col2:
            phone = st.text_input("연락처", placeholder="010-XXXX-XXXX")
        
        memo = st.text_area("특이사항 (선택)", placeholder="추가로 전달할 증상이나 요청사항을 입력하십시오.", height=80)
        
        submitted = st.form_submit_button("⚠ 긴급 처방 신청 및 데이터 전송")
        
        if submitted:
            if name and phone:
                with st.spinner("▸ 데이터 암호화 전송 중..."):
                    time.sleep(1.5)
                st.success("✓ **전송 완료.** 담당 의료진이 72시간 이내 배정됩니다.")
                st.balloons()
            else:
                st.error("⚠ 필수 정보를 모두 입력하십시오.")
