from pymongo import MongoClient
import boto3

client = MongoClient('mongodb+srv://test:sparta@cluster0.temtprh.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.animal

s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id='USER01',
            aws_secret_access_key='qBxZXr5{')

def s3_connection():
    try:
        s3
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3

s3 = s3_connection()

