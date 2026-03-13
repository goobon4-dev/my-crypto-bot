import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.graph_objects as go
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 설정 및 함수 ---
TELEGRAM_TOKEN = "8370033965:AAF1NYprBTunnUNdgt4QK1c8qkQ9MgKZBNc"
CHAT_ID = "5071081898"

def get_fear_and_greed():
    try:
        res = requests.get("https://api.alternative.me/fng/", timeout=5)
        data = res.json()['data'][0]
        return data['value'], data['value_classification']
    except:
        return "50", "Neutral"

# --- 페이지 설정 ---
st.set_page_config(page_title="본성 퀀트 비서", layout="wide")

# 사이드바 메뉴 (개인정보처리방침 추가)
menu = st.sidebar.radio("메뉴 선택", ["실시간 분석기", "개인정보처리방침"])

if menu == "실시간 분석기":
    # 1. 시장 심리 지수
    fng_val, fng_label = get_fear_and_greed()
    st.sidebar.header("🔥 시장 심리 지수")
    st.sidebar.metric("Fear & Greed Index", f"{fng_val} / 100", fng_label)
    st.sidebar.progress(int(fng_val))
    st.sidebar.write("---")

    # 2. 분석 설정
    symbol = st.sidebar.selectbox("종목 선택", ["BTC-USD", "ETH-USD", "SOL-USD"])
    interval = st.sidebar.selectbox("주기", ["1h", "1d", "15m"])
    
    st.title(f"📊 {symbol} 인공지능 패턴 분석")
    
    # [기존 데이터 분석 및 차트 코드]
    # 여기에 본성님의 기존 분석 로직이 들어갑니다.
    st.info("현재 시장 데이터를 분석 중입니다. 잠시만 기다려 주세요.")
    
    # 3. 광고 수익화 영역 (디자인 미리보기)
    st.write("---")
    st.markdown("""
    <div style="background-color: #1E1E1E; padding: 15px; border: 1px solid #444; border-radius: 10px; text-align: center;">
        <p style="color: #888; margin-bottom: 5px; font-size: 0.8em;">SPONSORED ADVERTISEMENT</p>
        <div style="height: 50px; display: flex; align-items: center; justify-content: center;">
            <p style="color: #555;">[이곳에 구글 애드몹 광고가 게재됩니다]</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # --- 구글 심사용 개인정보처리방침 ---
    st.title("📄 개인정보처리방침")
    st.write(f"최종 수정일: {time.strftime('%Y-%m-%d')}")
    st.markdown(f"""
    **본성 퀀트 비서** (이하 '앱')는 사용자의 개인정보를 소중히 다룹니다.
    
    1. **수집하는 정보:** 본 앱은 사용자의 개인 식별 정보를 수집하거나 저장하지 않습니다.
    2. **데이터 활용:** 분석을 위해 야후 파이낸스의 공개된 시장 데이터만을 사용합니다.
    3. **광고 관련:** 본 앱은 Google AdMob을 사용하여 광고를 표시하며, 이 과정에서 광고 ID가 사용될 수 있습니다.
    4. **문의:** dktkrk123@naver.com
    """)

# 자동 새로고침 (분석 페이지일 때만)
if menu == "실시간 분석기":
    time.sleep(60)
    st.rerun()
