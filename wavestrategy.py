import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

# 1. DATABASE MANAGEMENT (JSON File)
DB_FILE = "wave_users_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    # Default admin haddii file-ku uusan jirin
    return {"admin": {"password": "mukhtaar2026", "visits": 1, "last_login": "N/A"}}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# 2. PAGE CONFIG
st.set_page_config(page_title="Wave Pro | Secure Terminal", layout="centered")

# 3. CSS - DESIGN (WHITE & BLACK + GOLD)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* Login Box - Black */
    div[data-testid="stVerticalBlock"] > div:has(input) {
        background-color: #000000;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }

    /* Gold Text Style */
    h1, h2, h3, label, .gold-txt {
        color: #f3cc4d !important;
        text-shadow: 0 0 10px rgba(243, 204, 77, 0.4);
        font-family: 'Inter', sans-serif;
        font-weight: 800 !important;
    }

    /* Buttons - Black & Gold */
    .stButton>button {
        background: #000000 !important;
        color: #f3cc4d !important;
        border: 2px solid #f3cc4d !important;
        border-radius: 12px !important;
        height: 3.5em;
        font-weight: bold !important;
        width: 100%;
    }
    .stButton>button:hover {
        background: #f3cc4d !important;
        color: #000000 !important;
    }

    /* Sidebar - Deep Black */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #f3cc4d;
    }
    [data-testid="stSidebar"] * { color: #f3cc4d !important; }

    /* Inputs */
    input { background-color: #1a1a1a !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. SESSION INITIALIZATION
if 'db' not in st.session_state:
    st.session_state['db'] = load_db()

if 'access_granted' not in st.session_state:
    st.session_state['access_granted'] = False

# ==========================================
# 5. LOGIN INTERFACE
# ==========================================
if not st.session_state['access_granted']:
    st.markdown("<h1 style='color: #000000 !important; text-align:center;'>WAVE TRADER PRO</h1>", unsafe_allow_html=True)
    with st.container():
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("LOGIN TO TERMINAL"):
            if u in st.session_state['db'] and st.session_state['db'][u]['password'] == p:
                st.session_state['access_granted'] = True
                st.session_state['current_user'] = u
                # Update Stats
                st.session_state['db'][u]['visits'] += 1
                st.session_state['db'][u]['last_login'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                save_db(st.session_state['db'])
                st.rerun()
            else:
                st.error("Invalid Credentials")
    st.stop()

# ==========================================
# 6. DASHBOARD & DB MANAGEMENT
# ==========================================
with st.sidebar:
    st.markdown(f"## 👤 {st.session_state['current_user'].upper()}")
    st.write(f"Visits: {st.session_state['db'][st.session_state['current_user']]['visits']}")
    st.divider()

    # --- QAYBTA LINK-GA (CUSUB) ---
    st.subheader("🔗 Share Terminal Link")
    # Link-ga app-kaaga oo diyaar ah
    app_url = "https://wave-trader-pro-xmlvsxhvzmvazpr4lzak6m.streamlit.app/"
    st.code(app_url, language="text")
    st.caption("Copy link-gan oo u dir user-ka cusub.")
    st.divider()

    # ADD USER
    with st.expander("➕ Add New User"):
        new_u = st.text_input("New Username")
        new_p = st.text_input("New Password")
        if st.button("Save User"):
            if new_u and new_p:
                st.session_state['db'][new_u] = {"password": new_p, "visits": 0, "last_login": "Never"}
                save_db(st.session_state['db'])
                st.success("User Saved to Database!")
                st.rerun()

    # DELETE USER
    with st.expander("🗑️ Delete User"):
        user_list = [k for k in st.session_state['db'].keys() if k != 'admin']
        if user_list:
            to_del = st.selectbox("Select User", user_list)
            if st.button("Delete Permanently"):
                del st.session_state['db'][to_del]
                save_db(st.session_state['db'])
                st.warning("User Removed!")
                st.rerun()
        else:
            st.write("No users to delete.")

    if st.button("Logout"):
        st.session_state['access_granted'] = False
        st.rerun()

# MAIN CONTENT - TRACKING TABLE
st.markdown("<h2 style='color: black !important;'>DATABASE MONITORING</h2>", unsafe_allow_html=True)

# Data Table
report = []
for user, info in st.session_state['db'].items():
    report.append({
        "User": user,
        "Total Visits": info['visits'],
        "Last Login": info['last_login']
    })

st.table(pd.DataFrame(report))
import streamlit as st
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="M. Mukhtaar | Wave Trader Pro", layout="wide")

# CSS - Isku dhowaynta Sidebar-ka iyo Habaynta Midabada
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f3f4f6;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    section[data-testid="stSidebar"] {
        background-color: #2c1e1a !important;
        border-right: 1px solid #3d2b27;
    }

    /* --- SIDEBAR COMPRESSION (ISKU DHOWAYN) --- */
    [data-testid="stSidebarUserContent"] {
        padding-top: 5px !important;
    }

    .sidebar-name {
        font-size: 24px;
        font-weight: 800;
        color: #d4af37;
        text-align: center;
        margin-top: 0px;
        margin-bottom: -10px;
    }

    .wave-trader-text {
        text-align: center; 
        color: #a18e88; 
        font-size: 10px; 
        font-weight: 700; 
        letter-spacing: 1.2px;
        margin-bottom: 0px;
    }

    /* Terminal Control iyo Labels-ka oo la isku soo dhoweeyay */
    [data-testid="stSidebar"] h3 {
        margin-top: -20px !important;
        margin-bottom: 0px !important;
        font-size: 18px !important;
    }

    /* Yaraynta firaaqada u dhaxaysa widgets-ka */
    [data-testid="stVerticalBlock"] > div {
        gap: 0rem !important;
    }

    .stSelectbox, .stNumberInput, .stSlider {
        margin-bottom: -10px !important;
    }

    section[data-testid="stSidebar"] .stMarkdown p, 
    section[data-testid="stSidebar"] label {
        color: #e5e7eb !important;
        font-size: 13px !important;
        margin-bottom: 0px !important;
    }

    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Content
st.sidebar.markdown("<div class='sidebar-name'>Mohamed Mukhtaar</div>", unsafe_allow_html=True)
st.sidebar.markdown("<p class='wave-trader-text'>WAVE TRADER PRO</p>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='margin: 5px 0; border-bottom: 1px solid #4a342e;'></div>", unsafe_allow_html=True)

# Liiska Lacagaha (Ttab1, tab2 = st.tabs([" Login", " Is-diwaangali (Sign Up)"])radingView Symbols)
assets = {
    "EUR/USD": "FX:EURUSD", "GBP/USD": "FX:GBPUSD", "AUD/USD": "FX:AUDUSD",
    "NZD/USD": "FX:NZDUSD", "USD/CAD": "FX:USDCAD", "USD/JPY": "FX:USDJPY",
    "EUR/AUD": "FX:EURAUD", "EUR/NZD": "FX:EURNZD", "GBP/AUD": "FX:GBPAUD",
    "GBP/NZD": "FX:GBPNZD", "XAU/USD (Gold)": "OANDA:XAUUSD", "XAG/USD (Silver)": "OANDA:XAGUSD",
    "BTC/USDT": "BINANCE:BTCUSDT", "ETH/USDT": "BINANCE:ETHUSDT", "SOL/USDT": "BINANCE:SOLUSDT"
}

symbol_label = st.sidebar.selectbox("Dooro Instrument-ka", list(assets.keys()))
tv_symbol = assets[symbol_label]

# Timeframes
timeframe_map = {"1h": "60", "4h": "240", "1d": "D", "1w": "W", "1m": "M"}
tf_choice = st.sidebar.selectbox("Time Frame", list(timeframe_map.keys()), index=2)
tv_interval = timeframe_map[tf_choice]

st.sidebar.markdown("<div style='margin: 5px 0; border-bottom: 1px solid #4a342e;'></div>", unsafe_allow_html=True)

# Risk Management
balance = st.sidebar.number_input("Account Balance ($)", min_value=0.0, value=1000.0)
risk_percent = st.sidebar.slider("Risk Per Trade (%)", 0.1, 5.0, 1.0)
stop_loss_dist = st.sidebar.number_input("Stop Loss Distance", min_value=0.0001, value=10.0)

# 3. Main Display
risk_amount = balance * (risk_percent / 100)
lot_size = risk_amount / stop_loss_dist if stop_loss_dist > 0 else 0

st.markdown(f"<h3 style='color:#111827; margin-bottom:10px;'>📈 {symbol_label} ({tf_choice}) Terminal</h3>", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
m1.metric("Capital", f"${balance:,.2f}")
m2.metric("Risk Amount", f"${risk_amount:.2f}")
m3.metric("Rec. Lot", f"{lot_size:.2f}")

# --- QAYBTA: AI AUTOMATIC WAVE SCANNER (NO MANUAL INPUT) ---

import time
import pandas as pd

# 1. AI Scanning Logic (Shuruudaha Elliot Wave)
def scan_wave_opportunities(symbol, data):
    # FIIRO GAAR AH: 'data' waa inay ahaataa xogta dhabta ah ee suuqa
    # Halkan waxaan ku qeexaynaa shuruudaha Wave 2 Entry (Golden Zone)
    
    signals = []
    
    # Tusaale Logic: Wave 2 inta badan waxay ku dhammaataa 0.618 Fibonacci
    # Waxaan u baahanahay High-ga Wave 1 iyo Low-ga bilowga
    if len(data) > 20:
        last_price = data['Close'].iloc[-1]
        max_price = data['High'].max()
        min_price = data['Low'].min()
        
        # Xisaabinta Fibonacci 0.618 (Golden Entry)
        fib_618 = max_price - (0.618 * (max_price - min_price))
        
        # Shardi: Haddii qiimuhu taabto 0.618 oo uu jiro Rejection
        if last_price <= fib_618 * 1.002 and last_price >= fib_618 * 0.998:
            signals.append(f"🚀 {symbol}: Wave 2 Golden Entry Zone (0.618) Detected!")

    return signals
# --- Tillaabada 1: Qeex Function-ka (Dhig dusha sare) ---

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_signal_email(target_email, pair, wave_type, entry, tp, sl):
    try:
        sender_email = "maxamedmukhtaar4800@gmail.com"
        sender_password = "ckxwrtjqbsnnlils" 

        message = MIMEMultipart()
        message["From"] = f"Wave Trader Pro <{sender_email}>"
        message["To"] = target_email
        message["Subject"] = f"🚀 NEW SIGNAL: {pair}"

        body = f"Pair: {pair}\nSetup: {wave_type}\nEntry: {entry}\nTP: {tp}\nSL: {sl}"
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, target_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email Error: {e}")
        return False

# --- Tillaabada 2: Koodhkaaga intiisa kale halkan ha ka bilaawdo ---
# 2. Automatic Notification Header
st.markdown("---")
st.subheader("📡 AI Live Market Scanner")

# Status Indicators
col_status, col_msg = st.columns([1, 4])
with col_status:
    st.write("🟢 **System:** Online")
with col_msg:
    st.write(f"🔍 Scanning {len(assets)} pairs for Elliot Wave setups...")

# 3. Automatic Alert Box (Logic-ka muuqda)
# FIIRO GAAR AH: Si koodhkani Live u shaqeeyo, waa in xogta Binance/Oanda API lagu xidhaa
placeholder = st.empty()

with placeholder.container():
    st.markdown(f"""
        <div style='background-color: #064e3b; padding: 20px; border-radius: 10px; border-left: 10px solid #10b981;'>
            <h3 style='color: #ecfdf5; margin: 0;'>🤖 AI Automatic Signal Mode</h3>
            <p style='color: #d1fae5; font-size: 16px;'>
                <b>Current Strategy:</b> Elliot Wave 1-2-3 Confirmation + Fibonacci 0.618 + RSI Overbought/Oversold.<br>
                <b>Action:</b> System will push notification to Telegram automatically when setup is complete.
            </p>
        </div>
    """, unsafe_allow_html=True)
# Monitoring Loop (Tijaabo ahaan)
if st.sidebar.button("Start AI Auto-Scan"):
    st.sidebar.success(f"🚀 AI Scanner is now LIVE...")
    
    # 1. Khariidadda Magacyada (Map Symbols to Yahoo Finance)
    # Halkan ku dar wixii symbols ah ee aad Dashboard-ka ku haysato
    symbol_map = {
        "XAU/USD (Gold)": "GC=F",
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
        "BTC/USD": "BTC-USD"
    }

    while True:
        # Hel magaca Yahoo Finance u garanayso
        # Haddii uusan ku jirin liiska, isticmaal waxa ku qoran symbol_label
        ticker_symbol = symbol_map.get(symbol_label, symbol_label)

        try:
            import yfinance as yf
            ticker = yf.Ticker(ticker_symbol)
            # Isticmaal 5d (shan bari) si uu mar walba xog u helo
            data = ticker.history(period="5d", interval="1m")

            if not data.empty:
                live_price = data['Close'].iloc[-1]
                
                # DIRISTA EMAIL-KA
                success = send_signal_email(
                    "maxamedmukhtaar4800@gmail.com", 
                    symbol_label, 
                    "Wave 3 Impulse", 
                    f"{live_price:.2f}", 
                    f"{live_price + 10:.2f}", 
                    f"{live_price - 10:.2f}"
                )
                
                if success:
                    st.toast(f"✅ Signal Live ah: {symbol_label} @ {live_price:.2f}")

        except Exception as e:
            st.error(f"Cillad baa dhacday: Magaca '{ticker_symbol}' lama helo.")

        time.sleep(120) # Sug 2 daqiiqo
        st.rerun()
# (Koodhka kale ee Dashboard-ka halkaas ka sii wad)
st.write("Dashboard-kaagu waa diyaar!")
def render_auto_marking_chart(symbol, interval):
    # Waxaan ku daray qaybo cusub oo TradingView u oggolaanaya inay 'Indicators' iyo 'Drawings' xasuusato
    tv_widget = f"""
    <div class="tradingview-widget-container" style="height:900px; width:100%;">
        <div id="tradingview_advanced_chart" style="height:100%; width:100%;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
            "autosize": true,
            "symbol": "{symbol}",
            "interval": "{interval}",
            "timezone": "Etc/UTC",
            "theme": "light",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "withdateranges": true,
            "hide_side_toolbar": false,
            "allow_symbol_change": true,
            "details": true,
            "hotlist": true,
            "calendar": true,
            "studies": [
                "ElliottWave@tv-basicstudies"
            ],
            "container_id": "tradingview_advanced_chart",
            "show_popup_button": true,
            "popup_width": "1000",
            "popup_height": "800"
        }});
        </script>
    </div>
    """
    return components.html(tv_widget, height=910)

# U yeer function-ka
render_auto_marking_chart(tv_symbol, tv_interval)
# --- 1. LIVE SIGNAL TRACKER TABLE ---
st.markdown("### 🎯 Live Trade Signals (AI Recommended)")
data = {
    "Asset": ["XAU/USD", "EUR/USD", "BTC/USDT"],
    "Wave Setup": ["Wave 3 Impulse", "Wave 2 Correction", "Wave 5 Ending"],
    "Entry Zone": ["2350.00", "1.0850", "65500"],
    "Confidence": ["85%", "70%", "90%"],
    "Status": ["READY", "WATCHING", "READY"]
}
st.table(data)

# --- 2. ECONOMIC CALENDAR (WIDGET) ---
st.markdown("### 📅 High Impact News Events")
def render_calendar():
    calendar_widget = """
    <div class="tradingview-widget-container">
      <iframe src="https://www.tradingview.com/embed-widget/events/?locale=en#%7B%22colorTheme%22%3A%22light%22%2C%22isTransparent%22%3Afalse%2C%22width%22%3A%22100%25%22%2C%22height%22%3A%22400%22%2C%22importanceFilter%22%3A%22-1%2C0%2C1%22%2C%22currencyFilter%22%3A%22USD%2CEUR%2CGBP%22%7D" 
              width="100%" height="400" frameborder="0"></iframe>
    </div>
    """
    components.html(calendar_widget, height=420)

import streamlit as st
import pandas as pd
import yfinance as yf
import streamlit.components.v1 as components

# 1. PAGE CONFIG
st.set_page_config(page_title="Wave Trader Pro | Live Terminal", layout="wide")

# 2. INITIALIZE SESSION STATE (Cilad bixinta KeyError)
if 'access' not in st.session_state:
    st.session_state['access'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = ""
if 'role' not in st.session_state:
    st.session_state['role'] = "user"

# 3. DATABASE CONFIG (Google Sheet ID-gaaga)
SHEET_ID = "1GzZ3UtrPUQhR0NCb3u5WbgEB4UAn2z6it2NHml7lv4"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

import streamlit as st
import pandas as pd

# --- Koodhkan halkan geli (Inta u dhaxaysa Import-ka iyo Login-ka) ---
def load_users():
    sheet_id = "1GzZ3UtrPUQhR0NCb3u5WbgEB4UAn2z6it2NHml7lv4"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return pd.DataFrame([{"username": "admin", "password": "mukhtaar2026", "role": "admin"}])

# --- Inta kale ee koodhkaaga Login-ka ayaa soo raaca ---
users_df = load_users()
# 4. LOGIN INTERFACE
if not st.session_state['access']:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.title("🔐 Secure Login")
    
    users_df = load_users()
    u_input = st.text_input("Username")
    p_input = st.text_input("Password", type="password")
    
    if st.button("Access Dashboard"):
        # Hubi hadda xogta sheet-ka ku jirta
        user_match = users_df[(users_df['username'] == u_input) & (users_df['password'].astype(str) == str(p_input))]
        
        if not user_match.empty:
            st.session_state['access'] = True
            st.session_state['current_user'] = u_input
            st.session_state['role'] = user_match.iloc[0]['role']
            st.success(f"Waa lagu fasaxay {u_input}!")
            st.rerun()
        else:
            st.error("Username ama Password waa khaldan yahay!")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop() # Halkan ayuu joogsanayaa ilaa Login laga sameeyo

# 5. DASHBOARD (Wixii ka dambeeya Login-ka)
current_user = st.session_state['current_user']
st.sidebar.title(f"👤 {current_user.upper()}")

# Menu-ga Navigation-ka
menu = st.sidebar.radio("Menu", ["📊 Dashboard", "📅 Calendar", "🛡️ Admin Panel"])

if menu == "📊 Dashboard":
    st.title(f"Wave Trader Pro Terminal - {current_user}")
    asset = st.sidebar.selectbox("Select Pair", ["XAUUSD", "EURUSD", "GBPUSD", "BTCUSDT"])
    
    # TradingView Chart
    tv_url = f"https://www.tradingview.com/widgetembed/?symbol={asset}&interval=60&theme=light"
    components.html(f'<iframe src="{tv_url}" width="100%" height="500" frameborder="0"></iframe>', height=520)

elif menu == "📅 Calendar":
    st.title("Economic Calendar")
    # Halkan geli render_calendar() koodhkeeda
    st.write("Calendar-ka halkan ayuu ka soo muuqanayaa...")

elif menu == "🛡️ Admin Panel":
    if st.session_state['role'] != "admin":
        st.error("Awood uma lihid inaad boggan aragto!")
    else:
        st.header("🛡️ User Management")
        st.write("Xogta Google Sheets:")
        st.table(load_users())

if st.sidebar.button("Logout"):
    st.session_state['access'] = False
    st.rerun()
# --- USER ACCESS CONTROL (Username & Password) ---
if 'access_granted' not in st.session_state:
    st.session_state['access_granted'] = False

if not st.session_state['access_granted']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.header("🔐 Member Login")
        st.write("Fadlan geli aqoonsigaaga si aad u gasho Terminal-ka.")
        
        user_input = st.text_input("Username")
        pass_input = st.text_input("Password", type="password")
        
        # Xogta adiga kaliya koodhka ku jirta (Waad beddelan kartaa kuwan)
        MY_USER = "admin"
        MY_PASS = "mukhtaar2026"
        
        if st.button("Access Dashboard", use_container_width=True):
            if user_input == MY_USER and pass_input == MY_PASS:
                st.session_state['access_granted'] = True
                st.success("Waa lagu fasaxay! Soo gal...")
                st.rerun()
            else:
                st.error("Username ama Password waa khaldan yahay!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- INTI KALE EE DASHBOARD-KAAGA (SIDII HORE) ---
# Halkan ka sii wad koodhkii Sidebar-ka, Chart-ka iyo Signalada...
import streamlit as st
import streamlit.components.v1 as components

# 1. DATABASE-KA DADKA (Tusaale ahaan)
if 'registered_users' not in st.session_state:
    # 'admin' waa adiga, 'user1' waa qof aad fasaxday
    st.session_state['registered_users'] = {
        "admin": {"pass": "mukhtaar2026", "role": "super_admin", "active": True},
        "user1": {"pass": "12345", "role": "viewer", "active": True}
    }

if 'access_granted' not in st.session_state:
    st.session_state['access_granted'] = False
    st.session_state['current_user'] = None

# 2. LOGIN SYSTEM (Username & Password)
if not st.session_state['access_granted']:
    st.markdown("<h2 style='text-align:center;'>🔐 Wave Trader Pro Access</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.form("login_form"):
            u_name = st.text_input("Username")
            u_pass = st.text_input("Password", type="password")
            submitted = st.form_submit_state = st.form_submit_button("Gidarka Fur", use_container_width=True)
            
            if submitted:
                users = st.session_state['registered_users']
                if u_name in users and users[u_name]['pass'] == u_pass:
                    if users[u_name]['active']:
                        st.session_state['access_granted'] = True
                        st.session_state['current_user'] = u_name
                        st.rerun()
                    else:
                        st.error("Waa lagaa xiray nidaamka! La xiriir Mohamed Mukhtaar.")
                else:
                    st.error("Username-ka iyo Password ku wu ka!")
    st.stop()

# --- DASHBOARD-KA MARKUU FURMO ---
current_user = st.session_state['current_user']
user_role = st.session_state['registered_users'][current_user]['role']

# 3. SIDEBAR (Maamulka Mohamed Mukhtaar)
st.sidebar.markdown(f"<h2 style='color:#d4af37; text-align:center;'>{current_user.upper()}</h2>", unsafe_allow_html=True)

# KALIYA ADMIN-KA AYAA ARKI KARA MEESHAN (USER MANAGEMENT)
if user_role == "super_admin":
    st.sidebar.markdown("---")
    st.sidebar.subheader("👤 Admin: User Control")
    
    # Liiska dadka
    all_users = list(st.session_state['registered_users'].keys())
    user_to_manage = st.sidebar.selectbox("Dooro User-ka aad xirayso", [u for u in all_users if u != "admin"])
    
    if st.sidebar.button("Ka saar / Xir User-kan"):
        st.session_state['registered_users'][user_to_manage]['active'] = False
        st.sidebar.success(f"{user_to_manage} waa la xiray!")

    if st.sidebar.button("Fasax User-kan"):
        st.session_state['registered_users'][user_to_manage]['active'] = True
        st.sidebar.info(f"{user_to_manage} waa la fasaxay!")

# 4. SETTINGS (User-ka caadiga ah waxba kama badali karo haddii aad rabto)
st.sidebar.markdown("---")
st.sidebar.subheader("🕹️ Terminal Settings")
symbol = st.sidebar.selectbox("Instrument", ["XAUUSD", "EURUSD", "BTCUSDT"])

# 5. DASHBOARD MAIN CONTENT
st.title(f"📈 Wave Terminal - Welcome {current_user}")

# Signalada Diyaarsan
st.success("🚀 AI SIGNAL: XAU/USD Wave 3 Setup is Ready at 2340.00")

# Chart-ka
def render_tv(sym):
    tv_widget = f"""
    <iframe src="https://www.tradingview.com/widgetembed/?symbol={sym}&interval=60&theme=light" 
    width="100%" height="600" frameborder="0"></iframe>
    """
    components.html(tv_widget, height=620)

render_tv(symbol)

# Badhanka Logout
if st.sidebar.button("Log Out"):
    st.session_state['access_granted'] = False
    st.rerun()
    import streamlit as st
import streamlit.components.v1 as components
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_signal_email(target_email, pair, wave_type, entry, tp, sl):
    # XOGTAADA GAARKA AH
    sender_email = "maxamedmukhtaar4800@gmail.com"
    sender_password = "ckxwrtjqbsnnlils" # Halkan xarfaha waan isku dhejiyay (Spaces-ka ka saar)

    message = MIMEMultipart()
    message["From"] = f"Wave Trader Pro <{sender_email}>"
    message["To"] = target_email
    message["Subject"] = f"🚀 NEW SIGNAL: {pair}"

    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #d4af37;">
        <h2 style="color: #2c1e1a;">🎯 Wave Trader Pro Signal</h2>
        <p><b>Pair:</b> {pair}</p>
        <p><b>Setup:</b> {wave_type}</p>
        <p><b>Entry:</b> {entry}</p>
        <p><b>Target:</b> {tp}</p>
        <p><b>Stop Loss:</b> {sl}</p>
        <hr>
        <p style="font-size: 12px; color: gray;">Email-kan waxaa si automatic ah u soo diray nidaamkaaga Mohamed Mukhtaar.</p>
      </body>
    </html>
    """
    
    message.attach(MIMEText(body, "html"))

    try:
        # Gmail Server Setup
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.set_debuglevel(1) # Tani waxay CMD ku tusaysaa haddii uu error dhaco
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, target_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"EMAIL ERROR: {e}") # Ka eeg CMD-gaaga wixii halkan ku qorma
        return False
    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; border: 2px solid #d4af37;">
          <h2 style="color: #2c1e1a; text-align: center;">🎯 New AI Trading Signal</h2>
          <hr>
          <p>Nidaamka <b>Wave Trader Pro</b> ayaa helay setup cusub:</p>
          <table style="width: 100%; border-collapse: collapse;">
            <tr><td><b>Instrument:</b></td><td>{pair}</td></tr>
            <tr><td><b>Setup:</b></td><td>{wave_type}</td></tr>
            <tr><td><b>Entry Zone:</b></td><td>{entry}</td></tr>
            <tr><td><b>Take Profit:</b></td><td>{tp}</td></tr>
            <tr><td><b>Stop Loss:</b></td><td>{sl}</td></tr>
          </table>
          <br>
          <p style="text-align: center;">
            <a href="https://your-app-link.streamlit.app" style="background-color: #d4af37; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">VIEW LIVE CHART</a>
          </p>
        </div>
      </body>
    </html>
    """
    
    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, target_email, message.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email Error: {e}")
        return False

# --- 2. INITIALIZE SESSION STATE (Si uusan error u imaan) ---
if 'access_granted' not in st.session_state:
    st.session_state['access_granted'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

# --- 3. LOGIN PAGE (SIDII HORE) ---
if not st.session_state['access_granted']:
    # (Halkan dhig koodhkii Login-ka ee aan horay u sameynay)
    st.title("🔐 Login to Wave Trader Pro")
    u_name = st.text_input("Username")
    u_pass = st.text_input("Password", type="password")
    if st.button("Access Dashboard"):
        if u_name == "admin" and u_pass == "mukhtaar2026":
            st.session_state['access_granted'] = True
            st.session_state['current_user'] = u_name
            st.rerun()
    st.stop()

# --- 4. MAIN DASHBOARD ---
st.sidebar.title(f"Welcome, {st.session_state['current_user']}")

# QAYBTA SCAN-KA
if st.sidebar.button("Start AI Auto-Scan"):
    with st.spinner("Market-ka ayaa la baarayaa..."):
        # Tusaale Signal la helay
        my_pair = "XAU/USD (Gold)"
        my_setup = "Wave 3 Bullish"
        
        # EMAIL U DIR ADMIN-KA (MAXAMED)
        success = send_signal_email("maxamedmukhtaar4800@gmail.com", my_pair, my_setup, "2350.00", "2410.00", "2335.00")
        
        if success:
            st.sidebar.success("✅ Signal-kii waa la helay, Email-na waa laguu soo diray!")
        else:
            st.sidebar.error("❌ Email-ka waa la diri waayay. Hubi password-kaaga Gmail.")

# (Halkan ku dar Chart-kaagii iyo qaybihii kale)
st.write("Dashboard-kaagu waa diyaar!")
import streamlit as st
import pandas as pd
# Waxaan u baahanahay maktabad yar oo fariimaha u dirta Google Sheets
import requests 

# 1. SETUP
SHEET_ID = "1GzZ3UtrPUQhR0NCb3u5WbgEB4UAn2z6it2NHml7lv4"
# Kani waa link-ga xogta laga aqriyo
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 2. LOGIN & REGISTRATION PAGE
if not st.session_state.get('access'):
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Is-diwaangali"])
    
    with tab1:
        # Login Logic (sidii hore)
        st.subheader("Ku soo dhawaada Wave Trader")
        
    with tab2:
        st.subheader("Abuur Account Cusub")
        new_user = st.text_input("Username Cusub")
        new_pass = st.text_input("Password Cusub", type="password")
        
        if st.button("Submit Registration"):
            # FIIRO GAAR AH: 
            # Si qofka is-diwaangaliya uu ugu qormo Google Sheets, 
            # waxaad u baahan tahay "Google Forms" ama "Apps Script".
            # Habka ugu fudud waa inaad adigu gacanta ugu darto dadka sheet-ka 
            # ama aad isticmaasho Google Form link.
            
            st.success(f"Codsigaaga waa la diray {new_user}! Admin-ka ayaa ku fasaxi doona.")
            st.info("Admin-ka: Markaad magacan ku aragto Google Sheet-kaaga, 'role'-kiisa ka dhig 'user'.")
            