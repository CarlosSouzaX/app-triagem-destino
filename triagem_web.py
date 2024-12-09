import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from modulo.data_loader import carregar_dados_gsheets
from modulo.data_processor import buscar_modelo_por_device
from modulo.triagem import (
    inicializar_estado,
    reset_estado,
    exibir_perguntas_respondidas,
    processar_resposta,
    obter_entradas,
)


# Configurar o layout para "wide"
st.set_page_config(layout="wide", page_title="Minha Aplicação", page_icon="📊")

# Inicializa o estado
inicializar_estado()


SHEET_URL = "https://docs.google.com/spreadsheets/d/1B34FqK4aJWeJtm4RLLN2AqlBJ-n6AASRIKn6UrnaK0k/edit?gid=698133322#gid=698133322"
WORKSHEET = "Triagem"
USECOLS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

df = carregar_dados_gsheets(SHEET_URL, WORKSHEET, USECOLS)

# Título principal
st.title("📋 Sistema de Triagem")

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
                if campo == "marca" or campo == "modelo" or campo == "imei":
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

                # Exibe o campo com base no status
                if campo == "sr" or campo == "status_sr" or campo == "supplier":
                    if status == "success":
                        st.success(f"✅ {campo.capitalize()}: **{valor}**")
                    elif status == "warning":
                        st.warning(f"⚠️ {campo.capitalize()}: {valor}")
                    elif status == "error":
                        st.error(f"❌ {campo.capitalize()}: {valor}")

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
    return st.session_state.get("esteira")

# Terceira coluna: Triagem de Produtos
with col3:
    st.header("⚙️ Triagem de Produtos")

    # Obter esteira do estado
    esteira = obter_esteira_estado()
    if esteira:
        st.info(f"🔄 Usando a Esteira de Atendimento: **{esteira}**")

        # Obter perguntas com base na esteira
        perguntas = obter_entradas(esteira)

        if perguntas:
            progresso = st.session_state.get("progresso", 0)

            if progresso > 0:
                exibir_perguntas_respondidas(perguntas, st.session_state.get("respostas", []))

            if progresso < len(perguntas) and not st.session_state.get("saida"):
                pergunta_atual = perguntas[progresso]
                st.subheader(f"❓ Pergunta {progresso + 1}")
                st.markdown(f"**{pergunta_atual['texto']}**")

                if st.button("✅ Sim", key=f"sim_{progresso}"):
                    st.session_state.setdefault("respostas", []).append("sim")
                    processar_resposta(pergunta_atual, "sim")

                if st.button("❌ Não", key=f"nao_{progresso}"):
                    st.session_state.setdefault("respostas", []).append("não")
                    processar_resposta(pergunta_atual, "nao")

            if st.session_state.get("saida"):
                st.success(f"🏁 Destino Final: **{st.session_state['saida']}**")
        else:
            st.warning("⚠️ Nenhuma entrada definida para esta esteira.")
    else:
        st.warning("⚠️ Nenhuma esteira foi selecionada. Realize uma busca no campo acima.")
