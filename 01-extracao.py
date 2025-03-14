import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import os
from dotenv import load_dotenv

def request_julia(data_inicio, data_fim, quantidade=10000, termo_pesquisa="", max_retries=3, retry_delay=5):
    url = (
        f'https://juliapesquisa.trf5.jus.br/julia-pesquisa/api/v1/documento:dt/G2?draw=1'
        f'&columns[0][data]=codigoDocumento&columns[0][name]=&columns[0][searchable]=true'
        f'&columns[0][orderable]=false&columns[0][search][value]=&columns[0][search][regex]=false'
        f'&start=0&length={quantidade}&search[value]={termo_pesquisa}&search[regex]=true'
        f'&pesquisaLivre=&numeroProcesso=&orgaoJulgador=&relator=&dataIni={data_inicio}'
        f'&dataFim={data_fim}&_=1720108965511'
    )
    
    attempts = 0
    while attempts < max_retries:
        try:
            req = requests.get(url, timeout=10)
            req.raise_for_status()
            print(f"Status da Requisição: {req.status_code}")
            req_json = req.json()
            print(f"Quantidade de Documentos Coletados: {len(req_json['data'])}")
            return req_json
        except (requests.RequestException, ValueError) as e:
            print(f"Erro na requisição: {e}. Tentativa {attempts + 1} de {max_retries}...")
            attempts += 1
            time.sleep(retry_delay)
    
    print("Falha ao obter os dados após múltiplas tentativas.")
    return None

def generate_monthly_dates(start_date, end_date):
    start_date = datetime.strptime(start_date, '%d/%m/%Y')
    end_date = datetime.strptime(end_date, '%d/%m/%Y')
    
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime('%d/%m/%Y'))
        current_date += relativedelta(months=1)
    
    return dates

def main(data_inicio,data_fim):
    
    load_dotenv()
    
    date_list = generate_monthly_dates(inicio, fim)
    
    print(date_list)
    
    data_path = os.getenv('PATH_DADOS', './dados')
    os.makedirs(data_path, exist_ok=True)
    
    for i in range(len(date_list) - 1):
        data_inicio = date_list[i]
        data_fim = date_list[i + 1]
        print(f'Data de Início: {data_inicio}')
        data = request_julia(data_inicio, data_fim)
        
        if data and 'data' in data:
            cada_data = pd.DataFrame(data['data'])
            file_path = os.path.join(data_path, f"Dados_{data_inicio.replace('/', '_')}.parquet")
            cada_data.to_parquet(file_path)
            print(f"Arquivo salvo: {file_path}")
            time.sleep(10)
        else:
            print(f"Nenhum dado salvo para {data_inicio} - {data_fim}")

if __name__ == '__main__':
    main()
