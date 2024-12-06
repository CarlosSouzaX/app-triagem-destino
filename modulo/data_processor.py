import pandas as pd

def buscar_modelo_por_device(df, device_input):
    """
    Realiza a busca do modelo e informações associadas a partir do número do Device.

    Args:
        df (pd.DataFrame): DataFrame com os dados.
        device_input (str): Número do Device fornecido pelo usuário.

    Returns:
        dict: Dicionário com status e informações da busca (marca, IMEI ou mensagens de erro).
    """
    try:
        if not device_input.strip():
            return {"status": "warning", "message": "Por favor, insira um valor válido para o Device."}
        
        # Converter o input para float
        device_input_float = float(device_input.strip())
        
        if "device" in df.columns:
            # Filtrar pelo Device no DataFrame
            resultado = df.loc[df["device"] == device_input_float, df.columns[1:7]]
            if not resultado.empty:
                # Verificar e exibir a marca
                marca = resultado.iloc[0, 1]
                imei = None
                if pd.notnull(resultado.iloc[0, 3]):
                    try:
                        imei = int(resultado.iloc[0, 3])
                    except ValueError:
                        imei = "Valor inválido"

                return {
                    "status": "success",
                    "marca": marca if pd.notnull(marca) else "Marca não disponível",
                    "imei": imei if imei else "IMEI não disponível",
                }
            else:
                return {"status": "error", "message": f"Device '{device_input}' não encontrado no DataFrame."}
        else:
            return {"status": "error", "message": "As colunas 'Device' e/ou 'Modelo' não existem no DataFrame."}
    except ValueError:
        return {"status": "error", "message": "O valor inserido deve ser numérico."}
