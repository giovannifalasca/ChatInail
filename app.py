import streamlit as st
import duckdb
from openai import OpenAI
import os
import gdown
import re

# Inizializza il client OpenAI
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Configurazione DuckDB
DB_ID = "1zxdmAM6bP4gNS58yJCCsUMchcBE00NqQ"  # ID del tuo file DuckDB su Google Drive
DB_PATH = "infortuni.duckdb"

@st.cache_resource
def load_db():
    if not os.path.exists(DB_PATH):
        DB_URL = f"https://drive.google.com/uc?export=download&id={DB_ID}"
        gdown.download(DB_URL, DB_PATH, quiet=True)
    return duckdb.connect(DB_PATH)

conn = load_db()

st.title("Chat INAIL – Interroga i dati sugli infortuni")

user_question = st.text_input("Fai una domanda:", "")

if user_question.strip() != "":
    st.write("Domanda ricevuta:", user_question)

    try:
        # Recupera nome tabella e righe di esempio
        tables = conn.execute("SHOW TABLES").df()
        table_name = tables.iloc[0, 0]
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

        response_text = response.choices[0].message.content
        st.subheader("Risposta in linguaggio naturale:")
        st.write(response_text)

        # Prova ad estrarre ed eseguire una query SQL se presente
        if "SELECT" in response_text.upper():
            sql_match = re.search(r"(?i)(SELECT .*?)(?:;|$)", response_text, re.DOTALL)
            if sql_match:
                query = sql_match.group(1).strip()
                st.subheader("Query SQL eseguita:")
                st.code(query, language="sql")
                try:
                    result_df = conn.execute(query).fetchdf()
                    st.subheader("Risultato della query:")
                    st.dataframe(result_df)
                except Exception as e:
                    st.error(f"Errore nell'esecuzione della query: {e}")
    except Exception as e:
        st.error(f"Errore nella chiamata a GPT: {e}")
