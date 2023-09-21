import logging
import boto3
from botocore.exceptions import ClientError
import os

s3_client = boto3.client('s3')

def upload_file(file_name, object_name):
    try:
        response = s3_client.upload_file(file_name, "full-image", object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True