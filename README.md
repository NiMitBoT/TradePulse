# 🌐 TradePulse-Analytics
Welcome to TradePulse v1.0. This started as a "hope this works" prototype in my local terminal and has officially evolved into a full-stack monster that lives on the cloud.



### 🧠 The Brain (Machine Learning)
Most people look at a chart and guess. I built a Random Forest Regressor that actually does the math. It analyzes real-time technical indicators like RSI and Bollinger Bands to predict where the price is heading next. It isn't a magic crystal ball, but it’s a lot smarter than flipping a coin.

### 🛰️ The Heartbeat (Real-Time Data)
We are pulling live 1-minute ticks from the YFinance engine. The terminal pulses every 10 seconds to keep the data fresh. Whether you are tracking the Nifty 50 in India or the Nikkei 225 in Japan, the data is live, localized, and formatted in the correct currency. No more converting USD to INR in your head while the market is moving.

### ☁️ The Memory (Supabase Cloud)
A real project needs a real database. I’ve integrated a Supabase PostgreSQL backend to handle global user feedback and persistence. Every star rating and review you see in the sidebar is being synced across the world in real-time. It’s the difference between a static website and a living application.

### 🛠️ The Gear (Tech Stack)
1. Python 3.12 for the heavy lifting.
2. Scikit-Learn for the neural decision making.
3. Streamlit for the high-octane UI.
4. Pandas-TA for the deep technical math.
5. Plotly for the high-precision charts that actually let you zoom in.

### 🗺️ Global Reach
TradePulse currently supports seven major territories including India, USA, Japan, UK, Australia, Russia, and China. When you switch countries, everything follows you: the flags, the currency symbols, the regional news, and even the local time in a strict 24-hour format.

### 🚀 Deployment & Security
The app is built to be "future-proof." We use fragmented UI logic to ensure only the sensitive data refreshes, which keeps things fast on mobile. Also, if you’re looking for the API keys, they aren't here. They are locked away in the Streamlit Cloud secrets vault because security matters as much as the code itself.

### 👤 The Developer
Built with a lot of coffee and late-night debugging by NiMitBoT (Nimit Uppal). Final year B.Tech student at Chandigarh University. 

Feel free to check out the live sync or connect with me on LinkedIn if you want to talk about quant trading or why Python indentation is a struggle.

**[🔗 Connect on LinkedIn](https://www.linkedin.com/in/nimit-uppal-07b2a624a/)**
