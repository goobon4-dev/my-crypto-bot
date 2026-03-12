import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.graph_objects as go
import urllib3
import time
import io

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 텔레그램 설정 ---
TELEGRAM_TOKEN = "8370033965:AAF1NYprBTunnUNdgt4QK1c8qkQ9MgKZBNc"
CHAT_ID = "5071081898"

def send_telegram_all(msg, fig):
    try:
        # 1. 메시지 먼저 보내기
        msg_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.get(msg_url, params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
        
        # 2. 차트를 이미지(Bytes)로 변환 (엔진 명시)
        img_bytes = fig.to_image(format="png", engine="kaleido")
        
        # 3. 사진 보내기
        photo_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        files = {'photo': ('chart.png', img_bytes, 'image/png')}
        requests.post(photo_url, data={'chat_id': CHAT_ID}, files=files)
    except Exception as e:
        # 오류가 나면 웹 화면에 표시해서 원인 찾기
        st.error(f"알림 전송 중 에러 발생: {e}")

# 페이지 설정
st.set_page_config(page_title="본성 비주얼 비서", layout="wide")

# 사이드바 설정
symbol = st.sidebar.selectbox("종목 선택", ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD"])
interval = st.sidebar.selectbox("감시 주기", ["15m", "1h", "1d"], index=1)
threshold = st.sidebar.slider("알림 발송 유사도 (%)", 80, 98, 88) # 테스트를 위해 수치를 좀 낮춰볼게요

if 'last_alert_time' not in st.session_state:
    st.session_state.last_alert_time = 0

def get_data(symbol, interval):
    range_map = {"15m": "60d", "1h": "730d", "1d": "1095d"}
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval={interval}&range={range_map[interval]}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers, verify=False)
    data = res.json()['chart']['result'][0]
    df = pd.DataFrame({'Close': data['indicators']['quote'][0]['close']}, 
                      index=pd.to_datetime(data['timestamp'], unit='s'))
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
    
    # --- 차트 생성 ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=current_prices.values, name="현재 흐름", line=dict(color='white', width=4)))
    
    idx = scores[0][1]
    past_match = df['Close'][idx : idx + 30]
    p_min, p_max = past_match.min(), past_match.max()
    match_scaled = ((past_match - p_min) / (p_max - p_min) * (c_max - c_min)) + c_min
    fig.add_trace(go.Scatter(y=match_scaled.values, name=f"매칭 패턴({top_sim:.1f}%)", line=dict(color='orange', dash='dot')))
    
    fig.update_layout(title=f"📈 {symbol} 유사도 분석 ({interval})", template="plotly_dark")

    # --- 알림 발송 (테스트 버튼 추가) ---
    if st.button("📸 지금 바로 차트 알림 테스트"):
        msg = f"🚀 *차트 전송 테스트*\n유사도: `{top_sim:.1f}%`"
        send_telegram_all(msg, fig)
        st.success("텔레그램 확인해보세요!")

    # 자동 알림 조건
    curr_time = time.time()
    if top_sim >= threshold:
        if curr_time - st.session_state.last_alert_time > 600: # 테스트를 위해 10분으로 단축
            msg = f"🎯 *[{symbol}] 유사 패턴 포착!*\n🤝 유사도: `{top_sim:.1f}%`"
            send_telegram_all(msg, fig)
            st.session_state.last_alert_time = curr_time

    st.plotly_chart(fig, use_container_width=True)
    
    time.sleep(60)
    st.rerun()

except Exception as e:
    st.error(f"오류: {e}")
