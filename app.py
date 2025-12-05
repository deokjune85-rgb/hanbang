# app.py
"""
IMD Medical System - Gemini 스타일 챗봇
"""

import streamlit as st
import time
from conversation_manager import get_conversation_manager
from prompt_engine import get_prompt_engine, generate_ai_response
from lead_handler import LeadHandler
from config import (
    APP_TITLE,
    APP_ICON,
    LAYOUT,
    COLOR_PRIMARY,
    COLOR_BG,
    COLOR_TEXT,
    COLOR_AI_BUBBLE,
    COLOR_USER_BUBBLE,
    COLOR_BORDER,
    PREFERRED_DATE_OPTIONS
)

# ============================================
# 페이지 설정
# ============================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT,
    initial_sidebar_state="collapsed"
)

# ============================================
# CSS
# ============================================
st.markdown(f"""
<style>
/* 전체 흰색 배경 (가로 100%) */
.stApp {{
    background: white !important;
}}

.main {{
    background: white !important;
}}

.main .block-container {{
    padding: 0 !important;
    max-width: 720px !important;
    margin: 0 auto !important;
    background: white !important;
}}

header, .stDeployButton {{
    display: none !important;
}}

footer {{
    display: none !important;
}}

/* Streamlit 기본 여백 제거 */
.appview-container {{
    background: white !important;
}}

section[data-testid="stSidebar"] {{
    display: none !important;
}}

/* 타이틀 */
.title-box {{
    text-align: center;
    padding: 20px 20px 12px 20px;
    background: white;
}}

.title-box h1 {{
    font-family: Arial, sans-serif !important;
    font-size: 24px !important;
    font-weight: 700 !important;
    color: {COLOR_PRIMARY} !important;
    margin: 0 !important;
    letter-spacing: 0.5px !important;
    white-space: nowrap !important;
}}

.title-box .sub {{
    font-size: 12px;
    color: #4B5563;
    margin-top: 4px;
}}

/* 채팅 영역 */
.chat-area {{
    padding: 12px 20px 16px 20px;
    background: white !important;
    min-height: 150px;
    margin-bottom: 160px;
}}

.ai-msg {{
    background: white !important;
    color: #1F2937 !important;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 0;
    max-width: 85%;
    display: inline-block;
    font-size: 15px !important;
    line-height: 1.5;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    border: 1px solid #F3F4F6;
}}

/* 점점이 제거 */
.ai-msg::before,
.ai-msg::after {{
    display: none !important;
}}

.user-msg {{
    background: {COLOR_USER_BUBBLE};
    color: #1F2937;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0;
    max-width: 70%;
    display: inline-block;
    font-size: 14px;
    float: right;
    clear: both;
}}

.msg-right {{
    text-align: right;
    clear: both;
}}

/* 버튼 영역 */
.btn-area {{
    padding: 0 20px 16px 20px;
    background: white;
    margin-bottom: 160px;
}}

.btn-title {{
    text-align: center;
    font-size: 13px;
    font-weight: 600;
    color: {COLOR_PRIMARY};
    margin-bottom: 10px;
}}

.stButton > button {{
    width: 100% !important;
    background: white !important;
    color: {COLOR_PRIMARY} !important;
    border: 1.5px solid {COLOR_BORDER} !important;
    padding: 13px !important;
    font-size: 14px !important;
    border-radius: 20px !important;
    font-weight: 500 !important;
    margin-bottom: 8px !important;
}}

.stButton > button:hover {{
    background: #F9FAFB !important;
    border-color: {COLOR_PRIMARY} !important;
}}

/* 입력창 (가로 100% 흰색) */
.stChatInput {{
    position: fixed !important;
    bottom: 60px !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    background: white !important;
    padding: 10px 0 !important;
    box-shadow: 0 -2px 6px rgba(0,0,0,0.08) !important;
    z-index: 999 !important;
}}

.stChatInput > div {{
    max-width: 680px !important;
    margin: 0 auto !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 24px !important;
    background: white !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
}}

.stChatInput input {{
    color: #1F2937 !important;
    background: white !important;
}}

.stChatInput input::placeholder {{
    color: #9CA3AF !important;
    font-size: 14px !important;
}}

/* 푸터 (가로 100% 흰색) */
.footer {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    background: white !important;
    padding: 12px 20px;
    text-align: center;
    font-size: 11px;
    color: #9CA3AF;
    border-top: 1px solid {COLOR_BORDER};
    z-index: 998;
}}

.footer b {{
    color: {COLOR_TEXT};
    font-weight: 600;
}}

/* 폼 */
.stForm {{
    background: white;
    padding: 20px;
    border: 1px solid {COLOR_BORDER};
    border-radius: 12px;
    margin: 16px 20px 180px 20px;
}}

input, textarea, select {{
    border: 1px solid {COLOR_BORDER} !important;
    border-radius: 8px !important;
    background: white !important;
}}

/* 모든 Streamlit 요소 흰색 배경 */
.element-container, .stMarkdown, div[data-testid="stVerticalBlock"], 
div[data-testid="stHorizontalBlock"], .row-widget {{
    background: white !important;
}}

/* 스피너 등 모든 요소 */
div[data-testid="stspinner"] {{
    background: white !important;
}}

/* ========== 모바일 반응형 ========== */
@media (max-width: 768px) {{
    /* Streamlit 기본 여백 강제 제거 */
    .main .block-container {{
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }}
    
    .element-container {{
        margin: 0 !important;
        padding: 0 !important;
    }}
    
    div[data-testid="stVerticalBlock"] > div {{
        gap: 0 !important;
    }}
    
    /* 타이틀 작게 + 상단 여백 최소화 */
    .title-box {{
        padding: 4px 16px 4px 16px !important;
        margin: 0 !important;
    }}
    
    .title-box h1 {{
        font-size: 20px !important;
        line-height: 1.2 !important;
        margin: 0 !important;
    }}
    
    .title-box .sub {{
        font-size: 11px;
        margin: 2px 0 0 0 !important;
    }}
    
    /* 채팅 영역 여백 최소화 */
    .chat-area {{
        padding: 4px 16px 6px 16px !important;
        min-height: 100px;
        margin: 0 !important;
    }}
    
    .ai-msg {{
        font-size: 14px !important;
        padding: 12px 16px;
        max-width: 90%;
        margin: 4px 0 !important;
    }}
    
    .user-msg {{
        font-size: 13px;
        padding: 10px 16px;
        max-width: 75%;
        margin: 4px 0 !important;
    }}
    
    /* 버튼 영역 간격 최소화 */
    .btn-area {{
        padding: 0 16px 10px 16px !important;
        margin: 0 !important;
    }}
    
    .btn-title {{
        font-size: 12px;
        margin: 0 0 6px 0 !important;
    }}
    
    .stButton {{
        margin: 0 !important;
    }}
    
    .stButton > button {{
        padding: 11px !important;
        font-size: 13px !important;
        margin-bottom: 6px !important;
    }}
    
    /* 입력창 */
    .stChatInput {{
        padding: 8px 12px !important;
    }}
    
    .stChatInput > div {{
        max-width: 100% !important;
        margin: 0 !important;
    }}
    
    .stChatInput input::placeholder {{
        font-size: 13px !important;
    }}
    
    /* 푸터 */
    .footer {{
        padding: 10px 16px;
        font-size: 10px;
    }}
}}

/* 작은 모바일 (iPhone SE 등) */
@media (max-width: 400px) {{
    .title-box {{
        padding: 2px 12px 2px 12px !important;
    }}
    
    .title-box h1 {{
        font-size: 18px !important;
    }}
    
    .chat-area {{
        padding: 2px 12px 4px 12px !important;
    }}
    
    .ai-msg {{
        font-size: 13px !important;
        margin: 3px 0 !important;
    }}
    
    .btn-area {{
        padding: 0 12px 8px 12px !important;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ============================================
# 초기화
# ============================================
conv_manager = get_conversation_manager()
prompt_engine = get_prompt_engine()
lead_handler = LeadHandler()

# 첫 메시지 (한 번만)
if 'app_initialized' not in st.session_state:
    initial_msg = prompt_engine.generate_initial_message()
    conv_manager.add_message("ai", initial_msg)
    st.session_state.app_initialized = True

# ============================================
# 헤더
# ============================================
st.markdown("""
<div class="title-box">
    <h1>IMD MEDICAL SYSTEM</h1>
    <div class="sub">24시간 AI 한의사 상담</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# 채팅 히스토리
# ============================================
st.markdown('<div class="chat-area">', unsafe_allow_html=True)

for msg in conv_manager.get_history():
    if msg['role'] == 'ai':
        st.markdown(f'<div class="ai-msg">{msg["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="msg-right"><span class="user-msg">{msg["text"]}</span></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# 버튼
# ============================================
if not conv_manager.is_ready_for_conversion():
    st.markdown('<div class="btn-area">', unsafe_allow_html=True)
    st.markdown('<div class="btn-title">빠른 상담</div>', unsafe_allow_html=True)
    
    buttons = conv_manager.get_recommended_buttons()
    col1, col2 = st.columns(2)
    
    for idx, btn in enumerate(buttons[:4]):
        with (col1 if idx % 2 == 0 else col2):
            if st.button(btn, key=f"btn_{idx}", use_container_width=True):
                if "전화" in btn:
                    st.info("📞 02-1234-5678 (평일 09:00-18:00)")
                else:
                    conv_manager.add_message("user", btn, metadata={"type": "button"})
                    
                    context = conv_manager.get_context()
                    history = conv_manager.get_formatted_history(for_llm=True)
                    
                    with st.spinner("상담 중..."):
                        time.sleep(0.8)
                        ai_response = generate_ai_response(btn, context, history)
                    
                    conv_manager.add_message("ai", ai_response)
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# 입력창
# ============================================
user_input = st.chat_input("IMD입니다. 궁금하신 점을 물어보세요")

if user_input:
    conv_manager.add_message("user", user_input, metadata={"type": "text"})
    
    context = conv_manager.get_context()
    history = conv_manager.get_formatted_history(for_llm=True)
    
    with st.spinner("상담 중..."):
        time.sleep(1.0)
        ai_response = generate_ai_response(user_input, context, history)
    
    conv_manager.add_message("ai", ai_response)
    st.rerun()

# ============================================
# 예약 폼
# ============================================
if conv_manager.is_ready_for_conversion() and conv_manager.get_context()['stage'] != 'complete':
    st.markdown("---")
    st.markdown('<div style="text-align:center; color:#2563EB; font-weight:600; margin:20px 0 10px;">예약 신청</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#6B7280; font-size:13px;'>빠른 시일 내 연락드리겠습니다</p>", unsafe_allow_html=True)
    
    with st.form("reservation_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("성함 *", placeholder="홍길동")
        with col2:
            contact = st.text_input("연락처 *", placeholder="010-1234-5678")
        
        symptom = st.text_area("주요 증상 *", placeholder="예: 허리 통증, 다이어트 상담 등", height=80)
        preferred_date = st.selectbox("희망 방문 시기 *", PREFERRED_DATE_OPTIONS)
        
        submitted = st.form_submit_button("예약 신청", use_container_width=True)
        
        if submitted:
            if not name or not contact or not symptom:
                st.error("필수 정보를 모두 입력해주세요.")
            else:
                reservation_data = {
                    'name': name,
                    'contact': contact,
                    'symptom': symptom,
                    'preferred_date': preferred_date,
                    'chat_summary': conv_manager.get_summary(),
                    'source': 'IMD_Medical_Chatbot'
                }
                
                success, message = lead_handler.save_lead(reservation_data)
                
                if success:
                    completion_msg = f"""
예약 신청이 완료되었습니다

{name}님, 감사합니다.

빠른 시일 내 {contact}로 연락드려 예약 일정을 확정하겠습니다.

증상: {symptom}  
희망 시기: {preferred_date}

진료 전 준비사항:
- 기존 진단서/검사 결과가 있다면 지참해주세요
- 복용 중인 약이 있다면 말씀해주세요
- 편안한 복장으로 내원해주세요

궁금하신 점이 있으시면 언제든 문의주세요.
"""
                    conv_manager.add_message("ai", completion_msg)
                    conv_manager.update_stage('complete')
                    
                    st.success("예약 신청이 완료되었습니다!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"오류: {message}")

# ============================================
# 완료 후
# ============================================
if conv_manager.get_context()['stage'] == 'complete':
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("새 상담 시작", use_container_width=True):
            conv_manager.reset_conversation()
            st.rerun()
    
    with col2:
        if st.button("상담 내역 보기", use_container_width=True):
            with st.expander("상담 요약", expanded=True):
                st.markdown(conv_manager.get_summary())

# ============================================
# 푸터
# ============================================
st.markdown("""
<div class="footer">
    <b>아이엠디 메디컬 시스템</b><br>
    24시간 AI 상담 | 실제 예약은 진료시간 내 가능합니다
</div>
""", unsafe_allow_html=True)
