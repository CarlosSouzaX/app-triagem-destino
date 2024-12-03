import streamlit as st

# Dados de triagem com múltiplas perguntas para Entrada 1
entradas = {
    "Entrada 1": {
        "perguntas": [
            {"texto": "O produto está bloqueado?", "resposta_sim": "Saída 1", "resposta_nao": None},
            {"texto": "O produto está funcional?", "resposta_sim": "Saída 2", "resposta_nao": "Saída 3"}
        ]
    },
    "Entrada 2": {"pergunta": "O produto está funcional?", "saida_sim": "Saída 4", "saida_nao": "Saída 5"},
    "Entrada 3": {"pergunta": "Há danos estéticos?", "saida_sim": "Saída 6", "saida_nao": "Saída 7"},
    "Entrada 4": {"pergunta": "O cliente deseja reembolso?", "saida_sim": "Saída 8", "saida_nao": "Saída 1"},
    "Entrada 5": {"pergunta": "O produto está na garantia?", "saida_sim": "Saída 2", "saida_nao": "Saída 3"},
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

# Fluxo para Entrada 1 com múltiplas perguntas
if entrada_atual == "Entrada 1":
    perguntas = entradas["Entrada 1"]["perguntas"]
    progresso = st.session_state["progresso"]

    if progresso < len(perguntas):
        pergunta_atual = perguntas[progresso]
        st.write(f"**{pergunta_atual['texto']}**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sim", key=f"sim_{progresso}"):
                st.session_state["respostas"].append("sim")
                if pergunta_atual["resposta_sim"]:
                    st.session_state["saida"] = pergunta_atual["resposta_sim"]
                st.session_state["progresso"] += 1
                st.rerun()
        with col2:
            if st.button("Não", key=f"nao_{progresso}"):
                st.session_state["respostas"].append("não")
                if pergunta_atual["resposta_nao"]:
                    st.session_state["saida"] = pergunta_atual["resposta_nao"]
                st.session_state["progresso"] += 1
                st.rerun()

    # Exibir saída final após responder todas as perguntas
    if st.session_state["progresso"] == len(perguntas):
        if st.session_state["saida"]:
            st.success(f"Destino Final: {st.session_state['saida']}")
        else:
            st.error("Nenhum destino definido para as respostas fornecidas.")

# Fluxo para outras entradas com uma única pergunta
elif entrada_atual in entradas:
    pergunta = entradas[entrada_atual]["pergunta"]
    st.write(f"**{pergunta}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sim"):
            st.session_state["saida"] = entradas[entrada_atual]["saida_sim"]
            st.rerun()
    with col2:
        if st.button("Não"):
            st.session_state["saida"] = entradas[entrada_atual]["saida_nao"]
            st.rerun()

# Exibir saída final para entradas com uma pergunta
if st.session_state["saida"] and entrada_atual != "Entrada 1":
    st.success(f"Destino Final: {st.session_state['saida']}")
