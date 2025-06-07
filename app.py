import streamlit as st
import duckdb
from openai import OpenAI
import os
import gdown

# Inizializza il client OpenAI
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Configurazione DuckDB
DB_ID = "1zxdmAM6bP4gNS58yJCCsUMchcBE00NqQ"  # ID del tuo file DuckDB su Google Drive
DB_PATH = "infortuni.duckdb"

@st.cache_resource
def load_db():
    # Scarica il database da Google Drive se non è già presente
    if not os.path.exists(DB_PATH):
        # Crea un link diretto a Google Drive per il file
        DB_URL = f"https://drive.google.com/uc?export=download&id={DB_ID}"
        gdown.download(DB_URL, DB_PATH, quiet=True)
    return duckdb.connect(DB_PATH)

conn = load_db()

st.title("Chat INAIL – Interroga i dati sugli infortuni")

user_question = st.text_input("Fai una domanda:", "")

if user_question:
    # Ottieni la struttura delle tabelle per il contesto
    tables = conn.execute("SHOW TABLES").df()
    table_name = tables.iloc[0, 0]  # Prendi il nome della prima tabella
    
    # Estrai alcune righe di esempio come contesto
    sample_data = conn.execute(f"SELECT * FROM {table_name} LIMIT 10").df()
    
    prompt = f"""
    Questi sono i dati sugli infortuni INAIL (prime 10 righe):
    {sample_data.to_string(index=False)}

    Rispondi alla domanda basandoti sui dati:
    {user_question}
    
    Se la domanda richiede operazioni sui dati, suggerisci anche la query SQL che potrei usare.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[ 
            {"role": "system", "content": f"Sei un analista esperto dei dati INAIL. I dati sono in una tabella DuckDB chiamata '{table_name}'."},
            {"role": "user", "content": prompt}
        ]
    )

    st.write("Risposta:")
    st.write(response.choices[0].message.content)
    
    # Mostra anche i dati di esempio per riferimento
    with st.expander("Vedi dati di esempio"):
        st.dataframe(sample_data)

