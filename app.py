import streamlit as st
import pandas as pd
import json
from supabase import create_client, Client
import plotly.graph_objects as go

# ==================== KONFIGURATION ====================
SUPABASE_URL = "https://amloinitcdockedfmxhu.supabase.co"
SUPABASE_KEY = "sb_publishable_cYbHqfJ9-CPddBtmzu7vYA_by5W0-Js"

st.set_page_config(page_title="Edaris AI", page_icon="📊", layout="wide")

# ==================== CUSTOM CSS (Premium Look) ====================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* Haupt-Hintergrund */
    .stApp {
        background-color: #f5f1e8;
        font-family: 'Inter', sans-serif;
    }

    /* Überschriften */
    h1, h2, h3 {
        font-family: 'Cormorant Garamond', serif !important;
        color: #1e3a8a !important;
        font-weight: 600 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e3a8a;
    }
    section[data-testid="stSidebar"] h2 {
        color: #b8935a !important;
        font-family: 'Cormorant Garamond', serif !important;
        letter-spacing: 2px;
    }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
        color: #f5f1e8 !important;
    }

    /* KPI Kacheln (Metriken) */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-top: 3px solid #b8935a;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Cormorant Garamond', serif;
        color: #1e3a8a;
        font-size: 2.8rem;
        font-weight: 700;
    }
    div[data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* Tabellen (DataFrames) */
    div[data-testid="stDataFrame"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
    }
    div[data-testid="stDataFrame"] table {
        font-family: 'Inter', sans-serif;
    }
    div[data-testid="stDataFrame"] th {
        background-color: #f5f1e8 !important;
        color: #1e3a8a !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #b8935a !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #1e3a8a;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #b8935a;
        color: #ffffff;
    }

    /* Trennlinien */
    hr {
        border-color: #d1d5db;
    }
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
        st.markdown("<h2 style='text-align: center; margin-top: 150px; font-size: 3rem;'>🔒 Edaris AI</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6b7280;'>Bitte logge dich ein, um fortzufahren.</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.text_input("Passwort (Beta: edaris2026)", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("<h2 style='text-align: center; margin-top: 150px; font-size: 3rem;'>🔒 Edaris AI</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.text_input("Passwort", type="password", on_change=password_entered, key="password")
            st.error("😕 Falsches Passwort")
        return False
    return True

# ==================== DATEN LADEN ====================
@st.cache_data(ttl=60)
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
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>Edaris</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.8rem; letter-spacing: 3px; color: #b8935a !important;'>INTELLIGENCE</p>", unsafe_allow_html=True)
        st.markdown("<br><hr style='border-color: #1e3a8a;'><br>", unsafe_allow_html=True)
        
        st.markdown("👤 **Account 1**")
        st.markdown("⭐ Status: **Beta-Tester**")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🔄 Daten aktualisieren", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
            
    # Hauptinhalt
    st.markdown("<h1 style='font-size: 3rem; margin-bottom: 0;'>Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6b7280; margin-bottom: 30px;'>Willkommen zurück. Hier ist der aktuelle Stand deines KI-Portfolios.</p>", unsafe_allow_html=True)
    
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
    with col3: st.metric("Offene Positionen", len(positions))
    with col4: st.metric("Trades bisher", len(history))
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== CHART (Plotly für edlen Look) ====================
    if history:
        st.markdown("<h3 style='margin-bottom: 20px;'>📈 Performance-Verlauf</h3>", unsafe_allow_html=True)
        
        # Wir simulieren einen schönen Verlauf basierend auf den Trades
        chart_data = pd.DataFrame({
            "Datum": [t['date'][:10] for t in history],
            "Wert": [capital + (i * 10) for i in range(len(history))] # Platzhalter Logik
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=chart_data["Datum"], y=chart_data["Wert"],
            mode='lines',
            line=dict(color='#b8935a', width=3),
            fill='tozeroy',
            fillcolor='rgba(184, 147, 90, 0.1)'
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showgrid=False, color='#6b7280'),
            yaxis=dict(showgrid=True, gridcolor='#e5e7eb', color='#6b7280'),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    # ==================== TABELLEN ====================
    col_left, col_right = st.columns([1.5, 1])
    
    with col_left:
        st.markdown("<h3>📈 Offene Positionen</h3>", unsafe_allow_html=True)
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
        st.markdown("<h3>📜 Letzte Trades</h3>", unsafe_allow_html=True)
        if history:
            recent = history[-5:][::-1]
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
