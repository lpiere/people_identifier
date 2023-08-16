import logging
import boto3
from botocore.exceptions import ClientError
import os


def upload_file(file_name, object_name):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, "people-identifier", object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True