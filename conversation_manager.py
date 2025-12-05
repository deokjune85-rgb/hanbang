# conversation_manager.py
"""
IMD Medical System - 대화 상태 관리
환자 증상, 대화 히스토리 관리
"""

import streamlit as st
from typing import Dict, List, Optional
from datetime import datetime
import re

class ConversationManager:
    """대화 상태 및 컨텍스트 관리"""
    
    def __init__(self):
        """세션 상태 초기화"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        if 'user_context' not in st.session_state:
            st.session_state.user_context = {
                'symptom': None,          # 주요 증상
                'pain_area': None,        # 통증 부위
                'duration': None,         # 기간
                'treatment_interest': [], # 관심 치료
                'stage': 'initial',       # 대화 단계
                'trust_level': 0,         # 신뢰도
                'keywords': []            # 키워드
            }
        
        if 'interaction_count' not in st.session_state:
            st.session_state.interaction_count = 0
    
    def add_message(self, role: str, text: str, metadata: Optional[Dict] = None):
        """
        메시지 추가
        
        Args:
            role: 'ai' or 'user'
            text: 메시지 내용
            metadata: 추가 정보
        """
        message = {
            'role': role,
            'text': text,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        st.session_state.chat_history.append(message)
        
        if role == 'user':
            st.session_state.interaction_count += 1
            self._update_trust_level()
            self._extract_context(text)
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """대화 히스토리 조회"""
        history = st.session_state.chat_history
        if limit:
            return history[-limit:]
        return history
    
    def remove_last_thinking(self):
        """마지막 thinking 메시지 제거"""
        if st.session_state.chat_history:
            last_msg = st.session_state.chat_history[-1]
            if last_msg.get('role') == 'system' and last_msg.get('metadata', {}).get('type') == 'thinking':
                st.session_state.chat_history.pop()
    
    def get_formatted_history(self, for_llm: bool = False, last_n: int = 10) -> str:
        """
        포맷된 히스토리 문자열 반환
        
        Args:
            for_llm: LLM용 포맷 (True) vs 사람용 (False)
            last_n: 최근 N개만
        """
        recent = self.get_history(limit=last_n)
        
        if for_llm:
            lines = []
            for msg in recent:
                role = "환자" if msg['role'] == 'user' else "한의사"
                lines.append(f"{role}: {msg['text']}")
            return "\n".join(lines)
        else:
            return "\n\n".join([f"**{msg['role']}**: {msg['text']}" for msg in recent])
    
    def get_context(self) -> Dict:
        """현재 컨텍스트 반환"""
        return st.session_state.user_context
    
    def update_stage(self, stage: str):
        """대화 단계 업데이트"""
        st.session_state.user_context['stage'] = stage
    
    def get_summary(self) -> str:
        """대화 요약"""
        context = st.session_state.user_context
        history = self.get_history()
        
        summary = f"""
## 상담 요약

**주요 증상**: {context.get('symptom') or '파악 중'}
**통증 부위**: {context.get('pain_area') or '-'}
**기간**: {context.get('duration') or '-'}
**관심 치료**: {', '.join(context.get('treatment_interest', [])) or '-'}

**총 대화**: {len(history)}회
**상담 시작**: {history[0]['timestamp'] if history else '-'}
"""
        return summary
    
    def _extract_context(self, text: str):
        """사용자 입력에서 컨텍스트 추출"""
        context = st.session_state.user_context
        text_lower = text.lower()
        
        # 1. 통증 부위 감지
        pain_areas = {
            '허리': ['허리', '요통', '디스크'],
            '목': ['목', '경추', '목디스크'],
            '어깨': ['어깨', '견갑골', '오십견'],
            '무릎': ['무릎', '슬관절'],
            '골반': ['골반', '골반통증']
        }
        
        for area, keywords in pain_areas.items():
            if any(kw in text_lower for kw in keywords):
                context['pain_area'] = area
                context['symptom'] = f"{area} 통증"
        
        # 2. 다이어트 감지
        if any(word in text_lower for word in ['다이어트', '비만', '살', '체중', '뱃살']):
            context['symptom'] = '다이어트'
            context['treatment_interest'].append('다이어트 한약')
        
        # 3. 교통사고 감지
        if any(word in text_lower for word in ['교통사고', '사고', '후유증', '뒷목']):
            context['symptom'] = '교통사고 후유증'
        
        # 4. 기간 감지
        duration_patterns = [
            (r'(\d+)일', '일'),
            (r'(\d+)주', '주'),
            (r'(\d+)개월', '개월'),
            (r'(\d+)년', '년')
        ]
        
        for pattern, unit in duration_patterns:
            match = re.search(pattern, text)
            if match:
                context['duration'] = f"{match.group(1)}{unit}"
        
        # 5. 치료 관심도
        if '추나' in text_lower or '교정' in text_lower:
            if '추나요법' not in context['treatment_interest']:
                context['treatment_interest'].append('추나요법')
        
        if '침' in text_lower or '뜸' in text_lower:
            if '침구치료' not in context['treatment_interest']:
                context['treatment_interest'].append('침구치료')
        
        if '한약' in text_lower:
            if '한약' not in context['treatment_interest']:
                context['treatment_interest'].append('한약')
    
    def _update_trust_level(self):
        """신뢰도 업데이트 (대화 횟수 기반)"""
        user_message_count = sum(1 for msg in st.session_state.chat_history if msg['role'] == 'user')
        trust = min(user_message_count * 10, 100)
        st.session_state.user_context['trust_level'] = trust
    
    def is_ready_for_conversion(self) -> bool:
        """예약 폼 표시 여부"""
        self._update_trust_level()
        
        user_message_count = sum(1 for msg in st.session_state.chat_history if msg['role'] == 'user')
        
        # 4번 답변하면 폼 표시
        if user_message_count >= 4:
            return True
        
        return False
    
    def get_recommended_buttons(self) -> List[str]:
        """추천 버튼 생성"""
        from config import QUICK_REPLIES
        
        context = st.session_state.user_context
        stage = context['stage']
        
        # 증상 파악됨
        if context.get('symptom'):
            return QUICK_REPLIES.get('symptom', QUICK_REPLIES['initial'])
        
        # 기본
        return QUICK_REPLIES.get(stage, QUICK_REPLIES['initial'])
    
    def reset_conversation(self):
        """대화 초기화"""
        st.session_state.chat_history = []
        st.session_state.user_context = {
            'symptom': None,
            'pain_area': None,
            'duration': None,
            'treatment_interest': [],
            'stage': 'initial',
            'trust_level': 0,
            'keywords': []
        }
        st.session_state.interaction_count = 0


def get_conversation_manager() -> ConversationManager:
    """싱글톤 인스턴스"""
    if 'conversation_manager' not in st.session_state:
        st.session_state.conversation_manager = ConversationManager()
    return st.session_state.conversation_manager
