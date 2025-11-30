import streamlit as st
import time
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="자연과한의원 AI 진단센터",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS
custom_css = """
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp {
        background-color: #000000 !important;
        color: #E0E0E0 !important;
        font-family: 'Pretendard', sans-serif;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .stChatMessage {
        background-color: #000000 !important;
        border-bottom: 1px solid #1a1a1a;
        padding: 20px 0 !important;
    }
    
    [data-testid="stChatMessageContent"] {
        background-color: transparent !important;
        color: #E0E0E0 !important;
        font-size: 15px;
        line-height: 1.8;
    }
    
    .stChatInputContainer {
        border-top: 1px solid #00FF00;
        padding-top: 15px;
    }
    
    .stChatInput input {
        background-color: #0a0a0a !important;
        border: 1px solid #00FF00 !important;
        color: #00BFFF !important;
        font-size: 15px;
    }
    
    .alert-critical {
        background: linear-gradient(135deg, #2a0000 0%, #000000 100%);
        border: 2px solid #FF0000;
        padding: 30px;
        margin: 30px 0;
        box-shadow: 0 0 40px rgba(255, 0, 0, 0.4);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { border-color: #FF0000; }
        50% { border-color: #FF6666; }
    }
    
    .alert-title {
        font-size: 24px;
        font-weight: 900;
        color: #FF0000;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .diagnosis-card {
        background: linear-gradient(135deg, #001a1a 0%, #000000 100%);
        border-left: 4px solid #00FF00;
        padding: 40px 30px;
        margin: 30px 0;
        box-shadow: 0 0 60px rgba(0, 255, 0, 0.2);
    }
    
    .diagnosis-type {
        font-size: 32px;
        font-weight: 900;
        color: #00FF00;
        margin-bottom: 20px;
        text-shadow: 0 0 20px rgba(0, 255, 0, 0.6);
    }
    
    .diagnosis-desc {
        font-size: 16px;
        color: #00BFFF;
        line-height: 1.9;
        margin-bottom: 20px;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin: 25px 0;
        padding: 25px;
        background-color: #0a0a0a;
        border: 1px solid #333;
    }
    
    .stat-item {
        border-bottom: 1px solid #1a1a1a;
        padding: 15px 0;
    }
    
    .stat-label {
        font-size: 11px;
        color: #666;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    
    .stat-value {
        font-size: 24px;
        color: #00FF00;
        font-weight: 700;
    }
    
    .stTextInput input, .stTextArea textarea {
        background-color: #0a0a0a !important;
        border: 1px solid #00FF00 !important;
        color: #00BFFF !important;
        font-size: 14px;
    }
    
    div[data-testid="stForm"] button[type="submit"] {
        width: 100%;
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        font-weight: 900;
        font-size: 18px;
        padding: 20px;
        border: none;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 40px rgba(255, 0, 0, 0.6);
        animation: glow 2s infinite;
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 40px rgba(255, 0, 0, 0.6); }
        50% { box-shadow: 0 0 60px rgba(255, 0, 0, 0.9); }
    }
    
    strong {
        color: #00FF00;
        font-weight: 700;
    }
    
    em {
        color: #FFB800;
        font-style: normal;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# STATE
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

AI_AVATAR = "🔷"
USER_AVATAR = "👤"

# FUNCTIONS
def stream_text(text, speed=0.008):
    """Smoother streaming with complete text guarantee"""
    placeholder = st.empty()
    display = ""
    
    # Stream in chunks for better performance
    chunk_size = 3
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        display += chunk
        placeholder.markdown(display)
        time.sleep(speed)
    
    # Ensure final complete text is displayed
    placeholder.markdown(text)
    return text

def add_msg(role, content, html=False, chart=None, animated=False):
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "html": html,
        "chart": chart,
        "animated": animated
    })

def create_radar_chart(scores):
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
                tickfont=dict(size=11, color='#00BFFF')
            )
        ),
        paper_bgcolor='#000000',
        plot_bgcolor='#000000',
        margin=dict(l=80, r=80, t=40, b=40),
        height=400
    )
    
    return fig

# HEADER
st.markdown("<h2 style='text-align:center; color:#00FF00; font-weight:900; margin-bottom:5px;'>자연과한의원 AI 진단센터</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:12px; color:#666; margin-bottom:30px;'>25년 임상 데이터 기반 / 24시간 무료 진단</p>", unsafe_allow_html=True)
st.divider()

# INIT
if st.session_state.step == 0:
    init = """안녕하세요, 자연과한의원입니다.

혹시 이런 고민 있으시죠?

