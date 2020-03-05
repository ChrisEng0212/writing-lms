import sys, boto3, random, base64, os, secrets, httplib2, json, ast
from sqlalchemy import asc, desc 
from datetime import datetime, timedelta
from flask import render_template, url_for, flash, redirect, request, abort, jsonify  
from app import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from forms import *   
from models import *
from pprint import pprint

from meta import BaseConfig   
s3_resource = BaseConfig.s3_resource  
S3_LOCATION = BaseConfig.S3_LOCATION
S3_BUCKET_NAME = BaseConfig.S3_BUCKET_NAME

def loadAWS(file, unit):   
    if unit == 0 :
        jList = [S3_BUCKET_NAME, file] 
        content_object = s3_resource.Object(  jList[0], jList[1]   )
    else:
        jList = [S3_BUCKET_NAME, file]
        content_object = s3_resource.Object(  jList[0], jList[1]   )

    file_content = content_object.get()['Body'].read().decode('utf-8')
    jload = json.loads(file_content)
    print(type(jload))

    return jload


@app.route ("/", methods = ['GET', 'POST'])
@app.route ("/home", methods = ['GET', 'POST'])
def home():     
    
    return render_template('instructor/home.html' )


@app.route ("/about")
@login_required 
def about():   

    return render_template('instructor/about.html', about=about, siteName=S3_BUCKET_NAME)


def get_schedule():
    content_object = s3_resource.Object( S3_BUCKET_NAME, 'json_files/sources.json' )
    file_content = content_object.get()['Body'].read().decode('utf-8')    
    SOURCES = json.loads(file_content)  # json loads returns a dictionary
    #print(SOURCES)   
    return (SOURCES)

@app.route("/tips", methods = ['GET', 'POST'])
@login_required
def tips(): 

    with open('static/json_files/sources.json', 'r') as f:
        srcJSON = json.load(f)
        
    tips = json.dumps(srcJSON['tips']) 

    return render_template('instructor/tips.html', tips=tips)


@app.route("/course", methods = ['GET', 'POST'])
@login_required
def course():  
    # json dumps returns a string
    course = json.dumps(get_schedule())   
    color = current_user.theme

    return render_template('instructor/course.html', course=course, color=color)


@app.route('/upload/<string:assignment>', methods=['POST', 'GET'])
def upload(assignment):
    file = request.files['file']
    fn = file.filename
    file_name = current_user.username + '_' + fn + '_' + assignment + '.mp3'   
    my_bucket = s3_resource.Bucket(S3_BUCKET_NAME)
    my_bucket.Object(file_name).put(Body=file)

    return redirect(request.referrer)

