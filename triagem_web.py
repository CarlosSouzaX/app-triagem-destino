import streamlit as st
import pandas as pd
import gspread
import json
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError

# Escopo para acessar o Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def read_google_sheets(SPREADSHEET_ID, RANGE_NAME, CELL_RANGE):
    try:
        # Carrega as credenciais do Secrets Manager
        google_credentials = st.secrets["google_credentials"]
        creds = Credentials.from_service_account_info(google_credentials)

        # Autenticação com o gspread
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(SPREADSHEET_ID).worksheet(RANGE_NAME)
        tabela = sheet.get(CELL_RANGE)

        # Inicializando as listas
        device = []
        modelo = []

        # Percorre as linhas da tabela e adiciona os valores nas respectivas listas
        for row in tabela:
            device.append(row[0])
            modelo.append(row[1])

        # Cria uma lista de tuplas usando zip
        lista = list(zip(device, modelo))

        # Definindo os nomes das colunas
        colunas = ['Device', 'Modelo']

        # Cria o DataFrame a partir da lista de tuplas
        df = pd.DataFrame(lista, columns=colunas)

        return df

    except HttpError as err:
        st.error(f"Erro ao acessar o Google Sheets: {err}")
        return pd.DataFrame()

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
    st.rerun()

# Interface do Streamlit
st.title("Sistema de Triagem")

# Carrega os dados do Google Sheets
SPREADSHEET_ID = "1D6OukHWiEic0jIJN-pLl4mY59xNXmm8qZryzKrKbJh8"
RANGE_NAME = "Triagem"
CELL_RANGE = "A:B"
df = read_google_sheets(SPREADSHEET_ID, RANGE_NAME, CELL_RANGE)

# Seção de busca de modelo
st.write("## Buscar Modelo pelo Device")
device_input = st.text_input("Digite o Device:")
if st.button("Buscar"):
    if not device_input.strip():
        st.warning("Por favor, insira um valor válido para o Device.")
    else:
        # Procurar o modelo correspondente no DataFrame
        modelo_resultado = df.loc[df['Device'] == device_input, 'Modelo']
        if not modelo_resultado.empty:
            st.success(f"Modelo correspondente: {modelo_resultado.iloc[0]}")
        else:
            st.error("Device não encontrado.")

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
