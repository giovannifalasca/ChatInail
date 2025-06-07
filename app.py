<<<<<<< HEAD
import streamlit as st
import pandas as pd
from openai import OpenAI
import os

# Inizializza il client OpenAI con la tua chiave dalle secrets
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Carica i dati
df = pd.read_csv("Infortuni.csv")

st.title("Chat INAIL – Interroga i dati sugli infortuni")

user_question = st.text_input("Fai una domanda:", "")

if user_question:
    # Contesto minimo: prime 10 righe
    context = df.head(10).to_string(index=False)

    prompt = f"""
    Questi sono i dati sugli infortuni INAIL:
    {context}

    Rispondi alla domanda basandoti sui dati:
    {user_question}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sei un analista esperto dei dati INAIL."},
            {"role": "user", "content": prompt}
        ]
    )

    st.write("Risposta:")
    st.write(response.choices[0].message.content)
=======
import streamlit as st
import pandas as pd
from openai import OpenAI
import os

# Inizializza il client OpenAI con la tua chiave dalle secrets
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Carica i dati
df = pd.read_csv("Infortuni.csv")

st.title("Chat INAIL – Interroga i dati sugli infortuni")

user_question = st.text_input("Fai una domanda:", "")

if user_question:
    # Contesto minimo: prime 10 righe
    context = df.head(10).to_string(index=False)

    prompt = f"""
    Questi sono i dati sugli infortuni INAIL:
    {context}

    Rispondi alla domanda basandoti sui dati:
    {user_question}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sei un analista esperto dei dati INAIL."},
            {"role": "user", "content": prompt}
        ]
    )

    st.write("Risposta:")
    st.write(response.choices[0].message.content)
>>>>>>> origin/main
