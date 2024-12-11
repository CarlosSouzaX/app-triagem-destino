import streamlit as st

def inicializar_estado():
    """Inicializa o estado da triagem."""
    if "progresso" not in st.session_state:
        st.session_state["progresso"] = 0
    if "respostas" not in st.session_state:
        st.session_state["respostas"] = []
    if "saida" not in st.session_state:
        st.session_state["saida"] = None
    if "esteira" not in st.session_state:
        st.session_state["esteira"] = None
    if "detalhes_dispositivo" not in st.session_state:
        st.session_state["detalhes_dispositivo"] = []  # Inicializa como lista vazia


