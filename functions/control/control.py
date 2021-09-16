import json
from datetime import datetime

from aws.aws_layer import get_file_from_s3, save_file_into_s3
from config.config import Config


def control(event: dict, context: dict) -> list:
    '''
    Controla os metadados da extração

    :param event:
    :param context:
    '''

    # Pega os metadados no s3
    data = get_file_from_s3(Config.BUCKET_NAME, f'{Config.BUCKET_METADATA_KEY}/data.json')

    # Atualiza a data inicial de cada parametro
    for item in data:
        if 'start_date' in item['params']:
            item['params']['start_date'] = datetime.now().strftime('%Y-%m-%d')

    # Salva nova versão no s3
    save_file_into_s3(json.dumps(data), Config.BUCKET_NAME, f'{Config.BUCKET_METADATA_KEY}/data.json')

    # Retorno dos metadados das extrações
    return data

if __name__ == '__main__':
    control(None, None)