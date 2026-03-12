import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 텔레그램 설정 ---
TELEGRAM_TOKEN = "8370033965:AAF1NYprBTunnUNdgt4QK1c8qkQ9MgKZBNc"
CHAT_ID = "5071081898"

def send_telegram_msg(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": msg}
        requests.get(url, params=params)
    except:
        pass

# 페이지 설정
st.set_page_config(page_title="본성 퀀트 분석기 (알림기능)", layout="wide")

st.title("🚀 비트코인 통합 분석 및 텔레그램 알림 시스템")

# --- 사이드바 ---
st.sidebar.header("⚙️ 분석 설정")
symbol = st.sidebar.selectbox("종목 선택", ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD"])
interval = st.sidebar.selectbox("시간 단위", ["15m", "1h", "1d"], index=1)
window_size = st.sidebar.slider("비교 패턴 길이", 10, 100, 30)
future_size = st.sidebar.slider("예측 구간", 5, 50, 15)

def get_data(symbol, interval):
    range_map = {"15m": "60d", "1h": "730d", "1d": "1095d"}
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval={interval}&range={range_map[interval]}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers, verify=False)
    data = res.json()['chart']['result'][0]
    df = pd.DataFrame({
        'Close': data['indicators']['quote'][0]['close'],
        'Volume': data['indicators']['quote'][0]['volume']
    }, index=pd.to_datetime(data['timestamp'], unit='s'))
    return df.dropna()

def calculate_rsi(series, period=14):
    delta = series.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    ema_up = up.ewm(com=period-1, adjust=False).mean()
    ema_down = down.abs().ewm(com=period-1, adjust=False).mean()
    return 100 - (100 / (1 + (ema_up / ema_down)))

try:
    df = get_data(symbol, interval)
    df['RSI'] = calculate_rsi(df['Close'])
    
    current_prices = df['Close'][-window_size:]
    c_min, c_max = current_prices.min(), current_prices.max()
    curr_norm = (current_prices - c_min) / (c_max - c_min)

    # 패턴 매칭
    scores = []
    search_end = len(df) - (window_size + future_size + 1)
    for i in range(search_end):
        past_chunk = df['Close'][i : i + window_size]
        p_min, p_max = past_chunk.min(), past_chunk.max()
        if p_max == p_min: continue
        past_norm = (past_chunk - p_min) / (p_max - p_min)
        mse = np.mean((curr_norm.values - past_norm.values)**2)
        similarity = (1 - mse) * 100
        scores.append((similarity, i))
    
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # --- 알림 로직 ---
    top_sim = scores[0][0]
    current_rsi = df['RSI'].iloc[-1]
    
    if st.button("🔔 테스트 알림 보내기"):
        send_telegram_msg(f"✅ 테스트 성공! 현재 {symbol} 분석 중입니다.")

    # 특정 조건 시 알림 (예: 유사도 92% 이상 또는 RSI 극단값)
    if top_sim > 92 or current_rsi > 75 or current_rsi < 25:
        msg = f"🚨 [{symbol}] 포착!\n- 유사도: {top_sim:.1f}%\n- 현재 RSI: {current_rsi:.1f}\n- 분석 주기: {interval}"
        # 실시간 웹 접속 중에만 중복방지를 위해 버튼으로 처리하거나 자동으로 쏘게 할 수 있음
        st.info("💡 조건 충족! 텔레그램으로 알림을 보낼 수 있는 상태입니다.")

    # 대시보드 출력 (기존 차트 코드)
    col1, col2, col3 = st.columns(3)
    col1.metric("현재가", f"${df['Close'].iloc[-1]:,.2f}")
    col2.metric("최고 유사도", f"{top_sim:.1f}%")
    col3.metric("RSI", f"{current_rsi:.2f}")

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, row_heights=[0.5, 0.2, 0.3], vertical_spacing=0.05)
    fig.add_trace(go.Scatter(x=list(range(window_size)), y=current_prices.values, name="현재 흐름", line=dict(color='white', width=4)), row=1, col=1)
    
    for i in range(3):
        idx = scores[i][1]
        past_match = df['Close'][idx : idx + window_size]
        p_min, p_max = past_match.min(), past_match.max()
        match_scaled = ((past_match - p_min) / (p_max - p_min) * (c_max - c_min)) + c_min
        fig.add_trace(go.Scatter(x=list(range(window_size)), y=match_scaled, name=f"{i+1}위({scores[i][0]:.1f}%)", line=dict(dash='dash')), row=1, col=1)

    fig.add_trace(go.Bar(x=list(range(window_size)), y=df['Volume'][-window_size:], name="거래량"), row=2, col=1)
    fig.add_trace(go.Scatter(x=list(range(window_size)), y=df['RSI'][-window_size:], name="RSI", line=dict(color="#8884d8")), row=3, col=1)
    fig.add_hline(y=70, line_dash="dot", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dot", line_color="green", row=3, col=1)
    
    fig.update_layout(height=800, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"오류 발생: {e}")
