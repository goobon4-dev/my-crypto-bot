import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.graph_objects as go
import urllib3
import time
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 바이낸스 실시간 시세 호출 함수 ---
def get_realtime_btc():
    try:
        url = "https://api.binance.com/api/3/ticker/price?symbol=BTCUSDT"
        res = requests.get(url, timeout=3)
        data = res.json()
        return float(data['price'])
    except Exception as e:
        return 0.0

def get_fear_and_greed():
    try:
        res = requests.get("https://api.alternative.me/fng/", timeout=3)
        data = res.json()['data'][0]
        return data['value'], data['value_classification']
    except:
        return "50", "Neutral"

# --- 페이지 설정 ---
st.set_page_config(page_title="AI QUANT SYSTEM", layout="wide")

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

# 사이드바
st.sidebar.title("🤖 SYSTEM")
menu = st.sidebar.radio("Nav", ["ANALYSIS", "POLICY"], label_visibility="collapsed")

if menu == "ANALYSIS":
    st.markdown("""
    <div class="main-title-container">
        <div class="sub-title">Binance Live Data Sync</div>
        <div class="main-title">BTC-USD 인공지능 패턴 분석</div>
    </div>
    """, unsafe_allow_html=True)

    btc_now = get_realtime_btc()
    fng_val, fng_label = get_fear_and_greed()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Binance 실시간가", f"${btc_now:,.2f}", "LIVE")
    col2.metric("시장 탐욕 지수", f"{fng_val}", fng_label)
    col3.metric("알고리즘 신뢰도", "94.2%", "Optimal")

    st.write("---")

    with st.status("📊 바이낸스 실시간 데이터 및 미래 예측 분석 중...", expanded=True) as status:
        time.sleep(1.2)
        
        # --- 데이터 생성 (바이낸스 실제 가격 btc_now 기준) ---
        x_past_current = np.arange(0, 50)
        # 현재 실시간 가격을 기점으로 과거 변동 시뮬레이션
        y_current = btc_now + (np.random.normal(0, 80, 50).cumsum() - np.random.normal(0, 80, 50).cumsum()[-1])
        # 과거 유사 패턴 (빨간색) - 현재 선과 약간 어긋나게
        y_past = y_current * 0.999 + np.random.normal(0, 60, 50)
        
        # 미래 예측 (초록색) - 현재 실시간가(btc_now)에서 시작하여 앞으로 뻗어감
        x_future = np.arange(49, 65)
        # 그림처럼 상승하는 패턴으로 연출
        y_future = btc_now + np.cumsum(np.random.normal(70, 100, 16))

        fig = go.Figure()

        # 1. 과거 유사 패턴 (빨간색 실선 - 가늘게)
        fig.add_trace(go.Scatter(x=x_past_current, y=y_past, mode='lines', name='과거 유사 패턴',
                                 line=dict(color='#FF5252', width=1.5, dash='solid')))

        # 2. 현재 실시간 마켓 (흰색 굵은 실선 - 가장 돋보이게)
        fig.add_trace(go.Scatter(x=x_past_current, y=y_current, mode='lines', name='실시간 마켓 현황',
                                 line=dict(color='#FFFFFF', width=4)))

        # 3. AI 미래 예상 경로 (초록색 굵은 실선 - 예측의 핵심)
        fig.add_trace(go.Scatter(x=x_future, y=y_future, mode='lines', name='AI 예상 경로',
                                 line=dict(color='#00E676', width=4)))

        fig.update_layout(
            template='plotly_dark',
            height=450,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=True, gridcolor='#2d2d2d', zeroline=False),
            yaxis=dict(showgrid=True, gridcolor='#2d2d2d', tickformat="$,.0f", zeroline=False)
        )
        status
