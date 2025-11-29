# [Case 3: 내성 답변 받음 -> 최종 결과]
    elif st.session_state.step == 5:
        st.session_state.user_data['history'] = prompt
        
        # 1. 로딩 애니메이션 (권위 부여)
        with st.chat_message("assistant", avatar="🌿"):
            with st.status("🧬 25년 임상 데이터 대조 중...", expanded=True) as status:
                st.write("체질별 대사량 시뮬레이션...")
                time.sleep(1)
                st.write("약물 반응성 예측 중...")
                time.sleep(1)
                status.update(label="✅ 최적 처방 매칭 완료!", state="complete", expanded=False)
        
        # 2. 결과 도출 로직 (Rich Content)
        cause = st.session_state.user_data.get('cause', '대사')
        
        if cause == "식욕":
            diag_title = "위열(Stomach Heat) 과다형"
            sub_desc = "가짜 배고픔 / 포만 중추 마비"
            reasoning = "위장에 과도한 열이 쌓여, 뇌가 배부름을 인지하지 못하는 상태입니다."
            drug_name = "식탐사약"
            drug_desc = "위장의 열을 내리고 식욕 억제 호르몬 활성화"
            ba_img = "https://placehold.co/600x300/111/00E676?text=Before+After+(Belly)" 

        elif cause == "부종":
            diag_title = "수독(Water Poison) 정체형"
            sub_desc = "림프 순환 장애 / 만성 부종"
            reasoning = "체내 수분 대사가 고장 나, 노폐물이 지방과 엉겨 붙은 상태입니다."
            drug_name = "독소킬 + 지방사약"
            drug_desc = "수분 길을 열어 부종 배출 및 라인 정리"
            ba_img = "https://placehold.co/600x300/111/00E676?text=Before+After+(Legs)"

        elif cause == "대사":
            diag_title = "대사 기능 저하형 (Cold Body)"
            sub_desc = "기초대사량 부족 / 수족냉증"
            reasoning = "엔진이 꺼진 차와 같습니다. 남들과 똑같이 먹어도 고객님만 살이 찝니다."
            drug_name = "지방사약 (대사촉진형)"
            drug_desc = "심부 체온을 높여 숨만 쉬어도 칼로리 소모 유도"
            ba_img = "https://placehold.co/600x300/111/00E676?text=Before+After+(Body)"

        else: # 스트레스
            diag_title = "간기 울결형 (Stress Induced)"
            sub_desc = "코르티솔 과다 / 감정적 폭식"
            reasoning = "스트레스 호르몬(코르티솔)이 뱃살을 붙잡고 있습니다. 굶으면 폭식합니다."
            drug_name = "지방사약 + 소요산"
            drug_desc = "자율신경을 안정시켜 폭식 충동을 원천 차단"
            ba_img = "https://placehold.co/600x300/111/00E676?text=Before+After+(Stress)"

        # 3. HTML 결과 카드 생성 (CSS 인라인 적용으로 깨짐 방지)
        result_html = f"""
        <div style="background-color: #0A1F0A; border: 1px solid #00E676; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
            <div style="color: #00E676; font-size: 0.9rem; font-weight: bold; margin-bottom: 5px;">DIAGNOSIS REPORT</div>
            <h3 style="color: #fff; margin: 0 0 5px 0;">{diag_title}</h3>
            <div style="color: #FF5252; font-size: 0.9rem; margin-bottom: 15px;">⚠️ {sub_desc}</div>
            <hr style="border-color: #333; margin-bottom: 15px;">
            <p style="color: #ddd; font-size: 0.95rem; line-height: 1.5;">
                <b>"의지가 약한 게 아닙니다."</b><br>
                {reasoning}<br>
                이 상태에서는 운동을 해도 효율이 1/10밖에 나지 않습니다.
            </p>
            <div style="background-color: #1E1E1E; border-left: 4px solid #00E676; padding: 15px; margin-top: 15px;">
                <div style="color: #888; font-size: 0.8rem;">FINAL PRESCRIPTION</div>
                <div style="color: #00E676; font-size: 1.2rem; font-weight: bold;">💊 {drug_name}</div>
                <div style="color: #fff; font-size: 0.9rem; margin-top: 5px;">: {drug_desc}</div>
            </div>
        </div>
        """
        
        # 4. 봇 메시지 전송 (HTML 렌더링)
        bot_say(result_html)
        with st.chat_message("assistant", avatar="🌿"):
            st.markdown(result_html, unsafe_allow_html=True) # HTML 활성화 필수
            
            # 비포 애프터 & 가격 (기존 로직 유지)
            st.markdown("---")
            st.write("**👁 [증거] 동일 체질 환자의 3개월 변화**")
            st.image(ba_img, use_column_width=True)
            
            price_html = """
            <div style="background: linear-gradient(135deg, #111 0%, #000 100%); border: 1px solid #333; border-radius: 10px; padding: 15px; margin-top: 15px;">
                <h4 style='color:#00E676; margin:0; font-size:1rem;'>💰 합리적 비용 제안</h4>
                <table style='width:100%; color:white; text-align:center; margin-top:10px;'>
                    <tr style='border-bottom:1px solid #333;'>
                        <td style='padding:8px; color:#aaa;'>1개월</td>
                        <td style='color:#FF5252; font-weight:bold;'>150,000원</td>
                    </tr>
                    <tr>
                        <td style='padding:8px; color:#fff;'>6개월 (Best)</td>
                        <td style='color:#00E676; font-weight:bold;'>월 10만원대</td>
                    </tr>
                </table>
            </div>
            """
            st.markdown(price_html, unsafe_allow_html=True)
            bot_say(price_html)

        st.session_state.step = 6 # 완료 상태
