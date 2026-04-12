def send_telegram_alert(category, message):
    TOKEN = "8780775034:AAFlYB7JMAOQ_G9WU4XwLjZ5nAYpuEm9-vU"
    CHAT_ID = "6694010843"
    
    # Noocyada fariimaha iyo calaamadaha u gaarka ah
    categories = {
        "BLOCK": "🚫 *ACCOUNT BLOCKED*",
        "TRADE": "📈 *NEW TRADE ACTIVE*",
        "REMINDER": "🔔 *DAILY REMINDER*",
        "UNBLOCK": "✅ *ACCOUNT RESTORED*"
    }
    
    header = categories.get(category, "ℹ️ *NOTIFICATION*")
    full_msg = f"{header}\n\n{message}"
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": full_msg, "parse_mode": "Markdown"}
    
    try:
        requests.post(url, json=payload)
        return True
    except:
        return False
import streamlit as st
import json
import os

# 1. SETUP - Ballaca shashadda
st.set_page_config(page_title="MMI TRADER - Ultimate Control", layout="wide")

DB_FILE = "trading_security_db.json"

# --- FUNCTIONS: DATABASE MANAGEMENT ---
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            db = json.load(f)
            # Hubi in qof kasta uu leeyahay keys-ka muhiimka ah (Fix KeyError)
            for user in db:
                db[user].setdefault("errors", 0)
                db[user].setdefault("visits", 0)
                db[user].setdefault("status", "Active")
                db[user].setdefault("message", "")
            return db
    return {
        "admin": {"password": "123", "visits": 0, "errors": 0, "status": "Active", "message": "", "role": "Admin"}
    }

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Initialize
if 'user_db' not in st.session_state:
    st.session_state.user_db = load_db()
if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- SECURITY BOT LOGIC ---
def security_bot(u_name):
    if u_name == "admin": return
    st.session_state.user_db[u_name]["errors"] += 1
    # Haddii 3 jeer password khalad ah la geliyo
    if st.session_state.user_db[u_name]["errors"] >= 3:
        st.session_state.user_db[u_name]["status"] = "Blocked"
        st.session_state.user_db[u_name]["message"] = "🤖 SECURITY BOT: Account-kaaga waa la xannibay sababtoo ah waxaad gelisay 3 jeer password khalad ah."
    save_db(st.session_state.user_db)

