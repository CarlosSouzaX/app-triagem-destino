import streamlit as st

def runoff_flow():
    st.title("Fluxo de Formulário - RUNOFF")

    # Pergunta 1
    contract_expired = st.radio("O contrato expirou?", ["Sim", "Não"])

    if contract_expired == "Sim":
        # Pergunta 2
        has_balance = st.radio("Há saldo remanescente?", ["Sim", "Não"])
        
        if has_balance == "Sim":
            st.success("Saída: ENCERRAR O CONTRATO E PROCESSAR O SALDO.")
        else:
            st.success("Saída: ENCERRAR O CONTRATO SEM SALDO PENDENTE.")
    
    elif contract_expired == "Não":
        # Pergunta 3
        wants_renewal = st.radio("O cliente deseja renovar o contrato?", ["Sim", "Não"])
        
        if wants_renewal == "Sim":
            st.success("Saída: INICIAR PROCESSO DE RENOVAÇÃO.")
        else:
            st.success("Saída: ACOMPANHAR CLIENTE PARA OUTRAS OFERTAS.")
