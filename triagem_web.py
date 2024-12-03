import streamlit as st

# Dados de triagem simplificados
entradas = {
    "Entrada 1": {"pergunta": "O produto está bloqueado?", "saida_sim": "Saída 1", "saida_nao": "Saída 2"},
    "Entrada 2": {"pergunta": "O produto está funcional?", "saida_sim": "Saída 3", "saida_nao": "Saída 4"},
    "Entrada 3": {"pergunta": "Há danos estéticos?", "saida_sim": "Saída 5", "saida_nao": "Saída 6"},
    "Entrada 4": {"pergunta": "O cliente deseja reembolso?", "saida_sim": "Saída 7", "saida_nao": "Saída 8"},
    "Entrada 5": {"pergunta": "O produto está na garantia?", "saida_sim": "Saída 1", "saida_nao": "Saída 3"},
}

# Inicialização do estado
if "entrada_selecionada" not in st.session_state:
    st.session_state["entrada_selecionada"] = None
    st.session_state["resposta"] = None
    st.session_state["saida"] = None

# Interface do Streamlit
st.title("Sistema de Triagem - Escolha e Responda")

# Seleção da entrada
entrada_atual = st.selectbox(
    "Selecione a Entrada", 
    options=["Selecione uma entrada"] + list(entradas.keys()),
)

# Resetar o estado ao mudar a entrada
if entrada_atual != st.session_state["entrada_selecionada"]:
    st.session_state["entrada_selecionada"] = entrada_atual
    st.session_state["resposta"] = None
    st.session_state["saida"] = None

# Mostrar a pergunta correspondente
if entrada_atual in entradas:
    pergunta = entradas[entrada_atual]["pergunta"]
    
    # Adicionar placeholder "Escolha uma opção"
    resposta = st.radio(
        pergunta,
        options=["Escolha uma opção", "sim", "não"],
        index=0,  # Sempre começa com o placeholder selecionado
        key=f"pergunta_{entrada_atual}"
    )
    
    if resposta != "Escolha uma opção":
        st.session_state["resposta"] = resposta
        # Determinar a saída com base na resposta
        saida = entradas[entrada_atual]["saida_sim"] if resposta == "sim" else entradas[entrada_atual]["saida_nao"]
        st.session_state["saida"] = saida
        st.success(f"Resposta: {resposta} → {saida}")

# Exibir resposta final
if st.session_state["saida"]:
    st.write(f"Destino Final: **{st.session_state['saida']}**")
