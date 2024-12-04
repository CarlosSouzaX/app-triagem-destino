import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Configuração para acessar o Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS_FILE = 'credentials.json'  # Substitua pelo caminho do seu arquivo de credenciais

def read_google_sheets(spreadsheet_id, sheet_name, cell_range):
    """
    Lê dados de uma planilha do Google Sheets.
    Args:
        spreadsheet_id (str): ID da planilha do Google Sheets.
        sheet_name (str): Nome da aba dentro da planilha.
        cell_range (str): Intervalo de células a ser lido (ex.: "A1:C10").
    Returns:
        list: Dados do intervalo especificado.
    """
    try:
        # Credenciais da conta de serviço
        credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key(spreadsheet_id).worksheet(sheet_name)
        tabela = sheet.get(cell_range)
        return tabela
    except Exception as e:
        st.error(f"Erro ao acessar o Google Sheets: {e}")
        return None

# Configurações do Streamlit
st.title("Consulta no Google Sheets")

# ID da planilha e aba para consulta
SPREADSHEET_ID = "sua_planilha_id"  # Substitua pelo ID da sua planilha
SHEET_NAME = "Aba1"  # Substitua pelo nome da aba
CELL_RANGE = "A1:C100"  # Ajuste conforme necessário

# Entrada do usuário para consulta
valor_consulta = st.text_input("Insira um valor para consultar:")

if valor_consulta:
    # Lê os dados da planilha
    dados = read_google_sheets(SPREADSHEET_ID, SHEET_NAME, CELL_RANGE)

    if dados:
        # Converte os dados para um formato legível
        colunas = dados[0]  # Primeira linha contém os nomes das colunas
        registros = [dict(zip(colunas, linha)) for linha in dados[1:]]
        resultados = [registro for registro in registros if valor_consulta in registro.values()]

        # Exibe os resultados
        if resultados:
            st.write("Resultados Encontrados:")
            st.dataframe(resultados)
        else:
            st.warning("Nenhum resultado encontrado para o valor informado.")
