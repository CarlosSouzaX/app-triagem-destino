import streamlit as st

def runoff_flow():
    """
    Fluxo estático para RUNOFF, agora com navegabilidade por etapas.
    """

    st.title("Fluxo de Formulário - RUNOFF")

    # Inicializa o estado da pergunta atual
    if "current_question" not in st.session_state:
        st.session_state.current_question = 1

    # Perguntas estáticas
    questions = {
        1: {
            "question": "O contrato expirou?",
            "options": ["Sim", "Não"],
            "next": { "Sim": 2, "Não": 3 }
        },
        2: {
            "question": "Há saldo remanescente?",
            "options": ["Sim", "Não"],
            "next": { "Sim": 4, "Não": 5 }
        },
        3: {
            "question": "O cliente deseja renovar o contrato?",
            "options": ["Sim", "Não"],
            "next": { "Sim": 6, "Não": 7 }
        },
        4: {
            "question": "O saldo será devolvido?",
            "options": ["Sim", "Não"],
            "next": { "Sim": 8, "Não": "END1" }
        },
        5: {
            "question": "Deve ser arquivado sem saldo?",
            "options": ["Sim", "Não"],
            "next": { "Sim": "END2", "Não": "END3" }
        },
        6: {
            "question": "Há uma oferta de renovação?",
            "options": ["Sim", "Não"],
            "next": { "Sim": "END4", "Não": "END5" }
        },
        7: {
            "question": "Deseja oferecer um plano alternativo?",
            "options": ["Sim", "Não"],
            "next": { "Sim": "END6", "Não": "END7" }
        },
        8: {
            "question": "O saldo foi processado?",
            "options": ["Sim", "Não"],
            "next": { "Sim": "END8", "Não": "END9" }
        }
    }

    # Obtém a pergunta atual
    current_question = st.session_state.current_question
    question_data = questions.get(current_question)

    if question_data:
        # Exibe a pergunta atual
        response = st.radio(question_data["question"], question_data["options"], key=f"q{current_question}")
        if st.button("Próximo", key=f"next{current_question}"):
            next_step = question_data["next"].get(response)
            if isinstance(next_step, int):
                st.session_state.current_question = next_step
            else:
                st.success(f"Saída Final: {next_step}")
                st.session_state.current_question = 1  # Reinicia o fluxo
    else:
        st.error("Erro no fluxo. Contate o administrador.")
