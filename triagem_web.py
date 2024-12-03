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
    if not dados:
        return "Entrada inválida"
    
    respostas_tuple = tuple(respostas)
    return dados["decisoes"].get(respostas_tuple, "Destino não definido")

def reset_form():
    """
    Reseta o estado do formulário para permitir nova submissão.
    """
    st.session_state.clear()

# Interface Streamlit
st.title("Sistema de Triagem de Produtos")

# Seleção da entrada
entrada_selecionada = st.selectbox(
    "Selecione a Entrada", 
    options=list(entradas.keys()), 
    key="entrada_selecionada"
)

if entrada_selecionada:
    perguntas = entradas[entrada_selecionada]["perguntas"]

    # Inicializa o progresso e as respostas, se necessário
    if "progresso" not in st.session_state:
        st.session_state["progresso"] = 0
    if "respostas" not in st.session_state:
        st.session_state["respostas"] = [None] * len(perguntas)

    progresso = st.session_state["progresso"]
    respostas = st.session_state["respostas"]

    # Exibir perguntas anteriores e a atual
    for i in range(progresso):
        st.write(f"**Pergunta {i + 1}: {perguntas[i]['texto']}**")
        st.write(f"Resposta: {respostas[i]}")

    if progresso < len(perguntas):
        pergunta_atual = perguntas[progresso]
        resposta = st.radio(
            pergunta_atual["texto"], 
            options=["sim", "não"], 
            key=f"pergunta_{progresso}"
        )
        if resposta:
            respostas[progresso] = resposta
            st.session_state["respostas"] = respostas

            # Se a pergunta atual é um "corte" e a resposta for "sim", interrompe o fluxo
            if pergunta_atual["corte"] and resposta == "sim":
                st.session_state["progresso"] = len(perguntas)  # Marca todas as perguntas como respondidas
                destino = decidir_destino(entrada_selecionada, respostas[:progresso + 1])
                st.success(f"O destino recomendado é: {destino}")
                reset_form()
            else:
                st.session_state["progresso"] += 1

    # Botão "Voltar" para ajustar respostas anteriores
    if progresso > 0:
        if st.button("Voltar"):
            st.session_state["progresso"] -= 1

    # Mostrar botão Enviar quando todas as perguntas forem respondidas
    if progresso == len(perguntas) and not perguntas[progresso - 1]["corte"]:
        if st.button("Enviar"):
            destino = decidir_destino(entrada_selecionada, respostas)
            st.success(f"O destino recomendado é: {destino}")
            reset_form()
