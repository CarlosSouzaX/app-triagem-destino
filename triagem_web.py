import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from modulo.data_loader import carregar_dados_gsheets
from modulo.data_processor import buscar_modelo_por_device



# Configurar o layout para "wide"
st.set_page_config(layout="wide", page_title="Minha Aplicação", page_icon="📊")


SHEET_URL = "https://docs.google.com/spreadsheets/d/1B34FqK4aJWeJtm4RLLN2AqlBJ-n6AASRIKn6UrnaK0k/edit?gid=698133322#gid=698133322"
WORKSHEET = "Triagem"
USECOLS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

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
        st.write("🔍 Resultado da busca:")
        st.write(result["esteira"])

        # Mapeamento de cores para o Status da SR
        status_cores = {
            "tracked": "#FFA500",  # Laranja
            "open": "#008000",  # Verde
            "closed": "#0000FF",  # Azul
            "lost_in_delivery": "#808080",  # Cinza
            "rejected_documents": "#FF0000",  # Vermelho
            "arrived": "#FFFF00",  # Amarelo
            "swapped": "#FFA500",  # Laranja
            "logistics_failure_from_pitzi": "#808080",  # Cinza
            "expired": "#808080",  # Cinza
            "rejected_closed": "#FF0000",  # Vermelho
            "rejected_sent": "#FF0000",  # Vermelho
            "sent": "#FFA500",  # Laranja
        }

        # Verifica o status geral
        if result["status"] == "success":

            # Exibe a Esteira de Atendimento
            esteira = result.get("esteira", "Não definida")
            st.info(f"🚀 Esteira de Atendimento: **{esteira}**")

            st.success("✅ Dispositivo encontrado com sucesso!")

            for detalhe in result.get("detalhes", []):
                campo = detalhe["campo"]
                status = detalhe["status"]
                valor = detalhe["valor"]

                if campo == "status_sr" and status == "success":
                    # Aplica a cor de fundo correspondente ao status
                    cor = status_cores.get(valor, "#000000")  # Preto como cor padrão
                    st.markdown(
                        f"""
                        <div style="
                            background-color: {cor};
                            color: white;
                            padding: 10px;
                            border-radius: 5px;
                            margin-bottom: 10px;
                        ">
                            <strong>Status SR:</strong> {valor}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                elif status == "success":
                    st.success(f"✅ {campo.capitalize()}: **{valor}**")
                elif status == "warning":
                    st.warning(f"⚠️ {campo.capitalize()}: {valor}")
                elif status == "error":
                    st.error(f"❌ {campo.capitalize()}: {valor}")
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

# Terceira coluna: Triagem de Produtos
with col3:
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
            col_sim, col_nao = st.columns(2)
            with col_sim:
                if st.button("✅ Sim", key=f"sim_{progresso}"):
                    st.session_state["respostas"].append("sim")
                    processar_resposta(pergunta_atual, "sim")
            with col_nao:
                if st.button("❌ Não", key=f"nao_{progresso}"):
                    st.session_state["respostas"].append("não")
                    processar_resposta(pergunta_atual, "nao")

        if st.session_state["saida"]:
            st.success(f"🏁 Destino Final: **{st.session_state['saida']}**")
