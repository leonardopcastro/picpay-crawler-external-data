import os

class Config:
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    BUCKET_ERROR_KEY = os.getenv('BUCKET_ERROR_KEY')
    BUCKET_LOG_KEY = os.getenv('BUCKET_LOG_KEY')