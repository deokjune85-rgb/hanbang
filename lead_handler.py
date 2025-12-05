# lead_handler.py
"""
IMD Medical System - 예약 데이터 관리
Google Sheets 저장
"""

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from typing import Dict, Tuple
from config import SHEET_COLUMNS

class LeadHandler:
    """예약 데이터 저장 관리"""
    
    def __init__(self):
        """Google Sheets 클라이언트 초기화"""
        self.client = None
        self.sheet = None
        self._init_sheets_client()
    
    def _init_sheets_client(self):
        """Google Sheets API 연결"""
        try:
            creds_dict = st.secrets["gcp_service_account"].to_dict()
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
            self.client = gspread.authorize(creds)
            
            # 시트 열기
            sheet_name = st.secrets.get("SHEET_NAME", "IMD_Medical_Reservations")
            try:
                self.sheet = self.client.open(sheet_name).sheet1
            except gspread.SpreadsheetNotFound:
                # 없으면 생성
                spreadsheet = self.client.create(sheet_name)
                self.sheet = spreadsheet.sheet1
                self.sheet.append_row(SHEET_COLUMNS)
                
        except Exception as e:
            # 조용히 로컬 모드로
            self.client = None
            self.sheet = None
    
    def validate_lead(self, data: Dict) -> Tuple[bool, str]:
        """예약 데이터 검증"""
        
        # 필수 필드
        required = ['name', 'contact', 'symptom']
        for field in required:
            if not data.get(field):
                return False, f"{field} 필드가 비어있습니다"
        
        # 연락처 포맷 (간단히)
        contact = data['contact'].replace('-', '').replace(' ', '')
        if not contact.isdigit() or len(contact) < 10:
            return False, "올바른 연락처 형식이 아닙니다 (예: 010-1234-5678)"
        
        return True, "검증 완료"
    
    def save_lead(self, data: Dict) -> Tuple[bool, str]:
        """
        예약 데이터 저장
        
        Args:
            data: 예약 정보
        
        Returns:
            (성공 여부, 메시지)
        """
        # 검증
        is_valid, message = self.validate_lead(data)
        if not is_valid:
            return False, message
        
        # 타임스탬프 추가
        data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Google Sheets 저장
        if self.sheet:
            try:
                row = [
                    data.get('timestamp', ''),
                    data.get('name', ''),
                    data.get('contact', ''),
                    data.get('symptom', ''),
                    data.get('preferred_date', ''),
                    data.get('chat_summary', ''),
                    data.get('source', 'IMD_Medical_Chatbot')
                ]
                self.sheet.append_row(row)
                return True, "예약이 저장되었습니다"
            except Exception as e:
                return False, f"저장 실패: {str(e)}"
        else:
            # 로컬 저장 (세션)
            if 'local_reservations' not in st.session_state:
                st.session_state.local_reservations = []
            st.session_state.local_reservations.append(data)
            return True, "예약이 로컬에 저장되었습니다"
    
    def get_all_leads(self) -> list:
        """모든 예약 조회 (관리자용)"""
        if self.sheet:
            try:
                return self.sheet.get_all_records()
            except:
                return []
        else:
            return st.session_state.get('local_reservations', [])
