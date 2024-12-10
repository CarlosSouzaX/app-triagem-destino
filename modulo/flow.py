import streamlit as st

def runoff_flow():
    st.title("Fluxo de Formulário - RUNOFF")

    # Pergunta 1
    contract_expired = st.radio("O contrato expirou?", ["Sim", "Não"])

    if contract_expired == "Sim":
        # Pergunta 2
        has_balance = st.radio("Há saldo remanescente?", ["Sim", "Não"])

        if has_balance == "Sim":
            # Pergunta 4
            refund_balance = st.radio("O saldo será devolvido?", ["Sim", "Não"])
            
            if refund_balance == "Sim":
                # Pergunta 8
                balance_processed = st.radio("O saldo foi processado?", ["Sim", "Não"])
                
                if balance_processed == "Sim":
                    st.success("Saída: SALDO DEVOLVIDO E PROCESSO ENCERRADO.")
                else:
                    st.success("Saída: PROCESSAR SALDO PENDENTE.")
            else:
                st.success("Saída: ENCERRAR CONTRATO SEM DEVOLUÇÃO DE SALDO.")
        else:
            # Pergunta 5
            archive_no_balance = st.radio("Deve ser arquivado sem saldo?", ["Sim", "Não"])
            
            if archive_no_balance == "Sim":
                st.success("Saída: PROCESSO ARQUIVADO SEM SALDO.")
            else:
                st.success("Saída: VERIFICAR MOTIVO DO NÃO ARQUIVAMENTO.")
    elif contract_expired == "Não":
        # Pergunta 3
        wants_renewal = st.radio("O cliente deseja renovar o contrato?", ["Sim", "Não"])
        
        if wants_renewal == "Sim":
            # Pergunta 6
            offer_renewal = st.radio("Há uma oferta de renovação?", ["Sim", "Não"])
            
            if offer_renewal == "Sim":
                st.success("Saída: RENOVAÇÃO INICIADA.")
            else:
                st.success("Saída: SEM OFERTAS DISPONÍVEIS PARA RENOVAÇÃO.")
        else:
            # Pergunta 7
            alternative_plan = st.radio("Deseja oferecer um plano alternativo?", ["Sim", "Não"])
            
            if alternative_plan == "Sim":
                st.success("Saída: OFERTAR PLANO ALTERNATIVO.")
            else:
                st.success("Saída: SEM PLANOS DISPONÍVEIS, ACOMPANHAR CLIENTE.")