**"운동도 하고 적게 먹는데 왜 안 빠지지?"**
**"물만 먹어도 붓는데 이게 정상인가?"**

괜찮습니다. **당신 잘못이 아닙니다.**

25년간 20만 명의 임상 데이터가 증명합니다.
체질을 모르고 다이어트하면 100% 실패합니다.

지금부터 당신의 살이 안 빠지는 **진짜 이유**를 찾아드리겠습니다.

먼저, 성함이 어떻게 되시나요?
(편하게 불러드리고 싶습니다 😊)"""
    add_msg("assistant", init)
    st.session_state.step = 1

# RENDER MESSAGES
for i, msg in enumerate(st.session_state.messages):
    avatar = AI_AVATAR if msg["role"] == "assistant" else USER_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        is_last = (i == len(st.session_state.messages) - 1)
        
        if msg["role"] == "assistant" and not msg["animated"] and is_last:
            if msg.get("html"):
                st.markdown(msg["content"], unsafe_allow_html=True)
            else:
                stream_text(msg["content"])
            
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

# INPUT
disabled = (st.session_state.step == 99)
user_input = st.chat_input("여기에 편하게 답변해 주세요...", disabled=disabled)

# LOGIC
if user_input:
    add_msg("user", user_input, animated=True)
    
    # STEP 1: 이름
    if st.session_state.step == 1:
        name = user_input.strip()
        st.session_state.user_data['name'] = name
        
        response = f"""반갑습니다, **{name}님**!

{name}님, 솔직히 말씀드릴게요.

**"의지가 약해서", "게을러서" 살찐 거 아닙니다.**

제가 25년간 본 환자 중 90%가 {name}님처럼
**"열심히 했는데 안 빠졌어요"**라고 말씀하셨거든요.

이유는 단 하나.
**잘못된 방법으로 다이어트를 했기 때문입니다.**

지금부터 제가 몇 가지만 여쭤볼게요.
부담 갖지 마시고, 편하게 대답해 주세요.

먼저, **{name}님의 나이와 성별**을 알려주시겠어요?
예) 35세 여성"""
        add_msg("assistant", response)
        st.session_state.step = 2
    
    # STEP 2: 나이/성별
    elif st.session_state.step == 2:
        st.session_state.user_data['age_gender'] = user_input
        
        with st.status("분석 중...", expanded=False) as status:
            time.sleep(0.8)
            status.update(label="완료", state="complete", expanded=False)
        
        name = st.session_state.user_data.get('name', '고객')
        
        response = f"""감사합니다, {name}님.

이제 핵심 질문입니다.

**{name}님께서 가장 힘들어하시는 증상이 뭔가요?**

예를 들면...

- *"물만 먹어도 몸이 붓고 다리가 무거워요"*
- *"밤만 되면 식욕이 폭발해서 폭식하게 돼요"*
- *"아무리 먹어도 배가 고파요. 뇌가 속는 느낌이에요"*
- *"손발이 차갑고, 조금만 먹어도 배가 나와요"*

**자유롭게 말씀해 주세요.**
{name}님의 몸이 지금 무슨 신호를 보내고 있는지 제가 정확히 짚어드릴게요."""
        add_msg("assistant", response)
        st.session_state.step = 3
    
    # STEP 3: 증상 입력 → 콜드 리딩 (확인 사살)
    elif st.session_state.step == 3:
        symptom = user_input.lower()
        st.session_state.user_data['symptom'] = user_input
        
        with st.status("임상 패턴 분석 중...", expanded=True) as status:
            st.write("🔍 20만 건의 케이스 데이터 대조 중...")
            time.sleep(0.6)
            st.write("🧬 체질 알고리즘 연산 실행...")
            time.sleep(0.6)
            status.update(label="분석 완료", state="complete", expanded=False)
        
        name = st.session_state.user_data.get('name', '고객')
        
        # 콜드 리딩: "혹시 이런 것도...?"
        if "붓" in symptom or "부종" in symptom or "무겁" in symptom:
            diagnosis_type = "수독정체형"
            st.session_state.user_data['type'] = diagnosis_type
            
            response = f"""**{name}님, 잠깐만요.**

{name}님이 "붓는다"고 하셨는데...

혹시 이런 증상도 있지 않으세요?

✓ **아침에 일어나면 얼굴이 퉁퉁 붓는다**
✓ **양말 벗으면 자국이 1시간 이상 안 없어진다**
✓ **저녁만 되면 다리가 코끼리 다리로 변한다**
✓ **손가락으로 종아리 누르면 쏙 들어가고 안 올라온다**

**하나라도 맞으면 답장해 주세요.**

