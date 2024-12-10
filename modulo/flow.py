import streamlit as st

def runoff_flow():
    """
    Fluxo Funcional com avanço imediato no botão "Próximo".
    """

    st.title("Fluxo de Triagem - Funcional")

    # Inicializa o estado da pergunta atual e respostas, se não existir
    if "current_question" not in st.session_state:
        st.session_state.current_question = "Q1"
    if "responses" not in st.session_state:
        st.session_state.responses = {}

    # Estrutura estática do fluxo
    questions = {
        "Q1": {
            "question": "O IMEI está correto?",
            "options": ["Sim", "Não", "Não Sei"],
            "next": {
                "Sim": "Q2",
                "Não": "END_DevolverRecebimento",
                "Não Sei": "END_AT"
            }
        },
        "Q2": {
            "question": "O Modelo está correto?",
            "options": ["Sim", "Não"],
            "next": {
                "Sim": "Q3",
                "Não": "END_DevolverRecebimento"
            }
        },
        "Q3": {
            "question": "O dispositivo está na Blacklist?",
            "options": ["Sim - arrived", "Sim - tracked", "Não"],
            "next": {
                "Sim - arrived": "END_DevolverPicking",
                "Sim - tracked": "END_TriagemJuridico",
                "Não": "Q4_FMiP"
            }
        },
        "Q4_FMiP": {
            "question": "O dispositivo está com FMiP ativo?",
            "options": ["Sim - arrived", "Não"],
            "next": {
                "Sim - arrived": "END_DevolverPicking",
                "Não": "END_Bloqueio"
            }
        },
        "Q4.2": {
            "question": "Teve contato líquido?",
            "options": ["Sim", "Não"],
            "next": {
                "Sim": "END_Fabrica",
                "Não": "Q4.3"
            }
        },
        "Q4.3": {
            "question": "O sensor de umidade (gaveta do chip) está ativado?",
            "options": ["Sim", "Não"],
            "next": {
                "Sim": "END_Fabrica",
                "Não": "Q4.4"
            }
        },
        "Q4.4": {
            "question": "Tem evidências de carbonização?",
            "options": ["Sim", "Não"],
            "next": {
                "Sim": "END_Fabrica",
                "Não": "Q4.1"
            }
        },
        "Q4.1": {
            "question": "Teve dano por impacto?",
            "options": ["Sim", "Não"],
            "next": {
                "Sim": "END_Reparo",
                "Não": "Q4.5"
            }
        },
        "Q4.5": {
            "question": "O device está no período de garantia? (Moto, Samsung e Apple)",
            "options": ["Sim", "Não"],
            "next": {
                "Sim": "END_Garantia",
                "Não": "END_Reparo"
            }
        }
    }

    # Obter pergunta atual
    current_question = st.session_state.current_question
    question_data = questions.get(current_question)

    if question_data:
        # Inicializar resposta no estado, se ainda não existir
        if current_question not in st.session_state.responses:
            st.session_state.responses[current_question] = None

        # Adicionar uma opção inicial visível "Selecione uma opção"
        options = ["Selecione uma opção"] + question_data["options"]

        # Exibir pergunta
        st.write(f"**{question_data['question']}**")
        response = st.radio(
            "Escolha uma opção:",
            options=options,
            index=0,
            key=f"q{current_question}"
        )

        # Atualizar resposta no estado, ignorando a opção inicial
        if response != "Selecione uma opção":
            st.session_state.responses[current_question] = response

        # Habilitar botão "Próximo" apenas após uma resposta válida
        is_next_enabled = response != "Selecione uma opção"

        if st.button("Próximo", disabled=not is_next_enabled):
            # Avançar imediatamente para a próxima pergunta ou estado final
            next_step = question_data["next"].get(response)
            if next_step in final_states:
                st.success(f"Estado Final: {final_states[next_step]}")
                st.session_state.current_question = "Q1"
                st.session_state.responses = {}
            else:
                st.session_state.current_question = next_step
    else:
        st.warning("⚠️ Fluxo finalizado ou inválido. Reinicie o fluxo.")
        if st.button("Reiniciar"):
            st.session_state.current_question = "Q1"
            st.session_state.responses = {}