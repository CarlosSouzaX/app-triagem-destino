import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

url = "https://docs.google.com/spreadsheets/d/1D6OukHWiEic0jIJN-pLl4mY59xNXmm8qZryzKrKbJh8/edit?gid=350232245#gid=350232245"

conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(spreadsheet=url, worksheet="Triagem" ,usecols=[0, 1])
df = pd.DataFrame(df)

# Verificar os tipos de dados de cada coluna
print(df.dtypes)


# Normalizar os nomes das colunas
df.columns = df.columns.str.strip().str.lower()

# Verificar o DataFrame antes de prosseguir
st.write("### Verificando o DataFrame inicial")
st.write("Colunas do DataFrame:", df.columns)
st.write("Primeiras linhas do DataFrame:")
st.write(df.head())

# Converter a coluna 'Device' para int64
df["Device"] = df["Device"].astype(int)

st.write(df.info())
st.write(df.dtypes)


# Seção de busca de modelo
st.write("## Buscar Modelo pelo Device")
device_input = st.text_input("Digite o Device:")

if st.button("Buscar"):
    if not device_input.strip():
        st.warning("Por favor, insira um valor válido para o Device.")
    else:

        # Verificar se as colunas estão presentes
        if "device" in df.columns and "modelo" in df.columns:
            # Filtrar pelo Device no DataFrame
            resultado = df.loc[df["device"] == device_input, "modelo"]

            if not resultado.empty:
                st.success(f"Modelo correspondente: {resultado.iloc[0]}")
            else:
                st.error(f"Device '{device_input}' não encontrado no DataFrame.")
        else:
            st.error("As colunas 'Device' e/ou 'Modelo' não existem no DataFrame.")


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