# --- LOGIN SCREEN ---
def login():
    st.markdown("""<style>[data-testid="stSidebar"] {display: none;} header {visibility: hidden;}</style>""", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.title("🛡️ MMI TRADER")
        with st.container(border=True):
            u_name = st.text_input("Username")
            u_pass = st.text_input("Password", type="password")
            if st.button("LOG IN", use_container_width=True):
                if u_name in st.session_state.user_db:
                    info = st.session_state.user_db[u_name]
                    if info["status"] == "Blocked":
                        st.error("🚫 Akoonkaaga waa la xannibay.")
                    elif info["password"] == u_pass:
                        st.session_state.auth = True
                        st.session_state.user = u_name
                        info["visits"] += 1
                        info["errors"] = 0 
                        save_db(st.session_state.user_db)
                        st.rerun()
                    else:
                        security_bot(u_name)
                        st.error(f"Password khalad ah! Isku dayga: {st.session_state.user_db[u_name]['errors']}/3")
                else: st.error("Macmiilkan ma jiro!")

if not st.session_state.auth:
    login()
    st.stop()

# --- KA DIB LOGIN-KA ---
current_user = st.session_state.user
user_data = st.session_state.user_db[current_user]

# 🛑 FULL SCREEN MESSAGE BLOCK (Cidna ma dhuumato)
if current_user != "admin" and user_data.get("message"):
    st.markdown("""<style>[data-testid="stSidebar"] {display: none;} header {visibility: hidden;}</style>""", unsafe_allow_html=True)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, msg_col, _ = st.columns([1, 2, 1])
    with msg_col:
        st.error("⚠️ ACCOUNT-KAAGA WAA LA XANNIBAY")
        with st.container(border=True):
            st.write(f"### {user_data['message']}")
            st.write("---")
            st.info("Barnaamijka inta kale waa lagaa xiray ilaa laga xallinayo arrintan kor ku qoran. Fadlan la xiriir Admin-ka.")
    st.stop()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title(f"👤 {current_user.upper()}")
nav_options = ["📈 Dashboard"]
if current_user == "admin":
    nav_options.append("👥 User Management")
choice = st.sidebar.radio("Navigation", nav_options)

# --- USER MANAGEMENT (MEESHA ADD USER-KU JIRO) ---
if choice == "👥 User Management":
    st.title("👥 Control Center & Bot Tracker")
    
    # 1. ADD NEW USER
    with st.expander("➕ Add New Trader", expanded=True):
        c1, c2 = st.columns(2)
        new_u = c1.text_input("Username")
        new_p = c2.text_input("Password")
        if st.button("Abuur Macmiil Cusub"):
            if new_u and new_p:
                st.session_state.user_db[new_u] = {
                    "password": new_p, "visits": 0, "errors": 0, 
                    "status": "Active", "message": "", "role": "Trader"
                }
                save_db(st.session_state.user_db)
                st.success(f"Macmiilka {new_u} waa la keydiyey!")
                st.rerun()

    st.divider()

    # 2. TRACKER & BLOCK SYSTEM
    st.subheader("📊 Tracker & Blocking")
    for u, info in st.session_state.user_db.items():
        if u == "admin": continue
        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 2, 1])
            col1.write(f"**User:** `{u}`")
            col1.write(f"Booqasho: {info['visits']} | Khalad: {info['errors']}")
           # --- BADHANKA SAVE & BLOCK (Line 151) ---
            if col3.button("Dhig Fariinta / Block", key=f"b_{u}"):
                # 1. Keydi xogta system-ka
                st.session_state.user_db[u]["message"] = msg
                st.session_state.user_db[u]["status"] = "Blocked" if msg else "Active"
                save_db(st.session_state.user_db)
                
                # 2. DIR ALERT-GA GAARKA AH EE BLOCK-GA
                if msg:
                    # Halkan waxaan u diraynaa category-ga "BLOCK"
                    send_telegram_alert("BLOCK", f"Macmiilka: `{u}`\nSababta: {msg}\nStatus: Isirka hadda waa la xiray! 🛑")
                    st.success("Alert-gii Block-ga waa baxay!")
                st.rerun() 
           # --- 1. DHAMAADKA USER MANAGEMENT ---
        if col3.button("Dhig Fariinta / Block", key=f"btn_blk_{u}"):
            info["message"] = msg
            info["status"] = "Blocked" if msg else "Active"
            save_db(st.session_state.user_db)
            if msg:
                send_telegram_alert("BLOCK", f"Admin-ku wuxuu xiray `{u}`. Sababta: {msg}")
            st.rerun()

        if col3.button("Reset / Unblock ✅", key=f"btn_res_{u}"):
            info["status"] = "Active"
            info["errors"] = 0
            info["message"] = ""
            save_db(st.session_state.user_db)
            st.rerun()

# --- 2. DASHBOARD SECTION (Line 181/182) ---
# Hubi in 'elif' ay la safan tahay 'if choice == "User Management"'
elif choice == "📈 Dashboard":
    st.title("📈 MMI TRADER Dashboard")
    
    # Haddii Admin-ku yahay, tus meel dhakhso loogu daro user
    if current_user == "admin":
        with st.expander("👤 Quick Add User (Admin Only)"):
            qu, qp = st.columns(2)
            u_q = qu.text_input("Username", key="dash_u_q") # Key gaar ah
            p_q = qp.text_input("Password", key="dash_p_q", type="password")
            if st.button("Save Quick User", key="dash_save_q"):
                if u_q and p_q:
                    st.session_state.user_db[u_q] = {"password": p_q, "visits": 0, "errors": 0, "status": "Active", "message": "", "role": "Trader"}
                    save_db(st.session_state.user_db)
                    st.success("Waa la abuuray!")
                    st.rerun()
