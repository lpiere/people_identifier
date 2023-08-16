import os
import dlib
import cv2
import boto3

s3 = boto3.client('s3')
def download_pdf(path_s3, name_file):
    try:
        s3.download_file('people-identifier', path_s3, f"/tmp/{name_file}")
        return True
    except Exception as e:
        print(e)
        return False



def lambda_handler(event, context):
    s3_object = event["Records"][0]["s3"]["object"]
    user_name = s3_object.get("key", '').split('/')[0].replace("+", " ")
    pic_name = s3_object.get("key", '').split('/')[1]

    print(user_name, pic_name)
    if download_pdf(f"{user_name}/{pic_name}", pic_name):
        img = cv2.imread(f"/tmp/{pic_name}")
        face = get_only_face(img)
        if face is None:
            print("Face not found")
            return None
        
        
        
        cv2.imwrite(f"/tmp/face_{pic_name}", face)
        s3.upload_file(f"/tmp/face_{pic_name}", 'face-people-identifier', f"{user_name}/face_{pic_name}")


def get_only_face(img):
    face_detector = dlib.get_frontal_face_detector()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rects = face_detector(img_gray, 0)
    
    if len(rects) == 0:
        return None

    for rect in rects:
        x = rect.tl_corner().x
        y = rect.tl_corner().y
        x2 = rect.br_corner().x
        y2 = rect.br_corner().y

        image_to_show = img[y:y2, x:x2]

    return image_to_show

# lambda_handler({'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-2', 'eventTime': '2023-08-15T23:43:52.329Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDARUB7AMPK7BDGOGMNA'}, 'requestParameters': {'sourceIPAddress': '138.99.251.117'}, 'responseElements': {'x-amz-request-id': 'JAEH8CJQANQ55Y5T', 'x-amz-id-2': 'xgZDC/92WQDtd6V5d6aS8QaKfGg0wxws0OUOGRSwNKHr/3DeLVjLsr7TCHVHLZsqGQWhLCZt5rcUdqe3SLLVa96lB488/IlESBIkpGcA3AI='}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'b0810fb6-5a00-444d-aae7-51aea29f08b0', 'bucket': {'name': 'people-identifier', 'ownerIdentity': {'principalId': 'A3BQLQP86TY9PJ'}, 'arn': 'arn:aws:s3:::people-identifier'}, 'object': {'key': 'Luan+3.14eri+Santos/d5e34b8e59474df1d236c3447a281a7a.png', 'size': 15664, 'eTag': 'cc606fd729dd0ca957b7c5a712044062', 'sequencer': '0064DC0DB7F411C482'}}}]}, None)