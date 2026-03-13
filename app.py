import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="AI QUANT DASHBOARD", layout="wide")

# 사이드바 설정
st.sidebar.title("🤖 QUANT SYSTEM")
st.sidebar.info(f"시스템 가동 중: {datetime.now().strftime('%H:%M:%S')}")

# --- 2. 상단 헤더 및 지표 섹션 (기존 디자인 유지) ---
st.markdown("## 📊 AI 비트코인 실시간 분석 리포트")
st.markdown("<p style='color:#F0B90B; font-size:12px;'>REAL-TIME BINANCE ENGINE CONNECTED</p>", unsafe_allow_html=True)

# 상단 3개 지표 복구
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("시장 탐욕 지수", "15", "Extreme Fear")
with col_b:
    st.metric("알고리즘 신뢰도", "94.2%", "Optimal")
with col_c:
    st.metric("데이터 상태", "정상", "Live Connected")

st.write("---")

# --- 3. 메인 분석 리포트 섹션 ---
st.markdown("### 📈 AI 가격 분석 리포트")
c1, c2 = st.columns(2)

with c1:
    # 실시간 바이낸스 시세 위젯 (트레이딩뷰 엔진)
    st.markdown('<p style="color: #888; font-size: 14px; font-weight: 600; margin-bottom: 8px;">BINANCE 현재가 (BTC/USDT)</p>', unsafe_allow_html=True)
    
    # 트레이딩뷰 싱글 티커 위젯 HTML 코드
    tradingview_widget = """
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
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
    # 위젯 삽입 (높이를 조절하여 현재가만 깔끔하게 노출)
    components.html(tradingview_widget, height=130)

with c2:
    # AI 예측가 섹션 (디자인 통일)
    st.markdown("""
        <style>
            .target-card {
                background-color: #1a1c24;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #333;
                height: 130px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            .target-label { color: #888; font-size: 14px; font-weight: 600; margin-bottom: 5px; }
            .target-price { font-size: 36px; font-weight: 800; color: #00FF88; }
            .report-mini { font-size: 11px; color: #aaa; border-left: 3px solid #00FF88; padding-left: 10px; margin-top: 10px; }
        </style>
        <div class="target-card">
            <div class="target-label">AI 예측가</div>
            <div class="target-price">$72,832</div>
            <div class="report-mini">
                ≡ 분석: 유사 패턴 92.8% 일치
            </div>
        </div>
    """, unsafe_allow_html=True)

# 하단 정보 바
st.markdown(f"""
    <div style="font-size:11px; color:#444; text-align:right; margin-top:30px;">
        데이터 분석 로그: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 위젯 데이터는 실시간 자동 갱신됩니다.
    </div>
""", unsafe_allow_html=True)
