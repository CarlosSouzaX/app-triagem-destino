import pandas as pd
from modulo.verificar_imei import verificar_imei


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
        # Valida a entrada
        if not device_input.strip():
            return {"status": "warning", "message": "Por favor, insira um valor válido para o Device."}

        # Converte para float
        device_input_float = float(device_input.strip())

        # Verifica se a coluna "device" existe
        if "device" not in df.columns:
            return {"status": "error", "message": "A coluna 'Device' não existe no DataFrame."}

        # Filtra pelo Device
        resultado = df.loc[df["device"] == device_input_float, df.columns[1:7]]
        if resultado.empty:
            return {"status": "error", "message": f"Device '{device_input}' não encontrado no DataFrame."}

        # Inicializa o resultado parcial
        resultado_final = {"status": "success", "detalhes": []}

        # Verifica a marca
        marca = resultado.iloc[0, 1]  # Supondo que "marca" está na segunda coluna
        if pd.notnull(marca):
            resultado_final["detalhes"].append({"campo": "marca", "status": "success", "valor": marca})
        else:
            resultado_final["detalhes"].append({"campo": "marca", "status": "error", "valor": "Marca Não Disponível / Vazia"})

        # Verifica o IMEI
        imei = resultado.iloc[0, 3]  # Supondo que "imei" está na quarta coluna
        imei_status = "error"
        if pd.notnull(imei):
            try:
                imei_int = int(imei)  # Converte para inteiro
                if verificar_imei(imei_int):
                    imei_status = "success"
                    resultado_final["detalhes"].append({"campo": "imei", "status": "success", "valor": imei_int})
                else:
                    imei_status = "warning"
                    resultado_final["detalhes"].append({"campo": "imei", "status": "warning", "valor": "IMEI Não Válido"})
            except ValueError:
                imei_status = "warning"
                resultado_final["detalhes"].append({"campo": "imei", "status": "warning", "valor": "IMEI Não Válido"})
        else:
            resultado_final["detalhes"].append({"campo": "imei", "status": "error", "valor": "IMEI Não Disponível / Vazia"})
        
        # Verifica o Modelo
        modelo = resultado.iloc[0, 2]  # Supondo que "modelo" está na terceira coluna
        if pd.notnull(modelo):
            if imei_status == "success":
                resultado_final["detalhes"].append({"campo": "modelo", "status": "success", "valor": modelo})
            else:
                resultado_final["detalhes"].append({"campo": "modelo", "status": "warning", "valor": "Modelo Duvidoso"})
        else:
            resultado_final["detalhes"].append({"campo": "modelo", "status": "error", "valor": "Modelo Não Disponível / Vazio"})


        return resultado_final

    except ValueError:
        return {"status": "error", "message": "O valor inserido deve ser numérico."}