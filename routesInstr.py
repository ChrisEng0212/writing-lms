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
SCHEMA = BaseConfig.SCHEMA
DESIGN = BaseConfig.DESIGN
STUDENTID = []

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


@app.route('/courseCheck', methods=['POST'])
def courseCheck():  
    SOURCES = loadAWS('json_files/sources.json', 0)   
    print(SOURCES)       
    course = json.dumps(SOURCES['schedule'])     
    color = json.dumps(DESIGN)    
    return jsonify({'course' : course, 'color' : color})


@app.route("/course", methods = ['GET', 'POST'])
@login_required
def course():     
    return render_template('instructor/course.html')


@app.route('/upload/<string:assignment>', methods=['POST', 'GET'])
def upload(assignment):
    file = request.files['file']
    fn = file.filename
    file_name = current_user.username + '_' + fn + '_' + assignment + '.mp3'   
    my_bucket = s3_resource.Bucket(S3_BUCKET_NAME)
    my_bucket.Object(file_name).put(Body=file)

    return redirect(request.referrer)
