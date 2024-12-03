import streamlit as st

# Dados de triagem
entradas = {
    "Análise Meli": {
        "perguntas": [
            "O produto está funcional?",
            "Há danos estéticos?"
        ],
        "decisoes": {
            ("sim", "não"): "AT LN",
            ("sim", "sim"): "IN-HOUSE LN",
            ("não", "sim"): "Fábrica de Reparos",
            ("não", "não"): "Qualidade",
        }
    },
    "RunOff": {
        "perguntas": [
            "O produto está dentro da garantia?",
            "Há defeitos funcionais???"
        ],
        "decisoes": {
            ("sim", "não"): "AT Same",
            ("sim", "sim"): "Fábrica de Reparos",
            ("não", "sim"): "Qualidade",
            ("não", "não"): "IN-HOUSE Same",
        }
    },
    # Adicionar outras entradas conforme necessário...
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

    # Controle do progresso: Quantas perguntas foram respondidas
    if "progresso" not in st.session_state:
        st.session_state["progresso"] = 0
    if "respostas" not in st.session_state:
        st.session_state["respostas"] = [None] * len(perguntas)

    # Mostra perguntas dinamicamente
    progresso = st.session_state["progresso"]
    if progresso < len(perguntas):
        resposta = st.radio(
            perguntas[progresso], 
            options=["sim", "não"], 
            key=f"pergunta_{progresso}"
        )
        if resposta:
            st.session_state["respostas"][progresso] = resposta
            st.session_state["progresso"] += 1

    # Mostrar botão Enviar quando todas as perguntas forem respondidas
    if progresso == len(perguntas):
        if st.button("Enviar"):
            destino = decidir_destino(entrada_selecionada, st.session_state["respostas"])
            st.success(f"O destino recomendado é: {destino}")
            reset_form()
