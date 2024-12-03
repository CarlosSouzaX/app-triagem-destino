import streamlit as st

# Dados de triagem
entradas = {
    "Análise Meli": {
        "perguntas": [
            {"texto": "O produto está bloqueado?", "corte": True},
            {"texto": "O produto está funcional?", "corte": False},
            {"texto": "Há danos estéticos?", "corte": False}
        ],
        "decisoes": {
            ("sim",): "Destino: Produto Bloqueado",
            ("sim", "não", "não"): "AT LN",
            ("sim", "sim", "não"): "IN-HOUSE LN",
            ("não", "sim", "sim"): "Fábrica de Reparos",
            ("não", "não", "não"): "Qualidade",
        }
    },
    "RunOff": {
        "perguntas": [
            {"texto": "O produto está bloqueado?", "corte": True},
            {"texto": "O produto está dentro da garantia?", "corte": False},
            {"texto": "Há defeitos funcionais?", "corte": False},
            {"texto": "O cliente solicitou reembolso?", "corte": False}
        ],
        "decisoes": {
            ("sim",): "Destino: Produto Bloqueado",
            ("sim", "não", "não", "não"): "AT Same",
            ("sim", "sim", "não", "não"): "Fábrica de Reparos",
            ("não", "sim", "sim", "sim"): "Qualidade",
            ("não", "não", "não", "não"): "IN-HOUSE Same",
        }
    },
}

def decidir_destino(entrada, respostas):
    """
    Decide o destino com base na entrada e nas respostas.
    """
    dados = entradas.get(entrada)
    respostas_tuple = tuple(respostas)
    return dados["decisoes"].get(respostas_tuple, "Destino não definido")

def reset_form():
    """
    Reseta o estado do formulário para permitir nova submissão.
    """
    st.session_state["progresso"] = 0
    st.session_state["respostas"] = []

# Inicialização do estado
if "entrada_selecionada" not in st.session_state:
    st.session_state["entrada_selecionada"] = None
    st.session_state["progresso"] = 0
    st.session_state["respostas"] = []

# Interface do Streamlit
st.title("Sistema de Triagem de Produtos")

# Seleção da entrada
entrada_atual = st.selectbox(
    "Selecione a Entrada", 
    options=list(entradas.keys()), 
    index=0 if st.session_state["entrada_selecionada"] is None else list(entradas.keys()).index(st.session_state["entrada_selecionada"])
)

# Resetar o estado ao mudar a entrada
if entrada_atual != st.session_state["entrada_selecionada"]:
    st.session_state["entrada_selecionada"] = entrada_atual
    reset_form()

# Recuperar perguntas e progresso
perguntas = entradas[st.session_state["entrada_selecionada"]]["perguntas"]
progresso = st.session_state["progresso"]

# Garantir que a lista de respostas esteja sincronizada com o número de perguntas
if len(st.session_state["respostas"]) < len(perguntas):
    st.session_state["respostas"].extend([None] * (len(perguntas) - len(st.session_state["respostas"])))

respostas = st.session_state["respostas"]

# Exibir perguntas anteriores
for i in range(progresso):
    st.write(f"**Pergunta {i + 1}: {perguntas[i]['texto']}**")
    st.write(f"Resposta: {respostas[i]}")

# Exibir a próxima pergunta
if progresso < len(perguntas):
    pergunta_atual = perguntas[progresso]

    # Exibir a pergunta atual
    resposta = st.radio(
        pergunta_atual["texto"],
        options=["sim", "não"],
        index=-1 if respostas[progresso] is None else ["sim", "não"].index(respostas[progresso]),
        key=f"pergunta_{progresso}"
    )

    if resposta:
        respostas[progresso] = resposta
        st.session_state["respostas"] = respostas

        # Finalizar se for uma pergunta de corte
        if pergunta_atual["corte"] and resposta == "sim":
            destino = decidir_destino(entrada_atual, respostas[:progresso + 1])
            st.success(f"O destino recomendado é: {destino}")
            reset_form()
        else:
            st.session_state["progresso"] += 1
            st.experimental_rerun()

# Botão "Voltar" para ajustar respostas
if progresso > 0:
    if st.button("Voltar"):
        st.session_state["progresso"] -= 1
        st.session_state["respostas"][progresso - 1] = None
        st.experimental_rerun()

# Mostrar botão Enviar ao final
if progresso == len(perguntas):
    if st.button("Enviar"):
        destino = decidir_destino(entrada_atual, respostas)
        st.success(f"O destino recomendado é: {destino}")
        reset_form()
