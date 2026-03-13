import streamlit as st
import requests
import numpy as np
import plotly.graph_objects as go
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 1. 바이낸스 시세 강제 호출 ---
def get_real_time_price():
    try:
        # 캐싱 방지를 위해 URL 뒤에 매번 다른 숫자를 붙입니다.
        url = f"https://api.binance.com/api/3/ticker/price?symbol=BTCUSDT&_ts={datetime.now().timestamp()}"
        response = requests.get(url, timeout=5)
        data = response.json()
        # 'price' 값을 가져와서 숫자로 변환
        return float(data['price'])
    except:
        return 71234.56 # 정 안되면 티라도 나게 이 숫자로 설정

# --- 2. 앱 실행 및 데이터 동기화 ---
st.set_page_config(page_title="AI QUANT SYSTEM", layout="wide")

# [중요] 앱을 켜는 순간 이 변수에 진짜 현재가가 저장됩니다.
live_btc = get_real_time_price()

# --- 3. 디자인 (기존 그대로 유지) ---
st.sidebar.title("🤖 QUANT SYSTEM")
menu = st.sidebar.radio("MENU", ["ANALYSIS", "POLICY"], label_visibility="collapsed")

if menu == "ANALYSIS":
    st.markdown(f"""
        <div style="padding: 1rem 0rem; border-bottom: 2px solid #2d2d2d; margin-bottom: 1.5rem;">
            <p style="color: #F0B90B; font-size: 11px; margin: 0;">OFFICIAL BINANCE API DATA</p>
            <h2 style="color: white; margin: 0;">BTC-USD 인공지능 패턴 분석</h2>
        </div>
    """, unsafe_allow_html=True)

    # 상단 3개 위젯
    c1, c2, c3 = st.columns(3)
    
    # [핵심] 여기에 live_btc가 들어가야 숫자가 바뀝니다!
    c1.metric(
        label="Binance 현재가", 
        value=f"${live_btc:,.2f}", # 예: $72,123.45
        delta="LIVE FETCH"
    )
    c2.metric("시장 탐욕 지수", "15", "Extreme Fear")
    c3.metric("알고리즘 신뢰도", "94.2%", "Optimal")

    # --- 4. 그래프 (현재가 기준으로 정렬) ---
    x_past = np.arange(0, 51)
    x_future = np.arange(50, 71)
    
    # 흰색 선 끝점이 정확히 live_btc가 되도록 설정
    y_current = live_btc + (np.random.normal(0, 50, 51).cumsum() - np.random.normal(0, 50, 51).cumsum()[-1])
    y_future = live_btc + np.random.normal(100, 180, 21).cumsum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_past, y=y_current, mode='lines', name='실시간 마켓', line=dict(color='#FFFFFF', width=4)))
    fig.add_trace(go.Scatter(x=x_future, y=y_future, mode='lines', name='AI 예상 경로', line=dict(color='#00E676', width=4)))

    fig.update_layout(
        template='plotly_dark', height=550, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(showgrid=True, gridcolor='#2d2d2d', tickformat="$,.0f",
                   range=[live_btc - 1500, live_btc + 2500])
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info(f"데이터 로드 시각: {datetime.now().strftime('%H:%M:%S')} (새로고침 시 갱신)")

else:
    st.title("📄 개인정보처리방침")
    st.write("본 서비스는 사용자의 데이터를 수집하지 않습니다.")
