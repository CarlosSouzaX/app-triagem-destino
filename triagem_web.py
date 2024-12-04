import streamlit as st
import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Acessar as variáveis
METABASE_URL = os.getenv("METABASE_URL")
METABASE_USERNAME = os.getenv("METABASE_USERNAME")
METABASE_PASSWORD = os.getenv("METABASE_PASSWORD")

# Autenticação no Metabase
def autenticar_metabase():
    url = f"{METABASE_URL}/api/session"
    payload = {
        "username": METABASE_USERNAME,
        "password": METABASE_PASSWORD
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        raise Exception("Erro na autenticação com o Metabase")

# Consulta ao Metabase
def consultar_metabase(card_id):
    token = autenticar_metabase()
    headers = {"X-Metabase-Session": token}
    url = f"{METABASE_URL}/api/card/{card_id}/query/json"
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        raise Exception("Erro ao consultar dados do Metabase")

# Dados de triagem
entradas = {
    "Análise Meli": [
        {"texto": "O produto é da marca Xiaomi ou Apple ou Motorola?", "sim": {"proxima": 1}, "nao": {"proxima": 2}},
        {"texto": "O Mi/FMiP está bloqueado?", "sim": {"saida": "Rejeitar SR"}, "nao": {"proxima": 2}},
        {"texto": "Há danos estéticos?", "sim": {"saida": "Saída 2"}, "nao": {"saida": "Saída 3"}}
    ],
    "RunOff": [
        {"texto": "O produto está na garantia?", "sim": {"proxima": 1}, "nao": {"proxima": 2}},
        {"texto": "O produto está funcional?", "sim": {"saida": "Saída 4"}, "nao": {"proxima": 2}},
        {"texto": "Há defeitos graves?", "sim": {"saida": "Saída 5"}, "nao": {"saida": "Saída 6"}}
    ]
}

# Inicialização do estado
if "entrada_selecionada" not in st.session_state:
    st.session_state["entrada_selecionada"] = None
    st.session_state["progresso"] = 0
    st.session_state["respostas"] = []
    st.session_state["saida"] = None

# Funções auxiliares
def reset_estado():
    st.session_state["progresso"] = 0
    st.session_state["respostas"] = []
    st.session_state["saida"] = None

def exibir_perguntas_respondidas(perguntas, respostas):
    st.write("### Perguntas Respondidas")
    for i, resposta in enumerate(respostas):
        pergunta = perguntas[i]["texto"]
        st.write(f"**{i + 1}. {pergunta}**")
        st.write(f"Resposta: {resposta}")

def processar_resposta(pergunta_atual, resposta):
    destino = pergunta_atual[resposta]
    if "saida" in destino:
        st.session_state["saida"] = destino["saida"]
    elif "proxima" in destino:
        st.session_state["progresso"] = destino["proxima"]
    st.experimental_rerun()

# Interface do Streamlit
st.title("Sistema de Triagem")

# Seleção da entrada
entrada_atual = st.selectbox(
    "Selecione a Entrada",
    options=["Selecione uma entrada"] + list(entradas.keys()),
    on_change=reset_estado
)

# Fluxo principal
if entrada_atual in entradas:
    perguntas = entradas[entrada_atual]
    progresso = st.session_state["progresso"]

    if progresso > 0:
        exibir_perguntas_respondidas(perguntas, st.session_state["respostas"])

    if progresso < len(perguntas) and not st.session_state["saida"]:
        pergunta_atual = perguntas[progresso]
        st.write(f"**Pergunta {progresso + 1}: {pergunta_atual['texto']}**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sim", key=f"sim_{progresso}"):
                st.session_state["respostas"].append("sim")
                processar_resposta(pergunta_atual, "sim")
        with col2:
            if st.button("Não", key=f"nao_{progresso}"):
                st.session_state["respostas"].append("não")
                processar_resposta(pergunta_atual, "nao")

    if st.session_state["saida"]:
        st.success(f"Destino Final: {st.session_state['saida']}")