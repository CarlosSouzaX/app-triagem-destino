import streamlit as st

# Dados de triagem
entradas = {
    "Entrada 1": {
        "perguntas": [
            {"texto": "O produto está bloqueado?", "resposta_sim": None, "resposta_nao": None},
            {"texto": "O produto está funcional?", "resposta_sim": "Saída 1", "resposta_nao": None},
            {"texto": "Há danos estéticos?", "resposta_sim": "Saída 2", "resposta_nao": "Saída 3"}
        ]
    },
    "Entrada 2": {
        "perguntas": [
            {"texto": "O cliente deseja reembolso?", "resposta_sim": None, "resposta_nao": None},
            {"texto": "O produto está na garantia?", "resposta_sim": None, "resposta_nao": None},
            {"texto": "O produto está funcional?", "resposta_sim": "Saída 4", "resposta_nao": None},
            {"texto": "Há defeitos graves?", "resposta_sim": "Saída 5", "resposta_nao": "Saída 6"}
        ]
    },
}

# Inicialização do estado
if "entrada_selecionada" not in st.session_state:
    st.session_state["entrada_selecionada"] = None
    st.session_state["progresso"] = 0  # Para múltiplas perguntas
    st.session_state["respostas"] = []  # Para armazenar respostas
    st.session_state["saida"] = None

# Interface do Streamlit
st.title("Sistema de Triagem - Escolha e Responda")

# Seleção da entrada
entrada_atual = st.selectbox(
    "Selecione a Entrada", 
    options=["Selecione uma entrada"] + list(entradas.keys()),
)

# Resetar o estado ao mudar a entrada
if entrada_atual != st.session_state["entrada_selecionada"]:
    st.session_state["entrada_selecionada"] = entrada_atual
    st.session_state["progresso"] = 0
    st.session_state["respostas"] = []
    st.session_state["saida"] = None

# Fluxo para entradas com múltiplas perguntas
if entrada_atual in entradas:
    perguntas = entradas[entrada_atual]["perguntas"]
    progresso = st.session_state["progresso"]

    if progresso < len(perguntas):
        pergunta_atual = perguntas[progresso]
        st.write(f"**{pergunta_atual['texto']}**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sim", key=f"sim_{progresso}"):
                st.session_state["respostas"].append("sim")
                # Define o destino e interrompe o fluxo, se aplicável
                if pergunta_atual["resposta_sim"]:
                    st.session_state["saida"] = pergunta_atual["resposta_sim"]
                    st.rerun()
                else:
                    st.session_state["progresso"] += 1
                    st.rerun()
        with col2:
            if st.button("Não", key=f"nao_{progresso}"):
                st.session_state["respostas"].append("não")
                # Define o destino e interrompe o fluxo, se aplicável
                if pergunta_atual["resposta_nao"]:
                    st.session_state["saida"] = pergunta_atual["resposta_nao"]
                    st.rerun()
                else:
                    st.session_state["progresso"] += 1
                    st.rerun()

    # Exibir saída final após responder todas as perguntas
    if st.session_state["progresso"] == len(perguntas):
        if st.session_state["saida"]:
            st.success(f"Destino Final: {st.session_state['saida']}")
        else:
            st.error("Nenhum destino definido para as respostas fornecidas.")