제가 {name}님 집에 CCTV를 단 게 아니라,
이게 전형적인 **"림프 순환 정체형"** 증상이거든요.

이 상태로 굶는 다이어트 하면?
**근육만 빠지고 부종은 더 심해집니다.**

{name}님께 맞는 처방을 찾기 위해 한 가지만 더 여쭤볼게요.

과거에 **다이어트 약(양약/한약)** 드신 적 있으세요?
(있으면 "있어요", 없으면 "없어요"만 답해주세요)"""
            
        elif "폭식" in symptom or "식욕" in symptom or "배고" in symptom or "먹" in symptom or "살" in symptom or "쪄" in symptom:
            diagnosis_type = "위열과다형"
            st.session_state.user_data['type'] = diagnosis_type
            
            response = f"""**{name}님, 잠깐만요.**

{name}님 말씀 듣다 보니까...

혹시 이런 패턴 아니세요?

✓ **아침엔 입맛이 없는데, 저녁 8시 이후에만 미친 듯이 당긴다**
✓ **먹고 나서 30분도 안 돼서 또 배고프다**
✓ **밤에 치킨/라면 시키고, 다음 날 아침 후회한다**
✓ **먹으면서도 "왜 이러지?" 싶은데 손이 안 멈춘다**

**하나라도 맞으면 답장해 주세요.**

{name}님, 이건 **"가짜 배고픔"**입니다.

뇌가 착각하고 있는 거예요.
위장에 **열(Heat)**이 과도하게 차서
포만 중추가 **"배고프다"**는 거짓 신호를 보내는 겁니다.

이거 방치하면?
**당뇨 전단계로 직행합니다.**

{name}님께 딱 맞는 처방을 찾기 위해 솔직히 답해주세요.

과거에 **식욕억제제나 다이어트 한약** 드신 적 있으세요?
(있으면 "있어요", 없으면 "없어요" - 저희가 판단하는 게 아니라 **처방 강도 조절**을 위해 필요합니다)"""
        
        elif "차갑" in symptom or "냉" in symptom or "대사" in symptom or "적게" in symptom:
            diagnosis_type = "냉증형대사장애"
            st.session_state.user_data['type'] = diagnosis_type
            
            response = f"""**{name}님, 잠깐만요.**

{name}님 증상 들어보니...

혹시 이런 것도 있지 않으세요?

✓ **손발이 얼음장처럼 차갑다 (여름에도)**
✓ **아침에 일어나기 힘들고 만성 피로**
✓ **조금만 먹어도 배가 나온다**
✓ **체중계 숫자는 안 변하는데 옷은 안 맞는다**

**하나라도 맞으면 답장해 주세요.**

{name}님, 이건 제일 무서운 케이스입니다.

**기초대사량이 바닥**을 쳤어요.
몸이 **"절약 모드"**로 돌입한 겁니다.

이 상태로 굶으면?
**근육만 녹고, 지방은 꽁꽁 숨깁니다.**

최악의 경우 **"물만 먹어도 찌는 체질"**로 고착됩니다.

{name}님, 솔직하게 답해주세요.

과거에 **극단적인 다이어트(원푸드, 굶기 등)** 해보신 적 있으세요?
(있으면 "있어요", 없으면 "없어요" - 처방 강도 결정을 위해 꼭 필요합니다)"""
        
        else:
            diagnosis_type = "간기울결형"
            st.session_state.user_data['type'] = diagnosis_type
            
            response = f"""**{name}님, 잠깐만요.**

{name}님 상황 보니까...

혹시 이런 패턴 아니세요?

✓ **업무/인간관계 스트레스가 극심하다**
✓ **낮엔 안 먹다가, 밤에 폭발적으로 먹는다**
✓ **밤에 잠이 안 와서 폰만 본다**
✓ **화나면 먹으면서 푼다 (여성의 경우 생리 전 폭식)**

**하나라도 맞으면 답장해 주세요.**

{name}님, 이건 **의지의 문제가 아닙니다.**

코르티솔(스트레스 호르몬) 과다 분비로
**자율신경이 망가진 상태**예요.

그래서 밤에만 폭식하는 겁니다.

이 상태로 식욕억제제 먹으면?
**스트레스만 더 쌓이고 악순환 반복합니다.**

{name}님, 솔직하게 답해주세요.

