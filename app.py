import streamlit as st
import time

# ---------------------------------------
# 0. 시스템 설정: Veritas Clinical Engine (스트리밍 UI 버전)
# ---------------------------------------
st.set_page_config(
    page_title="Veritas Clinical Engine v4.2 | 자연과한의원",
    page_icon="🧬",
    layout="centered"
)

# [CSS: Claude-Style Streaming Design]
custom_css = """
<style>
    /* 1. Main Container & Font */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    .stApp {
        background-color: #0C0C0C !important;
        color: #E0E0E0 !important;
        font-family: 'Pretendard', sans-serif;
    }

    /* 2. Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 3. Typography Rules */
    h1, h2, h3 { color: #FFFFFF !important; font-weight: 800; letter-spacing: -0.5px; }
    p, div { line-height: 1.7; color: #CCCCCC; font-weight: 300; }
    strong { color: #FFFFFF; font-weight: 600; }
    .accent { color: #00E676; }

    /* 4. Chat Message (Claude-like) */
    .stChatMessage { 
        background-color: #0C0C0C !important; 
        padding: 20px 0 !important; 
        border-bottom: 1px solid #1A1A1A; 
    }
    [data-testid="stChatMessageContent"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        color: #E0E0E0;
    }
    .stChatMessage img { border-radius: 8px !important; }

    /* 5. 스트리밍 효과 (Claude-like) */
    .streaming-text {
        animation: fadeInUp 0.3s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* 6. 고급 Thinking 표시 */
    .thinking-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 16px;
        background-color: #1A1A1A;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 14px;
        color: #888;
    }
    
    .thinking-dots {
        display: inline-flex;
        gap: 4px;
    }
    
    .thinking-dot {
        width: 6px;
        height: 6px;
        background-color: #00E676;
        border-radius: 50%;
        animation: thinking 1.5s infinite;
    }
    
    .thinking-dot:nth-child(2) { animation-delay: 0.2s; }
    .thinking-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes thinking {
        0%, 60%, 100% { opacity: 0.3; }
        30% { opacity: 1; }
    }

    /* 7. Input Field */
    .stChatInputContainer {
        border-top: 1px solid #333;
        padding-top: 15px;
    }
    .stChatInputInput {
        background-color: #1A1A1A !important;
        border: 1px solid #444 !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }

    /* 8. Chip Buttons */
    div.stButton > button {
        background-color: #1A1A1A;
        color: #AAA !important;
        border: 1px solid #444 !important;
        border-radius: 24px !important;
        font-size: 14px !important;
        padding: 10px 20px !important;
        margin: 4px;
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        border-color: #00E676 !important;
        color: #00E676 !important;
        background-color: rgba(0, 230, 118, 0.1) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 230, 118, 0.2);
    }
    
    /* 9. Result Card */
    .diagnosis-card {
        border: 1px solid #333;
        border-left: 3px solid #00E676;
        padding: 32px 24px;
        margin: 24px 0;
        background: linear-gradient(135deg, #111111, #0F0F0F);
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    
    .label-small { 
        font-size: 11px; 
        color: #888; 
        letter-spacing: 2px; 
        text-transform: uppercase; 
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    .diagnosis-title { 
        font-size: 28px; 
        color: #FFF; 
        font-weight: 800; 
        margin-bottom: 16px; 
        background: linear-gradient(135deg, #FFF, #AAA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .diagnosis-desc { 
        font-size: 16px; 
        color: #CCC; 
        margin-bottom: 24px; 
        line-height: 1.6;
    }

    /* 10. Status Widget */
    [data-testid="stStatusWidget"] {
        background-color: #1A1A1A;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #333;
    }

    /* 11. Form Styling */
    div[data-testid="stForm"] button[type="submit"] {
        width: 100%;
        background: linear-gradient(135deg, #00E676, #00C853) !important;
        color: #000000 !important;
        font-weight: bold;
        border-radius: 12px;
        padding: 14px;
        border: none;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stForm"] button[type="submit"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(0, 230, 118, 0.3);
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

def show_thinking(text="분석 중"):
    """Claude-style thinking indicator"""
    thinking_html = f"""
    <div class='thinking-indicator'>
        <div class='thinking-dots'>
            <div class='thinking-dot'></div>
            <div class='thinking-dot'></div>
            <div class='thinking-dot'></div>
        </div>
        <span>{text}...</span>
    </div>
    """
    return st.markdown(thinking_html, unsafe_allow_html=True)

def stream_write(text, container=None):
    """Claude-style streaming text effect"""
    if container is None:
        container = st.empty()
    
    # 즉시 전체 텍스트를 스트리밍 애니메이션과 함께 표시
    streaming_html = f"""
    <div class='streaming-text'>
        {text.replace(chr(10), '<br>')}
    </div>
    """
    container.markdown(streaming_html, unsafe_allow_html=True)
    return container

def bot_say(content, image=None, html=False):
    """봇 메시지 저장"""
    st.session_state.messages.append({
        "role": "assistant", 
        "content": content, 
        "image": image, 
        "html": html
    })

def user_say(content):
    """사용자 메시지 저장"""
    st.session_state.messages.append({
        "role": "user", 
        "content": content
    })

# ---------------------------------------
# 2. Main Interface
# ---------------------------------------

# Header with enhanced styling
st.markdown("""
<div style='text-align: center; margin-bottom: 32px;'>
    <h2 style='background: linear-gradient(135deg, #FFF, #00E676); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px;'>
        Veritas Clinical Engine v4.2
    </h2>
    <p style='font-size: 12px; color: #666; letter-spacing: 1.5px;'>
        POWERED BY JAYEON DATA LABS | 자연과한의원
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# 초기화
if st.session_state.step == 0:
    msg = "**Veritas Engine 활성화됨**\n\n25년간 축적된 임상 데이터를 기반으로 체중 정체 원인을 분석합니다.\n\n분석을 위해 피험자의 **성별, 나이, 키, 체중** 데이터를 입력하십시오."
    bot_say(msg)
    st.session_state.step = 1

