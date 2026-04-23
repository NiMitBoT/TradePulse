import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import joblib
import plotly.express as px
import plotly.graph_objects as go
import os
import pytz
from datetime import datetime
from supabase import create_client, Client

# --- 1. GLOBAL CONFIG & CLOUD SYNC ---
os.environ["YFINANCE_CACHE_DIR"] = "" 
st.set_page_config(layout="wide", page_title="TradePulse AI", page_icon="🌐")

# Enhanced Market Configuration with Timezone Mapping
MARKETS = {
    "India": {"flag": "🇮🇳", "ticker": "^NSEI", "curr": "₹", "desc": "Nifty 50", "btc": "BTC-INR", "tz": "Asia/Kolkata"},
    "USA": {"flag": "🇺🇸", "ticker": "^GSPC", "curr": "$", "desc": "S&P 500", "btc": "BTC-USD", "tz": "US/Eastern"},
    "Australia": {"flag": "🇦🇺", "ticker": "^AXJO", "curr": "A$", "desc": "ASX 200", "btc": "BTC-AUD", "tz": "Australia/Sydney"},
    "Japan": {"flag": "🇯🇵", "ticker": "^N225", "curr": "¥", "desc": "Nikkei 225", "btc": "BTC-JPY", "tz": "Asia/Tokyo"},
    "UK": {"flag": "🇬🇧", "ticker": "^FTSE", "curr": "£", "desc": "FTSE 100", "btc": "BTC-GBP", "tz": "Europe/London"},
    "Russia": {"flag": "🇷🇺", "ticker": "IMOEX.ME", "curr": "₽", "desc": "MOEX Russia", "btc": "BTC-RUB", "tz": "Europe/Moscow"},
    "China": {"flag": "🇨🇳", "ticker": "000001.SS", "curr": "¥", "desc": "SSE Composite", "btc": "BTC-CNY", "tz": "Asia/Shanghai"}
}

try:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error(f"Database Offline: {e}")
    st.stop()

