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
    .stApp { background-color: #f5f1e8; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Cormorant Garamond', serif !important; color: #1e3a8a !important; font-weight: 600 !important; }

    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #0f172a; border-right: 1px solid #1e3a8a; }
    section[data-testid="stSidebar"] h2 { color: #b8935a !important; font-family: 'Cormorant Garamond', serif !important; letter-spacing: 2px; }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span { color: #f5f1e8 !important; }

    /* KPI Kacheln */
    div[data-testid="stMetric"] { background-color: #ffffff; padding: 20px; border-radius: 12px; border-top: 3px solid #b8935a; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    div[data-testid="stMetricValue"] { font-family: 'Cormorant Garamond', serif; color: #1e3a8a; font-size: 2.8rem; font-weight: 700; }
    div[data-testid="stMetricLabel"] { font-family: 'Inter', sans-serif; color: #6b7280; text-transform: uppercase; letter-spacing: 1.5px; font-size: 0.8rem; font-weight: 600; }

    /* Tabellen */
    div[data-testid="stDataFrame"] { background-color: #ffffff; padding: 15px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e5e7eb; }
    div[data-testid="stDataFrame"] th { background-color: #f5f1e8 !important; color: #1e3a8a !important; font-weight: 600 !important; border-bottom: 2px solid #b8935a !important; }

    /* Buttons (Haupt) */
    .stButton > button { background-color: #1e3a8a; color: #ffffff; border: none; border-radius: 8px; padding: 10px 20px; font-family: 'Inter', sans-serif; font-weight: 500; transition: all 0.3s; }
    .stButton > button:hover { background-color: #b8935a; color: #ffffff; border-color: #b8935a; }
    
    /* Eingabefelder im Login */
    div[data-testid="stTextInput"] input {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 12px 15px !important;
        color: #1e3a8a !important;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #b8935a !important;
        box-shadow: 0 0 0 2px rgba(184, 147, 90, 0.2) !important;
    }

    /* Tabs (für Login/Registrieren) */
    button[data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #6b7280;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1e3a8a;
        border-bottom-color: #b8935a !important;
    }
    
    hr { border-color: #d1d5db; }
    </style>
""", unsafe_allow_html=True)

# ==================== SUPABASE CLIENT ====================
@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# ==================== AUTHENTIFIZIERUNG ====================
def login():
    # Ein schicker Container für das Login
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        # Das Logo/Den Namen groß und edel darstellen
        st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-bottom: 0;'>Edaris</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.9rem; letter-spacing: 4px; color: #b8935a; text-transform: uppercase; margin-bottom: 40px;'>Intelligence</p>", unsafe_allow_html=True)
        
        # Weiße Karte für das Formular
        st.markdown("""
            <div style="background-color: #ffffff; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border-top: 4px solid #b8935a;">
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Einloggen", "Registrieren"])
        
        with tab1:
            st.markdown("<p style='color: #6b7280; font-size: 0.9rem; margin-bottom: 20px;'>Willkommen zurück. Bitte logge dich ein.</p>", unsafe_allow_html=True)
            email = st.text_input("E-Mail", key="login_email", placeholder="deine@email.de")
            password = st.text_input("Passwort", type="password", key="login_password", placeholder="••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Einloggen", use_container_width=True):
                try:
                    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = response.user
                    st.rerun()
                except Exception as e:
                    st.error(f"Login fehlgeschlagen: {e}")
                    
        with tab2:
            st.markdown("<p style='color: #6b7280; font-size: 0.9rem; margin-bottom: 20px;'>Erstelle ein neues Konto für die Beta.</p>", unsafe_allow_html=True)
            new_email = st.text_input("E-Mail", key="reg_email", placeholder="deine@email.de")
            new_password = st.text_input("Passwort", type="password", key="reg_password", placeholder="Mindestens 6 Zeichen")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Konto erstellen", use_container_width=True):
                try:
                    response = supabase.auth.sign_up({"email": new_email, "password": new_password})
                    st.success("Konto erstellt! Bitte prüfe deine E-Mails oder logge dich direkt ein.")
                except Exception as e:
                    st.error(f"Registrierung fehlgeschlagen: {e}")
                    
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== DATEN LADEN ====================
@st.cache_data(ttl=60)
def load_data():
    try:
        response = supabase.table('live_data').select('data').eq('id', 1).execute()
        if response.data:
            return response.data[0]['data']
        return None
    except Exception as e:
        st.error(f"Fehler beim Laden der Daten: {e}")
        return None

# ==================== HAUPT-APP ====================
def main():
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        login()
        return
    
    # Ab hier ist der Nutzer eingeloggt
    user_email = st.session_state.user.email
    
    # Sidebar
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>Edaris</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.8rem; letter-spacing: 3px; color: #b8935a !important;'>INTELLIGENCE</p>", unsafe_allow_html=True)
        st.markdown("<br><hr style='border-color: #1e3a8a;'><br>", unsafe_allow_html=True)
        
        st.markdown(f"👤 **{user_email}**")
        st.markdown("⭐ Status: **Beta-Tester**")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🔄 Daten aktualisieren", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
            
        if st.button("🚪 Ausloggen", use_container_width=True):
            supabase.auth.sign_out()
            st.session_state.user = None
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
    
    # ==================== CHART ====================
    if history:
        st.markdown("<h3 style='margin-bottom: 20px;'>📈 Performance-Verlauf</h3>", unsafe_allow_html=True)
        
        dates = [t['date'][:10] for t in history]
        values = [10000]
        current_val = 10000
        
        for t in history:
            if t['type'] == 'BUY':
                current_val -= (t['shares'] * t['price'])
            else:
                current_val += (t['shares'] * t['price']) + t.get('profit', 0)
            values.append(current_val)
            
        values[-1] = capital
        dates.append(pd.Timestamp.now().strftime('%Y-%m-%d'))
        
        chart_data = pd.DataFrame({"Datum": dates, "Wert": values})
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=chart_data["Datum"], y=chart_data["Wert"],
            mode='lines',
            line=dict(color='#b8935a', width=3),
            fill='tozeroy',
            fillcolor='rgba(184, 147, 90, 0.1)'
        ))
        
        min_val = min(values) * 0.98
        max_val = max(values) * 1.02
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=False, color='#6b7280', type='category'),
            yaxis=dict(showgrid=True, gridcolor='#e5e7eb', color='#6b7280', range=[min_val, max_val], tickprefix="$"),
            height=350
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
