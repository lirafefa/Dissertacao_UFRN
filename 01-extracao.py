import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import os
from dotenv import load_dotenv
load_dotenv()

def request_julia(data_inicio, data_fim, termo_pesquisa=""):
    quantidade = 10000
    # Modificando a URL para incluir o termo de pesquisa "ação coletiva"
    url = (
        f'https://juliapesquisa.trf5.jus.br/julia-pesquisa/api/v1/documento:dt/G2?draw=1'
        f'&columns[0][data]=codigoDocumento&columns[0][name]=&columns[0][searchable]=true'
        f'&columns[0][orderable]=false&columns[0][search][value]=&columns[0][search][regex]=false'
        f'&start=0&length={quantidade}&search[value]={termo_pesquisa}&search[regex]=true'
        f'&pesquisaLivre=&numeroProcesso=&orgaoJulgador=&relator=&dataIni={data_inicio}'
        f'&dataFim={data_fim}&_=1720108965511'
    )
    req = requests.get(url)
    print(f"Status da Requisição: {req.status_code}")
    req_json = req.json()
    print(f"Quantidade de Documentos Coletados: {len(req_json['data'])}")
    return req_json

# Definindo a função que gera as datas
def generate_monthly_dates(start_date, end_date):
    start_date = datetime.strptime(start_date, '%d/%m/%Y')
    end_date = datetime.strptime(end_date, '%d/%m/%Y')
    
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime('%d/%m/%Y'))
        current_date += relativedelta(months=1)
    
    return dates
if __name__=='__main__':
    # Definindo os intervalos de datas
    inicio = '01/11/2024'
    fim = '01/02/2025'

    load_dotenv()

    # Gerando as datas mensais
    date_list = generate_monthly_dates(inicio, fim)
    # print do intervalo de datas
    print(date_list)
    
    try:
        os.makedirs(os.getenv('PATH_DADOS'))
    except Exception as e:
        print(f'Erro {e}')

    # Coletando dados para cada intervalo de datas
    all_data = []
    textos = []
    for i in range(len(date_list) - 1):
        data_inicio = date_list[i]
        data_fim = date_list[i + 1]
        print(f'Data de Início: {data_inicio}')
        data = request_julia(data_inicio, data_fim)
        cada_data=pd.DataFrame(data['data'])
        cada_data.to_parquet(f"{os.getenv('PATH_DADOS')}/Dados_{str(data_inicio).replace('/','_')}.parquet")
        
        time.sleep(10)