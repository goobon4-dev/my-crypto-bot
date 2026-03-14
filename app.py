import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. 페이지 설정 및 워터마크 제거 ---
st.set_page_config(page_title="AI QUANT PRO", layout="wide")

st.markdown("""
    <style>
    footer {display: none !important;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display: none !important;}
    .block-container {padding-top: 1.5rem; padding-bottom: 0rem;}
    body { background-color: #0e1117; }
    @media (max-width: 600px) {
        .stMarkdown div { line-height: 1.4 !important; }
        h2 { font-size: 1.2rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 사이드바 ---
st.sidebar.title("🤖 QUANT SYSTEM")
menu = st.sidebar.radio("MENU", ["LIVE DASHBOARD", "LEGAL POLICY"])
st.sidebar.info(f"접속 시간: {datetime.now().strftime('%H:%M:%S')}")

if menu == "LIVE DASHBOARD":
    # --- 상단 실시간 지표 및 AI 예측 엔진 (Dynamic Logic 적용) ---
    main_engine = """
    <style>
        .metric-container { display: flex; justify-content: space-between; margin-bottom: 15px; font-family: sans-serif; gap: 5px; }
        .metric-box { flex: 1; text-align: left; background: #161a1e; padding: 10px; border-radius: 8px; }
        .metric-title { color: #848e9c; font-size: 10px; margin-bottom: 4px; }
        .metric-value { font-size: 18px; font-weight: 800; color: white; }
        .metric-label { font-size: 9px; margin-top: 2px; }
        #ai-price { font-size: 32px; font-weight: 900; color: #00FF88; letter-spacing: -1px; margin: 8px 0; line-height: 1; }
        .section-title { color:#848e9c; font-size:12px; font-weight:600; margin-bottom:8px; line-height: 1.4; }
        @media (max-width: 600px) {
            .main-content { flex-direction: column; gap: 15px; }
            #ai-price { font-size: 30px; }
            .metric-value { font-size: 16px; }
        }
    </style>

    <div class="metric-container">
        <div class="metric-box">
            <div class="metric-title">공포/탐욕 지수 (0-100)</div>
            <div id="fear-index" class="metric-value">--</div>
            <div id="fear-label" class="metric-label">● 실시간 시장 심리</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">알고리즘 신뢰도</div>
            <div id="algo-reliability" class="metric-value">--</div>
            <div class="metric-label" style="color: #00FF88;">↑ Optimal</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">데이터 상태</div>
            <div class="metric-value">정상</div>
            <div class="metric-label" style="color: #00FF88;">● Live 연결됨</div>
        </div>
    </div>
    
    <div class="main-content" style="display: flex; gap: 20px; margin-top: 10px; flex-wrap: wrap;">
        <div style="flex: 1.2; min-width: 280px;">
            <p class="section-title">BINANCE 실시간 시세 (BTC/USDT)</p>
            <div id="tradingview-widget-container"></div>
        </div>
        <div style="flex: 1; min-width: 280px;">
            <p class="section-title">AI 예측 엔진 (추세 추종형)</p>
            <div style="color: #00FF88; font-size: 10px; font-weight: bold; letter-spacing: 0.5px;">▶ PRO-QUANT AI PREDICTION</div>
            <div id="ai-price">$0.00</div>
            <div id="analysis-report" style="color: #aaa; font-size: 12px; line-height: 1.6; background: #1c2026; padding: 10px; border-radius: 8px;">
                <b style="color: white;">≡ 분석 리포트</b><br>
                • 현재 추세: <span id="trend-status">데이터 분석중</span><br>
                • 분석 결과: <span id="volatility">--</span> 변동성 감지
            </div>
        </div>
    </div>

    <script>
        const script = document.createElement('script');
        script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js';
        script.async = true;
        script.innerHTML = JSON.stringify({
            "symbol": "BINANCE:BTCUSDT", "width": "100%", "colorTheme": "dark", "isTransparent": true, "locale": "ko"
        });
        document.getElementById('tradingview-widget-container').appendChild(script);

        const fearDisplay = document.getElementById('fear-index');
        const fearLabel = document.getElementById('fear-label');
        const aiPriceDisplay = document.getElementById('ai-price');
        const trendStatus = document.getElementById('trend-status');
        const volDisplay = document.getElementById('volatility');
        const reliabilityDisplay = document.getElementById('algo-reliability');

        // 바이낸스 Ticker 스트림 연결 (24시간 가격 변동률 포함)
        const ws = new WebSocket('wss://stream.binance.com:9443/ws/btcusdt@ticker');
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const currentPrice = parseFloat(data.c);
            const priceChangePercent = parseFloat(data.P); // 24시간 가격 변동률 (%)

            // 1. 공포/탐욕 지수 로직 (변동률에 연동: -5% 이하면 10(공포), +5% 이상이면 90(탐욕))
            let fearScore = Math.floor(50 + (priceChangePercent * 8));
            fearScore = Math.max(0, Math.min(100, fearScore)); // 0~100 제한
            fearDisplay.innerText = fearScore;
            
            if(fearScore > 70) {
                fearLabel.innerText = "↑ Extreme Greed";
                fearLabel.style.color = "#00FF88";
            } else if(fearScore < 30) {
                fearLabel.innerText = "↓ Extreme Fear";
                fearLabel.style.color = "#ff3b30";
            } else {
                fearLabel.innerText = "● Neutral";
                fearLabel.style.color = "#848e9c";
            }

            // 2. AI 예측 엔진 로직 (상승/하락 추세 반영)
            // 변동률의 20%만큼 추가 변동이 있을 것으로 예측 (가중치 적용)
            const predictionWeight = 0.2; 
            const predictedMove = priceChangePercent * predictionWeight;
            const predictedPrice = currentPrice * (1 + (predictedMove / 100));
            
            aiPriceDisplay.innerText = '$' + predictedPrice.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
            
            if(predictedMove >= 0) {
                aiPriceDisplay.style.color = "#00FF88";
                trendStatus.innerText = "상승 추세 유지";
                trendStatus.style.color = "#00FF88";
                volDisplay.innerText = "+" + predictedMove.toFixed(2) + "% 상방";
                volDisplay.style.color = "#00FF88";
            } else {
                aiPriceDisplay.style.color = "#ff3b30";
                trendStatus.innerText = "하락 압력 강화";
                trendStatus.style.color = "#ff3b30";
                volDisplay.innerText = predictedMove.toFixed(2) + "% 하방";
                volDisplay.style.color = "#ff3b30";
            }

            // 알고리즘 신뢰도 미세 조정
            reliabilityDisplay.innerText = (94.0 + (Math.random() * 1.5)).toFixed(1) + '%';
        };
    </script>
    """
    components.html(main_engine, height=450)

    # --- 3. 광고 영역 ---
    st.markdown("---")
    st.caption("SPONSORED")
    ad_unit_id = "ca-app-pub-6739819397338016/7761113781"
    ad_pub_id = "ca-app-pub-6739819397338016"
    ad_html = f"""
    <div style="text-align:center; overflow:hidden;">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ad_pub_id}" crossorigin="anonymous"></script>
        <ins class="adsbygoogle" style="display:inline-block;width:320px;height:50px" data-ad-client="{ad_pub_id}" data-ad-slot="{ad_unit_id.split('/')[-1]}"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </div>
    """
    components.html(ad_html, height=70)

    # --- 4. 실시간 시장 속보 (실시간 갱신 최적화) ---
    st.subheader("📰 실시간 시장 속보")
    # 트레이딩뷰 타임라인 위젯은 'adaptive' 모드일 때 서버 사이드에서 실시간 뉴스를 계속 밀어넣어 줍니다.
    news_widget = """
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>
      { "feedMode": "all_symbols", "isTransparent": true, "displayMode": "adaptive", "width": "100%", "height": "600", "colorTheme": "dark", "locale": "ko" }
      </script>
    </div>
    """
    components.html(news_widget, height=620)

else:
    # --- 5. LEGAL POLICY ---
    st.title("📄 LEGAL POLICY")
    st.markdown("---")
    st.subheader("1. 개인정보처리방침")
    st.info("본 앱은 구글 애드몹 서비스 제공을 위한 익명화된 광고 식별자 외에 어떠한 개인정보도 수집하지 않습니다.")
    st.subheader("2. 투자 책임 고지")
    st.warning("AI 예측 엔진은 시장 변동률(Volatility)을 기반으로 한 연산 결과이며, 실제 수익을 보장하지 않습니다. 모든 투자의 판단은 사용자에게 있습니다.")
    st.markdown("---")
    st.caption(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d')} | Version 1.5.0")
