import streamlit as st
import pandas as pd
import json
from supabase import create_client, Client

# ==================== KONFIGURATION ====================
SUPABASE_URL = "https://amloinitcdockedfmxhu.supabase.co"
SUPABASE_KEY = "sb_publishable_cYbHqfJ9-CPddBtmzu7vYA_by5W0-Js"

st.set_page_config(page_title="Edaris AI", page_icon="📊", layout="wide")

# ==================== CUSTOM CSS (Premium Look) ====================
st.markdown("""
    <style>
    /* Haupt-Hintergrund und Schriften */
    .stApp { background-color: #f5f1e8; }
    h1, h2, h3 { font-family: 'Cormorant Garamond', serif; color: #1e3a8a !important; }
    
    /* Metriken (Kacheln) */
    div[data-testid="stMetricValue"] { font-family: 'Cormorant Garamond', serif; color: #1e3a8a; font-size: 2.5rem; }
    div[data-testid="stMetricLabel"] { font-family: 'Inter', sans-serif; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Tabellen */
    .stDataFrame { border-radius: 10px; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #1e3a8a; color: white; }
    section[data-testid="stSidebar"] h2 { color: #b8935a !important; }
    </style>
""", unsafe_allow_html=True)

# ==================== LOGIN ====================
def check_password():
    def password_entered():
        if st.session_state["password"] == "edaris2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='text-align: center; margin-top: 100px;'>🔒 Edaris AI Login</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input("Passwort (Beta: edaris2026)", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("<h2 style='text-align: center; margin-top: 100px;'>🔒 Edaris AI Login</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input("Passwort", type="password", on_change=password_entered, key="password")
            st.error("😕 Falsches Passwort")
        return False
    return True

# ==================== DATEN LADEN ====================
@st.cache_data(ttl=60) # Cache für 60 Sekunden (macht die App viel schneller)
def load_data():
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = supabase.table('live_data').select('data').eq('id', 1).execute()
        if response.data:
            return response.data[0]['data']
        return None
    except Exception as e:
        st.error(f"Fehler beim Laden der Daten: {e}")
        return None

# ==================== HAUPT-APP ====================
def main():
    if not check_password():
        return
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2933/2933245.png", width=60) # Platzhalter Logo
        st.markdown("<h2 style='color: #b8935a;'>Edaris Intelligence</h2>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("👤 **Account 1**")
        st.markdown("⭐ **Status:** Beta-Tester")
        st.markdown("---")
        if st.button("🔄 Daten aktualisieren", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
            
    st.title("📊 Dashboard")
    st.markdown("Willkommen zurück. Hier ist der aktuelle Stand deines KI-Portfolios.")
    
    data = load_data()
    if not data:
        st.warning("Noch keine Daten vorhanden. Das System führt gerade seinen ersten Scan durch.")
        return
        
    capital = data.get('capital', 0)
    positions = data.get('positions', {})
    history = data.get('history', [])
    
    # ==================== KPI KACHELN ====================
    col1, col2, col3, col4 = st.columns(4)
    total_profit = capital - 10000
    profit_pct = (total_profit / 10000) * 100
    
    with col1: st.metric("Kapital", f"${capital:,.2f}", f"{total_profit:+,.2f} $")
    with col2: st.metric("Rendite", f"{profit_pct:+.2f} %")
    with col3: st.metric("Offene Pos.", len(positions))
    with col4: st.metric("Trades", len(history))
        
    st.markdown("---")
    
    # ==================== CHART (Kapitalverlauf) ====================
    if history:
        st.subheader("📈 Performance-Verlauf")
        # Wir bauen aus der Historie eine einfache Kurve
        chart_data = pd.DataFrame({"Datum": [t['date'][:10] for t in history], "Wert": range(100, 100 + len(history))})
        st.line_chart(chart_data.set_index("Datum"), color="#1e3a8a")

    st.markdown("---")
    
    # ==================== TABELLEN ====================
    col_left, col_right = st.columns([1.5, 1])
    
    with col_left:
        st.subheader("📈 Offene Positionen")
        if positions:
            pos_data = []
            for sym, pos in positions.items():
                pos_data.append({
                    "Aktie": sym, "Stück": pos['shares'], 
                    "Einstieg": f"${pos['entry']:.2f}", 
                    "Stop": f"${pos['stop']:.2f}", 
                    "Ziel": f"${pos['target']:.2f}", 
                    "Score": pos.get('score', 0)
                })
            st.dataframe(pd.DataFrame(pos_data), use_container_width=True, hide_index=True)
        else:
            st.info("Aktuell sind keine Positionen offen.")

    with col_right:
        st.subheader("📜 Letzte Trades")
        if history:
            recent = history[-5:][::-1] # Nur die letzten 5
            hist_data = []
            for t in recent:
                if t['type'] == 'BUY':
                    hist_data.append({"Aktie": t['symbol'], "Aktion": "🟢 KAUF", "Preis": f"${t['price']:.2f}"})
                else:
                    profit = t.get('profit', 0)
                    emoji = "🟢" if profit > 0 else "🔴"
                    hist_data.append({"Aktie": t['symbol'], "Aktion": f"{emoji} VK", "Preis": f"${t['price']:.2f}"})
            st.dataframe(pd.DataFrame(hist_data), use_container_width=True, hide_index=True)
        else:
            st.info("Noch keine Trades.")

if __name__ == "__main__":
    main()
