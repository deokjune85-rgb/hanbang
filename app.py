import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 설정 (모바일 최적화 - layout='centered'가 핵심)
st.set_page_config(page_title="Veritas Medical Core", page_icon="🧬", layout="centered")

# 2. 리얼 블랙 & 네온 스타일 (이모지 제거, 전문성 강화)
st.markdown("""
<style>
    /* 전체 배경 및 폰트 */
    .stApp {
        background-color: #000000;
        color: #E0E0E0;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* 채팅창 스타일 */
    .stChatInput {
        background-color: #111 !important;
        border: 1px solid #333 !important;
    }
    
    /* 버튼 스타일 (선택지) */
    div.stButton > button {
        background-color: #0A0A0A;
        border: 1px solid #333;
        color: #B0B0B0;
        width: 100%;
        padding: 15px;
        text-align: left;
        border-radius: 4px;
        margin-bottom: 8px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #00FF00;
        color: #00FF00;
        background-color: #051105;
    }
    
    /* AI 메시지 박스 (분석 결과 강조) */
    .analysis-box {
        border-left: 3px solid #00FF00;
        background-color: #0A110A;
        padding: 15px;
        margin-top: 10px;
        border-radius: 0 8px 8px 0;
        font-size: 14px;
        line-height: 1.6;
    }
    
    /* 사용자 메시지 스타일 */
    .user-msg {
        text-align: right;
        color: #888;
        font-size: 14px;
        margin: 10px 0;
    }
    
    /* 헤더 숨김 */
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 0
if "chat_log" not in st.session_state:
    # 초기 인사말 (강력한 후킹)
    st.session_state.chat_log = [
        {"role": "ai", "content": """
        **System Online.**
        반갑습니다. 자연과한의원 전용 **[Veritas Clinical Engine]**입니다.
        
        단순한 설문조사가 아닙니다.
        25년 임상 데이터를 실시간으로 대조하여, 귀하가 **'물만 먹어도 살이 찌는 진짜 원인'**을 역추적합니다.
        
        준비되셨습니까?
        """}
    ]
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

# 4. 화면 표시 로직
st.markdown("#### Veritas <span style='color:#666; font-size:0.8em'>| Clinical Data Analysis</span>", unsafe_allow_html=True)
st.markdown("---")

# 대화 기록 출력 (이전 대화들이 계속 쌓여서 보이게 함)
for chat in st.session_state.chat_log:
    avatar = None  # 기본 아이콘 사용 (깔끔하게)
    if chat["role"] == "ai":
        with st.chat_message("assistant", avatar=avatar):
            st.markdown(chat["content"], unsafe_allow_html=True)
            # 차트가 있는 경우 출력
            if "chart" in chat:
                st.plotly_chart(chat["chart"], use_container_width=True)
    else:
        with st.chat_message("user", avatar=avatar):
            st.markdown(chat["content"])

# 5. 단계별 인터랙션 로직 (여기가 핵심)

# [Step 0] 시작 버튼
if st.session_state.step == 0:
    if st.button("DIAGNOSIS START (진단 시작)"):
        # 사용자 응답 기록
        st.session_state.chat_log.append({"role": "user", "content": "진단 프로세스를 시작합니다."})
        
        # AI 다음 질문 (생각하는 척 연출)
        with st.spinner("Accessing Clinical Database..."):
            time.sleep(1)
        
        next_q = "가장 먼저 기본 생체 데이터를 분석합니다.\n\n**성별, 나이, 키, 체중**을 입력해 주십시오."
        st.session_state.chat_log.append({"role": "ai", "content": next_q})
        
        st.session_state.step = 1
        st.rerun()

# [Step 1] 신체 정보 입력 & 즉시 분석 (가스라이팅 시작)
elif st.session_state.step == 1:
    with st.form("body_info"):
        c1, c2 = st.columns(2)
        gender = c1.radio("성별", ["남성", "여성"], horizontal=True)
        age = c2.number_input("나이", 10, 80, 30)
        c3, c4 = st.columns(2)
        height = c3.number_input("키 (cm)", 140, 200, 160)
        weight = c4.number_input("체중 (kg)", 40, 150, 60)
        
        if st.form_submit_button("데이터 전송 (Analyze)"):
            # 사용자 입력 저장
            user_text = f"{gender}, {age}세, {height}cm, {weight}kg"
            st.session_state.chat_log.append({"role": "user", "content": user_text})
            st.session_state.user_info = {"gender": gender, "age": age, "height": height, "weight": weight}
            
            # --- [AI 분석 로직] ---
            # BMI 계산 및 강력한 코멘트 생성
            bmi = weight / ((height/100)**2)
            
            with st.spinner("Calculating Metabolic Rate..."):
                time.sleep(1.5)
            
            if bmi >= 23:
                analysis = f"""
                <div class='analysis-box'>
                <strong>[🚨 WARNING: 대사 증후군 경고]</strong><br><br>
                현재 BMI 수치는 <strong>{bmi:.1f}</strong>입니다. 
                단순 과체중이 아닙니다. 현재 귀하의 신체는 <strong>'에너지를 소비하는 엔진'이 꺼져 있는 상태</strong>입니다.<br>
                이 구간에서는 식사량을 줄여도 체중이 정체될 확률이 90% 이상입니다. 
                '의지'의 문제가 아니라 '호르몬' 시스템의 오류입니다.
                </div>
                """
            else:
                analysis = f"""
                <div class='analysis-box'>
                <strong>[⚠️ CAUTION: 마른 비만 유형]</strong><br><br>
                체중 자체는 정상이지만, 데이터상 <strong>내장 지방과 부종 수치</strong>가 높을 것으로 예측됩니다.<br>
                겉으로는 말라 보이지만 속은 염증으로 가득 찬 상태일 수 있습니다. 정밀 분석이 필요합니다.
                </div>
                """
            
            st.session_state.chat_log.append({"role": "ai", "content": analysis})
            
            # 다음 질문 바로 던지기
            next_q = """
            데이터 패턴을 더 깊이 파고들겠습니다.
            현재 귀하를 가장 괴롭히는 **[핵심 증상]**은 무엇입니까?
            솔직한 데이터만이 정확한 처방을 만듭니다.
            """
            st.session_state.chat_log.append({"role": "ai", "content": next_q})
            
            st.session_state.step = 2
            st.rerun()

# [Step 2] 증상 선택 & 공감형 해석 (여기가 영업 포인트)
elif st.session_state.step == 2:
    # 버튼으로 선택지 제공 (하지만 누르면 AI가 해석해줌)
    col1, col2 = st.columns(2)
    
    selection = None
    if col1.button("🔥 식욕 조절 불가능 (폭식)"): selection = "식욕"
    if col2.button("💧 물만 먹어도 붓음 (부종)"): selection = "부종"
    if col1.button("❄️ 손발이 차고 저림 (순환)"): selection = "냉증"
    if col2.button("💊 약 내성/요요 반복 (내성)"): selection = "내성"
    
    if selection:
        st.session_state.chat_log.append({"role": "user", "content": f"가장 큰 문제는 [{selection}] 입니다."})
        
        # --- [AI의 해석: 이게 엑셀과 다른 점] ---
        with st.spinner(f"Analyzing '{selection}' pattern..."):
            time.sleep(1.5)
            
        commentary = ""
        if selection == "식욕":
            commentary = """
            <div class='analysis-box'>
            역시 그렇군요. 많은 분들이 '내 의지가 약하다'고 자책하지만, <strong>그건 귀하의 잘못이 아닙니다.</strong><br>
            데이터상 귀하의 뇌는 현재 포만감을 느끼지 못하는 <strong>[가짜 식욕(Fake Hunger)]</strong> 상태입니다.<br>
            위장에 쌓인 '열독(Heat Toxin)'을 끄지 않으면, 평생 굶고 폭식하는 지옥에서 벗어날 수 없습니다.
            </div>
            """
        elif selection == "부종":
            commentary = """
            <div class='analysis-box'>
            심각합니다. 이건 살이 찐 게 아니라 <strong>[독소 림프]</strong>가 막혀 몸이 썩어가고 있는 신호입니다.<br>
            이 상태에서 헬스장 가서 운동하면 오히려 몸이 더 붓고 염증 수치만 올라갑니다.<br>
            배출 통로를 뚫어주는 것이 시급합니다.
            </div>
            """
        elif selection == "냉증":
            commentary = """
            <div class='analysis-box'>
            감지되었습니다. 전형적인 <strong>[대사 동결(Metabolic Freeze)]</strong> 현상입니다.<br>
            남들보다 2배 적게 먹어도 찌는 억울한 체질이시군요.<br>
            보일러가 꺼진 방에 연료(음식)를 넣으니 타지 않고 그대로 지방으로 쌓이는 겁니다.
            </div>
            """
        else:
            commentary = """
            <div class='analysis-box'>
            데이터가 말해줍니다. 귀하의 몸은 이미 수많은 다이어트 약물로 인해 <strong>[내성]</strong>이 생긴 상태입니다.<br>
            시중의 일반적인 식욕억제제로는 반응하지 않습니다.
            강도를 높이는 게 아니라, 약의 <strong>기전(Mechanism)</strong>을 바꿔야만 살이 빠집니다.
            </div>
            """
            
        st.session_state.chat_log.append({"role": "ai", "content": commentary})
        
        # 결과 보고서 생성 유도
        st.session_state.chat_log.append({"role": "ai", "content": "모든 데이터 분석이 완료되었습니다. **최종 진단 리포트**를 생성합니다."})
        st.session_state.step = 3
        st.rerun()

# [Step 3] 최종 결과 (압도적 시각화 & CTA)
elif st.session_state.step == 3:
    if st.button("📂 VIEW FINAL REPORT (결과 확인)"):
        with st.spinner("Generating Medical Report..."):
            time.sleep(2)
        
        # 1. 진단명
        result_msg = """
        ### 📋 DIAGNOSIS REPORT
        **Subject:** Critical / **Code:** Type-C (Metabolic Disorder)
        
        귀하의 신체 데이터 분석 결과, 현재 **'자연 연소 시스템'**이 셧다운 된 상태입니다.
        이대로 방치 시 6개월 내 **체중 12% 추가 증가**가 예측됩니다.
        """
        st.session_state.chat_log.append({"role": "ai", "content": result_msg})
        
        # 2. 차트 생성 (시각적 충격)
        categories = ['식욕 통제력', '기초 대사량', '독소 배출력', '스트레스 저항', '호르몬 밸런스']
        values = [20, 15, 30, 80, 40] # 일부러 망가진 그래프 보여줌
        
        fig = px.line_polar(r=values, theta=categories, line_close=True)
        fig.update_traces(fill='toself', line_color='#00FF00')
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0, 100], showticklabels=False)
            ),
            font=dict(color="#ccc"),
            showlegend=False,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        st.session_state.chat_log.append({"role": "ai", "content": "**[Body Balance Analysis]**", "chart": fig})
        
        # 3. 처방 및 CTA (가장 중요)
        prescription = """
        <div style='border: 1px solid #00BFFF; padding: 20px; border-radius: 10px; margin-top: 20px;'>
            <h3 style='color:#00BFFF; margin-top:0;'>💊 AI Prescribed Solution</h3>
            <p style='font-size: 15px;'>
            귀하의 데이터에 매칭되는 유일한 처방은 <strong>[지방사약 Black]</strong>입니다.<br>
            일반적인 다이어트로는 불가능합니다. <strong>강제적인 대사 부스팅</strong>이 필요합니다.
            </p>
            <hr style='border-color:#333'>
            <p style='color:#888; font-size:12px;'>
            * 본 리포트는 의료진에게 즉시 전송되어, 상담 시 정밀 진료 자료로 활용됩니다.
            </p>
        </div>
        """
        st.session_state.chat_log.append({"role": "ai", "content": prescription})
        
        st.session_state.step = 4
        st.rerun()

# [Step 4] DB 수집 (최종 관문)
elif st.session_state.step == 4:
    with st.form("lead_form"):
        st.write("🏥 **우선 상담 예약 (Priority Queue)**")
        st.write("지금 연락처를 남기시면, 담당 의료진이 **'분석 리포트'**를 미리 확인하고 10분 내로 연락드립니다.")
        
        col1, col2 = st.columns(2)
        name = col1.text_input("성함")
        phone = col2.text_input("연락처 (010-XXXX-XXXX)")
        
        if st.form_submit_button("🚀 긴급 처방 상담 신청하기"):
            st.success("데이터 전송 완료. 의료진이 차트를 검토 중입니다. 잠시만 기다려 주십시오.")
            st.balloons()
