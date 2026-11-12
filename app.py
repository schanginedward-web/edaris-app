import streamlit as st
import pandas as pd
from supabase import create_client, Client

# ==================== KONFIGURATION ====================
# (Hier die gleichen Supabase-Daten eintragen wie in der main.py)
SUPABASE_URL = "https://amloinitcdockedfmxhu.supabase.co/rest/v1/"
SUPABASE_KEY = "sb_publishable_cYbHqfJ9-CPddBtmzu7vYA_by5W0-Js"

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
