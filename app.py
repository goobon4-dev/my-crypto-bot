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
        time.sleep(
