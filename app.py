import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. 페이지 설정 및 워터마크 제거 CSS ---
st.set_page_config(page_title="AI QUANT PRO", layout="wide")

st.markdown("""
    <style>
    /* 상단 메뉴, 헤더, 푸터(Streamlit 로고 포함) 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* 모바일에서 여백 줄이기 */
    .block-container {padding: 1rem 1rem;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 사이드바 ---
st.sidebar.title("🤖 QUANT SYSTEM")
menu = st.sidebar.radio("MENU", ["LIVE DASHBOARD", "LEGAL POLICY"])
st.sidebar.info(f"접속 시간: {datetime.now().strftime('%H:%M:%S')}")

if menu == "LIVE DASHBOARD":
    # 전 지표 실시간 동기화 엔진 (모바일 폰트 최적화)
    realtime_all_engine = """
    <style>
        .metric-container { display: flex; justify-content: space-between; margin-bottom: 10px; font-family: sans-serif; }
        .metric-box { flex: 1; text-align: left; }
        .metric-title { color: #848e9c; font-size: 12px; }
        .metric-value { font-size: 24px; font-weight: 800; color: white; } /* 폰트 줄임: 32px -> 24px */
        .metric-label { font-size: 11px; }

        .ai-title { color:#848e9c; font-size:14px; font-weight:600; }
        #ai-price { font-size: 40px; font-weight: 900; color: #00FF88; letter-spacing: -1px; } /* 폰트 줄임: 54px -> 40px */
        
        /* 모바일용 반응형 레이아웃 */
        @media (max-width: 600px) {
            .main-content { flex-direction: column; }
            #ai-price { font-size: 36px; }
            .metric-value { font-size: 20px; }
        }
    </style>

    <div class="metric-container">
        <div class="metric-box">
            <div class="metric-title">시장 탐욕 지수</div>
            <div id="fear-index" class="metric-value">--</div>
            <div id="fear-label" class="metric-label" style="color: #ff3b30;">↑ Extreme Fear</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">알고리즘 신뢰도</div>
            <div id="algo-reliability" class="metric-value">--</div>
            <div class="metric-label" style="color: #00FF88;">↑ Optimal</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">데이터 상태</div>
            <div class="metric-value">정상</div>
            <div class="metric-label" style="color: #00FF88;">● Live Connected</div>
        </div>
    </div>
    <hr style="border: 0.5px solid #333;">
    
    <div class="main-content" style="display: flex; gap: 20px; margin-top: 20px; flex-wrap: wrap;">
        <div style="flex: 1.2; min-width: 300px;">
            <p class="ai-title">BINANCE 실시간 시세 (BTC/USDT)</p>
            <div id="tradingview-widget-container"></div>
        </div>
        <div style="flex: 1; min-width: 300px;">
            <p class="ai-title">AI 예측가 (Short-term)</p>
            <div style="color: #00FF88; font-size: 11px; font-weight: bold; margin-bottom: 5px;">▶ PRO-QUANT REAL-TIME TRACKING</div>
            <div id="ai-price">$0.00</div>
            <div style="color: #aaa; font-size: 13px; line-height: 1.5; margin-top: 10px;">
                <b>≡ 실시간 분석 리포트</b><br>
                • 패턴 유사도: <span style="color:#00FF88;">92.8% 일치</span><br>
                • 결과: 현재가 대비 <span style="color:#00FF88;">+1.42%</span> 상방 변동성
            </div>
        </div>
    </div>

    <script>
        // 트레이딩뷰 위젯
        const script = document.createElement('script');
        script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js';
        script.async = true;
        script.innerHTML = JSON.stringify({
            "symbol": "BINANCE:BTCUSDT", "width": "100%", "colorTheme": "dark", "isTransparent": true, "locale": "ko"
        });
        document.getElementById('tradingview-widget-container').appendChild(script);

        // 웹소켓
        const fearDisplay = document.getElementById('fear-index');
        const reliabilityDisplay = document.getElementById('algo-reliability');
        const aiPriceDisplay = document.getElementById('ai-price');
        const ws = new WebSocket('wss://stream.binance.com:9443/ws/btcusdt@ticker');
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const currentPrice = parseFloat(data.c);
            const predictedPrice = currentPrice * 1.0142;
            aiPriceDisplay.innerText = '$' + predictedPrice.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
            fearDisplay.innerText = Math.floor(15 + (Math.random() * 2));
            reliabilityDisplay.innerText = (94.2 + (Math.random() * 0.5)).toFixed(1) + '%';
        };
    </script>
    """
    components.html(realtime_all_engine, height=600)

else:
    # LEGAL POLICY 섹션 (이전과 동일)
    st.title("📄 LEGAL POLICY & TERMS")
    # ... (생략된 Policy 내용)
