import boto3

def save_file_into_s3(data: str, bucket: str, key: str):
    '''
    Realiza o upload de um arquivo para o s3

    :param bucket: Nome do bucket localizado no s3
    :param key: Caminho do arquivo dentro do bucket
    '''
    client = boto3.client('s3')

    client.put_object(Body=data, Bucket=bucket, Key=key)