import streamlit as st

def inicializar_estado():
    """
    Inicializa todas as variáveis de estado no `st.session_state`.
    """
    estados_padrao = {
        "inicializado": True,
        "fluxo_finalizado": False,
        "current_question": "Q1",
        "esteira": None,
        "responses": {},
        "marca": None,
        "modelo": None,
        "status_sr": None,
        "device_input": "",  # Adiciona o controle do campo de texto
    }
    for chave, valor in estados_padrao.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor

def resetar_estado():
    """
    Reseta o estado para os valores padrão e força recarregamento.
    """
    inicializar_estado()
    for chave in list(st.session_state.keys()):
        del st.session_state[chave]
    inicializar_estado()

def obter_estado(chave, valor_padrao=None):
    """
    Retorna o valor de uma variável de estado ou o valor padrão se não estiver definida.
    """
    return st.session_state.get(chave, valor_padrao)
