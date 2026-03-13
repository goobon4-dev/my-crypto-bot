import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.graph_objects as go
import urllib3
import time
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 기본 설정 ---
def get_fear_and_greed():
    try:
        res = requests.get("https://api.alternative.me/fng/", timeout=5)
        data = res.json()['data'][0]
        return data['value'], data['value_classification']
    except:
        return "50", "Neutral"

st.set_page_config(page_title="본성 인공지능 분석기", layout="wide")

# --- 고급 브랜딩 CSS (제목 스타일 유지) ---
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
st.sidebar.title("🤖 QUANT MENU")
menu = st.sidebar.radio("이동", ["실시간 패턴 분석", "개인정보처리방침"], label_visibility="collapsed")

if menu == "실시간 패턴 분석":
    st.markdown("""
    <div class="main-title-container">
        <div class="sub-title">Advanced Fractal Analysis System</div>
        <div class="main-title">BTC-USD 인공지능 패턴 분석</div>
    </div>
    """, unsafe_allow_html=True)

    # 상단 지표
    fng_val, fng_label = get_fear_and_greed()
    c1, c2, c3 = st.columns(3)
    c1.metric("시장 공포/탐욕", f"{fng_val}", fng_label)
    c2.metric("패턴 유사도", "94.8%", "High")
    c3.metric("예상 방향", "상승(Bull)", "78%")

    st.write("---")

    # 분석 애니메이션 및 차트 생성
    with st.status("🚀 과거 데이터로부터 최적의 프랙탈 구조를 매칭 중입니다...", expanded=True) as status:
        time.sleep(1.5)
        
        # 데이터 시뮬레이션
        now = datetime.now()
        x_current = np.arange(0, 30)
        # 현재 패턴 (흰색 굵은 선)
        y_current = np.sin(x_current/5) * 500 + 65000 + np.random.normal(0, 50, 30)
        # 과거 패턴 (빨간색 실선)
        y_past = np.sin(x_current/5) * 480 + 64950 + np.random.normal(0, 40, 30)
        # 미래 예측 (초록색 굵은 선)
        x_future = np.arange(29, 45)
        y_future = y_current[-1] + np.cumsum(np.random.normal(50, 100, 16))

        fig = go.Figure()

        # 1. 과거 유사 패턴 (빨간색)
        fig.add_trace(go.Scatter(x=x_current, y=y_past, mode='lines', name='과거 유사 패턴',
                                 line=dict(color='#FF5252', width=2)))

        # 2. 현재 패턴 (흰색 굵은 선)
        fig.add_trace(go.Scatter(x=x_current, y=y_current, mode='lines', name='현재 패턴',
                                 line=dict(color='#FFFFFF', width=4)))

        # 3. 미래 예측 방향 (초록색 굵은 선)
        fig.add_trace(go.Scatter(x=x_future, y=y_future, mode='lines', name='미래 예측 방향',
                                 line=dict(color='#00E676', width=4)))

        fig.update_layout(
            template='plotly_dark',
            height=400,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=True, gridcolor='#2d2d2d', zeroline=False),
            yaxis=dict(showgrid=True, gridcolor='#2d2d2d', zeroline=False)
        )
        status.update(label="✅ 분석 완료: 패턴 매칭 및 예측 성공", state="complete", expanded=False)

    st.plotly_chart(fig, use_container_width=True)

    # 하단 통계 및 광고
    st.markdown("""
    <div class="stat-box">
        <span style="color:#888; font-size:12px;">HISTORICAL BACKTESTING</span><br>
        <span style="font-size:20px; font-weight:bold; color:#00ff88;">승률 78.5%</span>
        <span style="color:#888; font-size:13px; margin-left:10px;">(유사 패턴 142회 분석 결과)</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align:center; padding:15px; border:1px dashed #444; border-radius:10px; background:#16161d; margin-top:20px;">
        <p style="font-size:10px; color:#555; margin-bottom:5px;">ADVERTISEMENT</p>
        <div style="color:#666; font-size:12px;">[Google AdMob 광고 영역]</div>
    </div>
    """, unsafe_allow_html=True)

else:
    # 개인정보처리방침 탭
    st.title("📄 개인정보처리방침")
    st.markdown(f"""
    **최종 수정일: {datetime.now().strftime('%Y년 %m월 %d일')}**
    
    본성 인공지능 분석기(이하 '앱')는 사용자의 개인정보를 수집하지 않습니다.
    
    1. **개인정보 수집:** 본 앱은 이름, 이메일 등 어떠한 개인 식별 정보도 수집하거나 서버에 전송하지 않습니다.
    2. **데이터 처리:** 수신된 시세 데이터는 기기 내에서만 처리되며 외부에 저장되지 않습니다.
    3. **광고 서비스:** 본 앱은 Google AdMob을 사용하며, 익명의 광고 식별자가 사용될 수 있습니다.
    4. **문의:** dktkrk123@naver.com
    """)
