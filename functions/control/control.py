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

    # Seleciona quais bases vão ser extraidas e atualiza registros
    data = []
    date_now = datetime.date(datetime.now())
    for d in metadata:
        if not d.get('update_at'):
            data.append(d)
            d['update_at'] = date_now.strftime('%Y-%m-%d')
        else:
            if (d['update_frequency'] == 'year' and d['update_at'].year != date_now.year) or \
                    (d['update_frequency'] == 'month' and d['update_at'].month != date_now.month) or \
                    (d['update_frequency'] == 'day' and d['update_at'].day != date_now.day):
                data.append(d)
                d['update_at'] = date_now.strftime('%Y-%m-%d')

    # Salva nova versão no s3
    if data:
        save_file_into_s3(yaml.dump(metadata), Config.BUCKET_NAME, f'{Config.BUCKET_METADATA_KEY}/metadata.yaml')

    # Retorno dos metadados das extrações
    return data

if __name__ == '__main__':
    control({}, None)