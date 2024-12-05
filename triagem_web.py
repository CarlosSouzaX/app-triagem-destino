import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# URL do Google Sheets
url = "https://docs.google.com/spreadsheets/d/1B34FqK4aJWeJtm4RLLN2AqlBJ-n6AASRIKn6UrnaK0k/edit?gid=698133322#gid=698133322"

# Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Carregar os dados da planilha
df = conn.read(spreadsheet=url, worksheet="Triagem", usecols=[0, 1, 2, 3, 4, 5, 6])
df = pd.DataFrame(df)

# Normalizar os nomes das colunas
df.columns = df.columns.str.strip().str.lower()

# Título Principal
st.title("📋 Sistema de Triagem")

# Seção de Busca de Modelo
st.header("🔍 Buscar Modelo pelo Device")
device_input = st.text_input("Digite o número do Device:")

if st.button("Buscar"):
    if not device_input.strip():
        st.warning("⚠️ Por favor, insira um valor válido para o Device.")
    else:
        try:
            # Converter o input para float
            device_input_float = float(device_input.strip())
            if "device" in df.columns:
                # Filtrar pelo Device no DataFrame
                resultado = df.loc[df["device"] == device_input_float, df.columns[1:7]]
                if not resultado.empty:
                    
                    # Verificar e exibir a marca
                    marca = resultado.iloc[0, 1]
                    if pd.notnull(marca):
                        st.success(f"✅ Marca: **{marca}**")
                    else:
                        st.warning("⚠️ Marca não disponível.")

                    # Verificar e exibir o IMEI
                    try:
                        imei = int(resultado.iloc[0, 3]) if pd.notnull(resultado.iloc[0, 3]) else None
                        if imei:
                            st.success(f"✅ IMEI: **{imei}**")
                        else:
                            st.warning("⚠️ IMEI não disponível.")
                    except ValueError:
                        st.error("❌ O valor do IMEI não é válido.")

                   
                else:
                    st.error(f"❌ Device '{device_input}' não encontrado no DataFrame.")
            else:
                st.error("❌ As colunas 'Device' e/ou 'Modelo' não existem no DataFrame.")
        except ValueError:
            st.error("❌ O valor inserido deve ser numérico.")

# Divisor visual
st.divider()

# Dados de triagem
st.header("⚙️ Triagem de Produtos")
entradas = {
    "Análise Meli": [
        {"texto": "O produto é da marca Xiaomi, Apple ou Motorola?", "sim": {"proxima": 1}, "nao": {"proxima": 2}},
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
    st.subheader("📝 Perguntas Respondidas")
    for i, resposta in enumerate(respostas):
        st.markdown(f"**{i + 1}. {perguntas[i]['texto']}**")
        st.write(f"Resposta: **{resposta}**")

def processar_resposta(pergunta_atual, resposta):
    destino = pergunta_atual[resposta]
    if "saida" in destino:
        st.session_state["saida"] = destino["saida"]
    elif "proxima" in destino:
        st.session_state["progresso"] = destino["proxima"]
    st.rerun()

# Interface de Seleção
entrada_atual = st.selectbox(
    "Selecione a Análise",
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
        st.subheader(f"❓ Pergunta {progresso + 1}")
        st.markdown(f"**{pergunta_atual['texto']}**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sim", key=f"sim_{progresso}"):
                st.session_state["respostas"].append("sim")
                processar_resposta(pergunta_atual, "sim")
        with col2:
            if st.button("❌ Não", key=f"nao_{progresso}"):
                st.session_state["respostas"].append("não")
                processar_resposta(pergunta_atual, "nao")

    if st.session_state["saida"]:
        st.success(f"🏁 Destino Final: **{st.session_state['saida']}**")
