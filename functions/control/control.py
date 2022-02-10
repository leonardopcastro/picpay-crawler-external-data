from aws.aws_layer import get_file_from_s3
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

    # Seleciona quais bases vão ser extraidas
    data = [d for d in metadata if d.get('is_active')]

    # Retorno dos metadados das extrações
    return data

if __name__ == '__main__':
    control({}, None)