import streamlit as st

# 1. Hubi in bogga uu yahay mid ballaaran (Wide Mode)
# Tani waxay ka caawinaysaa inaysan xogtu isku dhuqmin
st.set_page_config(layout="wide")

with st.sidebar:
    # Qaybta sare oo aad u yar (Logo + Magaca hal xariiq ah)
    st.markdown("""
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: -25px;'>
            <h3 style='color: #58a6ff; margin: 0;'>💠 MMI TRADER</h3>
        </div>
        <hr style='margin: 15px 0;'>
        """, unsafe_allow_html=True)
    
   
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
# 1. SETUP & STARTUP (Xogta mar kasta faylka ha laga soo akhriyo)
if 'user_db' not in st.session_state:
    st.session_state.user_db = load_db()
else:
    # Haddii bogga la refresh-gareeyo, dib u soo aqri faylka si xogtu u noqoto mid joogto ah
    st.session_state.user_db = load_db()

if 'auth' not in st.session_state:
    st.session_state.auth = False

# 2. FUNCTION-KA CUSUB EE USER-KA LAGU DARAYO (Si aysan xogtu waligii u tirmayn)
def add_new_user(username, password):
    """Function-kan wuxuu xogta ku darayaa Session-ka iyo Faylka isku dar"""
    # Ku dar Session-ka (UI ahaan)
    st.session_state.user_db[username] = password
    
    # ISLA MARKIBA KU QOR FAYLKA (Tani waa sirtii Permanency-ga)
    save_db(st.session_state.user_db)
    
    st.success(f"User {username} si joogto ah ayaa loo kaydiyay! ✅")

# 3. TUSAALE: Markaad User cusub dhisayso koodkaaga dhexdiisa
# Halkii aad ku qori lahayd st.session_state.user_db[user] = pass
# Waxaad hadda isticmaalaysaa:
# add_new_user(new_username, new_password)
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
import streamlit as st
import json
import os
import requests
import time
import threading
from datetime import datetime

# 1. SETUP
DB_FILE = "trading_security_db.json"

# --- TELEGRAM FUNCTION ---
def send_telegram_alert(message):
    TOKEN = "8780775034:AAFlYB7JMAOQ_G9WU4XwLjZ5nAYpuEm9-vU"
    CHAT_ID = "6694010843"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}, timeout=10)
    except: pass

# --- DATABASE ---
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {}
    return {"admin": {"password": "123", "status": "Active"}}

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

# --- 🤖 BACKGROUND BOT MONITOR (Kani waa kan kuu maqan!) ---
def background_monitor():
    """Mashiinkan wuxuu shaqaynayaa isaga oo aan kuu baahnayn adiga"""
    while True:
        data = load_db()
        updated = False
        for u, info in data.items():
            if u == "admin": continue
            
            # Haddii qof uu 3 khalad gaaray, laakiin aan weli fariin laga dirin
            if info.get("errors", 0) >= 3 and info.get("blocked_by") != "SECURITY BOT":
                now = datetime.now().strftime("%d/%m/%Y %H:%M")
                info.update({
                    "status": "Blocked",
                    "message": "🤖 Auto-Block: 3 Password Attempts Failed.",
                    "blocked_by": "SECURITY BOT",
                    "date": now
                })
                # Dir fariinta Telegram (Isagaa iskiis u diraya)
                msg = f"⚠️ *AUTO SECURITY ALERT*\n\n👤 *User:* {u}\n🚨 *Action:* Blocked by Bot\n📅 *Time:* {now}"
                send_telegram_alert(msg)
                updated = True
        
        if updated:
            save_db(data)
        
        time.sleep(5) # 5-tii ilbiriqsiba mar ayuu iskiis u baarayaa

# --- BILOW MASHIINKA (Koodka la saxay oo xogta kaydinaya) ---
if "bot_thread" not in st.session_state:
    # 1. Hubi in xogtu ay markasta ka timaado faylka ka hor intaan mashiinku kicin
    st.session_state.user_db = load_db()
    
    # 2. Bilaaw mashiinka background-ka
    thread = threading.Thread(target=background_monitor, daemon=True)
    thread.start()
    
    # 3. Kaydi in mashiinku bilowday
    st.session_state.bot_thread = True
    
    # 4. ISLA MARKIBA KAYDI (Si uusan waligii u dhiman)
    save_db(st.session_state.user_db)
