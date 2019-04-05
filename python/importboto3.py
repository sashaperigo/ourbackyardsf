import boto3
import botocore

Bucket = "aws-practitioner-cert"
Key = "index.html"
outPutName = "index.html"
uploadname = "updatedIndex.html"

s3 = boto3.resource('s3')
try:
    s3.Bucket(Bucket).download_file(Key, outPutName)
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise

s3 = boto3.client('s3')
s3.upload_file(Key,Bucket,uploadname)