import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random

# -----------------------------------------------------------------------------
# 1. SYSTEM CONFIGURATION (THE BLACK BOX THEME)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="VERITAS AI DIAGNOSIS",
    page_icon="👁‍🗨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# [CSS: 압도적인 몰입감과 긴장감 조성]
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700;900&display=swap');

    .stApp {
        background-color: #000000 !important;
        color: #E0E0E0;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* UI Elements Hiding */
    #MainMenu, footer, header {visibility: hidden;}

    /* Typography */
    h1 { color: #FFF; font-weight: 900; letter-spacing: -1px; }
    .highlight-red { color: #FF0033; font-weight: bold; text-shadow: 0 0 10px #FF0033; }
    .highlight-blue { color: #00BFFF; font-weight: bold; text-shadow: 0 0 10px #00BFFF; }
    
    /* System Logs */
    .sys-msg {
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: #444;
        border-left: 2px solid #333;
        padding-left: 10px;
        margin-bottom: 10px;
    }

    /* Chat Message (AI Persona) */
    .stChatMessage {
        background-color: #0A0A0A !important;
        border: 1px solid #222;
        margin-bottom: 15px;
    }
    
    /* Input Fields (Terminal Style) */
    .stTextArea > div > div > textarea {
        background-color: #050505 !important;
        color: #00FF00 !important;
        border: 1px solid #333 !important;
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 16px;
    }
    .stTextInput > div > div > input {
        background-color: #050505 !important;
        color: #FFF !important;
        border: 1px solid #333 !important;
    }

    /* Action Buttons (Neon Glitch) */
    .stButton > button {
        background-color: #000000 !important;
        color: #00BFFF !important;
        border: 1px solid #00BFFF !important;
        font-weight: bold;
        padding: 15px 0;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #00BFFF !important;
        color: #000 !important;
        box-shadow: 0 0 20px #00BFFF;
    }
    
    /* Critical Alert Box */
    .alert-box {
        border: 1px solid #FF0033;
        background-color: rgba(255, 0, 51, 0.1);
        padding: 20px;
        border-radius: 5px;
        text-align: center;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. LOGIC ENGINE (Simulated AI Intelligence)
# -----------------------------------------------------------------------------
if 'stage' not in st.session_state:
    st.session_state.stage = 'INTRO'
if 'user_context' not in st.session_state:
    st.session_state.user_context = {}

def stream_text(text, speed=0.03):
    """AI가 실시간으로 말하는 듯한 효과"""
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(full_text + "▌")
        time.sleep(speed)
    placeholder.markdown(full_text)

def analyze_keywords(text):
    """키워드 기반의 '콜드 리딩(Cold Reading)' 로직"""
    text = text.lower()
    if any(x in text for x in ['물', '붓기', '부종', '아침', '반지', '신발', '퉁퉁']):
        return "Edema", "혹시 아침에 일어나면 손이 쥐어지지 않거나, 저녁에 신발이 꽉 끼지 않으십니까? 이건 살이 아니라 '독소 수분'입니다."
    elif any(x in text for x in ['밥', '빵', '면', '단거', '초콜릿', '간식', '식욕', '배고파']):
        return "Carb", "식사 후에도 금방 허기가 지고, 스트레스를 받으면 단 것부터 찾게 되시죠? '가짜 배고픔'에 뇌가 속고 있는 상태입니다."
    elif any(x in text for x in ['술', '야식', '회식', '고기', '기름', '치킨']):
        return "Liver", "단순한 칼로리 문제가 아닙니다. 간의 해독 기능이 마비되어 지방을 태우지 못하고 쌓아두기만 하는 '대사 정체' 상태입니다."
    elif any(x in text for x in ['피곤', '무기력', '잠', '힘들', '우울', '스트레스']):
        return "Stress", "아무리 굶어도 안 빠지셨죠? 몸이 '생존 모드'에 들어가서 지방을 꽉 붙들고 있습니다. 이건 의지 문제가 아니라 호르몬 문제입니다."
    else:
        return "General", "체중계의 숫자보다 더 심각한 것은 체내의 '염증 반응'입니다. 현재 대사 시스템이 셧다운 직전입니다."

def generate_danger_chart(score):
    """위협적인 붉은색 레이더 차트"""
    categories = ['식욕 통제력', '림프 순환', '기초 대사량', '호르몬 균형', '염증 수치']
    # 환자에게 충격을 주기 위해 일부러 극단적인 수치 생성
    values = [random.randint(10, 30), random.randint(10, 40), random.randint(20, 50), random.randint(10, 30), random.randint(80, 100)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(255, 0, 51, 0.3)', # 붉은색 채우기
        line=dict(color='#FF0033', width=3), # 붉은색 선
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, linecolor='#333'),
            angularaxis=dict(color='#AAA')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(family='Noto Sans KR', color='#FFF')
    )
    return fig

# -----------------------------------------------------------------------------
# 3. UI FLOW (THE SALES FUNNEL)
# -----------------------------------------------------------------------------

# [HEADER]
st.markdown("<div style='text-align:right; font-size:10px; color:#555;'>VERITAS MED-AI v10.0 ● CONNECTED</div>", unsafe_allow_html=True)
st.divider()

# -----------------------------------------------------------------------------
# STAGE 1: THE INTERROGATION (하소연 유도)
# -----------------------------------------------------------------------------
if st.session_state.stage == 'INTRO':
    st.markdown("<h2 class='highlight-blue'>시스템 접속 승인.</h2>", unsafe_allow_html=True)
    
    with st.chat_message("assistant", avatar="👁‍🗨"):
        st.write("반갑습니다. 저는 귀하의 데이터를 분석할 AI 진단관입니다.")
        time.sleep(1)
        st.write("객관식 설문은 하지 않겠습니다. 귀하의 몸 상태는 버튼 몇 개로 정의할 수 없으니까요.")
        time.sleep(1)
        st.write("**지금 귀하를 가장 힘들게 하는 증상을 솔직하게 말씀해 주세요.**")
        st.caption("(예: 물만 먹어도 붓는다, 밤마다 폭식을 참을 수 없다, 운동해도 1kg도 안 빠진다 등)")

    complaint = st.text_area("증상 입력", height=100, placeholder="여기에 고민을 털어놓으세요. AI가 행간의 의미를 분석합니다.")

    if st.button("내 몸 상태 분석 시작 (ANALYZE) >>"):
        if len(complaint) > 2: # 최소한의 입력 확인
            st.session_state.user_context['complaint'] = complaint
            # 분석 연출 (있어 보이게)
            with st.status("언어 패턴 분석 중...", expanded=True) as status:
                st.write("키워드 추출: 불안, 정체, 독소...")
                time.sleep(0.7)
                st.write("임상 데이터베이스 대조 중 (20만 건)...")
                time.sleep(0.7)
                st.write("심리 상태 프로파일링...")
                time.sleep(0.7)
                status.update(label="분석 완료", state="complete", expanded=False)
            
            st.session_state.stage = 'CONFIRM'
            st.rerun()
        else:
            st.warning("AI가 분석할 수 있도록 증상을 조금만 더 자세히 적어주세요.")

# -----------------------------------------------------------------------------
# STAGE 2: THE COLD READING (점쟁이 화법 & 의인화)
# -----------------------------------------------------------------------------
elif st.session_state.stage == 'CONFIRM':
    
    # 키워드 분석 결과 가져오기
    tag, insight = analyze_keywords(st.session_state.user_context['complaint'])
    st.session_state.user_context['tag'] = tag
    
    with st.chat_message("assistant", avatar="👁‍🗨"):
        st.markdown(f"<span class='highlight-blue'>[AI 분석 결과 리포트]</span>", unsafe_allow_html=True)
        # 천천히 읽어주는 효과 (Cold Reading)
        stream_text(insight) 
        time.sleep(0.5)
        st.markdown(f"**이것은 단순 비만이 아닙니다. 몸이 보내는 <span class='highlight-red'>구조 신호(SOS)</span>입니다.**", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.chat_message("assistant", avatar="👁‍🗨"):
        st.write("정밀 수치 계산을 위해 신체 지수를 확인합니다. 이 데이터는 분석 즉시 파기됩니다.")

    c1, c2 = st.columns(2)
    height = c1.number_input("키 (cm)", value=160)
    weight = c2.number_input("체중 (kg)", value=60)

    if st.button("최종 위험도 진단 (FINAL DIAGNOSIS)"):
        st.session_state.stage = 'RESULT'
        st.rerun()

# -----------------------------------------------------------------------------
# STAGE 3: THE VERDICT (공포 마케팅 & 권위)
# -----------------------------------------------------------------------------
elif st.session_state.stage == 'RESULT':
    
    # 긴장감 조성 로딩
    progress = st.progress(0, text="대사 시스템 시뮬레이션 가동...")
    for i in range(100):
        time.sleep(0.02)
        progress.progress(i + 1)
    progress.empty()

    # 결과 화면
    st.markdown(f"""
    <div class='alert-box'>
        <h2 style='color:#FF0033; margin:0;'>⚠ DANGER WARNING</h2>
        <p style='color:#DDD; font-size:14px; margin-top:10px;'>
        귀하의 대사 시스템은 현재 <b>'붕괴 직전'</b>입니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    
    with c1:
        # 붉은색 위협적인 차트 (값이 낮을수록 위험한 느낌 or 높을수록 염증이 심한 느낌)
        st.plotly_chart(generate_danger_chart(80), use_container_width=True)
    
    with c2:
        tag = st.session_state.user_context.get('tag', 'General')
        diagnosis_name = ""
        prescription_logic = ""

        if tag == "Edema":
            diagnosis_name = "수독(水毒) 정체형 고도비만"
            prescription_logic = "현재 림프관이 막혀 물만 마셔도 살이 찌는 상태입니다. 굶는 다이어트는 몸을 더 붓게 만듭니다. '배수(Drainage)' 처방이 시급합니다."
        elif tag == "Stress":
            diagnosis_name = "부신 피로 증후군 (Cortisol Overload)"
            prescription_logic = "스트레스 호르몬이 지방 분해 스위치를 꺼버렸습니다. 지금 운동하면 오히려 몸이 축납니다. 자율신경을 안정시키는 약재가 먼저 들어가야 합니다."
        elif tag == "Liver":
            diagnosis_name = "간기 울결형 대사 장애"
            prescription_logic = "대사 필터(간)가 막혀 노폐물이 지방으로 변환되고 있습니다. 해독(Detox) 없이는 어떤 약도 듣지 않는 내성 단계입니다."
        elif tag == "Carb":
            diagnosis_name = "인슐린 저항성 위기 단계"
            prescription_logic = "탄수화물 중독으로 인해 췌장이 지쳐있습니다. 혈당 스파이크를 잡지 않으면 당뇨 전단계로 진행될 수 있습니다."
        else:
            diagnosis_name = "대사 불감증 (Metabolic Freeze)"
            prescription_logic = "엔진이 꺼진 차에 기름만 넣는 격입니다. 아무리 적게 먹어도 소모되지 않습니다. 대사 엔진을 강제로 켜는 '부스팅' 처방이 필요합니다."

        st.markdown(f"""
        <div style='margin-top: 20px;'>
            <div style='font-size:12px; color:#888;'>CLINICAL DIAGNOSIS ID: #X9-2025</div>
            <div style='font-size:24px; font-weight:bold; color:#FFF;'>{diagnosis_name}</div>
            <hr style='border-color:#333;'>
            <div style='font-size:15px; color:#DDD; line-height:1.6;'>
                {prescription_logic}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # STAGE 4: THE CLOSE (영업 이사의 마무리)
    # -------------------------------------------------------------------------
    st.markdown("---")
    
    st.markdown("""
    <h3 style='text-align:center; color:#00BFFF;'>AI 진단관의 최종 소견</h3>
    <p style='text-align:center; color:#CCC; font-size:14px;'>
    "지금 이 상태를 방치하면, 3개월 뒤에는 되돌릴 수 없는 <b>'고착화 단계'</b>로 진입합니다.<br>
    다행히 귀하의 데이터는 <b>[TYPE-C 맞춤 처방]</b>에 94% 적합 반응을 보입니다."
    </p>
    """, unsafe_allow_html=True)

    with st.form("lead_magnet"):
        st.markdown("**[골든타임 확보] AI 정밀 결과지 및 우선 상담권 발급**")
        st.caption("※ 신청자가 많아 조기 마감될 수 있습니다. (현재 대기: 14명)")
        
        col1, col2 = st.columns(2)
        name = col1.text_input("성함", placeholder="김00")
        phone = col2.text_input("연락처", placeholder="010-XXXX-XXXX")
        
        # 버튼 텍스트가 '제출'이 아니라 '혜택'으로
        submit = st.form_submit_button("💊 내 맞춤 처방전 확인하기 (Click)")
        
        if submit:
            if name and phone:
                st.success(f"{name}님, 접수되었습니다. AI가 분석한 데이터를 담당 원장님께 긴급 전송했습니다. 잠시만 대기해 주세요.")
                st.balloons()
            else:
                st.error("연락처가 누락되었습니다. 골든타임을 놓치지 마세요.")
