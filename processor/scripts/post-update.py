import boto3

service_name = "image-processor"
BUCKET_SERVICES = "lambda-scripts-my-projects"


_lambda = boto3.client("lambda")

try:
    _lambda.update_function_code(
        FunctionName=f"{service_name}",
        S3Bucket=BUCKET_SERVICES,
        S3Key=f"{service_name}/package.zip",
        Publish=True,
    )
except Exception as e:
    print(e)