# --- UI START ---
st.set_page_config(page_title="MMI TRADER PRO", layout="wide")
st.title("📊 Security & Tracker Control")

if 'user_db' not in st.session_state:
    st.session_state.user_db = load_db()

# Excel Header
h = st.columns([1.5, 1, 1, 2.5, 1.5, 1.5, 1.5])
headers = ["Username", "Status", "Errors", "Reason", "Bylaw", "Date", "Action"]
for col, text in zip(h, headers):
    col.markdown(f"<div style='background:#1E1E1E;color:#00CCFF;padding:10px;border:1px solid #444;text-align:center;font-weight:bold;'>{text}</div>", unsafe_allow_html=True)

# Loop Users (Muqaalka Dashboard-ka - FIXED)
for u, info in st.session_state.user_db.items():
    if u == "admin": continue
    with st.container():
        r = st.columns([1.5, 1, 1, 2.5, 1.5, 1.5, 1.5])
        r[0].write(f"**{u}**")
        r[1].write("🔴 Blocked" if info.get("status") == "Blocked" else "🟢 Active")
        r[2].write(f"`{info.get('errors', 0)}/3`")
        
        # 1. Halkan waxaan ku daray amarka 'on_change' si Reason-ku u kaydmo isla marka aad qorto
        reason = r[3].text_input(
            "Reason", 
            value=info.get("message", ""), 
            key=f"rs_{u}", 
            label_visibility="collapsed"
        )
        
        # Hubi haddii Reason-ku isbeddelay, isla markiiba kaydi buugga (Permanent)
        if reason != info.get("message", ""):
            info["message"] = reason
            save_db(st.session_state.user_db)

        r[4].write(f"*{info.get('blocked_by', '-')}*")
        r[5].write(f"<small>{info.get('date', '-')}</small>", unsafe_allow_html=True)
        
        if info.get("status") == "Active":
            if r[6].button("🛑 BLOCK", key=f"b_{u}"):
                now = datetime.now().strftime("%d/%m/%Y %H:%M")
                info.update({"status": "Blocked", "message": reason, "blocked_by": "ADMIN", "date": now})
                # 2. Kaydi isbeddelka Block-ga (Permanent)
                save_db(st.session_state.user_db)
                send_telegram_alert(f"🛑 *ADMIN BLOCK*\n👤 *User:* {u}\n📝 *Sabab:* {reason}")
                st.rerun()
        else:
            if r[6].button("✅ RESET", key=f"ok_{u}"):
                info.update({"status": "Active", "errors": 0, "message": "", "blocked_by": "-", "date": "-"})
                # 3. Kaydi isbeddelka Reset-ka (Permanent)
                save_db(st.session_state.user_db)
                st.rerun()
    st.markdown("<hr style='margin:0; border:0.1px solid #333'>", unsafe_allow_html=True)
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

    # --- STEP 4: CLEAN RISK MANAGEMENT (Only Balance Input) ---

import streamlit as st
import json
import os

# --- 1. FUNCTIONS-KA KAYDINTA ---
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# --- 2. FUNCTION-KA AUTOMATIC KAYDINTA AH ---
def auto_save_balance():
    # Marka qofku uu sanduuqa wax ku qoro, halkan ayaa si toos ah u kicinaysa
    new_val = st.session_state.balance_input_key
    st.session_state.balance = new_val
    save_json("account.json", {"balance": new_val})

# --- 3. SETUP-KA XOGTA ---
if "balance" not in st.session_state:
    st.session_state.balance = load_json("account.json").get("balance", 1000.0)

# Default constants (Settings)
fixed_risk_percent = 1.0 
fixed_sl_pips = 30.0

# --- 4. DASHBOARD (Automatic Input) ---
st.subheader("💰 ACCOUNT BALANCE (Auto-Save)")

# Halkan waa sirtu: 'on_change' ayaa shaqada qabanaysa adiga la'aantaa
st.number_input(
    "Gali lacagta (System-ku si automatic ah ayuu u kaydinayaa):",
    value=float(st.session_state.balance),
    step=100.0,
    key="balance_input_key",
    on_change=auto_save_balance  # Markaad beddesho, isagaa ordaya oo kaydinaya
)

# --- 5. XISAABINTA LOT SIZE ---
balance = st.session_state.balance
lot_size = (balance * (fixed_risk_percent / 100)) / (fixed_sl_pips * 10)

