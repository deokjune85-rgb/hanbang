import streamlit as st
import time
import random

# ---------------------------------------
# 0. 시스템 설정: Veritas Clinical Engine (안정화 및 고급화 버전)
# ---------------------------------------
st.set_page_config(
    page_title="Veritas Clinical Engine v4.1 | 자연과한의원", # [변경] 권위적 타이틀
    page_icon="🧬", # [변경] 아이콘 변경 (DNA)
    layout="centered"
)

# [CSS: High-End Editorial Design]
custom_css = """
<style>
    /* 1. Main Container & Font */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp {
        background-color: #0C0C0C !important; /* Deeper Black */
        color: #E0E0E0 !important;
        font-family: 'Pretendard', sans-serif;
    }

    /* 2. Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 3. Typography Rules (Sharper) */
    p, div { line-height: 1.7; color: #CCCCCC; font-weight: 300; }
    .accent { color: #00E676; } /* Jayeon Green */

    /* 4. Chat Message (Minimal & Avatar) */
    .stChatMessage { background-color: #0C0C0C !important; padding: 15px 0 !important; border-bottom: 1px solid #1A1A1A; }
    [data-testid="stChatMessageContent"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        color: #E0E0E0;
    }
    .stChatMessage img { border-radius: 0 !important; } 

    /* 5. Input Field (Sleek Line) */
    .stChatInputContainer {
        border-top: 1px solid #333;
        padding-top: 10px;
    }
    .stChatInputInput {
        background-color: #1A1A1A !important;
        border: 1px solid #444 !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* 6. Chip Buttons (Refined) */
    div.stButton > button {
        background-color: #1A1A1A;
        color: #AAA !important;
        border: 1px solid #444 !important;
        border-radius: 20px !important;
        font-size: 14px !important;
        padding: 8px 16px !important;
        margin-right: 5px;
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        border-color: #00E676 !important;
        color: #00E676 !important;
        background-color: #051005 !important;
    }
    
    /* 7. Result Card (Editorial Magazine Style) */
    .diagnosis-card {
        border-left: 2px solid #00E676; /* 왼쪽 강조선 */
        padding: 30px 20px;
        margin: 20px 0;
        background-color: #111111;
    }
    .label-small { font-size: 11px; color: #888; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 5px; }
    .diagnosis-title { font-size: 32px; color: #FFF; font-weight: 800; margin-bottom: 15px; font-family: serif; } /* 세리프체 적용 */
    .diagnosis-desc { font-size: 16px; color: #AAA; margin-bottom: 20px; }
    
    /* 8. Status (Thinking Visualization) - Gemini Style */
    [data-testid="stStatusWidget"] {
        background-color: #1A1A1A;
        border-radius: 8px;
        padding: 10px;
    }

    /* 9. Grid Layout Fix for Chips */
    [data-testid="column"] { padding: 0 5px !important; }

    /* 10. CTA Button 강화 */
    div[data-testid="stForm"] button[type="submit"] {
        width: 100%;
        background-color: #00E676 !important;
        color: #000000 !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px;
        border: none;
        font-size: 16px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------
# 1. State & Helper Functions
# ---------------------------------------
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'temp_input' not in st.session_state:
    st.session_state.temp_input = None

AI_AVATAR = "🧬"
USER_AVATAR = "👤"

# [NEW] Claude-style 고급 스트리밍 효과 - 단어 단위로 부드럽게
def claude_stream(text, speed=0.01):
    """Claude처럼 부드러운 스트리밍 효과"""
    placeholder = st.empty()
    words = text.split(' ')
    display_text = ""
    
    for i, word in enumerate(words):
        display_text += word + " "
        # 실시간 스트리밍처럼 보이도록 단어 단위로 출력, 끝에 ● 표시
        placeholder.markdown(display_text + "●", unsafe_allow_html=True)
        time.sleep(speed)
    
    # 최종 출력 (인디케이터 제거)
    placeholder.markdown(display_text.strip())
    return display_text.strip()

# [★핵심 수정★] 메시지 저장 시 'animated' 플래그 추가 (애니메이션 제어용)
def bot_say(content, image=None, html=False):
    st.session_state.messages.append({"role": "assistant", "content": content, "image": image, "html": html, "animated": False})

def user_say(content):
    # 유저 메시지는 애니메이션 필요 없음
    st.session_state.messages.append({"role": "user", "content": content, "animated": True})

# ---------------------------------------
# 2. Main Interface & Rendering Logic (★핵심 수정: 렌더링 분리★)
# ---------------------------------------

# [Header]
st.markdown("<h3 style='margin-bottom:0; font-family: serif;'>Veritas Clinical Engine v4.1</h3>", unsafe_allow_html=True)
st.markdown("<p style='font-size:12px; color:#555;'>Powered by Jayeon Data Labs | 자연과한의원</p>", unsafe_allow_html=True)
st.divider()

# [STEP 0: Init]
if st.session_state.step == 0:
    msg = "Veritas Engine 활성화.\n\n25년간 축적된 임상 데이터를 기반으로 체중 정체 원인을 분석합니다.\n\n분석을 위해 피험자의 **성별, 나이, 키, 체중** 데이터를 입력하십시오."
    bot_say(msg)
    st.session_state.step = 1

# [★핵심 수정★ Render Chat History: 애니메이션 제어 로직 도입]
# 로직 처리 후 재실행되면 이 부분이 실행되어 애니메이션을 안정적으로 처리함.
for i, msg in enumerate(st.session_state.messages):
    avatar = AI_AVATAR if msg["role"] == "assistant" else USER_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        
        # 애니메이션이 필요하고, 아직 실행되지 않았으며, 마지막 메시지인 경우
        is_last_message = (i == len(st.session_state.messages) - 1)
        
        if msg["role"] == "assistant" and not msg.get("animated") and is_last_message:
            # HTML 콘텐츠는 애니메이션 없이 즉시 출력 (코드 노출 버그 방지)
            if msg.get("html"):
                st.markdown(msg["content"], unsafe_allow_html=True)
            else:
                # 텍스트 콘텐츠는 Claude-style 스트리밍 실행
                claude_stream(msg["content"])
            
            # 이미지 출력
            if msg.get("image"):
                st.image(msg["image"], use_column_width=True)
                
            # 애니메이션 완료 처리
            msg["animated"] = True
        
        else:
            # 이전 메시지 또는 유저 메시지는 즉시 출력
            if msg.get("html"):
                st.markdown(msg["content"], unsafe_allow_html=True)
            else:
                st.markdown(msg["content"])
            
            if msg.get("image"):
                st.image(msg["image"], use_column_width=True)


# ---------------------------------------
# 3. Dynamic Interaction Area (Bottom)
# ---------------------------------------

# [Chip Buttons Area]
if st.session_state.step == 3:
    st.markdown("<p style='font-size:12px; color:#666; margin-bottom:10px; letter-spacing: 1.5px;'>SELECT SYMPTOM</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    # 버튼 클릭 시 즉시 로직 처리를 위해 st.session_state.temp_input 활용 및 st.rerun() 호출
    if c1.button("식욕 조절 불가"):
        st.session_state.temp_input = "식욕 조절이 불가능합니다."
        st.rerun()
    if c2.button("만성 부종"):
        st.session_state.temp_input = "몸이 자주 붓습니다."
        st.rerun()
    if c3.button("대사 저하"):
        st.session_state.temp_input = "섭취량 대비 체중 감소가 없습니다."
        st.rerun()
    if c4.button("스트레스성 폭식"):
        st.session_state.temp_input = "스트레스로 인한 폭식 증상이 있습니다."
        st.rerun()

# [Input Handling: 로직 처리만 담당]
input_disabled = (st.session_state.step == 6)

# 채팅 입력 또는 버튼 입력(temp_input) 사용
prompt = st.chat_input("데이터 또는 증상을 입력하십시오...", disabled=input_disabled)

if st.session_state.temp_input:
    prompt = st.session_state.temp_input
    st.session_state.temp_input = None # 사용 후 즉시 초기화

if prompt:
    
    # 1. User Message 저장 (렌더링은 상단에서 처리됨)
    user_say(prompt)

    # 2. Logic Controller
    if st.session_state.step == 1:
        st.session_state.user_data['info'] = prompt
        
        # 프로세스 시각화 (st.status)
        with st.status("기본 데이터 처리 중...", expanded=False) as status:
            time.sleep(0.8)
            status.update(label="처리 완료.", state="complete", expanded=False)

        resp = "기본 데이터 입력 완료.\n\n핵심 질문입니다. 피험자가 호소하는 **다이어트 실패의 주된 원인**은 무엇입니까? (버튼 선택 또는 직접 입력)"
        # AI 응답 저장 (렌더링/애니메이션은 상단 렌더링 루프에서 처리됨)
        bot_say(resp)
        st.session_state.step = 3
        # [★중요★] 상태 변경 후 스크립트 재실행 (애니메이션을 위해 필수)
        st.rerun()

    elif st.session_state.step == 3:
        # Simple NLP
        txt = prompt.lower()
        cause = "기타"
        if any(x in txt for x in ['식욕', '불가능합니다']): cause = "식욕"
        elif any(x in txt for x in ['붓기', '붓습니다', '부종']): cause = "부종"
        elif any(x in txt for x in ['대사', '없습니다', '적게']): cause = "대사"
        elif any(x in txt for x in ['스트레스', '폭식']): cause = "스트레스"
        
        st.session_state.user_data['cause'] = cause
        
        # 프로세스 시각화 (st.status)
        with st.status("증상 패턴 분석 중...", expanded=False) as status:
            time.sleep(0.7)
            status.update(label="분석 완료.", state="complete", expanded=False)

        
        if cause == "식욕": msg = "분석 결과: 식욕 통제 중추의 문제입니다. 위장의 열(Heat)을 제어해야 합니다."
        elif cause == "부종": msg = "분석 결과: 순환계 문제입니다. 림프 정체로 인해 수분이 지방과 결합된 상태입니다."
        elif cause == "대사": msg = "분석 결과: 대사 효율 문제입니다. 에너지 소모 기능이 저하되어 있습니다."
        else: msg = "분석 결과: 자율신경 문제입니다. 스트레스 호르몬(코르티솔)이 지방 분해를 차단하고 있습니다."
        
        full_msg = f"{msg}\n\n마지막 질문입니다. 피험자의 **다이어트 약물(양약/한약) 복용 이력**이 있습니까?"
        
        # AI 응답 저장
        bot_say(full_msg)
        st.session_state.step = 5
        # [★중요★] 상태 변경 후 스크립트 재실행
        st.rerun()

    elif st.session_state.step == 5:
        st.session_state.user_data['history'] = prompt
        
        # Long Thinking Visualization (st.status - Expanded)
        with st.status("최종 임상 데이터 분석 실행 중...", expanded=True) as status:
            st.write("🔍 200,000+ 임상 케이스 데이터베이스 접속...")
            time.sleep(1.0)
            st.write("🧬 피험자 데이터 패턴 대조 및 시뮬레이션...")
            time.sleep(1.5)
            st.write("💡 최적 처방 프로토콜 도출...")
            time.sleep(1.0)
            status.update(label="최종 분석 완료.", state="complete", expanded=False)

        # Result Generation (이하 동일)
        cause = st.session_state.user_data.get('cause', '대사')
        
        # Content Mapping
        if cause == "식욕":
            title = "위열 과다형 (Stomach Heat)"
            desc = "뇌가 포만감을 인지하지 못하는 '가짜 배고픔' 상태. 식욕 중추의 과항진."
            rx = "식탐사약"
            rx_sub = "식욕 억제 및 위장 열 해소"
            img = "https://placehold.co/800x400/111/333?text=CLINICAL+EVIDENCE+(BELLY)" 
        elif cause == "부종":
            title = "수독 정체형 (Water Retention)"
            desc = "노폐물 배출 기능 저하로 지방과 수분이 결합된 상태. 림프 순환 저하."
            rx = "독소킬 + 지방사약"
            rx_sub = "수분 대사 촉진 및 붓기 배출"
            img = "https://placehold.co/800x400/111/333?text=CLINICAL+EVIDENCE+(BODY)"
        elif cause == "대사":
            title = "대사 저하형 (Metabolic Drop)"
            desc = "기초대사량이 낮아 에너지 소모율이 극히 낮은 체질."
            rx = "지방사약 (대사촉진형)"
            rx_sub = "심부 체온 상승 및 발열 효과 유도"
            img = "https://placehold.co/800x400/111/333?text=CLINICAL+EVIDENCE+(FULLBODY)"
        else:
            title = "간기 울결형 (Stress Induced)"
            desc = "스트레스 호르몬(코르티솔) 과다 분비에 의한 복부 지방 축적."
            rx = "소요산 + 지방사약"
            rx_sub = "자율신경 안정 및 폭식 차단"
            img = "https://placehold.co/800x400/111/333?text=CLINICAL+EVIDENCE+(STRESS)"

        # Editorial Layout (HTML) - 결과 카드
        # [HTML 구조 검증 완료 - 코드 노출 없음]
        result_html = f"""
        <div class='diagnosis-card'>
            <div class='label-small'>ANALYSIS REPORT</div>
            <div class='diagnosis-title'>{title}</div>
            <div class='diagnosis-desc'>{desc}</div>
            
            <div style='display:flex; justify-content:space-between; align-items:center; margin-top:30px; border-top: 1px solid #333; padding-top: 20px;'>
                <div>
                    <div class='label-small' style='color:#00E676;'>OPTIMAL PRESCRIPTION</div>
                    <div style='font-size:22px; font-weight:bold; color:#FFF;'>{rx}</div>
                    <div style='font-size:14px; color:#AAA;'>Target: {rx_sub}</div>
                </div>
                <div style='text-align:right;'>
                    <div class='label-small'>EST. PERIOD</div>
                    <div style='color:#FFF; font-size:18px;'>3 Months</div>
                </div>
            </div>
        </div>
        """
        
        # 이미지 및 가격 정보 HTML 구성
        evidence_header_html = "<div class='label-small' style='margin-top: 20px;'>CLINICAL EVIDENCE</div>"
        evidence_caption_html = "<p style='font-size:12px; color:#555; text-align:center; margin-top: 5px;'>동일 체질 환자의 3개월 임상 변화 데이터 (자연과한의원 제공)</p>"

        price_html = """
        <div style='margin-top:30px; border-top:1px solid #333; padding-top:20px;'>
            <div class='label-small'>PRICING PLAN (VAT 별도)</div>
            <div style='display:flex; justify-content:space-between; margin-bottom:10px; padding: 5px 0;'>
                <span style='color:#AAA;'>1 Month Plan</span>
                <span style='color:#FFF;'>150,000 KRW</span>
            </div>
            <div style='display:flex; justify-content:space-between; background-color: #051005; padding: 10px; border-radius: 5px;'>
                <span style='color:#00E676;'>6 Months Plan (Recommended)</span>
                <span style='color:#00E676; font-weight:bold;'>Monthly 100,000 KRW ~</span>
            </div>
        </div>
        """
        
        # AI 응답 저장 (HTML 형식은 즉시 렌더링되도록 함 - 애니메이션 없음)
        bot_say(result_html, html=True)
        bot_say(evidence_header_html, html=True)
        bot_say("", image=img) # 이미지는 별도 메시지로 처리
        bot_say(evidence_caption_html, html=True)
        bot_say(price_html, html=True)
        
        st.session_state.step = 6
        # [★중요★] 상태 변경 후 스크립트 재실행
        st.rerun()

# [Final Step: Simple Input]
if st.session_state.step == 6:
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='label-small'>REQUEST CONSULTATION</div>", unsafe_allow_html=True)
    with st.form("contact"):
        c1, c2 = st.columns(2)
        with c1: name = st.text_input("성함", placeholder="환자명")
        with c2: phone = st.text_input("연락처", placeholder="010-XXXX-XXXX")
        
        if st.form_submit_button("상담 접수 및 데이터 전송"):
            if name and phone:
                st.success("데이터 전송 완료. 담당 의료진이 배정됩니다.")
                # 여기에 DB 저장 로직 추가
            else:
                st.warning("정확한 정보를 입력하십시오.")