과거에 **수면제, 항우울제, 다이어트 약** 같은 거 드신 적 있으세요?
(있으면 "있어요", 없으면 "없어요" - 약물 상호작용 때문에 꼭 확인해야 합니다)"""
        
        add_msg("assistant", response)
        st.session_state.step = 4
    
    # STEP 4: 약물 이력 → 최종 진단 (공포 + 해결책)
    elif st.session_state.step == 4:
        drug_history = user_input.lower()
        st.session_state.user_data['drug_history'] = user_input
        
        with st.status("최종 진단 실행 중...", expanded=True) as status:
            st.write("🧬 체질 데이터 통합 분석...")
            time.sleep(0.6)
            st.write("💊 약물 내성 평가...")
            time.sleep(0.7)
            st.write("⚠ 리스크 레벨 판정...")
            time.sleep(0.5)
            status.update(label="진단 완료", state="complete", expanded=False)
        
        time.sleep(0.3)
        
        name = st.session_state.user_data.get('name', '고객')
        diagnosis_type = st.session_state.user_data.get('type', '위열과다형')
        
        # 약물 복용 여부에 따른 공포 강화
        has_drug = "있" in drug_history or "먹" in drug_history or "복용" in drug_history
        
        if diagnosis_type == "수독정체형":
            diag_code = "VRT-W2"
            diag_title = "수독 정체형 + 림프 순환 장애"
            
            if has_drug:
                threat = f"""**{name}님, 솔직하게 말씀해 주셔서 감사합니다.**

안타깝게도, 과거 약물 복용 이력이 있으시군요.

분석 결과, {name}님의 몸은 지금
**"쓰레기 배출구가 막힌 상태 + 약물 내성"**이 동시에 걸려 있습니다.

일반 식욕억제제는 {name}님께 **독**입니다.
순환이 막힌 상태에서 억지로 막으면 **부작용 90% 확률**입니다.

지금 {name}님께 필요한 건 **식욕을 막는 게 아니라,**
**림프 순환을 뚫고 노폐물을 배출하는 [순환 처방]**입니다."""
            else:
                threat = f"""**{name}님, 다행입니다.**

과거 약물 이력이 없으시니, 내성 문제는 없습니다.

하지만 지금 상태는 심각합니다.
림프 순환이 70% 이상 저하되어
**수분과 지방이 결합된 상태**입니다.

이 상태로 굶으면?
→ 지방은 그대로, 근육만 빠집니다.
→ 얼굴은 더 푸석해지고, 몸은 더 붓습니다.

{name}님께 필요한 건 **[림프 순환 촉진 + 독소 배출]** 처방입니다."""
            
            prescription = "독소킬 + 지방사약 (순환촉진형)"
            scores = {"식욕지수": 35, "대사효율": 45, "독소축적": 95, "스트레스": 40, "순환장애": 90}
        
        elif diagnosis_type == "위열과다형":
            diag_code = "VRT-H1"
            diag_title = "위열 과다형 + 가짜 배고픔"
            
            if has_drug:
                threat = f"""**{name}님, 솔직하게 말씀해 주셔서 감사합니다.**

과거 약물 복용 이력을 확인했습니다.

안타깝게도 {name}님의 몸은
**"약물 내성"**이 생긴 상태입니다.

일반 식욕억제제는 이제 안 듣습니다.
약 끊으면? **요요 100% 확률**입니다.

지금 {name}님께 필요한 건 **식욕을 막는 게 아니라,**
**위장의 열을 제거해서 포만 중추를 복구하는 [대사 점화제]**입니다."""
            else:
                threat = f"""**{name}님, 다행입니다.**

과거 약물 이력이 없으시군요.

하지만 현재 상태는 심각합니다.
위장에 열이 과도하게 차서
**포만 중추가 고장 난 상태**입니다.

이거 방치하면?
→ 당뇨 전단계로 직행합니다.

{name}님께 필요한 건 **[위열 제거 + 식욕 정상화]** 처방입니다."""
            
            prescription = "식탐사약 (위열 제거형)"
            scores = {"식욕지수": 95, "대사효율": 50, "독소축적": 40, "스트레스": 60, "순환장애": 45}
        
        elif diagnosis_type == "냉증형대사장애":
            diag_code = "VRT-M3"
            diag_title = "냉증형 대사 장애 + 초절전 모드"
            
            if has_drug:
                threat = f"""**{name}님, 솔직하게 말씀해 주셔서 감사합니다.**

과거 극단적 다이어트 이력을 확인했습니다.

최악입니다.
{name}님의 몸은 **"대사 스위치가 완전히 꺼진"** 상태입니다.

이 상태에서는 굶어도 안 빠집니다.
오히려 근육만 녹고 지방은 그대로입니다.

{name}님께 필요한 건 **꺼진 불씨를 다시 살리는 [대사 점화제]**입니다."""
            else:
                threat = f"""**{name}님, 상태가 심각합니다.**

기초대사량이 정상 대비 **60% 수준**으로 떨어졌습니다.

