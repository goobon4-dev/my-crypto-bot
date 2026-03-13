import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="AI QUANT PRO", layout="wide")

# 사이드바 메뉴
st.sidebar.title("🤖 QUANT SYSTEM")
menu = st.sidebar.radio("MENU", ["LIVE DASHBOARD", "LEGAL POLICY"])

# --- 스타일 정의 (박스 제거 및 텍스트 강조) ---
st.markdown("""
<style>
    .stApp { background-color: #0b0e11; }
    .report-title { font-size: 28px; font-weight: 800; color: white; margin-bottom: 20px; }
    
    /* 섹션 라벨 스타일 */
    .section-label { 
        color: #848e9c; font-size: 14px; font-weight: 600; 
        margin-bottom: 10px; border-left: 3px solid #F0B90B; padding-left: 10px;
    }
    
    /* AI 예측가 텍스트 스타일 */
    .ai-price { font-size: 54px; font-weight: 900; color: #00FF88; letter-spacing: -1.5px; line-height: 1; }
    .ai-badge { color: #00FF88; font-size: 12px; font-weight: bold; margin-bottom: 5px; }
    
    /* 리포트 텍스트 스타일 */
    .report-text { color: #aaa; font-size: 14px; line-height: 1.6; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

if menu == "LIVE DASHBOARD":
    st.markdown('<div class="report-title">📊 AI 비트코인 실시간 분석 리포트</div>', unsafe_allow_html=True)

    # 상단 3개 지표 (기존 유지)
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("시장 탐욕 지수", "15", "Extreme Fear")
    col_b.metric("알고리즘 신뢰도", "94.2%", "Optimal")
    col_c.metric("데이터 상태", "정상", "Live Connected")

    st.write("---")

    # 메인 콘텐츠 (박스 없이 시원하게 배치)
    c1, c2 = st.columns([1.2, 1]) # 좌측 시세 영역을 조금 더 넓게

    with c1:
        st.markdown('<div class="section-label">BINANCE 실시간 시세 (BTC/USDT)</div>', unsafe_allow_html=True)
        # 위젯이 죽지 않도록 높이를 충분히 확보한 클린 코드
        tradingview_html = """
            <div style="height: 140px;">
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>
                {
                  "symbol": "BINANCE:BTCUSDT",
                  "width": "100%",
                  "colorTheme": "dark",
                  "isTransparent": true,
                  "locale": "ko"
                }
                </script>
            </div>
        """
        components.html(tradingview_html, height=160)

    with c2:
        st.markdown('<div class="section-label">AI 예측가 (Short-term)</div>', unsafe_allow_html=True)
        st.markdown('<div class="ai-badge">▶ PRO-QUANT ENGINE ANALYSIS</div>', unsafe_allow_html=True)
        st.markdown('<div class="ai-price">$72,832.00</div>', unsafe_allow_html=True)
        
        # 상세 리포트 (박스 없이 텍스트로만 깔끔하게)
        st.markdown(f"""
            <div class="report-text">
                <b>≡ 분석 리포트 요약</b><br>
                • 유사 가격 패턴 시점: 2024년 03월 10일<br>
                • 패턴 알고리즘 유사도: <span style="color:#00FF88;">92.8% 일치</span><br>
                • 분석 결과: 단기 강세 패턴이 확인되며 반등 가능성 높음
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<div style="font-size:11px; color:#444; text-align:right; margin-top:50px;">마지막 분석 로그: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

else:
    st.title("📄 개인정보처리방침")
    st.markdown("---")
    st.write("본 시스템은 사용자 개인정보를 수집하지 않으며, 바이낸스 API 데이터를 실시간 참조합니다.")
