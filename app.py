# app.py
import streamlit as st
import pandas as pd
import openai
import os

# Imposta chiave OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Carica dati
df = pd.read_csv("infortuni.csv")

st.title("Chat INAIL – Interroga i dati sugli infortuni")

user_question = st.text_input("Fai una domanda:", "")

if user_question:
    # Prepara contesto
    context = df.head(10).to_string(index=False)

    prompt = f"""
    Questi sono i dati sugli infortuni INAIL:
    {context}

    Rispondi alla domanda basandoti sui dati:
    {user_question}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sei un esperto di sicurezza sul lavoro e analisi dei dati INAIL."},
            {"role": "user", "content": prompt}
        ]
    )

    st.write("Risposta:")
    st.write(response['choices'][0]['message']['content'])
