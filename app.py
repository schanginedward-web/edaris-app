import streamlit as st
import pandas as pd
import json
from supabase import create_client, Client
import plotly.graph_objects as go

# ==================== KONFIGURATION ====================
SUPABASE_URL = "https://amloinitcdockedfmxhu.supabase.co"
SUPABASE_KEY = "sb_publishable_cYbHqfJ9-CPddBtmzu7vYA_by5W0-Js"

st.set_page_config(page_title="Edaris AI", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color: #f5f1e8; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Cormorant Garamond', serif !important; color: #1e3a8a !important; font-weight: 600 !important; }
    html, body, [class*="css"] { font-weight: 500 !important; }

    section[data-testid="stSidebar"] { background-color: #0f172a; border-right: 1px solid #1e3a8a; }
    section[data-testid="stSidebar"] h2 { color: #b8935a !important; font-family: 'Cormorant Garamond', serif !important; letter-spacing: 2px; }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span { color: #f5f1e8 !important; font-weight: 500; }

    div[data-testid="stMetric"] { background-color: #ffffff; padding: 20px; border-radius: 12px; border-top: 3px solid #b8935a; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    div[data-testid="stMetricValue"] { font-family: 'Cormorant Garamond', serif; color: #1e3a8a; font-size: 2.8rem; font-weight: 700; }
    div[data-testid="stMetricLabel"] { font-family: 'Inter', sans-serif; color: #4b5563; text-transform: uppercase; letter-spacing: 1.5px; font-size: 0.85rem; font-weight: 700; }

    div[data-testid="stDataFrame"] { background-color: #ffffff; padding: 15px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e5e7eb; }
    div[data-testid="stDataFrame"] th { background-color: #f5f1e8 !important; color: #1e3a8a !important; font-weight: 700 !important; border-bottom: 2px solid #b8935a !important; }

    .stButton > button { background-color: #1e3a8a; color: #ffffff; border: none; border-radius: 8px; padding: 10px 20px; font-family: 'Inter', sans-serif; font-weight: 600; transition: all 0.3s; letter-spacing: 0.5px; }
    .stButton > button:hover { background-color: #b8935a; color: #ffffff; border-color: #b8935a; }
    
    div[data-testid="stTextInput"] input { background-color: #ffffff !important; border: 1px solid #d1d5db !important; border-radius: 8px !important; padding: 12px 15px !important; color: #1e3a8a !important; font-weight: 500 !important; box-shadow: inset 0 1px 2px rgba(0,0,0,0.05); }
    div[data-testid="stTextInput"] input:focus { border-color: #b8935a !important; box-shadow: 0 0 0 2px rgba(184, 147, 90, 0.2) !important; }
    div[data-testid="stTextInput"] label { color: #4b5563 !important; font-weight: 600 !important; font-size: 0.9rem !important; }

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
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-bottom: 0; color: #1e3a8a;'>Edaris</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.9rem; letter-spacing: 4px; color: #b8935a; text-transform: uppercase; margin-bottom: 30px; font-weight: 600;'>Intelligence</p>", unsafe_allow_html=True)
        
        if "auth_view" not in st.session_state:
            st.session_state.auth_view = "login"
            
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Einloggen", key="btn_tab_login", use_container_width=True, type="primary" if st.session_state.auth_view == "login" else "secondary"):
                st.session_state.auth_view = "login"
                st.rerun()
        with c2:
            if st.button("Registrieren", key="btn_tab_register", use_container_width=True, type="primary" if st.session_state.auth_view == "register" else "secondary"):
                st.session_state.auth_view = "register"
                st.rerun()
                
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.auth_view == "login":
            st.markdown("<p style='color: #4b5563; font-size: 0.95rem; font-weight: 500;'>Willkommen zurück. Bitte logge dich ein.</p>", unsafe_allow_html=True)
            email = st.text_input("E-Mail", key="login_email", placeholder="deine@email.de")
            password = st.text_input("Passwort", type="password", key="login_password", placeholder="••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Jetzt einloggen", key="btn_submit_login", use_container_width=True, type="primary"):
                try:
                    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = response.user
                    st.rerun()
                except Exception as e:
                    st.error(f"Login fehlgeschlagen: {e}")
        else:
            st.markdown("<p style='color: #4b5563; font-size: 0.95rem; font-weight: 500;'>Erstelle ein neues Konto für die Beta.</p>", unsafe_allow_html=True)
            new_email = st.text_input("E-Mail", key="reg_email", placeholder="deine@email.de")
            new_password = st.text_input("Passwort", type="password", key="reg_password", placeholder="Mindestens 6 Zeichen")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Jetzt registrieren", key="btn_submit_register", use_container_width=True, type="primary"):
                try:
                    response = supabase.auth.sign_up({"email": new_email, "password": new_password})
                    st.success("Konto erstellt! Bitte prüfe deine E-Mails oder logge dich direkt ein.")
                except Exception as e:
                    st.error(f"Registrierung fehlgeschlagen: {e}")

# ==================== DATEN LADEN (OHNE CACHE!) ====================
def load_data():
    try:
        # Wir holen uns die neuesten Daten direkt aus der Datenbank
        response = supabase.table('live_data').select('*').eq('id', 1).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Fehler beim Laden der Daten: {e}")
        return None

# ==================== APP-ANSICHTEN ====================
def show_dashboard(data):
    # HIER IST DER DEBUG-TEXT
    st.info(f"DEBUG: Die App empfängt vom Server ein Kapital von ${data.get('capital', 0):.2f}")

    capital = data.get('capital', 0)
    positions = data.get('positions', {})
    history = data.get('history', [])
    
    col1, col2, col3, col4 = st.columns(4)
    total_profit = capital - 10000
    profit_pct = (total_profit / 10000) * 100
    
    with col1: st.metric("Kapital", f"${capital:,.2f}", f"{total_profit:+,.2f} $")
    with col2: st.metric("Rendite", f"{profit_pct:+.2f} %")
    with col3: st.metric("Offene Positionen", len(positions))
    with col4: st.metric("Trades bisher", len(history))
        
    st.markdown("<br>", unsafe_allow_html=True)
    
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
            xaxis=dict(showgrid=False, color='#4b5563', type='category', tickfont=dict(weight='bold')),
            yaxis=dict(showgrid=True, gridcolor='#e5e7eb', color='#4b5563', range=[min_val, max_val], tickprefix="$", tickfont=dict(weight='bold')),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
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
                    "Score": round(pos.get('score', 0), 1)
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

def show_scanner(data):
    scanner_results = data.get('scanner_data', [])
    
    st.markdown("<h1 style='font-size: 3rem; margin-bottom: 0;'>Aktien-Scanner</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #4b5563; margin-bottom: 30px; font-size: 1.1rem;'>Hier siehst du die aktuell stärksten Aktien aus dem letzten Scan.</p>", unsafe_allow_html=True)
    
    if not scanner_results:
        st.warning("Noch keine Scanner-Daten vorhanden. Bitte warte auf den nächsten Scan.")
        return

    search_query = st.text_input("🔍 Aktie suchen (z.B. NVDA, AAPL, TSLA)", "")
    
    df_data = []
    for r in scanner_results:
        if search_query.upper() in r['symbol'].upper():
            df_data.append({
                "Aktie": r['symbol'],
                "Preis": f"${r['price']:.2f}",
                "Score": round(r['score'], 1),
                "RSI": round(r.get('rsi', 0), 1),
                "5T Trend": f"{r.get('chg5', 0):+.2f}%"
            })
            
    if df_data:
        st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True)
    else:
        st.info("Keine Aktie gefunden, die deiner Suche entspricht.")

# ==================== HAUPT-APP ====================
def main():
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        login()
        return
    
    user_email = st.session_state.user.email
    
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>Edaris</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.8rem; letter-spacing: 3px; color: #b8935a !important;'>INTELLIGENCE</p>", unsafe_allow_html=True)
        st.markdown("<br><hr style='border-color: #1e3a8a;'><br>", unsafe_allow_html=True)
        
        if "page" not in st.session_state:
            st.session_state.page = "Dashboard"
            
        if st.button("📊 Dashboard", use_container_width=True, type="primary" if st.session_state.page == "Dashboard" else "secondary"):
            st.session_state.page = "Dashboard"
            st.rerun()
        if st.button("🔍 Aktien-Scanner", use_container_width=True, type="primary" if st.session_state.page == "Scanner" else "secondary"):
            st.session_state.page = "Scanner"
            st.rerun()
            
        st.markdown("<br><br><hr style='border-color: #1e3a8a;'><br>", unsafe_allow_html=True)
        
        st.markdown(f"👤 **{user_email}**")
        st.markdown("⭐ Status: **Beta-Tester**")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Daten aktualisieren", use_container_width=True, key="btn_refresh"):
            st.rerun()
            
        if st.button("🚪 Ausloggen", use_container_width=True, key="btn_logout"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()
            
    data = load_data()
    if not data:
        st.warning("Noch keine Daten vorhanden. Das System führt gerade seinen ersten Scan durch.")
        return
        
    if st.session_state.page == "Dashboard":
        st.markdown("<h1 style='font-size: 3rem; margin-bottom: 0;'>Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #4b5563; margin-bottom: 30px; font-size: 1.1rem;'>Willkommen zurück. Hier ist der aktuelle Stand deines KI-Portfolios.</p>", unsafe_allow_html=True)
        show_dashboard(data)
        
    elif st.session_state.page == "Scanner":
        show_scanner(data)

if __name__ == "__main__":
    main()
