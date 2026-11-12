import streamlit as st
import pandas as pd
from supabase import create_client, Client

# ==================== KONFIGURATION ====================
SUPABASE_URL = "https://amloinitcdockedfmxhu.supabase.co/rest/v1/"
SUPABASE_KEY = "sb_publishable_cYbHqfJ9-CPddBtmzu7vYA_by5W0-Js"

st.set_page_config(page_title="Edaris AI", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f5f1e8; }
    h1, h2, h3 { font-family: 'Cormorant Garamond', serif; color: #1e3a8a !important; }
    div[data-testid="stMetricValue"] { font-family: 'Cormorant Garamond', serif; color: #1e3a8a; font-size: 2.5rem; }
    </style>
""", unsafe_allow_html=True)

def check_password():
    def password_entered():
        if st.session_state["password"] == "edaris2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    if "password_correct" not in st.session_state:
        st.text_input("Passwort (Beta: edaris2026)", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Passwort", type="password", on_change=password_entered, key="password")
        st.error("😕 Falsches Passwort")
        return False
    return True

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

def main():
    if not check_password():
        return
        
    st.title("📊 Edaris AI — Dashboard")
    st.markdown("Willkommen bei deinem persönlichen KI-Trading-Assistenten.")
    
    data = load_data()
    if not data:
        st.warning("Noch keine Daten vorhanden. Das System führt gerade seinen ersten Scan durch.")
        return
        
    capital = data.get('capital', 0)
    positions = data.get('positions', {})
    history = data.get('history', [])
    
    col1, col2, col3, col4 = st.columns(4)
    total_profit = capital - 10000
    profit_pct = (total_profit / 10000) * 100
    
    with col1: st.metric("Aktuelles Kapital", f"${capital:,.2f}", f"{total_profit:+,.2f} $")
    with col2: st.metric("Rendite", f"{profit_pct:+.2f} %")
    with col3: st.metric("Offene Positionen", len(positions))
    with col4: st.metric("Trades bisher", len(history))
        
    st.markdown("---")
    st.subheader("📈 Offene Positionen")
    
    if positions:
        pos_data = []
        for sym, pos in positions.items():
            pos_data.append({
                "Aktie": sym, "Stück": pos['shares'], 
                "Einstieg ($)": f"{pos['entry']:.2f}", 
                "Stop-Loss ($)": f"{pos['stop']:.2f}", 
                "Ziel ($)": f"{pos['target']:.2f}", 
                "Score": pos.get('score', 0)
            })
        st.dataframe(pd.DataFrame(pos_data), use_container_width=True, hide_index=True)
    else:
        st.info("Aktuell sind keine Positionen offen.")

    st.markdown("---")
    st.subheader("📜 Letzte Trades")
    
    if history:
        recent = history[-10:][::-1]
        hist_data = []
        for t in recent:
            if t['type'] == 'BUY':
                hist_data.append({"Datum": t['date'][:10], "Aktion": "🟢 KAUF", "Aktie": t['symbol'], "Preis ($)": f"{t['price']:.2f}", "Gewinn ($)": "-"})
            else:
                profit = t.get('profit', 0)
                emoji = "🟢" if profit > 0 else "🔴"
                hist_data.append({"Datum": t['date'][:10], "Aktion": f"{emoji} VERKAUF", "Aktie": t['symbol'], "Preis ($)": f"{t['price']:.2f}", "Gewinn ($)": f"{profit:+.2f}"})
        st.dataframe(pd.DataFrame(hist_data), use_container_width=True, hide_index=True)
    else:
        st.info("Noch keine Trades in der Historie.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Daten aktualisieren"):
        st.rerun()

if __name__ == "__main__":
    main()