st.success(f"Xogta hadda firfircoon: **${balance}**")
st.info(f"Lot Size-ka ku habboon: **{lot_size:.2f}**")
# Xisaabta gudaha ku jirta (Lama soo bandhigayo)
fixed_risk_percent = 1.0
fixed_sl_pips = 50

# Xisaabinta Lot-ka si uu diyaarsane ugu ahaado Step-ka 6-aad
lot_size = (balance * (fixed_risk_percent / 100)) / (fixed_sl_pips * 10)
final_lot = max(lot_size, 0.01)

# Xasuusin: Halkan wax 'st.info' ama 'st.write' ah kuma lihin 
# si uusan u soo bixin 'Recommended Lot' iyo qoraalka kale.
# 3. Bogga Dhexe (Main Dashboard)
# --- 1. SETUP-KA XOGTA (Manual Stats) ---
# Waxaan hubinaynaa in xogtan ay ku jirto Session-ka si aysan u tirmid
if "total_trades" not in st.session_state:
    st.session_state.total_trades = 0
if "win_rate" not in st.session_state:
    st.session_state.win_rate = 0
if "net_profit" not in st.session_state:
    st.session_state.net_profit = 0.0

# --- 2. MEESHA XOGTA LAGU SHUBAYO (Manual Entry Form) ---
with st.expander("🛠️ MAAMUL PERFORMANCE-KA (Manual)"):
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        m_trades = st.number_input("Total Trades", value=st.session_state.total_trades)
    with col_b:
        m_win_rate = st.number_input("Win Rate (%)", value=st.session_state.win_rate)
    with col_c:
        m_profit = st.number_input("Net Profit ($)", value=float(st.session_state.net_profit))
    
    if st.button("Update Dashboard ✅"):
        st.session_state.total_trades = m_trades
        st.session_state.win_rate = m_win_rate
        st.session_state.net_profit = m_profit
        st.success("Dashboard-ka waa la cusboonaysiiyay!")
        st.rerun()

