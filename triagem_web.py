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

# Função para resetar o formulário
def reset_form():
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

    respostas = st.session_state.get("respostas", [])

    # Mostra perguntas dinamicamente
    for i, pergunta in enumerate(perguntas):
        if i < st.session_state["progresso"]:
            st.write(f"{pergunta} - Resposta: {respostas[i]}")
        elif i == st.session_state["progresso"]:
            resposta = st.radio(pergunta, options=["sim", "não"], key=f"pergunta_{i}")
            if resposta:
                respostas.append(resposta)
                st.session_state["progresso"] += 1
                st.session_state["respostas"] = respostas
                st.experimental_rerun()
            break

    # Mostrar botão Enviar quando todas as perguntas forem respondidas
    if st.session_state["progresso"] == len(perguntas):
        if st.button("Enviar"):
            destino = decidir_destino(entrada_selecionada, respostas)
            st.success(f"O destino recomendado é: {destino}")
            reset_form()
