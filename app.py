import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib3
import time
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 텔레그램 및 설정 ---
TELEGRAM_TOKEN = "8370033965:AAF1NYprBTunnUNdgt4QK1c8qkQ9MgKZBNc"
CHAT_ID = "5071081898"

def send_telegram_msg(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.get(url, params=params)
    except:
        pass

# 페이지 설정
st.set_page_config(page_title="본성 인공지능 퀀트 비서", layout="wide")

# --- 자동 감시 로직 (접속 안 해도 돌아가는 핵심 기능) ---
if 'last_alert_time' not in st.session_state:
    st.session_state.last_alert_time = 0

st.title("🤖 24시간 자동 패턴 감시 시스템")
st.info("이 화면을 켜두시면 1시간마다 자동으로 데이터를 갱신하며, 조건 충족 시 텔레그램으로 즉시 알림을 보냅니다.")

# 사이드바 설정
symbol = st.sidebar.selectbox("종목 선택", ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD"])
interval = st.sidebar.selectbox("감시 주기 (Timeframe)", ["15m", "1h", "1d"], index=1)
threshold = st.sidebar.slider("알림 발송 유사도 (%)", 85, 98, 93)

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
    
    current_prices = df['Close'][-30:] # 고정 패턴 길이 30
    c_min, c_max = current_prices.min(), current_prices.max()
    curr_norm = (current_prices - c_min) / (c_max - c_min)

    # 패턴 매칭 루프
    scores = []
    search_end = len(df) - 50
    for i in range(search_end):
        past_chunk = df['Close'][i : i + 30]
        p_min, p_max = past_chunk.min(), past_chunk.max()
        if p_max == p_min: continue
        past_norm = (past_chunk - p_min) / (p_max - p_min)
        mse = np.mean((curr_norm.values - past_norm.values)**2)
        similarity = (1 - mse) * 100
        scores.append((similarity, i))
    
    scores.sort(key=lambda x: x[0], reverse=True)
    top_sim = scores[0][0]
    current_rsi = df['RSI'].iloc[-1]
    current_price = df['Close'].iloc[-1]

    # --- 실시간 자동 알림 조건 체크 ---
    current_time = time.time()
    # 1시간(3600초)마다 혹은 조건 충족 시 알림
    if top_sim >= threshold or current_rsi >= 75 or current_rsi <= 25:
        # 중복 알림 방지 (최소 30분 간격)
        if current_time - st.session_state.last_alert_time > 1800:
            status = "🔴 과매수" if current_rsi > 70 else "🟢 과매도" if current_rsi < 30 else "🔍 패턴포착"
            msg = f"""
📌 *[{symbol} {interval} 분석 보고]*
💰 현재가: `${current_price:,.2f}`
🎯 최고 유사도: `{top_sim:.1f}%`
📊 현재 RSI: `{current_rsi:.2f}` ({status})

💡 *과거 {df.index[scores[0][1]].strftime('%Y-%m-%d')} 패턴과 매우 흡사합니다!*
            """
            send_telegram_msg(msg)
            st.session_state.last_alert_time = current_time
            st.success("✅ 조건 충족으로 텔레그램 알림을 발송했습니다!")

    # 대시보드 시각화 (기본 출력)
    col1, col2, col3 = st.columns(3)
    col1.metric("현재가", f"${current_price:,.2f}")
    col2.metric("매칭 스코어", f"{top_sim:.1f}%")
    col3.metric("상태", "중립" if 30<current_rsi<70 else "신호 발생")

    fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], vertical_spacing=0.1)
    fig.add_trace(go.Scatter(x=list(range(30)), y=current_prices.values, name="현재", line=dict(color='white', width=3)), row=1, col=1)
    
    for i in range(2): # 상위 2개만 표시
        idx = scores[i][1]
        past_match = df['Close'][idx : idx + 30]
        p_min, p_max = past_match.min(), past_match.max()
        match_scaled = ((past_match - p_min) / (p_max - p_min) * (c_max - c_min)) + c_min
        fig.add_trace(go.Scatter(x=list(range(30)), y=match_scaled, name=f"{i+1}위({scores[i][0]:.1f}%)", line=dict(dash='dot')), row=1, col=1)

    fig.add_trace(go.Scatter(x=list(range(30)), y=df['RSI'][-30:], name="RSI", line=dict(color="#8884d8")), row=2, col=1)
    fig.update_layout(height=600, template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

    # 페이지 자동 새로고침 코드 (중요!)
    time.sleep(60) # 1분마다 체크
    st.rerun()

except Exception as e:
    st.error(f"감시 중 오류: {e}")
