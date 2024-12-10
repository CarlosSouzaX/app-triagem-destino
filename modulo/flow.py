import streamlit as st

def runoff_flow():
    """
    Fluxo estático para RUNOFF com melhoria:
    O botão "Próximo" é habilitado somente após selecionar uma resposta.
    """

    st.title("Fluxo de Formulário - RUNOFF")

    # Inicializa o estado da pergunta atual e respostas
    if "current_question" not in st.session_state:
        st.session_state.current_question = 1
    if "responses" not in st.session_state:
        st.session_state.responses = {}

    # Estrutura estática do fluxo
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
        st.write(f"**Pergunta {current_question}:**")
        response = st.radio(
            question_data["question"],
            question_data["options"],
            index=-1,  # Nenhuma resposta selecionada inicialmente
            key=f"q{current_question}"
        )

        # Habilita o botão "Próximo" apenas se houver uma resposta selecionada
        is_next_enabled = response in question_data["options"]

        if st.button("Próximo", key=f"next{current_question}", disabled=not is_next_enabled):
            # Salva a resposta atual
            st.session_state.responses[current_question] = response
            # Avança para a próxima pergunta ou final
            next_step = question_data["next"][response]
            if isinstance(next_step, int):
                st.session_state.current_question = next_step
            else:
                st.success(f"Saída Final: {next_step}")
                # Reseta o fluxo após conclusão
                st.session_state.current_question = 1
                st.session_state.responses = {}
    else:
        st.error("Erro no fluxo. Contate o administrador.")
