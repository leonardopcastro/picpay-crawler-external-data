import importlib
from datetime import datetime

from aws.aws_layer import save_file_into_s3
from config.config import Config


def crawler(event: dict, context: dict):
    ''''
    Faz a extração dos dados externos conforme os parâmetros passados

    :param event: contém os parâmetros que vão ser usados na extração
        - folder: string da pasta do external_data
        - file: arquivo .py da pasta do external_data/folder
        - params: parâmetros da função de extração
    '''

    # Parâmetros da extração
    name = event['name']
    file = event['file']
    folder = event['folder']
    params = event['params']

    # Importação da exportação
    f = importlib.import_module(f'external_data.{folder}.{file}')

    # Exportação
    data = f.extract(**params)

    # retorna o resultado para s3
    if data:
        save_file_into_s3(data, Config.BUCKET_NAME, f'{Config.BUCKET_EXTRACT_KEY}/{folder}_{file}_{name}_{datetime.now().strftime("%Y_%m_%d")}.json')

if __name__ == '__main__':
    crawler({'name':'selic', 'folder': 'bacen', 'file': 'historic_series', 'params': {'url': 'https://www3.bcb.gov.br/sgspub/consultarvalores/consultarValoresSeries.do?method=consultarValores', 'series': 11, 'start_date': '1900-01-01', 'end_date': ''}}, None)