# app.py
"""
IMD Medical System - AI 상담 챗봇
화이트 모드 / 친절한 한의사
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
    HOSPITAL_NAME,
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_BG,
    COLOR_TEXT,
    COLOR_AI_BUBBLE,
    COLOR_USER_BUBBLE,
    COLOR_BORDER,
    PREFERRED_DATE_OPTIONS
)

# ============================================
# 0. 페이지 설정
# ============================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=LAYOUT
)

# ============================================
# 1. CSS 스타일링 (화이트 모드)
# ============================================
def load_css():
    """화이트 모드 CSS"""
    custom_css = f"""
    <style>
    /* 전체 배경 */
    .stApp {{
        background: {COLOR_BG};
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
        color: {COLOR_TEXT};
    }}
    
    /* 타이틀 */
    h1 {{
        color: {COLOR_PRIMARY} !important;
        font-weight: 700;
        text-align: center;
        margin-bottom: 8px;
    }}
    
    h2, h3 {{
        color: {COLOR_TEXT} !important;
        font-weight: 600;
    }}
    
    /* 서브타이틀 */
    .subtitle {{
        text-align: center;
        color: #6B7280;
        font-size: 15px;
        margin-bottom: 32px;
    }}
    
    /* 채팅 컨테이너 */
    .chat-container {{
        max-width: 720px;
        margin: 24px auto;
        padding-bottom: 100px;
    }}
    
    /* AI 메시지 버블 */
    .chat-bubble-ai {{
        background: {COLOR_AI_BUBBLE};
        color: {COLOR_TEXT} !important;
        padding: 18px 20px;
        border-radius: 16px 16px 16px 4px;
        margin-bottom: 12px;
        width: fit-content;
        max-width: 85%;
        font-size: 15px;
        line-height: 1.6;
        border: 1px solid {COLOR_BORDER};
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}
    
    /* 사용자 메시지 버블 */
    .chat-bubble-user {{
        background: {COLOR_USER_BUBBLE};
        color: {COLOR_TEXT} !important;
        padding: 14px 18px;
        border-radius: 16px 16px 4px 16px;
        margin-bottom: 12px;
        margin-left: auto;
        width: fit-content;
        max-width: 75%;
        font-size: 15px;
        font-weight: 500;
        border: 1px solid {COLOR_PRIMARY};
    }}
    
    /* 추천 버튼 */
    .stButton > button {{
        width: 100%;
        background: white;
        color: {COLOR_PRIMARY} !important;
        border: 1.5px solid {COLOR_BORDER};
        padding: 12px 16px;
        font-size: 14px;
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.2s ease;
        margin-bottom: 8px;
    }}
    
    .stButton > button:hover {{
        background: {COLOR_AI_BUBBLE};
        border-color: {COLOR_PRIMARY};
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(37, 99, 235, 0.1);
    }}
    
    /* 입력창 */
    .stChatInput > div {{
        background-color: white !important;
        border: 1px solid {COLOR_BORDER} !important;
        border-radius: 12px !important;
    }}
    
    input[type="text"], textarea, .stSelectbox > div > div {{
        background-color: white !important;
        color: {COLOR_TEXT} !important;
        border: 1px solid {COLOR_BORDER} !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }}
    
    /* 폼 스타일 */
    .stForm {{
        background: {COLOR_AI_BUBBLE};
        padding: 24px;
        border-radius: 16px;
        border: 1px solid {COLOR_BORDER};
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }}
    
    /* 섹션 제목 */
    .section-title {{
        color: {COLOR_PRIMARY};
        font-size: 17px;
        font-weight: 600;
        margin: 20px 0 12px 0;
        text-align: center;
    }}
    
    /* 구분선 */
    hr {{
        border-color: {COLOR_BORDER};
        opacity: 1;
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

load_css()

# ============================================
# 2. 초기화
# ============================================
conv_manager = get_conversation_manager()
prompt_engine = get_prompt_engine()
lead_handler = LeadHandler()

# 첫 방문 시 웰컴 메시지
if len(conv_manager.get_history()) == 0:
    initial_msg = prompt_engine.generate_initial_message()
    conv_manager.add_message("ai", initial_msg)

# ============================================
# 3. 헤더
# ============================================
st.title(f"🏥 {HOSPITAL_NAME}")
st.markdown('<p class="subtitle">24시간 AI 한의사 상담</p>', unsafe_allow_html=True)

# ============================================
# 4. 채팅 히스토리 렌더링
# ============================================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for chat in conv_manager.get_history():
    role_class = "chat-bubble-ai" if chat['role'] == 'ai' else "chat-bubble-user"
    st.markdown(f'<div class="{role_class}">{chat["text"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# 5. 추천 버튼
# ============================================
if not conv_manager.is_ready_for_conversion():
    st.markdown('<p class="section-title">빠른 상담</p>', unsafe_allow_html=True)
    
    buttons = conv_manager.get_recommended_buttons()
    
    cols = st.columns(3)
    
    for idx, button_text in enumerate(buttons[:3]):
        with cols[idx]:
            if st.button(button_text, key=f"quick_{idx}"):
                conv_manager.add_message("user", button_text, metadata={"type": "button"})
                
                context = conv_manager.get_context()
                history = conv_manager.get_formatted_history(for_llm=True)
                
                with st.spinner("상담 중..."):
                    time.sleep(0.8)
                    ai_response = generate_ai_response(button_text, context, history)
                
                conv_manager.add_message("ai", ai_response)
                st.rerun()

# ============================================
# 6. 채팅 입력창
# ============================================
user_input = st.chat_input("증상이나 궁금한 점을 말씀해주세요")

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
# 7. 예약 신청 폼
# ============================================
if conv_manager.is_ready_for_conversion() and conv_manager.get_context()['stage'] != 'complete':
    st.markdown("---")
    st.markdown('<p class="section-title">📅 예약 신청</p>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#6B7280; font-size:14px;'>빠른 시일 내 연락드리겠습니다</p>", unsafe_allow_html=True)
    
    with st.form("reservation_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("성함 *", placeholder="홍길동")
        with col2:
            contact = st.text_input("연락처 *", placeholder="010-1234-5678")
        
        symptom = st.text_area("주요 증상 *", placeholder="예: 허리 통증, 다이어트 상담 등", height=80)
        preferred_date = st.selectbox("희망 방문 시기 *", PREFERRED_DATE_OPTIONS)
        
        submitted = st.form_submit_button("✅ 예약 신청", use_container_width=True)
        
        if submitted:
            if not name or not contact or not symptom:
                st.error("필수 정보를 모두 입력해주세요.")
            else:
                # 예약 정보 저장
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
### ✅ 예약 신청이 완료되었습니다

**{name}님**, 감사합니다.

빠른 시일 내 **{contact}**로 연락드려 예약 일정을 확정하겠습니다.

**증상**: {symptom}  
**희망 시기**: {preferred_date}

---

**진료 전 준비사항:**
- 기존 진단서/검사 결과가 있다면 지참해주세요
- 복용 중인 약이 있다면 말씀해주세요
- 편안한 복장으로 내원해주세요

궁금하신 점이 있으시면 언제든 문의주세요.
"""
                    conv_manager.add_message("ai", completion_msg)
                    conv_manager.update_stage('complete')
                    
                    st.success("예약 신청이 완료되었습니다!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"오류: {message}")

# ============================================
# 8. 완료 후 액션
# ============================================
if conv_manager.get_context()['stage'] == 'complete':
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 새 상담 시작", use_container_width=True):
            conv_manager.reset_conversation()
            st.rerun()
    
    with col2:
        if st.button("📋 상담 내역 보기", use_container_width=True):
            with st.expander("상담 요약", expanded=True):
                st.markdown(conv_manager.get_summary())

# ============================================
# 9. 푸터
# ============================================
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align:center; color:#9CA3AF; font-size:12px; padding: 20px 0;'>
        <b style='color:{COLOR_PRIMARY};'>{HOSPITAL_NAME}</b><br>
        24시간 AI 상담 | 실제 예약은 진료시간 내 가능합니다<br>
        © 2024 IMD Medical System. Powered by Claude AI.
    </div>
    """,
    unsafe_allow_html=True
)
