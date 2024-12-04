from flask import Flask, render_template, request
import os
import pandas as pd
import requests
import json
from dotenv import load_dotenv
import streamlit as st

app = Flask(__name__)

# Carregar variáveis do .env
#load_dotenv()
METABASE_URL = st.secrets["METABASE_URL"]
METABASE_USERNAME = st.secrets["METABASE_USERNAME"]
METABASE_PASSWORD = st.secrets["METABASE_PASSWORD"]

# Função para autenticação no Metabase
def autenticar_metabase():
    try:
        url = f"{'METABASE_URL'}/api/session"
        payload = {
            "username": 'METABASE_USERNAME',
            "password": 'METABASE_PASSWORD'
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()["id"]
        else:
            raise Exception(f"Erro na autenticação: {response.status_code}")
    except Exception as e:
        return str(e)

# Carregar dados do Metabase
def carregar_dados_metabase():
    token = autenticar_metabase()
    headers = {"X-Metabase-Session": token}
    url = f"{os.getenv('METABASE_URL')}/api/card/1175/query/json"  # Substitua o ID do card
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
    else:
        raise Exception("Erro ao carregar dados do Metabase")

# Dados de triagem (hardcoded para exemplo)
entradas = {
    "Análise Meli": {
        "perguntas": [
            "O produto está funcional?",
            "Há danos estéticos?"
        ],
        "decisoes": {
            ("sim", "não"): "AT LN",
            ("sim", "sim"): "IN-HOUSE LN",
            ("não", "sim"): "Fábrica de Reparos",
            ("não", "não"): "Qualidade",
        }
    },
    "RunOff": {
        "perguntas": [
            "O produto está dentro da garantia?",
            "Há defeitos funcionais?"
        ],
        "decisoes": {
            ("sim", "não"): "AT Same",
            ("sim", "sim"): "Fábrica de Reparos",
            ("não", "sim"): "Qualidade",
            ("não", "não"): "IN-HOUSE Same",
        }
    }
}

# Função para decidir o destino
def decidir_destino(entrada, respostas):
    dados = entradas.get(entrada)
    if not dados:
        return "Entrada inválida"
    
    respostas_tuple = tuple(respostas)
    return dados["decisoes"].get(respostas_tuple, "Destino não definido")

@app.route("/", methods=["GET", "POST"])
def index():
    destino = None
    if request.method == "POST":
        entrada = request.form.get("entrada")
        respostas = [request.form.get(f"pergunta_{i}") for i in range(len(entradas[entrada]["perguntas"]))]
        destino = decidir_destino(entrada, respostas)
    
    return render_template("index.html", entradas=entradas, destino=destino)

if __name__ == "__main__":
    app.run(debug=True)