# --- DASHBOARD ---
elif choice == "📈 Dashboard":
    st.title(f"MMI TRADER Dashboard")
    
    # Haddii Admin-ku yahay, tus meel dhakhso loogu daro user
    if current_user == "admin":
        with st.expander("👤 Quick Add User (Admin Only)"):
            qu, qp = st.columns(2)
            u_q = qu.text_input("Username", key="qu")
            p_q = qp.text_input("Password", key="qp")
            if st.button("Save Quick User"):
                if u_q and p_q:
                    st.session_state.user_db[u_q] = {"password": p_q, "visits": 0, "errors": 0, "status": "Active", "message": "", "role": "Trader"}
                    save_db(st.session_state.user_db)
                    st.success("Waa la abuuray!")

    
if st.sidebar.button("🚪 Logout"):
    st.session_state.auth = False
    st.rerun()

import streamlit as st
import pandas as pd

# 1. Habaynta Bogga (Layout & Theme)
st.set_page_config(page_title="MMI Trader - Step 1", layout="wide")

# CSS: Koodkan wuxuu qurxinayaa midabada iyo qaabka (Styling)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stMetric { background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #007bff; color: white; border: None; height: 3em; }
    .stButton>button:hover { background-color: #0056b3; border: 1px solid white; }
    </style>
    """, unsafe_allow_html=True)

# 2. Dhinaca (Sidebar - Maamulka)
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #58a6ff;'>💠 MMI TRADER</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Version 1.0 (BETA)</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Badanka ON/OFF (Codsigaagii)
    st.subheader("🕹️ Bot Control")
    bot_status = st.toggle("System Live Connection")
    
    if bot_status:
        st.success("Bot-ku hadda waa SHIDAN YAHAY")
    else:
        st.warning("Bot-ku waa DANSAN YAHAY")
    
    st.markdown("---")
    
    # --- STEP 4: CLEAN RISK MANAGEMENT (Only Balance Input) ---

st.subheader("ACCOUNT BALANCE ($)")

# Qofku kaliya wuxuu galinayaa Balance-ka, wax kale lama tusayo
balance = st.number_input("GALI LACAGTA ACCOUNT KA KUUGU JIRTA", value=1000, step=100)

# Xisaabta gudaha ku jirta (Lama soo bandhigayo)
fixed_risk_percent = 1.0
fixed_sl_pips = 50

# Xisaabinta Lot-ka si uu diyaarsane ugu ahaado Step-ka 6-aad
lot_size = (balance * (fixed_risk_percent / 100)) / (fixed_sl_pips * 10)
final_lot = max(lot_size, 0.01)

# Xasuusin: Halkan wax 'st.info' ama 'st.write' ah kuma lihin 
# si uusan u soo bixin 'Recommended Lot' iyo qoraalka kale.
# 3. Bogga Dhexe (Main Dashboard)
st.markdown("<h2 style='color: white;'> Performance Overview</h2>", unsafe_allow_html=True)

# Qaybta Xisaab-xidhka (Metrics)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Balance", f"${balance:,.2f}", "+2.5%")
col2.metric("Monthly Win Rate", "0%", "N/A")
col3.metric("Total Trades", "0", "New")
col4.metric("Net Profit", "$0.00", "0%")


# 1. Habaynta Bogga
st.set_page_config(page_title="MMI Trader - Watchlist", layout="wide")

# CSS Qurxinta
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    [data-testid="stMetric"] { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stMultiSelect div div div div { background-color: #58a6ff !format; }
    </style>
    """, unsafe_allow_html=True)

# 2. MAAMULKA WATCHLIST-KA (Session State)
# Liiska lacagaha aad sawirka ku soo dirtay oo loo beddelay qaabka yfinance
default_pairs = [
    'EURUSD=X', 'GBPUSD=X', 'NZDUSD=X', 'USDCAD=X', 'USDJPY=X', 
    'USDZAR=X', 'GC=F', 'SI=F', 'GBPAUD=X', 'GBPNZD=X', 
    'EURAUD=X', 'EURNZD=X', 'EURJPY=X', 'AUDCAD=X', 'USDCHF=X'
]

