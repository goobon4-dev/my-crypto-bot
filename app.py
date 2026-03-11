import streamlit as st
import pandas as pd
import requests
import numpy as np
import plotly.graph_objects as go
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(page_title="BTC 퀀트 분석기 - Top 3 매칭", layout="wide")

st.title("🤖 비트코인 패턴 매칭 엔진 (Top 3 Case Study)")

# --- 사이드바 설정 ---
st.sidebar.header("🔍 분석 옵션")
symbol = st.sidebar.text_input("종목 코드", value="BTC-USD")
interval = st.sidebar.selectbox("시간 단위", ["1m", "5m", "15m", "1h", "1d"], index=4)
range_map = {"1m": "7d", "5m": "60d", "15m": "60d", "1h": "730d", "1d": "1095d"}
data_range = range_map[interval]

window_size = st.sidebar.slider("비교 패턴 길이", 10, 60, 20)
future_size = st.sidebar.slider("예측 구간 길이", 5, 30, 10)

def get_data(symbol, interval, range_str):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval={interval}&range={range_str}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers, verify=False)
    data = res.json()
    result = data['chart']['result'][0]
    prices = result['indicators']['quote'][0]['close']
    dates = pd.to_datetime(result['timestamp'], unit='s')
    return pd.Series(prices, index=dates).dropna()

try:
    with st.spinner('방대한 데이터를 전수 조사 중...'):
        all_prices = get_data(symbol, interval, data_range)
        current_pattern = all_prices[-window_size:]
        c_min, c_max = current_pattern.min(), current_pattern.max()
        curr_norm = (current_pattern - c_min) / (c_max - c_min)
        
        # 모든 구간의 오차(Score)를 계산하여 저장
        scores = []
        search_end = len(all_prices) - (window_size + future_size + 1)
        
        for i in range(search_end):
            past_chunk = all_prices[i : i + window_size]
            p_min, p_max = past_chunk.min(), past_chunk.max()
            if p_max == p_min: continue
            
            past_norm = (past_chunk - p_min) / (p_max - p_min)
            score = np.mean((curr_norm.values - past_norm.values)**2)
            scores.append((score, i))
        
        # 오차순으로 정렬 후 상위 3개 추출 (서로 겹치지 않게 거리 유지)
        scores.sort(key=lambda x: x[0])
        top_matches = []
        used_indices = set()
        
        for score, idx in scores:
            # 선택된 지점들이 서로 너무 가깝지 않게 (패턴 길이만큼 간격 유지)
            if all(abs(idx - used) > window_size for used in used_indices):
                top_matches.append((score, idx))
                used_indices.add(idx)
            if len(top_matches) >= 3: break

        # --- 차트 그리기 ---
        fig = go.Figure()

        # 1. 현재 데이터 (가장 굵게)
        fig.add_trace(go.Scatter(
            x=list(range(window_size)), y=current_pattern.values,
            mode='lines+markers', name='<b>현재 흐름</b>',
            line=dict(color='white', width=5)
        ))

        colors = ['#FF4B4B', '#FFAA00', '#00CC96'] # 레드, 오렌지, 그린
        
        for rank, (score, idx) in enumerate(top_matches):
            match_date = all_prices.index[idx]
            past_match = all_prices[idx : idx + window_size]
            past_future = all_prices[idx + window_size : idx + window_size + future_size]
            
            # 스케일 조정
            p_min, p_max = past_match.min(), past_match.max()
            match_scaled = ((past_match - p_min) / (p_max - p_min) * (c_max - c_min)) + c_min
            future_scaled = ((past_future - p_min) / (p_max - p_min) * (c_max - c_min)) + c_min
            
            # 과거 패턴 (점선)
            fig.add_trace(go.Scatter(
                x=list(range(window_size)), y=match_scaled.values,
                mode='lines', name=f'{rank+1}위: {match_date.date()}',
                line=dict(color=colors[rank], dash='dash', width=2)
            ))
            
            # 미래 예측 (실선)
            fig.add_trace(go.Scatter(
                x=list(range(window_size, window_size + future_size)), y=future_scaled.values,
                mode='lines+markers', name=f'{rank+1}위 미래 경로',
                line=dict(color=colors[rank], width=2)
            ))

        fig.update_layout(
            title=f"<b>{symbol} {interval} 분석: 상위 3개 유사 패턴 대조</b>",
            xaxis_title="봉 개수 (Time Steps)", yaxis_title="가격 ($)",
            template="plotly_dark", height=600,
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

        # 요약 정보 표로 출력
        st.subheader("📋 분석 결과 요약")
        summary_data = []
        for rank, (score, idx) in enumerate(top_matches):
            match_date = all_prices.index[idx]
            past_future = all_prices[idx + window_size : idx + window_size + future_size]
            change = (past_future.values[-1] - all_prices[idx + window_size - 1]) / all_prices[idx + window_size - 1] * 100
            summary_data.append({
                "순위": f"{rank+1}위",
                "날짜": match_date.date(),
                "유사도": f"{100-(score*100):.2f}%",
                "이후 10일 변동": f"{change:+.2f}%"
            })
        st.table(summary_data)

except Exception as e:
    st.error(f"오류: {e}")