import streamlit as st
import pandas as pd
from supabase import create_client, Client

# ==================== KONFIGURATION ====================
# (Hier die gleichen Supabase-Daten eintragen wie in der main.py)
SUPABASE_URL = "DEINE_SUPABASE_URL_HIER"
SUPABASE_KEY = "DEIN_SUPABASE_ANON_KEY_HIER"

st.set_page_config(page_title="Edaris AI", page_icon="📊", layout="wide")

# ... (Hier kommt das gleiche CSS und die Login-Logik rein wie vorhin) ...

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

# ... (Der Rest der App bleibt genau gleich, ruft nur load_data() auf) ...
