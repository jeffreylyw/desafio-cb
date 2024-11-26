import requests
import pandas as pd
import logging

def fetch_data_from_api(endpoint, payload):
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        data = response.json()

        df = pd.json_normalize(data)
        return df
    
    except requests.exceptions.Timeout:
        logging.error(f"Timeout ao acessar o endpoint: {endpoint} com payload: {payload}")
        raise

    except requests.exceptions.RequestException as error:
        logging.error(f"Erro na requisição para o endpoint: {endpoint} com payload: {payload}. Detalhes: {str(error)}")
        raise

    except ValueError as error:
        logging.error(f"Erro ao transformar resposta da API em JSON: {str(error)}")
        raise