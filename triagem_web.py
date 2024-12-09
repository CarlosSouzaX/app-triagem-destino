import streamlit as st
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
st.set_page_config(layout="wide", page_title="Sistema de Triagem", page_icon="📋")

# Inicializa o estado
inicializar_estado()

# Configurações de conexão com o Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1B34FqK4aJWeJtm4RLLN2AqlBJ-n6AASRIKn6UrnaK0k/edit#gid=698133322"
WORKSHEET = "Triagem"
USECOLS = list(range(15))

# Carregar dados do Google Sheets
df = carregar_dados_gsheets(SHEET_URL, WORKSHEET, USECOLS)

# Título principal
st.title("📋 Sistema de Triagem")

# Layout com colunas
col1, col2, col3 = st.columns([1, 0.1, 1])


# Função para exibir a busca por Device
def exibir_busca_por_device():
    with col1:
        st.header("🔍 Buscar Modelo pelo Device")
        device_input = st.text_input("Digite o número do Device:")

        if st.button("Buscar", key="buscar_device"):
            # Resetar estado de perguntas ao buscar novamente
            reset_estado()

            # Processar busca pelo modelo do device
            result = buscar_modelo_por_device(df, device_input)

            if not result or not isinstance(result, dict):
                st.error("❌ Nenhum resultado encontrado ou formato inválido.")
                return

            if result["status"] == "success":
                # Exibe os dados do dispositivo
                st.success("✅ Dispositivo encontrado com sucesso!")
                esteira = result.get("esteira", "Não definida")
                st.session_state["esteira"] = esteira
                st.session_state["detalhes_dispositivo"] = result.get("detalhes", [])

                # Exibe detalhes
                st.subheader("📱 Dados do Device")
                for detalhe in st.session_state["detalhes_dispositivo"]:
                    campo = detalhe["campo"]
                    status = detalhe["status"]
                    valor = detalhe["valor"]
                    if status == "success":
                        st.success(f"✅ {campo.capitalize()}: **{valor}**")
                    elif status == "warning":
                        st.warning(f"⚠️ {campo.capitalize()}: {valor}")
                    elif status == "error":
                        st.error(f"❌ {campo.capitalize()}: {valor}")

                # Exibe observação do cliente
                st.subheader("📌 Observação do Cliente")
                obs_cliente = result.get("obs_cliente", None)
                if obs_cliente:
                    st.info(f"🔍 **Observação:** {obs_cliente}")
                else:
                    st.warning("⚠️ **Sem observações registradas para este cliente.**")
            elif result["status"] == "warning":
                st.warning(f"⚠️ {result['message']}")
            elif result["status"] == "error":
                st.error(f"❌ {result['message']}")
        else:
            # Manter dados carregados anteriormente
            if "detalhes_dispositivo" in st.session_state:
                st.subheader("📱 Dados do Device (Persistente)")
                for detalhe in st.session_state["detalhes_dispositivo"]:
                    campo = detalhe["campo"]
                    status = detalhe["status"]
                    valor = detalhe["valor"]
                    if status == "success":
                        st.success(f"✅ {campo.capitalize()}: **{valor}**")
                    elif status == "warning":
                        st.warning(f"⚠️ {campo.capitalize()}: {valor}")
                    elif status == "error":
                        st.error(f"❌ {campo.capitalize()}: {valor}")


# Função para exibir a triagem de produtos
def exibir_triagem():
    with col3:
        st.header("⚙️ Triagem de Produtos")

        # Obter a esteira do estado
        esteira = st.session_state.get("esteira")
        if not esteira:
            st.warning("⚠️ Nenhuma esteira foi selecionada. Realize uma busca no campo acima.")
            return

        st.info(f"🔄 Usando a Esteira de Atendimento: **{esteira}**")
        perguntas = obter_entradas(esteira)

        if not perguntas:
            st.warning("⚠️ Nenhuma entrada definida para esta esteira.")
            return

        progresso = st.session_state["progresso"]

        # Botão "Voltar" para ajustar respostas
        if progresso > 0:
            if st.button("⬅️ Voltar"):
                st.session_state["progresso"] -= 1
                st.session_state["respostas"].pop()

        # Exibe perguntas já respondidas
        if progresso > 0:
            exibir_perguntas_respondidas(perguntas, st.session_state["respostas"])

        # Exibe a pergunta atual
        if progresso < len(perguntas) and not st.session_state.get("saida"):
            pergunta_atual = perguntas[progresso]
            st.subheader(f"❓ Pergunta {progresso + 1}")
            st.markdown(f"**{pergunta_atual['texto']}**")

            col_sim, col_nao = st.columns(2)
            with col_sim:
                if st.button("✅ Sim", key=f"sim_{progresso}"):
                    st.session_state["respostas"].append("sim")
                    processar_resposta(pergunta_atual, "sim")
            with col_nao:
                if st.button("❌ Não", key=f"nao_{progresso}"):
                    st.session_state["respostas"].append("não")
                    processar_resposta(pergunta_atual, "nao")

        # Exibe a saída final
        if st.session_state.get("saida"):
            st.success(f"🏁 Destino Final: **{st.session_state['saida']}**")


# Exibir as funcionalidades
exibir_busca_por_device()
st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)
exibir_triagem()