# --- 2. TERMINAL UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700; color: #4ade80; }
    .insight-box { 
        background-color: #161b22; border-left: 5px solid #4ade80; 
        padding: 15px; border-radius: 8px; margin: 10px 0; font-size: 0.95rem; color: #d1d5db;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #161b22; border-radius: 5px 5px 0 0; padding: 10px 20px; color: #8b949e; 
    }
    .stTabs [aria-selected="true"] { background-color: #1f2937 !important; color: #4ade80 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA & ANALYTICS ENGINES ---
@st.cache_data(ttl=15)
def fetch_live_market(ticker):
    data = yf.download(ticker, period='2d', interval='1m', progress=False)
    if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.droplevel(1)
    if not data.empty: data.index = data.index.tz_convert('Asia/Kolkata')
    return data

@st.cache_resource
def load_tp_model():
    return joblib.load('tradepulse_model.pkl')

model = load_tp_model()

def get_pro_narrative(df, m_conf, type="price"):
    try:
        last = df.iloc[-1]; prev = df.iloc[-2]
        if type == "price":
            bbm = [c for c in df.columns if c.startswith('BBM')][0]
            trend = "Rising" if last['Close'] > prev['Close'] else "Falling"
            pos = "Overbought (High)" if last['Close'] > last[bbm] else "Oversold (Low)"
            return f"🟢 **{m_conf['desc']} Update:** The price is currently **{trend}**. Market position is **{pos}** relative to its 1-hour average."
        elif type == "rsi":
            val = last['RSI_14']
            mood = "Greedy" if val > 70 else "Fearful" if val < 30 else "Balanced"
            return f"🧠 **Momentum Insight:** Market mood is **{mood}** (RSI: {val:.2f}). Speed of change is {'increasing' if val > prev['RSI_14'] else 'slowing down'}."
    except: return "Analyzing patterns..."

# --- 4. SIDEBAR: GLOBAL STATS, TECH STACK & FEEDBACK ---
with st.sidebar:
    st.header("⚙️ System Control")
    
    with st.expander("🛠️ System Architecture", expanded=True):
        st.markdown("""
        ### **Core Engine**
        - **Language:** Python 3.12+
        - **ML Model:** Random Forest Regressor
        - **Database:** Supabase (Cloud Sync)
        
        ### **Data Pipeline**
        - **API:** YFinance (Real-time)
        - **Technicals:** Pandas-TA (RSI, MACD, BB)
        
        ### **UI & Deployment**
        - **Framework:** Streamlit (Fragmented UI)
        - **Visuals:** Plotly High-Precision
        """)
    
    st.divider()

    try:
        res = supabase.table("feedback").select("rating").execute()
        ratings = [r['rating'] for r in res.data]
        avg = round(sum(ratings)/len(ratings), 1) if ratings else 0.0
        st.subheader(f"⭐ Global: {avg} / 5.0")
        st.caption(f"Based on {len(ratings)} verified global users")
        st.progress(avg / 5.0)
    except: 
        st.caption("Syncing global ratings...")

    st.divider()
    st.write("### Review the Terminal")
    stars = st.feedback("stars")
    msg = st.text_area("Review", placeholder="Accuracy feedback...")
    if st.button("Submit"):
        if stars is not None and msg:
            supabase.table("feedback").insert({"rating": stars + 1, "review": msg}).execute()
            st.success("Synced!")
            st.rerun()

    st.divider()
    st.markdown(f"**[🔗 Dev: Nimit Uppal](https://www.linkedin.com/in/nimit-uppal-07b2a624a/)**")
    if st.button("Hard System Sync"): 
        st.rerun()

# --- 5. MAIN INTERFACE ---
t1, t2 = st.columns([2.5, 1])
with t1:
    st.title("TradePulse-Analytics")
with t2:
    country = st.selectbox("Select Territory", list(MARKETS.keys()), index=0)

m_conf = MARKETS[country]

@st.fragment(run_every=10)
def main_terminal_loop():
    # 1. TIMEZONE LOGIC & LIVE PULSE
    target_tz = pytz.timezone(m_conf['tz'])
    local_time = datetime.now(target_tz).strftime('%H:%M:%S')
    
    df = fetch_live_market(m_conf['ticker'])
    display_date = datetime.now(target_tz).strftime('%A, %d %b %Y')
    st.write(f"📡 **Terminal Status:** Live Pulse — {display_date} | {local_time} (Local)")

    if df.empty:
        st.warning(f"Market for {country} is currently closed. Showing session-close data.")
        return

    # 2. INDICATORS
    df.ta.rsi(length=14, append=True); df.ta.macd(append=True); df.ta.bbands(length=5, append=True)
    df.dropna(inplace=True)

    # 3. AI INFERENCE
    feat = df.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume'], errors='ignore')
    latest_feat = feat.iloc[-1:]
    pred = model.predict(latest_feat)[0]; conf = model.predict_proba(latest_feat)[0][1 if pred == 1 else 0]

    # 4. METRIC GRID
    c1, c2, c3 = st.columns(3)
    c1.metric(f"{m_conf['flag']} {country} Price", f"{m_conf['curr']}{df['Close'].iloc[-1]:,.2f}", f"{df['Close'].iloc[-1]-df['Close'].iloc[-2]:+.2f}")
    c2.metric("AI SIGNAL", "BUY" if pred == 1 else "SELL", f"{(conf*100):.1f}% Accuracy")
    with c3:
        st.caption("Intelligence Confidence")
        st.progress(float(conf))

    st.divider()

    # 5. WORKSPACE TABS
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Live Price Action", "🔍 Tech Depth", "🤖 AI Weights", "🗞️ Regional News"])
    
    with tab1:
        fig = px.line(df.tail(60), y='Close', template='plotly_dark', title=f"{m_conf['desc']} 1-Min Ticks")
        fig.update_layout(height=450, margin=dict(l=0, r=0, b=20, t=40), yaxis_autorange=True)
        fig.update_yaxes(tickformat=".2f")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"<div class='insight-box'>{get_pro_narrative(df, m_conf, 'price')}</div>", unsafe_allow_html=True)

    with tab2:
        st.plotly_chart(px.line(df.tail(60), y='RSI_14', template='plotly_dark', title="Momentum Index (RSI)"), use_container_width=True)
        st.markdown(f"<div class='insight-box'>{get_pro_narrative(df, m_conf, 'rsi')}</div>", unsafe_allow_html=True)

    with tab3:
        w_df = pd.DataFrame({'Factor': latest_feat.columns, 'Weight': model.feature_importances_}).sort_values('Weight', ascending=False)
        st.bar_chart(w_df, x='Factor', y='Weight', color="#4ade80", height=300)

    with tab4:
        st.caption(f"Regional Headlines for {country}")
        try:
            news = yf.Search(f"{m_conf['desc']} market news", news_count=4).news
            for n in news:
                st.markdown(f"**{n.get('publisher','Finance')}**: [{n.get('title')}]({n.get('link')})")
        except: 
            st.info("Syncing news data...")
    
    # 6. LOCALIZED BTC MONITOR
    with st.expander(f"🚀 BTC-{country} Live Sync"):
        btc_ticker = m_conf["btc"]
        btc_data = fetch_live_market(btc_ticker)
        if not btc_data.empty:
            st.metric(f"Bitcoin ({m_conf['flag']})", f"{m_conf['curr']}{btc_data['Close'].iloc[-1]:,.2f}")
            st.plotly_chart(px.line(btc_data.tail(40), y='Close', template='plotly_dark', height=200), use_container_width=True)
        
    # 7. ABSOLUTE FOOTER (Localized 24hr Time)
    st.write("---")
    st.markdown(f"TradePulse v6.0 | Built by [NiMitBoT](https://github.com/NiMitBoT/TradePulse) | Local Time: {local_time}")

main_terminal_loop()