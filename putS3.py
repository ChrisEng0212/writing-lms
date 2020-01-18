from aws import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SCHEMA


from pprint import pprint
import os
import boto3
import json

s3_resource = boto3.resource('s3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key= AWS_SECRET_ACCESS_KEY)


def putJson(file, course):

    courseList = [
        'blank',       #0
        "writing-lms"  #1 
        ]
    fileList = [
        'blank',       #0
        "json_files/meta.json", #1
        "json_files/sources.json"  #2
        ]
    string = "static/" + fileList[file]
    bucket = courseList[course]
    key = fileList[file]
    with open(string, "r") as f:
        jload = json.load(f)
    jstring = json.dumps(jload)
    s3_resource.Bucket(bucket).put_object(
        Key=key, Body=jstring)
    return [bucket, key]


course = 1
file = 2
 
result = putJson(file, course)
print('json put in', result )