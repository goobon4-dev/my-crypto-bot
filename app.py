import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib3
import time
import io
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 텔레그램 설정 ---
TELEGRAM_TOKEN = "8370033965:AAF1NYprBTunnUNdgt4QK1c8qkQ9MgKZBNc"
CHAT_ID = "5071081898"

def send_telegram_all(msg, fig):
    try:
        # 1. 메시지 보내기
        msg_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.get(msg_url, params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
        
        # 2. 차트 이미지로 변환하여 보내기
        img_bytes = fig.to_image(format="png", width=800, height=500)
        photo_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        files = {'photo': ('chart.png', img_bytes, 'image/png')}
        requests.post(photo_url, data={'chat_id': CHAT_ID}, files=files)
    except Exception as e:
        print(f"알림 전송 실패: {e}")

# 페이지 설정
st.set_page_config(page_title="본성 인공지능 비주얼 비서", layout="wide")

st.title("🤖 24시간 비주얼 패턴 감시 시스템")

# 사이드바 설정
symbol = st.sidebar.selectbox("종목 선택", ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD"])
interval = st.sidebar.selectbox("감시 주기", ["15m", "1h", "1d"], index=1)
threshold = st.sidebar.slider("알림 발송 유사도 (%)", 85, 98, 92)

if 'last_alert_time' not in st.session_state:
    st.session_state.last_alert_time = 0

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

try:
    df = get_data(symbol, interval)
    current_prices = df['Close'][-30:]
    c_min, c_max = current_prices.min(), current_prices.max()
    curr_norm = (current_prices - c_min) / (c_max - c_min)

    # 패턴 분석
    scores = []
    for i in range(len(df) - 50):
        past_chunk = df['Close'][i : i + 30]
        p_min, p_max = past_chunk.min(), past_chunk.max()
        if p_max == p_min: continue
        past_norm = (past_chunk - p_min) / (p_max - p_min)
        similarity = (1 - np.mean((curr_norm.values - past_norm.values)**2)) * 100
        scores.append((similarity, i))
    
    scores.sort(key=lambda x: x[0], reverse=True)
    top_sim = scores[0][0]
    current_price = df['Close'].iloc[-1]

    # --- 차트 생성 (알림용 및 화면용) ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=current_prices.values, name="현재", line=dict(color='white', width=4)))
    
    idx = scores[0][1]
    past_match = df['Close'][idx : idx + 30]
    p_min, p_max = past_match.min(), past_match.max()
    match_scaled = ((past_match - p_min) / (p_max - p_min) * (c_max - c_min)) + c_min
    fig.add_trace(go.Scatter(y=match_scaled.values, name=f"과거({top_sim:.1f}%)", line=dict(color='orange', dash='dot')))
    
    fig.update_layout(title=f"{symbol} 패턴 대조표", template="plotly_dark")

    # --- 실시간 알림 로직 ---
    curr_time = time.time()
    if top_sim >= threshold:
        if curr_time - st.session_state.last_alert_time > 1800:
            msg = f"🎯 *[{symbol}] 역대급 패턴 포착!*\n💰 현재가: `${current_price:,.2f}`\n🤝 유사도: `{top_sim:.1f}%`"
            send_telegram_all(msg, fig)
            st.session_state.last_alert_time = curr_time
            st.success("📸 차트 이미지를 포함한 알림을 전송했습니다!")

    st.plotly_chart(fig, use_container_width=True)
    
    # 1분 뒤 자동 재실행
    time.sleep(60)
    st.rerun()

except Exception as e:
    st.error(f"실행 중 오류: {e}")
