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
            "Há defeitos funcionais?"
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
    for key in st.session_state.keys():
        if "pergunta" in key or key == "entrada_selecionada":
            del st.session_state[key]

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
    respostas = []

    # Loop para todas as perguntas na mesma página
    for i, pergunta in enumerate(perguntas):
        resposta = st.radio(
            pergunta,
            options=["sim", "não"],
            key=f"pergunta_{i}"
        )
        respostas.append(resposta)

    # Botão de envio
    if st.button("Enviar"):
        if None in respostas:
            st.warning("Responda todas as perguntas antes de enviar.")
        else:
            destino = decidir_destino(entrada_selecionada, respostas)
            st.success(f"O destino recomendado é: {destino}")
            reset_form()  # Reseta o formulário após o envio
