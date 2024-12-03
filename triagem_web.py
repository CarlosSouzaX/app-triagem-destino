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
    st.session_state["progresso"] = 0  # Controle do progresso nas perguntas
    st.session_state["respostas"] = []  # Respostas dadas
    st.session_state["saida"] = None  # Destino final

# Interface do Streamlit
st.title("Sistema de Triagem de Produtos")

# Seleção da entrada
entrada_atual = st.selectbox(
    "Selecione a Entrada",
    options=["Selecione uma entrada"] + list(entradas.keys())
)

# Resetar o estado ao mudar a entrada
if entrada_atual != st.session_state["entrada_selecionada"]:
    st.session_state["entrada_selecionada"] = entrada_atual
    st.session_state["progresso"] = 0
    st.session_state["respostas"] = []
    st.session_state["saida"] = None

# Fluxo para entradas com perguntas
if entrada_atual in entradas:
    perguntas = entradas[entrada_atual]["perguntas"]
    progresso = st.session_state["progresso"]

    # Exibir perguntas respondidas
    if progresso > 0:
        st.write("### Perguntas Respondidas")
        for i in range(progresso):
            pergunta = perguntas[i]["texto"]
            resposta = st.session_state["respostas"][i]
            st.write(f"**{i + 1}. {pergunta}**")
            st.write(f"Resposta: {resposta}")

    # Exibir a próxima pergunta
    if progresso < len(perguntas) and not st.session_state["saida"]:
        pergunta_atual = perguntas[progresso]
        st.write(f"**Pergunta {progresso + 1}: {pergunta_atual['texto']}**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sim", key=f"sim_{progresso}"):
                st.session_state["respostas"].append("sim")
                # Define o destino imediato, se aplicável
                if pergunta_atual["resposta_sim"]:
                    st.session_state["saida"] = pergunta_atual["resposta_sim"]
                else:
                    st.session_state["progresso"] += 1
                st.rerun()
        with col2:
            if st.button("Não", key=f"nao_{progresso}"):
                st.session_state["respostas"].append("não")
                # Define o destino imediato, se aplicável
                if pergunta_atual["resposta_nao"]:
                    st.session_state["saida"] = pergunta_atual["resposta_nao"]
                else:
                    st.session_state["progresso"] += 1
                st.rerun()

    # Exibir saída final
    if st.session_state["saida"]:
        st.success(f"Destino Final: {st.session_state['saida']}")
    elif progresso == len(perguntas):
        st.error("Nenhum destino definido para as respostas fornecidas.")
