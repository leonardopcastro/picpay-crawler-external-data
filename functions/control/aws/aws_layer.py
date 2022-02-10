import boto3
import yaml


def list_files_from_s3(bucket: str, prefix: str) -> list:
    s3 = boto3.resource('s3')
    s3_bucket = s3.Bucket(bucket)

    objs = s3_bucket.objects.filter(Prefix=prefix)

    return [obj.key for obj in objs]

def get_file_from_s3(bucket: str, key: str) -> dict:
    '''
    Realiza o download de um arquivo do s3

    :param bucket: Nome do bucket localizado no s3
    :param key: Caminho do arquivo dentro do bucket
    '''
    s3 = boto3.client('s3')

    obj = s3.get_object(Bucket=bucket, Key=key)
    return yaml.load(obj['Body'].read())

def save_file_into_s3(data: str, bucket: str, key: str):
    '''
    Realiza o upload de um arquivo para o s3

    :param bucket: Nome do bucket localizado no s3
    :param key: Caminho do arquivo dentro do bucket
    '''
    client = boto3.client('s3')

    client.put_object(Body=data, Bucket=bucket, Key=key)