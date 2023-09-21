import os
import boto3

s3_client = boto3.client('s3')
bucket_name = 'face-people-identifier'
if "face_data" not in os.listdir():
    os.mkdir("face_data")

def download_data_from_s3():
    users_names = get_users_names()
    for name in users_names:
        if name not in os.listdir("face_data"):
            os.mkdir(f"face_data/{name}")

        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=name)

        for obj in response.get('Contents', []):
            download_file(name, obj)

def download_file(name, obj):
    obj_key = obj['Key']
    obj_name = os.path.basename(obj_key)
    local_path = os.path.join(f"face_data/{name}/", obj_name)
    s3_client.download_file(bucket_name, obj_key, local_path)
    
def get_users_names():
    response = s3_client.list_objects_v2(Bucket=bucket_name, Delimiter='/')
    return [common_prefix.get('Prefix')[:-1] for common_prefix in response.get('CommonPrefixes', [])]


download_data_from_s3()