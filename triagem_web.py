import streamlit as st

# Verificar se o Streamlit está rodando corretamente
st.title("Teste de Inicialização do Streamlit")

entrada = st.selectbox("Escolha uma entrada", ["Opção 1", "Opção 2", "Opção 3"])
st.write(f"Você selecionou: {entrada}")

if st.button("Avançar"):
    st.write("Botão Avançar clicado!")
