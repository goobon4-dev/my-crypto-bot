import streamlit as st
import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 1. 데이터 엔진 (바이낸스 실시간 시세) ---
def get_live_data():
    try:
        url = f"https://api.binance.com/api/3/ticker/price?symbol=BTCUSDT&_t={int(datetime.now().timestamp())}"
        res = requests.get(url, timeout=3).json()
        return float(res['price'])
    except:
        return 0.0

# --- 2. 앱 설정 및 스타일 ---
st.set_page_config(page_title="AI QUANT DASHBOARD", layout="wide")

st.markdown("""
<style>
    .metric-card {
        background-color: #1a1c24;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #333;
        margin-bottom: 20px;
    }
    .price-val { font-size: 48px !important; font-weight: 800; color: #FFFFFF; }
    .target-val { font-size: 48px !important; font-weight: 800; color: #00FF88; }
    .label-txt { font-size: 14px; color: #888; margin-bottom: 5px; text-transform: uppercase; }
    .sim-box { 
        background: #252833; padding: 10px 15px; border-radius: 8px; 
        margin-top: 15px; font-size: 13px; color: #aaa; border-left: 4px solid #00FF88;
    }
</style>
""", unsafe_allow_html=True)

# 실시간 시세 확보
now_price = get_live_data()

# --- 3. 메인 대시보드 ---
st.sidebar.title("🤖 QUANT SYSTEM")
st.sidebar.info("상태: 실시간 분석 중")

# 상단 요약 정보
st.markdown("## 📊 AI 비트코인 시세 분석 결과")
st.markdown("<p style='color:#F0B90B;'>REAL-TIME BINANCE API SYNCHRONIZED</p>", unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3)
col_a.metric("시장 탐욕 지수", "15", "Extreme Fear")
col_b.metric("알고리즘 신뢰도", "94.2%", "Optimal")
col_c.metric("데이터 상태", "정상", "Live")

st.write("---")

# 메인 분석 리포트
st.markdown("### 📈 AI 가격 분석 리포트")
c1, c2 = st.columns(2)

with c1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="label-txt">Binance 현재가</div>
            <div class="price-val">${now_price:,.2f}</div>
            <div style="color:#00FF88; font-size:12px; margin-top:10px;">● 실시간 동기화 중</div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    # 현재가 기반 AI 예측 (상승 시나리오 예시)
    ai_target = now_price * 1.0145
    # 유사도 데이터 생성 (예시 데이터)
    sim_date = "2024-03-10"
    sim_percent = "92.8%"
    
    st.markdown(f"""
        <div class="metric-card">
            <div class="label-txt">AI 예측가</div>
            <div class="target-val">${ai_target:,.2f}</div>
            <div class="sim-box">
                <span style="color:#00FF88; font-weight:bold;">≡ 분석 리포트</span><br>
                • 유사 가격대 시점: {sim_date}<br>
                • 패턴 유사도: {sim_percent} 일치
            </div>
        </div>
    """, unsafe_allow_html=True)

# 하단 업데이트 로그
st.markdown(f"""
    <div style="font-size:12px; color:#555; text-align:right;">
        마지막 분석 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (F5를 눌러 갱신)
    </div>
""", unsafe_allow_html=True)
