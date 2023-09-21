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
            print(event)
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