if 'watchlist' not in st.session_state:
    st.session_state.watchlist = default_pairs

# 3. Sidebar (Maamulka Lacagaha)
with st.sidebar:
    st.markdown("<h1 style='color: #58a6ff;'>💠 MMI TRADER</h1>", unsafe_allow_html=True)
    
    st.subheader(" Maamul Watchlist-ka")
    
    # Meel lacag cusub looga daro (Add)
    new_pair = st.text_input("Ku dar Lacagaha:").upper()
    if st.button("Add to List"):
        if new_pair and new_pair not in st.session_state.watchlist:
            st.session_state.watchlist.append(new_pair)
            st.rerun()

    # Meel looga saaro lacagaha (Remove)
    pair_to_remove = st.selectbox("Ka saar Lacag:", ["None"] + st.session_state.watchlist)
    if st.button("Remove Selected"):
        if pair_to_remove != "None":
            st.session_state.watchlist.remove(pair_to_remove)
            st.rerun()

    st.markdown("---")
    
    # Dooro lacagta aad hadda rabto inaad falanqayso (Analyze)
    selected_symbol = st.selectbox("Dooro Lacagta aad eegayso:", st.session_state.watchlist)
    timeframe = st.selectbox("Timeframe:", ["15m", "1h", "4h", "1d"])
    
    st.markdown("---")
    bot_status = st.toggle("System Live Connection", key="bot_switch")
# --- STEP 4: RISK MANAGEMENT ENGINE ---

st.sidebar.markdown("---")
st.sidebar.header("🛡️ Risk Management")

# 1. User Input: Inta lacag ah ee koontada ku jirta
account_balance = st.sidebar.number_input("Account Balance ($):", min_value=10.0, value=1000.0, step=100.0)

# 2. User Input: Inta % ee la halis galinayo (Risk Per Trade)
risk_percent = st.sidebar.slider("Risk Per Trade (%):", 0.5, 5.0, 1.0)

# 3. User Input: Stop Loss (Pips) - Tan waxaa lagu xiri doonaa Step 6
sl_pips = st.sidebar.number_input("Standard SL (Pips):", min_value=5, value=20)

# --- XISAABINTA LOT SIZE ---
def calculate_lot_size(balance, risk_pc, stop_loss):
    # Cadadka lacagta la halis galinayo (Risk Amount)
    risk_amount = balance * (risk_pc / 100)
    
    # Lot Size formula: Risk Amount / (Stop Loss * Pip Value)
    # Pip value caadiyan waa $10 haddii uu yahay Standard Lot
    if stop_loss > 0:
        lots = risk_amount / (stop_loss * 10)
        return round(lots, 2)
    return 0.01

recommended_lots = calculate_lot_size(account_balance, risk_percent, sl_pips)

# Bandhigga Natiijada Risk-ka
st.sidebar.info(f"""
    **Risk Summary:**
    * Amount to Risk: `${account_balance * (risk_percent/100):,.2f}`
    * Recommended Lot: `{recommended_lots}`
""")
# 4. Soo Qabashada Xogta
@st.cache_data(ttl=60)
def load_data(ticker, interval):
    try:
        data = yf.download(ticker, period="5d", interval=interval)
        return data
    except:
        return pd.DataFrame()

df = load_data(selected_symbol, timeframe)

# 5. Muuqaalka Dashboard-ka
st.title(f"Market Analysis: {selected_symbol}")

if not df.empty:
    # Metrics
    c1, c2, c3 = st.columns(3)
    current_price = df['Close'].iloc[-1].item()
    change = current_price - df['Open'].iloc[0].item()
    
    c1.metric("Qiimaha Hadda", f"${current_price:,.4f}", f"{change:,.4f}")
    c2.metric("Xaaladda Bot-ka", "ACTIVE" if bot_status else "STANDBY")
    c3.metric("Pairs in Watchlist", len(st.session_state.watchlist))

    # --- Qaybta Shaxda iyo Signals-ka (Fixed & Dynamic) ---
left_col, right_col = st.columns([3, 1])

