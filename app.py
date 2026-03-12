import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 페이지 설정
st.set_page_config(page_title="BTC 전문 퀀트 분석기", layout="wide")

# --- CSS로 디자인 커스텀 ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 비트코인 통합 퀀트 분석 대시보드")

# --- 사이드바: 설정 ---
st.sidebar.header("⚙️ 분석 설정")
symbol = st.sidebar.selectbox("종목 선택", ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "DOGE-USD"])
interval = st.sidebar.selectbox("시간 단위", ["1m", "5m", "15m", "1h", "1d"], index=3)
window_size = st.sidebar.slider("비교 패턴 길이", 10, 100, 30)
future_size = st.sidebar.slider("예측 구간", 5, 50, 15)

# --- 데이터 로드 함수 ---
def get_data(symbol, interval):
    range_map = {"1m": "7d", "5m": "60d", "15m": "60d", "1h": "730d", "1d": "1095d"}
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval={interval}&range={range_map[interval]}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers, verify=False)
    data = res.json()['chart']['result'][0]
    
    df = pd.DataFrame({
        'Close': data['indicators']['quote'][0]['close'],
        'Volume': data['indicators']['quote'][0]['volume']
    }, index=pd.to_datetime(data['timestamp'], unit='s'))
    return df.dropna()

# --- 보조지표 계산 (RSI) ---
def calculate_rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=period-1, adjust=False).mean()
    ema_down = down.ewm(com=period-1, adjust=False).mean()
    rs = ema_up / ema_down
    return 100 - (100 / (1 + rs))

try:
    df = get_data(symbol, interval)
    df['RSI'] = calculate_rsi(df['Close'])
    
    # 분석 구간 설정
    current_prices = df['Close'][-window_size:]
    c_min, c_max = current_prices.min(), current_prices.max()
    curr_norm = (current_prices - c_min) / (c_max - c_min)

    # 패턴 매칭 (Top 3)
    scores = []
    search_end = len(df) - (window_size + future_size + 1)
    for i in range(search_end):
        past_chunk = df['Close'][i : i + window_size]
        p_min, p_max = past_chunk.min(), past_chunk.max()
        if p_max == p_min: continue
        past_norm = (past_chunk - p_min) / (p_max - p_min)
        score = np.mean((curr_norm.values - past_norm.values)**2)
        scores.append((score, i))
    
    scores.sort(key=lambda x: x[0])
    top_indices = []
    for s, idx in scores:
        if all(abs(idx - used) > window_size for used in top_indices):
            top_indices.append(idx)
        if len(top_indices) >= 3: break

    # --- 메인 대시보드 레이아웃 ---
    col1, col2, col3 = st.columns(3)
    col1.metric("현재가", f"${df['Close'].iloc[-1]:,.2f}")
    col2.metric("현재 RSI", f"{df['RSI'].iloc[-1]:.2f}", delta_color="inverse")
    col3.metric("분석 범위", f"{len(df)} 캔들")

    # --- 차트 생성 (서브플롯 사용: 가격/패턴 + 거래량 + RSI) ---
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, row_heights=[0.5, 0.2, 0.3],
                        subplot_titles=("패턴 비교 및 예측", "거래량(Volume)", "상대강도지수(RSI)"))

    # 1. 가격 및 패턴 차트
    fig.add_trace(go.Scatter(x=list(range(window_size)), y=current_prices.values, name="현재 흐름", line=dict(color='white', width=4)), row=1, col=1)
    
    colors = ['#FF4B4B', '#FFAA00', '#00CC96']
    for i, idx in enumerate(top_indices):
        past_match = df['Close'][idx : idx + window_size]
        past_future = df['Close'][idx + window_size : idx + window_size + future_size]
        
        # 스케일 보정
        p_min, p_max = past_match.min(), past_match.max()
        match_scaled = ((past_match - p_min) / (p_max - p_min) * (c_max - c_min)) + c_min
        future_scaled = ((past_future - p_min) / (p_max - p_min) * (c_max - c_min)) + c_min
        
        match_date = df.index[idx].strftime('%Y-%m-%d')
        fig.add_trace(go.Scatter(x=list(range(window_size)), y=match_scaled, name=f"{i+1}위:{match_date}", line=dict(color=colors[i], dash='dash')), row=1, col=1)
        fig.add_trace(go.Scatter(x=list(range(window_size, window_size+future_size)), y=future_scaled, name=f"{i+1}위 예측", line=dict(color=colors[i])), row=1, col=1)

    # 2. 거래량 차트
    fig.add_trace(go.Bar(x=list(range(window_size)), y=df['Volume'][-window_size:], name="거래량", marker_color="gray"), row=2, col=1)

    # 3. RSI 차트
    fig.add_trace(go.Scatter(x=list(range(window_size)), y=df['RSI'][-window_size:], name="RSI", line=dict(color="#8884d8")), row=3, col=1)
    fig.add_hline(y=70, line_dash="dot", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dot", line_color="green", row=3, col=1)

    fig.update_layout(height=800, template="plotly_dark", showlegend=True, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"데이터 분석 중 오류 발생: {e}")
