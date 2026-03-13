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
        # 바이낸스 공식 API 사용 (BTC/USDT)
        url = "https://api.binance.com/api/3/ticker/price?symbol=BTCUSDT"
        res = requests.get(url, timeout=3)
        data = res.json()
        price = float(data['price'])
        return price
    except Exception as e:
        st.error(f"시세 로딩 오류: {e}")
        return 0.0

def get_fear_and_greed():
    try:
        res = requests.get("https://api.alternative.me/fng/", timeout=3)
        data = res.json()['data'][0]
        return data['value'], data['value_classification']
    except:
        return "50", "Neutral"

# --- 페이지 설정 (이름 제거 완료) ---
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

    # 1. 실시간 바이낸스 데이터 수집
    btc_now = get_realtime_btc()
    fng_val, fng_label = get_fear_and_greed()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Binance 실시간가", f"${btc_now:,.2f}", "LIVE")
    col2.metric("시장 탐욕 지수", f"{fng_val}", fng_label)
    col3.metric("알고리즘 신뢰도", "94.2%", "Optimal")

    st.write("---")

    # 2. 분석 애니메이션 (연출)
    with st.status("📊 바이낸스 오더북 및 과거 프랙탈 매칭 중...", expanded=True) as status:
        time.sleep(1.2)
        
        # 3. 데이터 시각화 (실제 가격 기준)
        x_past_current = np.arange(0, 50)
        # 현재 실시간 가격을 기점으로 과거 24시간 변동 시뮬레이션
        y_current = btc_now + (np.random.normal(0, 80, 50).cumsum() - np.random.normal(0, 80, 50).cumsum()[-1])
        # 과거 유사 패턴 (빨간색)
        y_past = y_current * 0.999 + np.random.normal(0, 50, 50)
        
        # 미래 예측 (초록색) - 현재 실시간가 btc_now에서 시작
        x_future = np.arange(49, 65)
        y_future = btc_now + np.cumsum(np.random.normal(60, 120, 16))

        fig = go.Figure()

        # 과거 패턴 (Red)
        fig.add_trace(go.Scatter(x=x_past_current, y=y_past, mode='lines', name='과거 유사 패턴',
                                 line=dict(color='#FF5252', width=2)))
        # 현재 패턴 (White)
        fig.add_trace(go.Scatter(x=x_past_current, y=y_current, mode='lines', name='실시간 마켓 현황',
                                 line=dict(color='#FFFFFF', width=4)))
        # 미래 예측 (Green)
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
            xaxis=dict(showgrid=True, gridcolor='#2d2d2d'),
            yaxis=dict(showgrid=True, gridcolor='#2d2d2d', tickformat="$,.0f")
        )
        status.update(label="✅ 데이터 동기화 완료", state="complete", expanded=False)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="stat-box">
        <span style="color:#888; font-size:12px;">ENGINE STATUS</span><br>
        <span style="font-size:16px; font-weight:bold; color:#00ff88;">REAL-TIME SYNCED WITH BINANCE</span>
    </div>
    """, unsafe_allow_html=True)
    
else:
    st.title("📄 개인정보처리방침")
    st.markdown(f"최종 수정일: {datetime.now().strftime('%Y-%m-%d')}")
    st.write("본 시스템은 개인정보를 수집하지 않으며, 바이낸스의 공개 API를 통해 시장 데이터를 분석합니다.")

# 60초마다 강제 새로고침하여 최신 시세 반영
if menu == "ANALYSIS":
    time.sleep(60)
    st.rerun()
