import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from modulo.data_loader import carregar_dados_gsheets
from modulo.data_processor import buscar_modelo_por_device
from modulo.triagem import (
    inicializar_estado
)

from modulo.flow import (
    runoff_flow
)

# Configurar o layout para "wide"
st.set_page_config(layout="wide", page_title="Minha Aplicação", page_icon="📊")

# Inicializa o estado se não estiver configurado
if "inicializado" not in st.session_state:
    inicializar_estado()
    st.session_state["inicializado"] = True
    st.session_state["fluxo_finalizado"] = False
    st.session_state["current_question"] = "Q1"  # Define a pergunta inicial

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

         # Exibe o resultado completo na tela
        #st.write("🔍 Resultado da busca:")
        #st.write(result)

        # Mapeamento de cores e ícones para o status_sr
        status_componentes = {
            "open": st.success,  # Verde
            "arrived": st.success,  # Verde
            "tracked": st.warning,  # Amarelo
            "swapped": st.warning,  # Amarelo
            "sent": st.warning,  # Amarelo
            "closed": st.info,  # Azul Claro
            "lost_in_delivery": st.error,  # Vermelho
            "rejected_documents": st.error,  # Vermelho
            "logistics_failure_from_pitzi": st.error,  # Vermelho
            "expired": st.error,  # Vermelho
            "rejected_closed": st.error,  # Vermelho
            "rejected_sent": st.error  # Vermelho
        }

        # Verifica o status geral
        if result["status"] == "success":

            # Exibe a validação da consulta
            st.success("✅ Dispositivo encontrado com sucesso!")

            # Exibe a Esteira de Atendimento
            esteira = result.get("esteira", "Não definida")
            st.info(f"🚀 Esteira de Atendimento: **{esteira}**")

            # Armazenar a esteira no estado para uso posterior
            st.session_state["esteira"] = esteira

            # Exibe dados do Device
            st.subheader("📱 Dados do Device")
            for detalhe in result.get("detalhes", []):
                campo = detalhe["campo"]
                status = detalhe["status"]
                valor = detalhe["valor"]

                 # Exibe o campo com base no status
                if campo == "marca":
                    if status == "success":
                        st.success(f"✅ {campo.capitalize()}: **{valor}**")
                        st.session_state["marca"] = valor
                    elif status == "warning":
                        st.warning(f"⚠️ {campo.capitalize()}: {valor}")
                    elif status == "error":
                        st.error(f"❌ {campo.capitalize()}: {valor}")
                if campo == "modelo":
                    if status == "success":
                        st.session_state["modelo"] = valor
                        st.success(f"✅ {campo.capitalize()}: **{valor}**")
                    elif status == "warning":
                        st.warning(f"⚠️ {campo.capitalize()}: {valor}")
                    elif status == "error":
                        st.error(f"❌ {campo.capitalize()}: {valor}")
                if campo == "imei":
                    if status == "success":
                        st.success(f"✅ {campo.capitalize()}: **{valor}**")
                    elif status == "warning":
                        st.warning(f"⚠️ {campo.capitalize()}: {valor}")
                    elif status == "error":
                        st.error(f"❌ {campo.capitalize()}: {valor}")
            
            # # Exibe dados da SR
            st.subheader("📄 Dados da SR")
            for detalhe in result.get("detalhes", []):
                campo = detalhe["campo"]
                status = detalhe["status"]
                valor = detalhe["valor"]

                if campo == "sr":
                    if status == "success":
                        st.success(f"✅ **SR:** **{valor}**")
                    elif status == "warning":
                        st.warning(f"⚠️ **SR:** **{valor}**")
                    elif status == "error":
                        st.error(f"❌ **SR:** **{valor}**")

                if campo == "supplier":
                    if status == "success":
                        st.success(f"✅ **Supplier Device:** **{valor}**")
                    elif status == "warning":
                        st.warning(f"⚠️ **Supplier Device:** **{valor}**")
                    elif status == "error":
                        st.error(f"❌ **Supplier Device:** **{valor}**")

                if campo == "status_sr":
                    componente = status_componentes.get(valor)
                    # Armazenar a o status da SR no estado para uso posterior
                    st.session_state["status_sr"] = valor
                    if componente:  # Se o status estiver mapeado, exibe com o componente correspondente
                        componente(f"✅ **Status SR:** **{valor}**")
                    else:  # Caso o status não esteja no mapeamento, exibe um aviso genérico
                        st.warning(f"⚠️ **Status SR:** {valor} (Status não reconhecido)")

            # Mostrar a observação do cliente com destaque
            st.subheader("📌 Observação do Cliente")
            obs_cliente = result.get("obs_cliente", None)  # Obtém a observação do cliente do resultado
            if obs_cliente:
                st.info(f"🔍 **Observação:** {obs_cliente}")
            else:
                st.warning("⚠️ **Sem observações registradas para este cliente.**")    

        elif result["status"] == "warning":
            st.warning(f"⚠️ {result['message']}")
        elif result["status"] == "error":
            st.error(f"❌ {result['message']}")




# Divisor vertical na segunda coluna
with col2:
    st.markdown(
        """
        <div style="width: 2px; height: 100%; background-color: #ccc; margin: auto;"></div>
        """,
        unsafe_allow_html=True,
    )

# Função auxiliar para obter a esteira do estado
def obter_esteira_estado():
    """Retorna a esteira armazenada no estado, se disponível."""
    return st.session_state.get("esteira", None)  # Retorna None se não existir

def carregar_status():
    """Retorna o status da SR armazenado no estado, se disponível."""
    return st.session_state.get("status_sr", None)

def carregar_device_brand():
    """Retorna a marca do dispositivo armazenada no estado, se disponível."""
    return st.session_state.get("marca", None)

def carregar_device_model():
    """Retorna o modelo do dispositivo armazenado no estado, se disponível."""
    return st.session_state.get("modelo", None)

# Terceira coluna: Triagem de Produtos
with col3:
    st.subheader("⚙️ Triagem de Produtos")

    if "esteira" in st.session_state and st.session_state["esteira"]:
        st.info(f"🚀 Esteira de Atendimento: **{st.session_state['esteira']}**")

        # Executar o fluxo com os dados fornecidos
        flow = st.session_state["esteira"]
        device_brand = st.session_state.get("marca", None)

        if flow == "RUNOFF":
            runoff_flow(device_brand)
            st.session_state["fluxo_finalizado"] = True
        else:
            st.warning("⚠️ Fluxo não reconhecido ou não definido.")
    else:
        st.warning("⚠️ Nenhuma esteira foi selecionada. Realize uma busca do device no campo disponível.")


    # Exibir botão "Reiniciar" apenas se o fluxo estiver finalizado
    if st.session_state.get("fluxo_finalizado", False):
        if st.button("Reiniciar"):
            
            st.session_state["inicializado"] = False
            st.session_state["fluxo_finalizado"] = False
            st.session_state["esteira"] = None
            st.session_state["current_question"] = "Q1"  # Reinicia a primeira pergunta
            st.success("Fluxo reiniciado com sucesso!")
            inicializar_estado()