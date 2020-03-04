import boto3
import json
import os

try:
    from aws import KEYS  
    AWS_ACCESS_KEY_ID = KEYS.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = KEYS.AWS_SECRET_ACCESS_KEY
    SQLALCHEMY_DATABASE_URI = KEYS.SQLALCHEMY_DATABASE_URI
    MAIL_PASSWORD = KEYS.MAIL_PASSWORD
    SECRET_KEY = KEYS.SECRET_KEY
    DEBUG = True

except: 
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID'] 
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']     
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = False


s3_resource = boto3.resource('s3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key= AWS_SECRET_ACCESS_KEY)

s3_client = boto3.client('s3',
         aws_access_key_id=AWS_ACCESS_KEY_ID,
         aws_secret_access_key= AWS_SECRET_ACCESS_KEY)


class BaseConfig:
    
    s3_resource = s3_resource
    s3_client = s3_client

    SECRET_KEY = SECRET_KEY
    S3_LOCATION = "https://writing-lms.s3.ap-northeast-1.amazonaws.com/"
    S3_BUCKET_NAME = 'writing-lms'      
    AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI      
    MAIL_PASSWORD = MAIL_PASSWORD
    DEBUG = DEBUG
        






