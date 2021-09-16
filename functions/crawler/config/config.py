import os

class Config:
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    BUCKET_EXTRACT_KEY = os.getenv('BUCKET_EXTRACT_KEY')
    BUCKET_METADATA_KEY = os.getenv('BUCKET_METADATA_KEY')