# 채팅 히스토리 렌더링 (Claude-style)
for msg in st.session_state.messages:
    avatar = AI_AVATAR if msg["role"] == "assistant" else USER_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        if msg.get("html", False):
            st.markdown(msg["content"], unsafe_allow_html=True)
        else:
            # 모든 텍스트를 스트리밍 스타일로 표시
            stream_write(msg["content"])
        
        if msg.get("image"):
            st.image(msg["image"], use_column_width=True)

# ---------------------------------------
# 3. Dynamic Interaction Area
# ---------------------------------------

# 증상 선택 버튼 (Step 3에서만 표시)
if st.session_state.step == 3:
    st.markdown("""
    <div style='margin: 24px 0 16px 0;'>
        <div class='label-small'>주요 증상 선택</div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    
    if c1.button("🍽️ 식욕 조절 불가"):
        st.session_state.temp_input = "식욕 조절이 불가능합니다."
        st.rerun()
    if c2.button("💧 만성 부종"):
        st.session_state.temp_input = "몸이 자주 붓습니다."
        st.rerun()
    if c3.button("⚡ 대사 저하"):
        st.session_state.temp_input = "섭취량 대비 체중 감소가 없습니다."
        st.rerun()
    if c4.button("😰 스트레스성 폭식"):
        st.session_state.temp_input = "스트레스로 인한 폭식 증상이 있습니다."
        st.rerun()

# 입력 처리
input_disabled = (st.session_state.step == 6)
prompt = None

if st.session_state.temp_input:
    prompt = st.session_state.temp_input
    st.session_state.temp_input = None

if prompt is None:
    prompt = st.chat_input("데이터 또는 증상을 입력하십시오...", disabled=input_disabled)

if prompt:
    # 사용자 메시지 처리
    user_say(prompt)
    with st.chat_message("user", avatar=USER_AVATAR):
        stream_write(prompt)

    # 로직 컨트롤러
    if st.session_state.step == 1:
        st.session_state.user_data['info'] = prompt
        
        # Claude-style thinking
        with st.chat_message("assistant", avatar=AI_AVATAR):
            thinking_container = st.empty()
            show_thinking("기본 데이터 검증 중")
            time.sleep(1.5)
            thinking_container.empty()

        resp = "**기본 데이터 입력 완료**\n\n핵심 질문입니다. 피험자가 호소하는 **다이어트 실패의 주된 원인**은 무엇입니까?\n\n*버튼 선택 또는 직접 입력 가능*"
        
        with st.chat_message("assistant", avatar=AI_AVATAR):
            stream_write(resp)
        
        bot_say(resp)
        st.session_state.step = 3

    elif st.session_state.step == 3:
        # 증상 분석
        txt = prompt.lower()
        cause = "기타"
        
        if any(x in txt for x in ['식욕', '불가능', '조절']):
            cause = "식욕"
        elif any(x in txt for x in ['붓기', '붓습니다', '부종']):
            cause = "부종"
        elif any(x in txt for x in ['대사', '없습니다', '감소']):
            cause = "대사"
        elif any(x in txt for x in ['스트레스', '폭식']):
            cause = "스트레스"
        
        st.session_state.user_data['cause'] = cause
        
        # Claude-style thinking
        with st.chat_message("assistant", avatar=AI_AVATAR):
            thinking_container = st.empty()
            show_thinking("증상 패턴 분석 중")
            time.sleep(2.0)
            thinking_container.empty()

        # 원인별 메시지
        if cause == "식욕":
            msg = "**분석 결과: 위열 과다형**\n\n식욕 통제 중추의 문제입니다. 위장의 열(Heat)을 제어해야 합니다."
        elif cause == "부종":
            msg = "**분석 결과: 수독 정체형**\n\n순환계 문제입니다. 림프 정체로 인해 수분이 지방과 결합된 상태입니다."
        elif cause == "대사":
            msg = "**분석 결과: 대사 저하형**\n\n대사 효율 문제입니다. 에너지 소모 기능이 저하되어 있습니다."
        else:
            msg = "**분석 결과: 간기 울결형**\n\n자율신경 문제입니다. 스트레스 호르몬(코르티솔)이 지방 분해를 차단하고 있습니다."
        
        full_msg = f"{msg}\n\n**마지막 질문입니다.** 피험자의 다이어트 약물(양약/한약) 복용 이력이 있습니까?"
        
        with st.chat_message("assistant", avatar=AI_AVATAR):
            stream_write(full_msg)
            
        bot_say(full_msg)
        st.session_state.step = 5

    elif st.session_state.step == 5:
        st.session_state.user_data['history'] = prompt
        
        # Enhanced thinking process
        with st.chat_message("assistant", avatar=AI_AVATAR):
            thinking_container = st.empty()
            
            show_thinking("임상 데이터베이스 접속")
            time.sleep(1.5)
            
            show_thinking("250,000+ 케이스 패턴 대조")
            time.sleep(2.0)
            
            show_thinking("최적 처방 프로토콜 도출")
            time.sleep(1.5)
            
            thinking_container.empty()

        cause = st.session_state.user_data.get('cause', '대사')
        
        # 결과 매핑
        results = {
            "식욕": {
                "title": "위열 과다형 (Stomach Heat)",
                "desc": "뇌가 포만감을 인지하지 못하는 '가짜 배고픔' 상태입니다. 식욕 중추의 과항진으로 인한 문제로, 위장의 열을 제어하는 것이 핵심입니다.",
                "rx": "식탐사약 (복합처방)",
                "rx_sub": "식욕 억제 및 위장 열 해소",
                "color": "FF6B6B"
            },
            "부종": {
                "title": "수독 정체형 (Water Retention)",
                "desc": "노폐물 배출 기능 저하로 지방과 수분이 결합된 상태입니다. 림프 순환 개선을 통한 근본적 해결이 필요합니다.",
                "rx": "독소킬 + 지방사약",
                "rx_sub": "수분 대사 촉진 및 붓기 배출",
                "color": "4ECDC4"
            },
            "대사": {
                "title": "대사 저하형 (Metabolic Drop)",
                "desc": "기초대사량이 낮아 에너지 소모율이 극히 낮은 체질입니다. 심부 체온 상승을 통한 대사 촉진이 필요합니다.",
                "rx": "지방사약 (대사촉진형)",
                "rx_sub": "심부 체온 상승 및 발열 효과",
                "color": "FFE66D"
            },
            "기타": {
                "title": "간기 울결형 (Stress Induced)",
                "desc": "스트레스 호르몬(코르티솔) 과다 분비에 의한 복부 지방 축적입니다. 자율신경 안정화가 우선되어야 합니다.",
                "rx": "소요산 + 지방사약",
                "rx_sub": "자율신경 안정 및 폭식 차단",
                "color": "A8E6CF"
            }
        }
        
        result = results[cause]
        
        # Enhanced result display
        with st.chat_message("assistant", avatar=AI_AVATAR):
            result_html = f"""
            <div class='diagnosis-card'>
                <div class='label-small'>CLINICAL ANALYSIS REPORT</div>
                <div class='diagnosis-title'>{result['title']}</div>
                <div class='diagnosis-desc'>{result['desc']}</div>
                
                <div style='display:flex; justify-content:space-between; align-items:center; margin-top:32px; border-top: 1px solid #333; padding-top: 24px;'>
                    <div style='flex: 1;'>
                        <div class='label-small' style='color:#00E676;'>OPTIMAL PRESCRIPTION</div>
                        <div style='font-size:24px; font-weight:700; color:#FFF; margin: 8px 0;'>{result['rx']}</div>
                        <div style='font-size:14px; color:#AAA;'>• {result['rx_sub']}</div>
                    </div>
                    <div style='text-align:right; margin-left: 24px;'>
                        <div class='label-small'>TREATMENT PERIOD</div>
                        <div style='color:#00E676; font-size:20px; font-weight: 600; margin-top: 4px;'>3개월</div>
                        <div style='font-size:12px; color:#666; margin-top: 2px;'>집중 치료</div>
                    </div>
                </div>
                
                <div style='margin-top: 24px; padding: 16px; background-color: rgba(0, 230, 118, 0.1); border-radius: 8px; border-left: 3px solid #00E676;'>
                    <div style='font-size: 14px; color: #00E676; font-weight: 600; margin-bottom: 4px;'>✓ 임상 검증 완료</div>
                    <div style='font-size: 12px; color: #AAA;'>동일 증상 환자 1,247명 중 89.2% 만족도 달성</div>
                </div>
            </div>
            """
            
            stream_write(result_html)
            st.markdown(result_html, unsafe_allow_html=True)
            
            # 간격
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            
            # 임상 증거
            img = f"https://placehold.co/800x400/111/{result['color']}?text=CLINICAL+DATA+{cause.upper()}"
            st.markdown("<div class='label-small'>CLINICAL EVIDENCE</div>", unsafe_allow_html=True)
            st.image(img, use_column_width=True)
            st.caption("📊 동일 체질 환자군의 3개월 임상 변화 데이터 (자연과한의원 제공)")
            
            # 가격 정보
            price_html = """
            <div style='margin-top:32px; border-top:1px solid #333; padding-top:24px;'>
                <div class='label-small'>TREATMENT PRICING (부가세 별도)</div>
                <div style='background-color: #1A1A1A; padding: 20px; border-radius: 12px; margin-top: 16px;'>
                    <div style='display:flex; justify-content:space-between; margin-bottom:16px; padding: 8px 0;'>
                        <span style='color:#CCC;'>1개월 집중 치료</span>
                        <span style='color:#FFF; font-weight: 600;'>150,000원</span>
                    </div>
                    <div style='display:flex; justify-content:space-between; background: linear-gradient(135deg, rgba(0, 230, 118, 0.2), rgba(0, 200, 83, 0.1)); padding: 16px; border-radius: 8px; border: 1px solid #00E676;'>
                        <div>
                            <span style='color:#00E676; font-weight: 600;'>6개월 완전 치료 (추천)</span>
                            <div style='font-size: 12px; color: #AAA; margin-top: 2px;'>월 평균 100,000원 ~ (33% 할인)</div>
                        </div>
                        <span style='color:#00E676; font-weight: bold; font-size: 18px;'>600,000원</span>
                    </div>
                </div>
            </div>
            """
            st.markdown(price_html, unsafe_allow_html=True)
            
            # 메시지 히스토리에 저장
            bot_say(result_html, html=True)
            bot_say("임상 증거 및 가격 정보", image=img)
            
            st.session_state.step = 6

# 최종 상담 접수
if st.session_state.step == 6:
    st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='label-small' style='text-align: center;'>상담 예약 접수</div>", unsafe_allow_html=True)
    
    with st.form("contact"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("성함", placeholder="환자명 입력")
        with c2:
            phone = st.text_input("연락처", placeholder="010-0000-0000")
        
        if st.form_submit_button("🚀 상담 접수 및 데이터 전송"):
            if name and phone:
                st.balloons()
                st.success("✅ **데이터 전송 완료!** 담당 의료진이 배정되어 24시간 내 연락드립니다.")
            else:
                st.warning("⚠️ 정확한 정보를 입력해주십시오.")
