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


def reset_estado():
    """Reseta o estado da triagem."""
    st.session_state["progresso"] = 0
    st.session_state["respostas"] = []
    st.session_state["saida"] = None

def exibir_perguntas_respondidas(perguntas, respostas):
    """Exibe as perguntas já respondidas."""
    st.subheader("📝 Perguntas Respondidas")
    for i, resposta in enumerate(respostas):
        st.markdown(f"**{i + 1}. {perguntas[i]['texto']}**")
        st.write(f"Resposta: **{resposta}**")

def processar_resposta(pergunta_atual, resposta):
    """Atualiza o progresso ou determina a saída final."""
    destino = pergunta_atual[resposta]
    if "saida" in destino:
        st.session_state["saida"] = destino["saida"]
    elif "proxima" in destino:
        st.session_state["progresso"] = destino["proxima"]

def obter_entradas(esteira):
    """Retorna as entradas de triagem com base na esteira."""
    entradas_por_esteira = {
        "RUNOFF": [
            {"texto": "O produto é da marca Xiaomi, Apple ou Motorola?", "sim": {"proxima": 1}, "nao": {"proxima": 2}},
            {"texto": "O Mi/FMiP está bloqueado?", "sim": {"saida": "Rejeitar SR"}, "nao": {"proxima": 2}},
            {"texto": "Há danos estéticos?", "sim": {"saida": "Saída 2"}, "nao": {"saida": "Saída 3"}},
        ],
        "PADRÃO": [
            {"texto": "O produto está na garantia?", "sim": {"proxima": 1}, "nao": {"proxima": 2}},
            {"texto": "O produto está funcional?", "sim": {"saida": "Saída 4"}, "nao": {"proxima": 2}},
            {"texto": "Há defeitos graves?", "sim": {"saida": "Saída 5"}, "nao": {"saida": "Saída 6"}},
        ],
    }
    return entradas_por_esteira.get(esteira, [])