# --- 3. MUUQAALKA DASHBOARD-KA (Performance Overview) ---
st.markdown("<h2 style='color: white;'> Performance Overview</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# 1. Balance (Wuxuu isticmaalayaa kii aan hore u kaydinay)
balance = st.session_state.get('balance', 1000.0)
col1.metric("Balance", f"${balance:,.2f}", "+Manual")

# 2. Monthly Win Rate (Manual)
col2.metric("Monthly Win Rate", f"{st.session_state.win_rate}%", "N/A")

# 3. Total Trades (Manual)
col3.metric("Total Trades", f"{st.session_state.total_trades}", "Updated")

# 4. Net Profit (Manual)
profit_color = "inverse" if st.session_state.net_profit < 0 else "normal"
col4.metric("Net Profit", f"${st.session_state.net_profit:,.2f}", f"{st.session_state.net_profit:,.2f}$", delta_color=profit_color)
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
    'USDZAR=X', 'XAUUSD=F', 'XAGUSD=F', 'GBPAUD=X', 'GBPNZD=X', 
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
    
    import json
import os

# --- 1. FUNCTION-KA AKHRISKA XOGTA ---
def load_json(filename):
    """Xogta ka soo akhri faylka JSON haddii uu jiro"""
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# --- 2. FUNCTION-KA KAYDINTA XOGTA ---
def save_json(filename, data):
    """Xogta ku qor faylka JSON si ay u noqoto Permanent"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
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


import streamlit as st
import pandas as pd

# --- 1. SETUP ---
st.set_page_config(page_title="Realistic Trading Goal", layout="wide")
st.title("Qorshaha kordhinta accoun-kaaga")

# --- 2. GALI XOGTAADA ---
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        username = st.text_input("Magacaaga:", value="ku qor magacaaga")
    with col2:
        balance = st.number_input("Balance-kaaga ($):", value=1000)
    with col3:
        # Waxaan xaddidnay inaanu 10% ka badan bishii (Safety First)
        monthly_pct = st.slider("Hadafka Bisha (%):", 1.0, 100.0, 100.0)

# --- 3. XISAABINTA CAQLIGA AH (LOGIC) ---
# Bishu waa 22 maalmood oo shaqo
total_profit_goal = balance * (monthly_pct / 100)
daily_profit_goal = total_profit_goal / 22

# --- 4. MUUQAALKA "QOFKU UU GASHAN KARO" ---
st.markdown("---")
st.subheader(f"Qorshaha Shaqada: {username}")

# Qaybtan waxaan u sameeyay si qofka maskaxdiisa ay u aqbasho
c1, c2, c3 = st.columns(3)
c1.metric("Hadafka Bishii", f"${total_profit_goal:,.2f}")
c2.metric("Hadafka Maalintii", f"${daily_profit_goal:,.2f}")
c3.metric("Risk-ga Trade-kiiba", "0.5% - 1%")

# --- 5. JADWALKA SHAQADA (THE ACTION PLAN) ---
plan_list = []
temp_bal = balance
for day in range(1, 23):
    temp_bal += daily_profit_goal
    plan_list.append({
        "Maalinta": f"Day {day}",
        "Hadafka Lacageed": f"${daily_profit_goal:,.2f}",
        "Balance-ka la rabo": f"${temp_bal:,.2f}",
        "Talo": "Jooji trading-ka markaad gaarto hadafka maanta."
    })

df = pd.DataFrame(plan_list)
st.table(df)



import streamlit as st
import json
import os
import requests
import time
import threading
from datetime import datetime
import pytz
import pandas as pd

# 1. SETUP & TIMEZONE (Somalia GMT+3)
SOMALIA_TZ = pytz.timezone('Africa/Mogadishu')
SIGNALS_FILE = "signals.json"
CURRENT_MONTH = datetime.now(SOMALIA_TZ).strftime("%B_%Y")
HISTORY_FILE = f"History_{CURRENT_MONTH}.json"

def get_now():
    return datetime.now(SOMALIA_TZ)

def send_telegram_alert(message):
    TOKEN = "8780775034:AAFlYB7JMAOQ_G9WU4XwLjZ5nAYpuEm9-vU"
    CHAT_ID = "6694010843"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def load_data(file):
    if os.path.exists(file):
        try:
            with open(file, "r") as f: return json.load(f)
        except: return {}
    return {}

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# 2. 🤖 MASHIINKA HUBINTA (Checks if Entry, SL, TP & Wave are valid)
def is_signal_valid(sinfo):
    """Wuxuu hubinayaa in dhammaan xogtu ay buuxdo oo aysan marna madnayn"""
    required_keys = ['pair', 'type', 'wave', 'entry', 'sl', 'tp', 'time']
    for key in required_keys:
        if not sinfo.get(key) or str(sinfo.get(key)).strip() == "":
            return False
    return True

def background_worker():
    # Bot-ku wuxuu ahaanayaa mid mar kasta shaqaynaya (Always ON)
    while True:
        try:
            now = datetime.now(SOMALIA_TZ)
            current_minute = now.strftime("%H:%M")
            
            # 1. Si toos ah uga akhriso signals-ka disk-ka (Permanent Storage)
            signals = load_json(SIGNALS_FILE)
            sent_log = load_json(SENT_LOG_FILE)
            
            # Haddii faylku madhan yahay, ka dhig dict (Safety check)
            if not isinstance(sent_log, dict):
                sent_log = {}

            for sid, sinfo in list(signals.items()):
                # Hubi waqtiga iyo inaan horay loo dirin
                if sinfo.get('time') == current_minute and sid not in sent_log:
                    
                    msg = (
                        f"🛰️ *AUTO-SIGNAL EXECUTED*\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"💹 *Pair:* `{sinfo.get('pair')}`\n"
                        f"⚡️ *Action:* `{sinfo.get('type')}`\n"
                        f"💰 *Entry:* `{sinfo.get('entry')}`\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"🕒 *Time:* `{sinfo.get('time')} (EAT)`\n"
                        f"🟢 *Status:* `System Live`"
                    )
                    
                    # 2. U dir fariinta Telegram
                    send_telegram(msg)
                    
                    # 3. XOG KAYDINTA (PERMANENT LOCK): 
                    # Isla markiiba u qor faylka si uusan waligii ugu soo noqon
                    sent_log[sid] = True
                    save_json(SENT_LOG_FILE, sent_log)
                    
        except Exception as e:
            # Anti-Crash: Haddii error dhaco, sug 10 ilbiriqsi
            time.sleep(10)
            continue
            
        # Sug 30 ilbiriqsi ka hor intaadan mar kale hubin
        time.sleep(30)