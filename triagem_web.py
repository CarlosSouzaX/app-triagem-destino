import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from modulo.data_loader import carregar_dados_gsheets
from modulo.data_processor import buscar_modelo_por_device
from modulo.triagem import inicializar_estado
from modulo.flow import runoff_flow, warrantyOEM_flow

# Configurar o layout para "wide"
st.set_page_config(layout="wide", page_title="Minha Aplicação", page_icon="📊")

# Inicializa o estado
inicializar_estado()

SHEET_URL = "https://docs.google.com/spreadsheets/d/1B34FqK4aJWeJtm4RLLN2AqlBJ-n6AASRIKn6UrnaK0k/edit?gid=698133322#gid=698133322"
WORKSHEET = "Triagem"
USECOLS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

df = carregar_dados_gsheets(SHEET_URL, WORKSHEET, USECOLS)

# Título principal
st.title("📋 Device Verification Workflow")

# Layout com colunas para incluir divisor vertical
col1, col2, col3 = st.columns([1, 0.1, 1])  # Ajustar proporções das colunas

# Primeira coluna: Buscar Modelo pelo Device
with col1:
    st.header("🔍 Buscar Modelo pelo Device")
    device_input = st.text_input("Digite o número do Device:")

    if st.button("Buscar", key="buscar_device"):
        # Chama a função de busca
        result = buscar_modelo_por_device(df, device_input)

        # Salva o resultado no estado
        st.session_state["result"] = result

        # Processa o resultado
        if result["status"] == "success":
            st.success("✅ Dispositivo encontrado com sucesso!")

            # Exibe dados do Device e SR
            st.subheader("📱 Dados do Device")
            for detalhe in result.get("detalhes", []):
                campo = detalhe["campo"]
                status = detalhe["status"]
                valor = detalhe["valor"]

                if status == "success":
                    st.success(f"✅ {campo.capitalize()}: **{valor}**")
                elif status == "warning":
                    st.warning(f"⚠️ {campo.capitalize()}: {valor}")
                elif status == "error":
                    st.error(f"❌ {campo.capitalize()}: {valor}")

            # Armazena dados no estado
            st.session_state.update({
                "esteira": result.get("esteira", None),
                "status_sr": result.get("status_sr", None),
                "marca": result.get("marca", None),
                "modelo": result.get("modelo", None),
            })

            # Exibe observação do cliente
            obs_cliente = result.get("obs_cliente", None)
            if obs_cliente:
                st.info(f"🔍 **Observação:** {obs_cliente}")
            else:
                st.warning("⚠️ **Sem observações registradas para este cliente.**")

# Recuperar o resultado do estado
result = st.session_state.get("result", None)

# Divisor vertical na segunda coluna
with col2:
    st.markdown(
        """
        <div style="width: 2px; height: 100%; background-color: #ccc; margin: auto;"></div>
        """,
        unsafe_allow_html=True,
    )

# Terceira coluna: Triagem de Produtos
#if result and result.get("status") == "success":
with col3:
    st.subheader("⚙️ Triagem de Produtos")
    st.info(f"🚀 Esteira de Atendimento: **{st.session_state['esteira']}**")

    # Executar o fluxo com os dados fornecidos
    flow = st.session_state["esteira"]
    device_brand = st.session_state["marca"]

    if flow == "RUNOFF":
        runoff_flow(device_brand)
    #elif flow == "GARANTIA FUNCIONAL":
       # warrantyOEM_flow(device_brand)
    else:
        st.warning("⚠️ Fluxo não reconhecido ou não definido.")

