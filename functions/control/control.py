import re
from datetime import datetime

from aws.aws_layer import get_file_from_s3, list_files_from_s3
from config.config import Config

def extract_max_date(files_name: list, start_date: str) -> datetime:
    '''
    Função para extração da maior data

    :param files_name: array com o nome dos arquivos
    :param start_date: data inicial da extração
    '''
    max_date = datetime.strptime(start_date, '%Y-%m-%d')
    for file_name in files_name:
        match = re.search('(\d{8})\.', file_name)
        if match:
            date = datetime.strptime(match.group(1), '%Y%m%d')
            max_date = date if date > max_date else max_date

    return max_date.strftime('%Y-%m-%d')

def control(event: dict, context: dict) -> list:
    '''
    Controla os metadados da extração

    :param event:
    :param context:
    '''

    if event.get('metadata'):
        return event.get('metadata')

    # Pega os metadados no s3
    metadata = get_file_from_s3(Config.BUCKET_NAME, f'{Config.BUCKET_METADATA_KEY}/metadata.yaml')

    # Seleciona quais bases vão ser extraidas
    data = []
    for d in metadata:
        if d.get('is_active'):
            prefix = f'{Config.BUCKET_EXTRACT_KEY}/{d["folder"]}_{d["file"]}_{d["name"]}'
            d['start_date'] = extract_max_date(list_files_from_s3(Config.BUCKET_NAME, prefix), d['start_date'])
            data.append(d)

    # Retorno dos metadados das extrações
    return data
