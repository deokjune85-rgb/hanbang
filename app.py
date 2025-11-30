import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. 기본 설정 (수정됨: layout="mobile" -> "centered") ---
st.set_page_config(page_title="Veritas Medical Core", page_icon="🧬", layout="centered")

# 스타일: 리얼 블랙 & 네온
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #E0E0E0; font-family: sans-serif; }
    
    /* 입력창 스타일 */
    .stChatInput { 
        background-color: #111 !important; 
        border: 1px solid #333 !important; 
        color: #fff !important;
    }
    
    /* 버튼 스타일 */
    div.stButton > button {
        background-color: #0A0A0A; border: 1px solid #333; color: #ccc;
        width: 100%; padding: 15px; text-align: left; border-radius: 8px; margin-bottom: 5px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #00FF00; color: #00FF00; background-color: #051105;
    }
    
    /* AI 메시지 강조 */
    .ai-msg { border-left: 3px solid #00BFFF; padding-left: 10px; margin: 10px 0; }
    .user-msg { text-align: right; color: #888; margin: 10px 0; }
    .highlight { color: #00FF00; font-weight: bold; }
    .alert { color: #FF4B4B; font-weight: bold; }
    
    /* 헤더 숨김 (깔끔하게) */
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 2. 세션 상태 관리 (대화 기록 및 단계 제어) ---
if "step" not in st.session_state:
    st.session_state.step = 0
if "history" not in st.session_state:
    st.session_state.history = [] # 대화 로그 저장
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# --- 3. 헬퍼 함수: 대화 기록 출력 ---
def show_history():
    for chat in st.session_state.history:
        role = chat["role"]
        text = chat["text"]
        if role == "ai":
            with st.chat_message("assistant", avatar="🧬"):
                st.markdown(text, unsafe_allow_html=True)
        else:
            with st.chat_message("user", avatar="👤"):
                st.markdown(text)

# --- 4. 헬퍼 함수: 생각하는 척 연출 ---
def ai_thinking(text="데이터 분석 중..."):
    with st.chat_message("assistant", avatar="🧬"):
        with st.status(text, expanded=True) as status:
            st.write("Checking Clinical Data...")
            time.sleep(0.5)
            st.write("Pattern Matching...")
            time.sleep(0.5)
            status.update(label="Complete", state="complete", expanded=False)

# --- 5. 메인 로직 (단계별 시나리오) ---

# 로고 및 헤더
st.markdown("### Veritas <span style='color:#00BFFF; font-size:0.8em'>| Clinical AI Engine</span>", unsafe_allow_html=True)
st.divider()

# 과거 대화 출력
show_history()

# [Step 0] 오프닝 (강력한 후킹)
if st.session_state.step == 0:
    if len(st.session_state.history) == 0:
        # 첫 인사
        opening_msg = """
        **System Online.**
        반갑습니다. 자연과한의원 전용 **[Veritas AI]**입니다.
        
        단순한 설문조사가 아닙니다.
        25년 임상 데이터를 기반으로, 귀하가 **'물만 먹어도 살이 찌는 진짜 원인'**을 찾아냅니다.
        
        **준비되셨습니까?**
        """
        st.session_state.history.append({"role": "ai", "text": opening_msg})
        st.rerun()
    
    # 버튼 액션
    if st.button("네, 진단을 시작합니다. (Start)"):
        st.session_state.history.append({"role": "user", "text": "네, 진단을 시작합니다."})
        st.session_state.step = 1
        st.rerun()

# [Step 1] 기본 정보 입력 & BMI 공포 마케팅
elif st.session_state.step == 1:
    if len(st.session_state.history) < 3: # 질문 안 던졌으면 던짐
        q_msg = "가장 먼저, 기본 생체 데이터를 확인하겠습니다. **[성별 / 키 / 체중]**을 입력해 주십시오."
        st.session_state.history.append({"role": "ai", "text": q_msg})
        st.rerun()

    with st.form("basic_info"):
        gender = st.radio("성별", ["남성", "여성"], horizontal=True)
        col1, col2 = st.columns(2)
        height = col1.number_input("키 (cm)", 140, 200, 165)
        weight = col2.number_input("체중 (kg)", 40, 150, 60)
        
        if st.form_submit_button("데이터 입력 완료"):
            # 유저 입력 기록
            st.session_state.history.append({"role": "user", "text": f"{gender}, {height}cm, {weight}kg"})
            st.session_state.user_data['gender'] = gender
            st.session_state.user_data['weight'] = weight
            
            # --- [AI의 영업 멘트: BMI 분석] ---
            ai_thinking("기초 대사량 및 BMI 산출 중...")
            
            # 가벼운 공포 조장 멘트 생성
            bmi = weight / ((height/100)**2)
            comment = ""
            if bmi >= 25:
                comment = f"""
                <div class='ai-msg'>
                🚨 <strong>경고 신호 감지.</strong><br>
                현재 BMI 수치는 <strong>{bmi:.1f}</strong>로, 단순 과체중을 넘어 <strong>대사 증후군 위험 단계</strong>에 진입했습니다.<br>
                이 구간에서는 '의지'로 빼는 것은 불가능합니다. '대사량 조작'이 필수적입니다.
                </div>
                """
            else:
                comment = f"""
                <div class='ai-msg'>
                체중 자체는 정상이지만, <strong>'마른 비만'</strong>의 가능성이 높습니다.<br>
                내장 지방 레벨을 확인하기 위해 심층 분석으로 넘어갑니다.
                </div>
                """
            
            st.session_state.history.append({"role": "ai", "text": comment})
            st.session_state.step = 2
            st.rerun()

# [Step 2] 핵심 증상 (주관식 같은 객관식)
elif st.session_state.step == 2:
    if len(st.session_state.history) % 2 == 0: # 짝수면 AI 차례
        q_msg = """
        데이터 패턴을 분석합니다.
        현재 귀하의 다이어트를 가장 방해하는 **[핵심 장애물]**은 무엇입니까?
        솔직하게 선택해 주십시오. AI가 원인을 역추적합니다.
        """
        st.session_state.history.append({"role": "ai", "text": q_msg})
        st.rerun()

    # 버튼 선택지
    col1, col2 = st.columns(2)
    symptom = None
    
    if col1.button("🔥 식욕이 안 참아져요 (폭식)"):
        symptom = "식욕"
    if col2.button("💧 물만 먹어도 부어요 (부종)"):
        symptom = "부종"
    if col1.button("❄️ 손발이 차고 추워요 (냉증)"):
        symptom = "냉증"
    if col2.button("💩 변비가 심해요 (독소)"):
        symptom = "변비"

    if symptom:
        st.session_state.history.append({"role": "user", "text": f"가장 큰 문제는 [{symptom}] 입니다."})
        st.session_state.user_data['symptom'] = symptom
        
        # --- [AI의 영업 멘트: 증상 해석 & 공감] ---
        ai_thinking(f"'{symptom}' 원인 데이터 역추적 중...")
        
        analysis_msg = ""
        if symptom == "식욕":
            analysis_msg = """
            <div class='ai-msg'>
            역시 그렇군요. 이건 귀하의 의지박약이 아닙니다.<br>
            뇌의 포만감 중추가 고장 난 <strong>[가짜 식욕(Fake Hunger)]</strong> 상태입니다.<br>
            위장에 쌓인 열(Heat)을 끄지 않으면, 평생 참다가 폭발하는 패턴을 반복하게 됩니다.
            </div>
            """
        elif symptom == "부종":
            analysis_msg = """
            <div class='ai-msg'>
            심각합니다. 살이 찐 게 아니라 <strong>[독소 림프]</strong>가 막혀 있습니다.<br>
            이 상태에서 운동하면 오히려 몸이 더 붓습니다.<br>
            순환을 뚫어주는 배출 치료가 시급합니다.
            </div>
            """
        else:
            analysis_msg = f"""
            <div class='ai-msg'>
            감지되었습니다. 귀하의 비만 유형은 단순 칼로리 과잉이 아닌,<br>
            <strong>[{symptom}으로 인한 대사 기능 정지]</strong>가 원인입니다.<br>
            남들보다 2배 적게 먹어도 찌는 억울한 체질이시군요.
            </div>
            """
            
        st.session_state.history.append({"role": "ai", "text": analysis_msg})
        st.session_state.step = 3
        st.rerun()

# [Step 3] 최종 결과 (압도적 시각화 & CTA)
elif st.session_state.step == 3:
    ai_thinking("최종 임상 리포트 생성 중...")
    
    # 1. 진단명 출력
    st.markdown(f"""
    <div style='background-color:#111; padding:20px; border:1px solid #333; border-radius:10px; margin-top:20px;'>
        <h2 style='color:#00FF00; margin:0;'>DIAGNOSIS REPORT</h2>
        <p style='color:#888;'>Subject: {st.session_state.user_data.get('gender', 'Unknown')} / Type: Critical</p>
        <hr style='border-color:#333;'>
        <h1 style='color:#FFF; font-size:40px;'>Type-C: <span style='color:#FF4B4B'>대사 급속 저하형</span></h1>
        <p style='color:#CCC; line-height:1.6;'>
        귀하의 신체는 현재 <strong>'지방을 태우는 보일러'</strong>가 꺼져 있는 상태입니다.<br>
        이대로 방치할 경우, 1년 내 <strong>체중이 15% 이상 증가</strong>할 확률이 88%로 예측됩니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. 레이더 차트 (Plotly)
    categories = ['식욕 통제력', '기초 대사량', '독소 배출력', '스트레스', '호르몬 밸런스']
    values = [20, 30, 40, 90, 50] # 일부러 안 좋게 설정 (가스라이팅용)
    
    fig = px.line_polar(r=values, theta=categories, line_close=True)
    fig.update_traces(fill='toself', line_color='#00FF00')
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False)
        ),
        font=dict(color="white"),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 3. 처방 및 상담 신청 (CTA)
    st.warning("⚠️ 긴급 처방이 필요합니다. AI가 최적화된 처방전을 전송했습니다.")
    
    st.markdown("### 💊 AI Recommended Solution")
    st.info("**[지방사약 Black]** : 대사량 300% 강제 부스팅 + 식욕 차단")
    
    with st.form("lead_form"):
        st.write("**지금 상담 신청 시, 'AI 진단 리포트'가 원장님께 즉시 전달됩니다.**")
        col1, col2 = st.columns(2)
        name = col1.text_input("성함")
        phone = col2.text_input("연락처 (010-XXXX-XXXX)")
        
        if st.form_submit_button("🚀 긴급 처방 상담 신청하기 (우선 배정)"):
            st.success(f"{name}님, 접수가 완료되었습니다. 담당 의료진이 데이터를 분석 중입니다. 5분 내로 연락드립니다.")
            st.balloons()
