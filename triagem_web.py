import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# URL do Google Sheets
url = "https://docs.google.com/spreadsheets/d/1D6OukHWiEic0jIJN-pLl4mY59xNXmm8qZryzKrKbJh8/edit?gid=350232245#gid=350232245"

# Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Carregar os dados da planilha
df = conn.read(spreadsheet=url, worksheet="Triagem", usecols=[0, 1])
df = pd.DataFrame(df)

# Normalizar os nomes das colunas
df.columns = df.columns.str.strip().str.lower()

# Seção de busca de modelo
st.title("Sistema de Triagem")
st.header("Buscar Modelo pelo Device")
device_input = st.text_input("Digite o Device:")

if st.button("Buscar"):
    if not device_input.strip():
        st.warning("Por favor, insira um valor válido para o Device.")
    else:
        try:
            # Converter o input para float
            device_input_float = float(device_input.strip())
            if "device" in df.columns and "modelo" in df.columns:
                # Filtrar pelo Device no DataFrame
                resultado = df.loc[df["device"] == device_input_float, "modelo"]
                if not resultado.empty:
                    st.success(f"Modelo correspondente: {resultado.iloc[0]}")
                else:
                    st.error(f"Device '{device_input}' não encontrado no DataFrame.")
            else:
                st.error("As colunas 'Device' e/ou 'Modelo' não existem no DataFrame.")
        except ValueError:
            st.error("O valor inserido deve ser numérico.")

# Dados de triagem
entradas = {
    "Análise Meli": [
        {"texto": "O produto é da marca Xiaomi ou Apple ou Motorola?", "sim": {"proxima": 1}, "nao": {"proxima": 2}},
        {"texto": "O Mi/FMiP está bloqueado?", "sim": {"saida": "Rejeitar SR"}, "nao": {"proxima": 2}},
        {"texto": "Há danos estéticos?", "sim": {"saida": "Saída 2"}, "nao": {"saida": "Saída 3"}},
    ],
    "Análise Gazin": [
        {"texto": "O produto está na garantia?", "sim": {"proxima": 1}, "nao": {"proxima": 2}},
        {"texto": "O produto está funcional?", "sim": {"saida": "Saída 4"}, "nao": {"proxima": 2}},
        {"texto": "Há defeitos graves?", "sim": {"saida": "Saída 5"}, "nao": {"saida": "Saída 6"}},
    ],
    "Análise RunOff": [
        {"texto": "O produto está na garantia?", "sim": {"proxima": 1}, "nao": {"proxima": 2}},
        {"texto": "O produto está funcional?", "sim": {"saida": "Saída 4"}, "nao": {"proxima": 2}},
        {"texto": "Há defeitos graves?", "sim": {"saida": "Saída 5"}, "nao": {"saida": "Saída 6"}},
    ],
}

# Inicialização do estado
if "entrada_selecionada" not in st.session_state:
    st.session_state.update({
        "entrada_selecionada": None,
        "progresso": 0,
        "respostas": [],
        "saida": None
    })

# Funções auxiliares
def reset_estado():
    st.session_state.update({"progresso": 0, "respostas": [], "saida": None})

def exibir_perguntas_respondidas(perguntas, respostas):
    st.subheader("Perguntas Respondidas")
    for i, resposta in enumerate(respostas):
        st.write(f"**{i + 1}. {perguntas[i]['texto']}**")
        st.write(f"Resposta: {resposta}")

def processar_resposta(pergunta_atual, resposta):
    destino = pergunta_atual[resposta]
    if "saida" in destino:
        st.session_state["saida"] = destino["saida"]
    elif "proxima" in destino:
        st.session_state["progresso"] = destino["proxima"]
    st.experimental_rerun()

# Interface de triagem
st.header("Triagem")

# Seleção da entrada
entrada_atual = st.selectbox(
    "Selecione a Entrada",
    options=["Selecione uma entrada"] + list(entradas.keys()),
    on_change=reset_estado
)

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
