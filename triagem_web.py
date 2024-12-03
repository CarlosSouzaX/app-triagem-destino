import streamlit as st

# Dados de triagem simplificados
entradas = {
    "Entrada 1": {"pergunta": "O produto está bloqueado?"},
    "Entrada 2": {"pergunta": "O produto está funcional?"},
    "Entrada 3": {"pergunta": "Há danos estéticos?"},
    "Entrada 4": {"pergunta": "O cliente deseja reembolso?"},
    "Entrada 5": {"pergunta": "O produto está na garantia?"},
}

# Inicialização do estado
if "entrada_selecionada" not in st.session_state:
    st.session_state["entrada_selecionada"] = None
    st.session_state["resposta"] = None

# Interface do Streamlit
st.title("Sistema de Triagem - Passo Inicial")

# Seleção da entrada
entrada_atual = st.selectbox(
    "Selecione a Entrada", 
    options=["Selecione uma entrada"] + list(entradas.keys()),
)

# Resetar o estado ao mudar a entrada
if entrada_atual != st.session_state["entrada_selecionada"]:
    st.session_state["entrada_selecionada"] = entrada_atual
    st.session_state["resposta"] = None

# Mostrar a pergunta correspondente
if entrada_atual in entradas:
    pergunta = entradas[entrada_atual]["pergunta"]
    resposta = st.radio(
        pergunta,
        options=["Selecione uma opção", "sim", "não"],
        index=0,  # Sempre começa com o placeholder selecionado
    )
    
    if resposta != "Selecione uma opção":
        st.session_state["resposta"] = resposta
        st.write(f"Você respondeu: {resposta}")

# Exibir resposta final
if st.session_state["resposta"]:
    st.success(f"Resposta registrada: {st.session_state['resposta']}")
