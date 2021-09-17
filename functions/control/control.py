import copy
import yaml
from datetime import datetime

from aws.aws_layer import get_file_from_s3, save_file_into_s3
from config.config import Config


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

    # # Atualiza a data inicial de cada parametro
    cp_data = copy.deepcopy(metadata)
    for item in cp_data:
        if 'start_date' in item['params']:
            item['params']['start_date'] = datetime.now().strftime('%Y-%m-%d')

    # Salva nova versão no s3
    save_file_into_s3(yaml.dump(metadata), Config.BUCKET_NAME, f'{Config.BUCKET_METADATA_KEY}/metadata.yaml')

    # Retorno dos metadados das extrações
    return metadata

if __name__ == '__main__':
    control({}, None)