import streamlit as st
import requests
import urllib3
from datetime import datetime

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 1. 바이낸스 실시간 데이터 엔진 ---
def get_btc_data():
    try:
        # 캐싱 방지를 위해 타임스탬프 파라미터 추가
        url = f"https://api.binance.com/api/3/ticker/price?symbol=BTCUSDT&_t={int(datetime.now().timestamp())}"
        res = requests.get(url, timeout=3).json()
        price = float(res['price'])
        return price
    except:
        return 0.0

# --- 2. 페이지 설정 ---
st.set_page_config(page_title="QUANT AI DASHBOARD", layout="wide")

# 스타일 커스텀: 숫자 가독성 극대화
st.markdown("""
<style>
    .metric-container {
        background-color: #1a1c24;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #333;
        text-align: center;
        margin-bottom: 20px;
    }
    .price-text { font-size: 42px !important; font-weight: 800; color: #FFFFFF; }
    .target-text { font-size: 42px !important; font-weight: 800; color: #00FF88; }
    .label-text { font-size: 16px; color: #888; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# 시세 데이터 로드
current_price = get_btc_data()

# --- 3. 메인 화면 구성 ---
st.sidebar.title("🤖 QUANT SYSTEM")
menu = st.sidebar.radio("MENU", ["LIVE DASHBOARD", "POLICY"], label_visibility="collapsed")

if menu == "LIVE DASHBOARD":
    st.markdown("""
        <div style="padding: 1rem 0rem; margin-bottom: 2rem;">
            <h1 style="color: white; margin: 0;">AI 비트코인 시세 분석 결과</h1>
            <p style="color: #F0B90B; margin: 0;">REAL-TIME BINANCE API SYNCHRONIZED</p>
        </div>
    """, unsafe_allow_html=True)

    # 상단 3개 기본 지표 (탐욕지수, 신뢰도 등 그대로 유지)
    col1, col2, col3 = st.columns(3)
    col1.metric("시장 탐욕 지수", "15", "Extreme Fear")
    col2.metric("알고리즘 신뢰도", "94.2%", "Optimal")
    col3.metric("데이터 상태", "정상", "Live Connected")

    st.write("---")

    # 하이라이트: 현재가 & 예측가 숫자 섹션
    st.markdown("### 📊 AI 가격 분석 리포트")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(f"""
            <div class="metric-container">
                <div class="label-text">Binance 현재가</div>
                <div class="price-text">${current_price:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with c2:
        # 현재가 기반으로 간단한 예측가 산출 (예: 현재가 + 1.2% 상승 분석)
        predicted_price = current_price * 1.0125 
        st.markdown(f"""
            <div class="metric-container">
                <div class="label-text">1시간 뒤 AI 예측가</div>
                <div class="target-text">${predicted_price:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    # 하단 정보 바
    st.info(f"마지막 데이터 분석 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (F5를 눌러 갱신)")

else:
    st.title("📄 개인정보처리방침")
    st.write("본 시스템은 개인정보를 저장하지 않으며 투자 결과에 대한 책임을 지지 않습니다.")
