import cv2
import boto3

s3 = boto3.client('s3')
def download_pdf(path_s3, name_file):
    try:
        s3.download_file('full-image', path_s3, f"/tmp/{name_file}")
        return True
    except Exception as e:
        print(e)
        return False

def lambda_handler(event, context):
    s3_object = event["Records"][0]["s3"]["object"]
    user_name = s3_object.get("key", '').split('/')[0].replace("+", " ")
    pic_name = s3_object.get("key", '').split('/')[1]

    if download_pdf(f"{user_name}/{pic_name}", pic_name):
        img = cv2.imread(f"/tmp/{pic_name}")
        face = get_only_face(img)
        if face is None:
            print("Face not found")
            return None

        cv2.imwrite(f"/tmp/face_{pic_name}", face)
        s3.upload_file(f"/tmp/face_{pic_name}", 'face-people-identifier', f"{user_name}/face_{pic_name}")


def get_only_face(img):
    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    rects = face_detector.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    
    if len(rects) == 0 or len(rects) > 1:
        return None

    for (x, y, w, h) in rects:
        image_to_show = img[y:y+h, x:x+w]

    return image_to_show



event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-2', 'eventTime': '2023-09-11T22:53:32.458Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDARUB7AMPK7BDGOGMNA'}, 'requestParameters': {'sourceIPAddress': '143.208.41.19'}, 'responseElements': {'x-amz-request-id': 'SEEJVY42KDWERGQX', 'x-amz-id-2': 'jmG4KCDEu6urFHS05wd4pfAm65dlFV/1msomJL4lnN1rBPUom+plMjUT5fP7zW8qss122rOgKVEiSTJlNsydfJIluXPc1mhD31XFvnJopQc='}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': '4fede7c5-5f67-4ca6-afac-46dddbf78aa8', 'bucket': {'name': 'people-identifier', 'ownerIdentity': {'principalId': 'A3BQLQP86TY9PJ'}, 'arn': 'arn:aws:s3:::people-identifier'}, 'object': {'key': 'Luan+3.14eri+Santos/14e461fbff7c3654ad0123dca7c50b20.png', 'size': 15664, 'eTag': 'cc606fd729dd0ca957b7c5a712044062', 'sequencer': '0064FF9A6C0C2E89C0'}}}]}

lambda_handler(event, None)