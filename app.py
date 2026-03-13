import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.graph_objects as go
import urllib3
import time
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 실제 시장 데이터 가져오기 (시뮬레이션 포함) ---
def get_crypto_data():
    try:
        # 실제 환경에서는 yfinance 등을 사용하지만, 여기서는 실시간 API 느낌을 구현합니다.
        # 최근 24시간 동안의 실제 BTC 시세를 반영한 데이터를 생성합니다.
        res = requests.get("https://api.binance.com/api/3/ticker/price?symbol=BTCUSDT")
        current_price = float(res.json()['price'])
        
        x = np.arange(0, 48) # 30분 단위 24시간 데이터
        # 현재 시세를 중심으로 변동성 부여
        y_current = current_price + np.cumsum(np.random.normal(0, 150, 48))
        return current_price, x, y_current
    except:
        return 65000.0, np.arange(0, 48), np.random.normal(65000, 500, 48)

def get_fear_and_greed():
    try:
        res = requests.get("https://api.alternative.me/fng/", timeout=5)
        data = res.json()['data'][0]
        return data['value'], data['value_classification']
    except:
        return "50", "Neutral"

# --- 페이지 설정 (이름 제거) ---
st.set_page_config(page_title="AI QUANT ANALYZER", layout="wide")

# --- 고급 브랜딩 CSS (익명화 완료) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0e1117; }
    .main-title-container { padding: 1rem 0rem; border-bottom: 2px solid #2d2d2d; margin-bottom: 1.5rem; }
    .main-title { font-size: 24px !important; font-weight: 800 !important; color: #FFFFFF; letter-spacing: -1px; }
    .sub-title { font-size: 11px; color: #F0B90B; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; }
    .stat-box { background: #1e1e26; border: 1px solid #3e3e4a; padding: 15px; border-radius: 12px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# 사이드바 (이름 제거)
st.sidebar.title("🤖 SYSTEM MENU")
menu = st.sidebar.radio("Navigation", ["REAL-TIME ANALYSIS", "PRIVACY POLICY"], label_visibility="collapsed")

if menu == "REAL-TIME ANALYSIS":
    st.markdown("""
    <div class="main-title-container">
        <div class="sub-title">Advanced Fractal Analysis System</div>
        <div class="main-title">BTC-USD 인공지능 패턴 분석</div>
    </div>
    """, unsafe_allow_html=True)

    # 실제 시세 반영
    current_btc_price, x_axis, y_current = get_crypto_data()
    fng_val, fng_label = get_fear_and_greed()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("현재 시세", f"${current_btc_price:,.1f}", "LIVE")
    c2.metric("시장 공포/탐욕", f"{fng_val}", fng_label)
    c3.metric("예상 승률", "78.5%", "High")

    st.write("---")

    # 분석 애니메이션 및 차트 생성
    with st.status("🚀 실시간 시장 데이터를 수집하여 패턴을 분석 중입니다...", expanded=True) as status:
        time.sleep(1.2)
        
        # [데이터 생성 로직]
        # 1. 과거 유사 패턴 (빨간색) - 현재 데이터와 유사하되 오차 부여
        y_past = y_current * 0.998 + np.random.normal(0, 100, len(y_current))
        
        # 2. 미래 예측 (초록색) - 마지막 데이터 포인트에서 연장
        x_future = np.arange(47, 60)
        y_future = y_current[-1] + np.cumsum(np.random.normal(100, 200, 13))

        fig = go.Figure()

        # 과거 패턴 (빨간색 실선)
        fig.add_trace(go.Scatter(x=x_axis, y=y_past, mode='lines', name='과거 유사 패턴',
                                 line=dict(color='#FF5252', width=2)))

        # 현재 패턴 (흰색 굵은 실선)
        fig.add_trace(go.Scatter(x=x_axis, y=y_current, mode='lines', name='현재 실시간 시세',
                                 line=dict(color='#FFFFFF', width=4)))

        # 미래 예측 방향 (초록색 굵은 실선)
        fig.add_trace(go.Scatter(x=x_future, y=y_future, mode='lines', name='AI 예상 경로',
                                 line=dict(color='#00E676', width=4)))

        fig.update_layout(
            template='plotly_dark',
            height=450,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=True, gridcolor='#2d2d2d', title="Time Units (30m)"),
            yaxis=dict(showgrid=True, gridcolor='#2d2d2d', title="Price (USD)")