# 1. Nadiifinta Symbol-ka si uu u bedbedalo (Fixes chart sync)
tv_sym = selected_symbol.replace("=X", "").replace("-", "")
if len(tv_sym) == 6: 
    tv_sym = f"FX:{tv_sym}"

with left_col:
    # 2. Shaxda TradingView oo si toos ah ula socota Sidebar-ka
    import streamlit.components.v1 as components
    
    # ID-ga halkan (container_id) ayaa ku qasbaya shaxda inay dhalato mar walba
    chart_id = f"tv_chart_{tv_sym.lower()}"
    
    tv_widget_html = f"""
        <div id="{chart_id}" style="height:480px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
          "autosize": true,
          "symbol": "{tv_sym}",
          "interval": "15",
          "timezone": "Etc/UTC",
          "theme": "dark",
          "style": "1",
          "locale": "en",
          "container_id": "{chart_id}"
        }});
        </script>
    """
    # Waxaan u isticmaalay 'height' sax ah si Placeholder-ka uu meesha uga baxo
    components.html(tv_widget_html, height=500)

with right_col:
    st.markdown("<h4 style='color: #58a6ff;'>🚀 New Signals</h4>", unsafe_allow_html=True)
    
    # 3. Bot Analysis oo isna la socda lacagta la doortay (Fixes NameError)
    if 'df' in locals() and not df.empty:
        # Halkan waxaa laga saxay VALUE_ERROR-kii Pandas
        last_price = df['Close'].iloc[-1]
        if hasattr(last_price, 'iloc'): last_price = last_price.iloc[0]
            
        st.markdown(f"""
            <div style='background-color: #1c2128; padding: 15px; border-radius: 10px; border-left: 5px solid #238636;'>
                <b style='color: #238636;'>SIGNAL ACTIVE</b><br>
                <small>Asset: {selected_symbol}</small><br>
                <small>Price: {last_price:,.4f}</small>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Haddii xogta la la'yahay (Fixes OFFLINE error)
        st.warning("Sugaya xogta...")
        import streamlit as st
import yfinance as yf
import pandas as pd

# --- CONFIGURATION ---
FOREX_METALS = ["EURUSD=X", "GBPUSD=X", "XAUUSD=X", "XAGUSD=X"]
CRYPTO = ["BTC-USD", "ETH-USD"]

def get_market_signals(balance):
    all_signals = []
    
    for symbol in (FOREX_METALS + CRYPTO):
        try:
            # 1. ANALYSIS (1D Trend confirmation)
            d_data = yf.download(symbol, period="60d", interval="1d", progress=False)
            ema200_d = d_data['Close'].iloc[-1]
            curr_p = d_data['Close'].iloc[-1]
            trend = "UP" if curr_p > ema200_d else "DOWN"

            # 2. TRADE EXECUTION (1H Timeframe)
            data = yf.download(symbol, period="5d", interval="1h", progress=False)
            data['EMA10'] = data['Close'].ewm(span=10, adjust=False).mean()
            data['ATR'] = (data['High'] - data['Low']).rolling(window=14).mean()
            
            p = float(data['Close'].iloc[-1])
            ema10 = float(data['EMA10'].iloc[-1])
            atr = float(data['ATR'].iloc[-1])

            # ANTI-CHASING LOGIC: 
            # Waxaan oggolnahay kaliya 0.3x ATR masaafo ah. 
            # Haddii qiimuhu ka fogaado EMA10 in ka badan intaas, waa "Too Late".
            max_chase_dist = atr * 0.3 

            sig = None
            # --- BUY LOGIC (Forex, Metals, Crypto) ---
            if p > ema10 and trend == "UP":
                dist = p - ema10
                if dist <= max_chase_dist: # Kaliya haddii uu u dhow yahay Entry-ga
                    sig = {"Type": "BUY 🟢", "Entry": ema10, "SL": p-(atr*2), "TP": p+(atr*4), "Color": "#02c076"}
                else:
                    sig = {"Type": "MISSED ⚠️", "Note": "Qiimuhu waa uu fogaaday, ha ka daba ordin."}

            # --- SELL LOGIC (Forex & Metals Only) ---
            elif p < ema10 and trend == "DOWN" and symbol in FOREX_METALS:
                dist = ema10 - p
                if dist <= max_chase_dist:
                    sig = {"Type": "SELL 🔴", "Entry": ema10, "SL": p+(atr*2), "TP": p-(atr*4), "Color": "#f84960"}
                else:
                    sig = {"Type": "MISSED ⚠️", "Note": "Trend-ka waa la dhaafay, sug retrace."}

            if sig:
                all_signals.append({"Symbol": symbol.replace('=X',''), "Data": sig})
        except: continue
    return all_signals

# --- UI DASHBOARD ---
st.title("🎯 Precision Wave Scanner")
st.write("system-ku wuxuu diidayaa trade kasta oo ka fog aagga saxda ah ee laga galo.")

if st.button("🚀 Scan for Best Entries"):
    results = get_market_signals(1000) # Balance tusaale ah
    if results:
        for r in results:
            s = r['Data']
            if s['Type'] == "MISSED ⚠️":
                st.warning(f"**{r['Symbol']}**: {s['Note']}")
            else:
                st.success(f"**{r['Symbol']} {s['Type']}**")
                st.markdown(f"""
                    <div style="border:1px solid {s['Color']}; padding:10px; border-radius:10px;">
                        Entry: <b>{s['Entry']:.5f}</b> | SL: {s['SL']:.5f} | TP: {s['TP']:.5f}
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Ma jiraan fursado sax ah (Precision) hadda. Sug inta qiimuhu ku soo laabanayo aagga laga galo.")
        

        
        import streamlit as st

# 1. SETUP - Ballaarinta Computer-ka (Wide Mode)
st.set_page_config(
    page_title="MMI TRADER Analytics",
    layout="wide", # Computer-ka wuu ballaarinayaa
    initial_sidebar_state="collapsed"
)

# 2. CSS CUSTOM - Tani waxay u sheegaysaa Mobile-ka inuu yareeyo bannaanka (padding)
st.markdown("""
    <style>
    /* Mobile optimization */
    @media (max-width: 640px) {
        .main .block-container {
            padding-left: 10px;
            padding-right: 10px;
            padding-top: 20px;
        }
        .stMetric {
            background-color: #1e2130;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CIWAANKA
st.title("📊 Xisaab-xidhka Ganacsiga")
st.write("Muuqaalku wuxuu si toos ah isugu hagaajinayaa shashaddaada (PC/Mobile).")

st.divider()

# 4. PERFORMANCE OVERVIEW (Metrics)
# Afar tiir Computer-ka, hal tiir Mobile-ka
m_col1, m_col2, m_col3, m_col4 = st.columns([1, 1, 1, 1])
with m_col1:
    st.metric("Balance", "$1,000", "+2.5%")
with m_col2:
    st.metric("Win Rate", "64%", "Stable")
with m_col3:
    st.metric("Total Trades", "128")
with m_col4:
    st.metric("Net Profit", "$2,450", "+12%")

st.divider()

# 5. INPUTS & PROGRESS (Hadafka)
# Computer-ka waxay noqonayaan laba dhinac, Mobile-kana isku dul
left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    st.subheader("📥 Gali Xogtaada")
    hadafka = st.number_input("Hadafka bisha ($):", value=5000)
    hadda = st.number_input("Faa'iidada hadda ($):", value=2450)
    win_rate_val = st.slider("Win Rate (%):", 0, 100, 64)

with right_col:
    st.subheader("🏆 Horumarkaaga")
    
    # Xisaabinta
    if hadafka > 0:
        percent = (hadda / hadafka) * 100
        progress_val = min(hadda / hadafka, 1.0)
    else:
        percent, progress_val = 0, 0
    
    st.write(f"Waxaad gaartay: **{percent:.1f}%**")
    st.progress(progress_val)
    
    # Warbixin kooban
    st.info(f"Hadafka hadda kuu dhiman: **${max(hadafka - hadda, 0):,.2f}**")

st.divider()

