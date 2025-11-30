import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random

# -----------------------------------------------------------------------------
# 1. SYSTEM CONFIGURATION & CSS ARCHITECTURE (THE BLACK BOX THEME)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="VERITAS MED-OS | Medical Intelligence",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# [CSS: Cyberpunk/Medical Terminal Style]
st.markdown("""
<style>
    /* Google Font: Space Mono for Terminal feel */
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

    /* Global Reset */
    .stApp {
        background-color: #000000 !important;
        color: #E0E0E0;
        font-family: 'Space Mono', monospace;
    }

    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Text Colors & Glows */
    h1, h2, h3 { color: #FFFFFF !important; text-transform: uppercase; letter-spacing: 2px; }
    .neon-blue { color: #00BFFF; text-shadow: 0 0 10px #00BFFF; }
    .neon-green { color: #00FF00; text-shadow: 0 0 10px #00FF00; }
    .neon-red { color: #FF3333; text-shadow: 0 0 10px #FF3333; }
    
    /* Terminal Logs */
    .terminal-log {
        font-size: 12px;
        color: #666;
        border-left: 2px solid #333;
        padding-left: 10px;
        margin-bottom: 5px;
    }

    /* Chat Messages (Modified to look like System Logs) */
    .stChatMessage {
        background-color: #050505 !important;
        border: 1px solid #1A1A1A;
        margin-bottom: 10px;
    }
    [data-testid="stChatMessageContent"] {
        color: #00BFFF !important;
        font-weight: 500;
    }
    .stChatMessage[data-testid="user-message"] {
        background-color: #0A0A0A !important;
        border: 1px solid #333;
    }

    /* Input Fields */
    .stTextInput > div > div > input {
        background-color: #000000 !important;
        color: #00FF00 !important;
        border: 1px solid #333 !important;
        border-radius: 0px !important;
        font-family: 'Space Mono', monospace;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00BFFF !important;
        box-shadow: 0 0 10px #00BFFF inset;
    }

    /* Buttons (Futuristic Blocks) */
    .stButton > button {
        background-color: #000000 !important;
        color: #00BFFF !important;
        border: 1px solid #00BFFF !important;
        border-radius: 0px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #00BFFF !important;
        color: #000000 !important;
        box-shadow: 0 0 15px #00BFFF;
    }

    /* Status Container */
    [data-testid="stStatusWidget"] {
        background-color: #0A0A0A;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. STATE MANAGEMENT & HELPER FUNCTIONS
# -----------------------------------------------------------------------------
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

def type_text(text, speed=0.01):
    """타자기 효과"""
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(f"<span style='color:#00BFFF'>{full_text}█</span>", unsafe_allow_html=True)
        time.sleep(speed)
    placeholder.markdown(f"<span style='color:#00BFFF'>{full_text}</span>", unsafe_allow_html=True)

def generate_radar_chart():
    """Plotly Radar Chart - Dark Mode"""
    categories = ['APPETITE (식욕)', 'METABOLISM (대사)', 'TOXIN (독소)', 'STRESS (스트레스)', 'EDEMA (부종)']
    
    # 임의의 높은 수치 생성 (환자에게 경각심을 주기 위함)
    values = [random.randint(80, 100), random.randint(20, 40), random.randint(70, 90), random.randint(85, 100), random.randint(60, 90)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(0, 255, 0, 0.2)',
        line=dict(color='#00FF00', width=2),
        name='Current Status'
    ))

    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, linecolor='#333'),
            angularaxis=dict(color='#00BFFF')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=40, r=40, t=20, b=20),
        font=dict(family='Space Mono', color='#E0E0E0')
    )
    return fig

# -----------------------------------------------------------------------------
# 3. MAIN LOGIC FLOW
# -----------------------------------------------------------------------------

# [HEADER]
c1, c2 = st.columns([8, 2])
with c1:
    st.markdown("### VERITAS MED-OS <span style='font-size:12px; color:#333;'>v9.4.2</span>", unsafe_allow_html=True)
with c2:
    st.markdown("<div style='text-align:right; color:#00FF00; font-size:12px;'>● SYSTEM ONLINE</div>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: #333; margin-top:0;'>", unsafe_allow_html=True)

# ---------------- STEP 0: INTRO ----------------
if st.session_state.step == 0:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/1px-Apple_logo_black.svg.png", width=1) # Dummy pixel for spacing
    
    # Intro Animation
    with st.container():
        st.markdown("<div class='terminal-log'>Init.sequence_boot_check... OK</div>", unsafe_allow_html=True)
        time.sleep(0.3)
        st.markdown("<div class='terminal-log'>Loading_medical_protocols... OK</div>", unsafe_allow_html=True)
        time.sleep(0.3)
        st.markdown("<div class='terminal-log'>Connecting_to_neural_network... ESTABLISHED</div>", unsafe_allow_html=True)
        time.sleep(0.5)
    
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>INITIALIZE DIAGNOSIS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>MEDICAL INTELLIGENCE TERMINAL</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("START SYSTEM"):
            st.session_state.step = 1
            st.rerun()

# ---------------- STEP 1: BIO DATA ----------------
elif st.session_state.step == 1:
    st.markdown("<div class='neon-blue'>[STEP 01] SUBJECT IDENTIFICATION</div>", unsafe_allow_html=True)
    
    with st.chat_message("assistant", avatar="💠"):
        st.write("피험자의 신체 데이터를 입력하십시오. 데이터는 중앙 서버와 동기화됩니다.")
    
    with st.form("bio_form"):
        c1, c2 = st.columns(2)
        gender = c1.selectbox("Gender", ["Male", "Female"])
        age = c2.number_input("Age", min_value=10, max_value=80, value=30)
        height = c1.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        weight = c2.number_input("Weight (kg)", min_value=30, max_value=200, value=65)
        
        submitted = st.form_submit_button("TRANSMIT DATA >>")
        
        if submitted:
            st.session_state.user_data.update({'gender': gender, 'age': age, 'height': height, 'weight': weight})
            
            # Fake Calculation Animation
            with st.status("PROCESSING BIOMETRICS...", expanded=True) as status:
                st.write("Calculating BMI Index...")
                time.sleep(0.8)
                st.write("Analyzing Basal Metabolic Rate (BMR)...")
                time.sleep(0.8)
                st.write("Cross-referencing Global Obesity Database...")
                time.sleep(0.8)
                status.update(label="DATA VERIFIED", state="complete", expanded=False)
            
            st.session_state.step = 2
            st.rerun()

# ---------------- STEP 2: SYMPTOM CHECK ----------------
elif st.session_state.step == 2:
    st.markdown("<div class='neon-blue'>[STEP 02] SYMPTOM ANALYSIS</div>", unsafe_allow_html=True)
    
    with st.chat_message("assistant", avatar="💠"):
        type_text("현재 가장 두드러지는 임상 증상을 선택하십시오. 다중 벡터 분석이 수행됩니다.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    if col1.button("식욕 통제 불능 (Hyperphagia)"):
        st.session_state.user_data['symptom'] = 'Appetite'
        st.session_state.step = 3
        st.rerun()
    if col2.button("만성 부종/붓기 (Edema)"):
        st.session_state.user_data['symptom'] = 'Edema'
        st.session_state.step = 3
        st.rerun()
        
    col3, col4 = st.columns(2)
    if col3.button("대사 저하/냉증 (Metabolic Drop)"):
        st.session_state.user_data['symptom'] = 'Metabolism'
        st.session_state.step = 3
        st.rerun()
    if col4.button("스트레스성 폭식 (Cortisol Spike)"):
        st.session_state.user_data['symptom'] = 'Stress'
        st.session_state.step = 3
        st.rerun()

# ---------------- STEP 3: DEEP ANALYSIS (TWIST) ----------------
elif st.session_state.step == 3:
    st.markdown("<div class='neon-red'>⚠ ANOMALY DETECTED</div>", unsafe_allow_html=True)
    
    # Fake System Interrupt
    with st.spinner("Re-evaluating correlation coefficient..."):
        time.sleep(2.5)
    
    with st.chat_message("assistant", avatar="💠"):
        st.markdown(f"""
        입력된 데이터 <span class='neon-green'>{st.session_state.user_data.get('symptom')}</span> 벡터와 신체 지수 간의 불일치가 감지되었습니다.
        
        정확도를 99.8%로 보정하기 위해 추가 확인이 필요합니다.
        
        **수면 장애(불면 혹은 과수면)를 동반하고 있습니까?**
        """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    if c1.button("YES (Positive)"):
        st.session_state.step = 4
        st.rerun()
    if c2.button("NO (Negative)"):
        st.session_state.step = 4
        st.rerun()

# ---------------- STEP 4: FINAL RESULT ----------------
elif st.session_state.step == 4:
    # Final Loading Sequence
    progress_text = "COMPILING FINAL MEDICAL REPORT..."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.02)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(0.5)
    my_bar.empty()

    # Diagnosis Header
    st.markdown("""
    <div style='border: 2px solid #FF3333; padding: 20px; background-color: rgba(255, 51, 51, 0.05); margin-bottom: 20px;'>
        <h2 class='neon-red' style='text-align:center; margin:0;'>DIAGNOSIS: CRITICAL</h2>
        <h3 style='text-align:center; color: #FFF; margin-top:10px;'>TYPE-C: Metabolic Freeze (대사 동결)</h3>
    </div>
    """, unsafe_allow_html=True)

    # Visualization (Radar Chart)
    col_chart, col_text = st.columns([1, 1])
    
    with col_chart:
        st.plotly_chart(generate_radar_chart(), use_container_width=True)
    
    with col_text:
        st.markdown("<div class='neon-blue' style='font-size:14px; margin-bottom:10px;'>CLINICAL SUMMARY</div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size:13px; color:#CCC; line-height:1.6;'>
        ▪ <b>대사 효율(Metabolic Efficiency):</b> <span style='color:#FF3333'>CRITICAL LOW</span><br>
        ▪ <b>독소 축적도(Toxicity):</b> <span style='color:#FF3333'>LEVEL 8 (Danger)</span><br>
        ▪ <b>자율신경 균형:</b> 교감신경 과항진 상태<br><br>
        
        "일반적인 식욕억제제 단독 투여 시 부작용 확률 85% 이상. 
        단순 체중 감량이 아닌, <b>순환계 강제 부스팅(System Reboot)</b>이 필수적인 상태입니다."
        </div>
        """, unsafe_allow_html=True)

    # Prescription & CTA
    st.markdown("---")
    st.markdown("<div class='neon-green' style='text-align:center; margin-bottom:15px;'>RECOMMENDED PROTOCOL</div>", unsafe_allow_html=True)
    
    st.info("⚠ 경고: 귀하의 골든타임은 앞으로 14일입니다. 즉각적인 의료 개입이 필요합니다.")

    with st.form("cta_form"):
        st.markdown("**[PRIORITY ACCESS] 긴급 처방 예약**")
        name = st.text_input("Subject Name", placeholder="Enter Full Name")
        phone = st.text_input("Contact Frequency", placeholder="010-XXXX-XXXX")
        
        submit_final = st.form_submit_button("REQUEST EMERGENCY PROTOCOL")
        
        if submit_final:
            if name and phone:
                with st.spinner("Securely Transmitting to Medical DB..."):
                    time.sleep(2)
                st.success("TRANSMISSION COMPLETE. Medical Team dispatched.")
            else:
                st.error("INPUT ERROR. Required fields missing.")

    # Footer Logic
    st.markdown("<div style='text-align:center; color:#333; font-size:10px; margin-top:50px;'>VERITAS MED-OS SYSTEM COPYRIGHT 2025. ALL RIGHTS RESERVED.</div>", unsafe_allow_html=True)