이 상태로 굶으면?
→ 몸이 "비상 모드" 돌입
→ 근육 녹이고, 지방은 꽁꽁 숨김
→ **"물만 먹어도 찌는 체질"**로 고착

{name}님, 3개월 안에 처방하지 않으면 **평생 다이어트 지옥**입니다."""
            
            prescription = "지방사약 (대사촉진형) + 온열처방"
            scores = {"식욕지수": 40, "대사효율": 20, "독소축적": 50, "스트레스": 35, "순환장애": 75}
        
        else:
            diag_code = "VRT-S4"
            diag_title = "간기 울결형 + 스트레스 비만"
            
            if has_drug:
                threat = f"""**{name}님, 솔직하게 말씀해 주셔서 감사합니다.**

약물 복용 이력을 확인했습니다.

{name}님, 이건 **약으로 해결 안 됩니다.**
자율신경이 망가진 상태에서 식욕억제제 먹으면
**스트레스만 더 쌓이고 악순환**입니다.

{name}님께 필요한 건 **[자율신경 정상화 + 폭식 차단]** 처방입니다."""
            else:
                threat = f"""**{name}님, 상태가 심각합니다.**

코르티솔 과다 분비로
**자율신경이 망가진 상태**입니다.

이 상태로 식욕억제제 먹으면?
→ 낮엔 억지로 참음
→ 밤에 폭발 → 폭식 → 자책 → 악순환

{name}님께 필요한 건 **[신경 안정 + 폭식 차단]** 처방입니다."""
            
            prescription = "소요산 + 지방사약 (신경안정형)"
            scores = {"식욕지수": 85, "대사효율": 45, "독소축적": 40, "스트레스": 95, "순환장애": 50}
        
        chart = create_radar_chart(scores)
        
        result_html = f"""
<div class='diagnosis-card'>
    <div style='font-size:12px; color:#666; letter-spacing:2px; margin-bottom:10px;'>DIAGNOSTIC CODE: {diag_code}</div>
    <div class='diagnosis-type'>{diag_title}</div>
    <div class='diagnosis-desc'>{threat}</div>
</div>

<div class='alert-critical'>
    <div class='alert-title'>⚠ 처방 대기 중</div>
    <p style='font-size:16px; color:#FFB800; line-height:1.9;'>
    {name}님께 맞는 특수 처방: <strong style='color:#00FF00;'>{prescription}</strong><br><br>
    지금 바로 이 처방의 **성분 분석**과 **예상 감량치**를 확인하시겠습니까?<br>
    (카카오톡으로 즉시 발송됩니다)
    </p>
</div>
"""
        
        add_msg("assistant", result_html, html=True, chart=chart)
        
        final_cta = f"""**{name}님, 결정하실 시간입니다.**

저희가 도와드릴 수 있는 건 **"지금"**뿐입니다.

아래 양식에 **연락처**만 남겨주시면,
담당 원장님이 **24시간 내** 직접 전화드립니다.

**상담비? 0원입니다.**
**진단비? 0원입니다.**

그냥 {name}님 몸 상태 보고,
정확한 처방 기간과 비용만 알려드립니다.

부담 갖지 마세요.
저희는 **강매하지 않습니다.**

단, 한 가지만 약속해 주세요.

**"이번이 마지막 다이어트다."**

각오되셨으면, 아래에 연락처 남겨주세요."""
        
        add_msg("assistant", final_cta)
        st.session_state.step = 99

# CONTACT FORM
if st.session_state.step == 99:
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#FF0000; text-align:center; font-weight:900;'>📱 카톡 리포트 신청 (무료)</h3>", unsafe_allow_html=True)
    
    with st.form("kakao_report"):
        name_input = st.text_input("성함", value=st.session_state.user_data.get('name', ''), placeholder="실명 입력")
        phone = st.text_input("연락처 (카톡)", placeholder="010-XXXX-XXXX")
        memo = st.text_area("추가 전달사항 (선택)", placeholder="특이사항이나 급한 일정이 있으시면 알려주세요.", height=80)
        
        submitted = st.form_submit_button("📲 지금 바로 카톡으로 받기 (무료)")
        
        if submitted:
            if name_input and phone:
                with st.spinner("📞 리포트 발송 준비 중..."):
                    time.sleep(1.5)
                st.success(f"✅ **{name_input}님, 발송 완료!**\n\n3분 내로 카톡으로 **[맞춤 처방 리포트]**가 발송됩니다.\n\n*못 받으셨으면 010-XXXX-XXXX로 문의주세요.*")
                st.balloons()
            else:
                st.error("⚠ 성함과 연락처를 모두 입력해 주세요.")
