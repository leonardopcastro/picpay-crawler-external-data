import json
from datetime import datetime

from aws.aws_layer import save_file_into_s3
from config.config import Config


def log(event: dict, context: dict):
    '''
    Criação de log para a extração dos dados

    :param event:
    :param context:
    :return:
    '''
    bucket_key = Config.BUCKET_ERROR_KEY if isinstance(event, dict) and event.get('error') else Config.BUCKET_LOG_KEY
    key = f'{bucket_key}/picpay_crawler_external_data_log_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")}.txt'

    save_file_into_s3(data=json.dumps(event), bucket=Config.BUCKET_NAME, key=key)
