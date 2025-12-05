# prompt_engine.py
"""
IMD Medical System - AI 응답 생성
Gemini API 연동 (친절한 한의사 톤)
"""

import streamlit as st
import google.generativeai as genai
from typing import Dict
import time
from config import (
    SYSTEM_PROMPT,
    GEMINI_MODEL,
    GEMINI_TEMPERATURE,
    GEMINI_MAX_TOKENS,
    TREATMENT_INFO
)

class PromptEngine:
    """AI 응답 생성 엔진"""
    
    def __init__(self):
        """Gemini API 초기화"""
        self.model = None
        self.retry_count = 0
        self._init_gemini()
    
    def _init_gemini(self):
        """Gemini API 설정"""
        try:
            if "GEMINI_API_KEY" not in st.secrets:
                st.error("❌ GEMINI_API_KEY가 Secrets에 없습니다.")
                self.model = None
                return
            
            api_key = st.secrets["GEMINI_API_KEY"]
            
            if not api_key or api_key == "":
                st.error("❌ API 키가 비어있습니다.")
                self.model = None
                return
            
            # Gemini 설정
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                model_name=GEMINI_MODEL,
                generation_config={
                    "temperature": GEMINI_TEMPERATURE,
                    "max_output_tokens": GEMINI_MAX_TOKENS,
                }
            )
            
            # 조용히 초기화 (메시지 없음)
            
        except Exception as e:
            st.error(f"❌ Gemini 초기화 실패: {str(e)}")
            self.model = None
    
    def generate_response(
        self,
        user_input: str,
        context: Dict,
        conversation_history: str
    ) -> str:
        """AI 응답 생성"""
        
        if not self.model:
            st.warning("⚠️ Gemini 모델 초기화 실패 - Fallback 사용")
            return self._fallback_response(user_input, context)
        
        # 재시도 로직
        max_retries = 2
        for attempt in range(max_retries):
            try:
                full_prompt = self._build_prompt(user_input, context, conversation_history)
                
                response = self.model.generate_content(full_prompt)
                
                if not response or not response.text:
                    raise ValueError("빈 응답 수신")
                
                ai_response = self._post_process_response(response.text.strip(), context)
                
                self.retry_count = 0
                return ai_response
                
            except Exception as e:
                self.retry_count += 1
                error_msg = str(e)
                
                # 에러 상세 로그
                st.warning(f"⚠️ AI 응답 실패 (시도 {attempt+1}/{max_retries}): {error_msg}")
                
                if attempt == max_retries - 1:
                    st.error(f"❌ Gemini API 최종 실패. Fallback 사용합니다.")
                    return self._fallback_response(user_input, context)
                else:
                    time.sleep(1)
        
        return self._fallback_response(user_input, context)
    
    def _build_prompt(
        self,
        user_input: str,
        context: Dict,
        conversation_history: str
    ) -> str:
        """프롬프트 조립 (간결화)"""
        
        system_prompt = SYSTEM_PROMPT.format(
            symptom=context.get('symptom') or '파악 중',
            trust_level=context.get('trust_level', 0)
        )
        
        # 최근 3개 대화만
        history_lines = conversation_history.split('\n')
        recent_history = '\n'.join(history_lines[-6:])  # 3턴 = 6줄
        
        full_prompt = f"""{system_prompt}

## 최근 대화
{recent_history}

## 환자 입력
{user_input}

**3-4문장으로 친절하게 응답하세요.**
"""
        return full_prompt
    
    def _post_process_response(self, response: str, context: Dict) -> str:
        """응답 후처리"""
        import re
        
        # 줄바꿈 정리
        response = response.replace('\n\n\n', '\n\n')
        
        # 마크다운 굵기
        response = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', response)
        
        # 길이 제한
        if len(response) > 600:
            response = response[:580] + "\n\n더 궁금하신 점 있으신가요?"
        
        # 예약 유도 (적절한 타이밍)
        if context.get('trust_level', 0) >= 40 and '예약' not in response.lower():
            response += "\n\n편하신 시간에 방문하시면 자세히 상담해드리겠습니다."
        
        return response
    
    def _fallback_response(self, user_input: str, context: Dict) -> str:
        """Fallback 응답"""
        user_lower = user_input.lower()
        
        # 다이어트 문의
        if any(word in user_lower for word in ['다이어트', '살', '비만', '체중', '뱃살', '빼고']):
            return """다이어트로 고민이시군요. 많은 분들이 찾으시는 상담입니다.

**다이어트 한약 프로그램:**
- 체질에 맞춰 신진대사 개선
- 식욕 조절 & 체지방 감소
- 1개월 기준 3-5kg 감량 목표

**비용**: 1개월 30-50만원 (한약 + 관리)
**기간**: 보통 3-6개월 권장

현재 몸무게와 목표 체중이 어떻게 되시나요?"""
        
        # 비용 문의
        elif any(word in user_lower for word in ['가격', '비용', '얼마', '요금']):
            return """비용 안내해드립니다.

**초진**: 5-8만원 (진찰 + 침/부항)
**추나요법**: 회당 3-5만원
**다이어트 한약**: 1개월 30-50만원

정확한 비용은 환자분 상태를 진찰 후 말씀드릴 수 있습니다.
편하신 시간에 방문해주세요."""
        
        # 시간/위치 문의
        elif any(word in user_lower for word in ['시간', '언제', '위치', '어디']):
            return """**진료 시간 안내**

평일: 09:00 - 18:00
토요일: 09:00 - 14:00
일요일/공휴일: 휴진

**위치**: 서울 강남구

예약하시겠습니까?"""
        
        # 증상 문의
        elif any(word in user_lower for word in ['아프', '통증', '아파']):
            return """많이 불편하시겠어요.

어느 부위가 아프신가요?
- 허리/목
- 어깨/팔
- 무릎/다리

언제부터 아프셨는지도 말씀해주시면 도움이 됩니다."""
        
        # 기본
        else:
            return """안녕하세요, 무엇을 도와드릴까요?

편하게 증상이나 궁금하신 점을 말씀해주세요.
- 통증 치료
- 다이어트 상담
- 교통사고 후유증
- 만성 피로

자세히 상담해드리겠습니다."""
    
    def generate_initial_message(self) -> str:
        """첫 메시지"""
        return """안녕하세요, <b>아이엠디 메디컬 시스템</b> AI 한의사입니다.

편안하게 상담해드리겠습니다.

어떤 증상으로 불편하신가요?"""


def get_prompt_engine() -> PromptEngine:
    """싱글톤 인스턴스"""
    if 'prompt_engine' not in st.session_state:
        st.session_state.prompt_engine = PromptEngine()
    return st.session_state.prompt_engine


def generate_ai_response(user_input: str, context: Dict, history: str) -> str:
    """빠른 호출"""
    engine = get_prompt_engine()
    return engine.generate_response(user_input, context, history)
