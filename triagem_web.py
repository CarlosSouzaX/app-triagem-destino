import streamlit as st

# Dados de triagem
entradas = {
    "Análise Meli": {
        "perguntas": [
            {"texto": "O produto está bloqueado?", "corte": True},
            {"texto": "O produto está funcional?", "corte": False},
            {"texto": "Há danos estéticos?", "corte": False}
        ],
        "decisoes": {
            ("sim",): "Destino: Produto Bloqueado",
            ("sim", "não", "não"): "AT LN",
            ("sim", "sim", "não"): "IN-HOUSE LN",
            ("não", "sim", "sim"): "Fábrica de Reparos",
            ("não", "não", "não"): "Qualidade",
        }
    },
    "RunOff": {
        "perguntas": [
            {"texto": "O produto está bloqueado?", "corte": True},
            {"texto": "O produto está dentro da garantia?", "corte": False},
            {"texto": "Há defeitos funcionais?", "corte": False},
            {"texto": "O cliente solicitou reembolso?", "corte": False}
        ],
        "decisoes": {
            ("sim",): "Destino: Produto Bloqueado",
            ("sim", "não", "não", "não"): "AT Same",
            ("sim", "sim", "não", "não"): "Fábrica de Reparos",
            ("não", "sim", "sim", "sim"): "Qualidade",
            ("não", "não", "não", "não"): "IN-HOUSE Same",
        }
    },
}

# Função para decidir o destino com base nas respostas
def decidir_destino(entrada, respostas):
    dados = entradas.get(entrada)
    respostas_tuple = tuple(respostas)
    return dados["decisoes"].get(respostas_tuple, "Destino não definido")

# Função para resetar o formulário
def reset_form():
    st.session_state["progresso"] = 0
    st.session_state["respostas"] = []

# Interface Streamlit
st.title("Sistema de Triagem de Produtos")

# Inicialização do estado
if "entrada_selecionada" not in st.session_state:
    st.session_state["entrada_selecionada"] = None
    st.session_state["progresso"] = 0
    st.session_state["respostas"] = []

# Seleção da entrada
entrada_atual = st.selectbox(
    "Selecione a Entrada", 
    options=list(entradas.keys()), 
    index=0 if st.session_state["entrada_selecionada"] is None else list(entradas.keys()).index(st.session_state["entrada_selecionada"])
)

# Resetar progresso ao mudar a entrada
if entrada_atual != st.session_state["entrada_selecionada"]:
    st.session_state["entrada_selecionada"] = entrada_atual
    reset_form()

# Recuperar perguntas e progresso
perguntas = entradas[st.session_state["entrada_selecionada"]]["perguntas"]
progresso = st.session_state["progresso"]
respostas = st.session_state["respostas"]

# Exibir perguntas respondidas anteriormente
for i in range(progresso):
    st.write(f"**Pergunta {i + 1}: {perguntas[i]['texto']}**")
    st.write(f"Resposta: {respostas[i]}")

# Exibir a próxima pergunta
if progresso < len(perguntas):
    pergunta_atual = perguntas[progresso]
    resposta = st.radio(
        pergunta_atual["texto"], 
        options=["sim", "não"], 
        key=f"pergunta_{progresso}"
    )
    if resposta:
        respostas.append(resposta)
        st.session_state["respostas"] = respostas

        # Interromper fluxo se pergunta de corte for respondida com "sim"
        if pergunta_atual["corte"] and resposta == "sim":
            destino = decidir_destino(entrada_atual, respostas)
            st.success(f"O destino recomendado é: {destino}")
            reset_form()
        else:
            st.session_state["progresso"] += 1

# Botão "Voltar" para corrigir respostas anteriores
if progresso > 0:
    if st.button("Voltar"):
        st.session_state["progresso"] -= 1
        respostas.pop()
        st.session_state["respostas"] = respostas

# Mostrar botão Enviar quando todas as perguntas forem respondidas
if progresso == len(perguntas):
    if st.button("Enviar"):
        destino = decidir_destino(entrada_atual, respostas)
        st.success(f"O destino recomendado é: {destino}")
        reset_form()
