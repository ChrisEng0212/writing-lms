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
s3_client = BaseConfig.s3_client 
S3_LOCATION = BaseConfig.S3_LOCATION
S3_BUCKET_NAME = BaseConfig.S3_BUCKET_NAME
SCHEMA = BaseConfig.SCHEMA
STUDENTID = []


def loadAWS(file, unit):   
    if unit == 0 :
        key = file
        content_object = s3_resource.Object(  S3_BUCKET_NAME, key  )
    else:
        key = str(unit) + '/' + file
        
        content_object = s3_resource.Object(  S3_BUCKET_NAME, key   )
        print('SEARCH', content_object)
    try:
        file_content = content_object.get()['Body'].read().decode('utf-8')
        jload = json.loads(file_content)
        print(type(jload))
    except:
        jload = None

    return jload

def putAWS(unit, data): 

    keyName = (str(unit) + '/')  #adding '/' makes a folder object
    jData = json.dumps(data)    
    print (keyName)    
    s3_resource.Bucket(S3_BUCKET_NAME).put_object(Key=keyName) 
    object = s3_resource.Object(S3_BUCKET_NAME, keyName + current_user.username + '.json')         
    object.put(Body=jData) 
    print('Added: ' +  jData)  

    return keyName


SOURCES = loadAWS('json_files/sources.json', 0)   
#print(SOURCES)       
topics = json.dumps(SOURCES['sources'])


@app.route('/sendData', methods=['POST'])
def sendData():  
    unit = request.form ['unit']  
    stage = request.form ['stage'] 
    obj = request.form ['obj'] 
    name = current_user.username
    user = User.query.filter_by(username=name).first()  
    
    #### user dict with all info
    userDict = {}
    
    dataDict = ast.literal_eval(obj)    
    userDict['meta'] = {
        'name' : name, 
        'avatar' : user.avatar, 
        'image' : user.image_file, 
        'theme' : user.theme,
        'score' : stage
    }
    userDict['plan'] = dataDict
    
    putAWS(int(unit), userDict)
    
    return jsonify({'name' : name})


@app.route('/topicCheck', methods=['POST'])
def topicCheck():         
    return jsonify({'topics' : topics})


@app.route("/topic_list", methods = ['GET', 'POST'])
@login_required
def topic_list():       

    return render_template('work/topic_list.html')


@app.route('/jCheck/<string:check>/<string:unit>', methods=['POST'])
def jChecker(check, unit):
    print('ACTIVE')
    
    if check == 'plan':
        file = current_user.username + '.json'
        obj = loadAWS(file, int(unit))

    try:
        data = json.dumps(obj[check])
    except:
        data = 'None'

    print(data)

    return jsonify({'data' : data})




@app.route("/plan/<string:unit>", methods = ['GET', 'POST'])
@login_required
def plan(unit):     
    slides = SOURCES['sources'][unit]['Materials']
    return render_template('work/plan.html', unit=unit, slides=slides)





@app.route("/topic/<int:unit>", methods = ['GET', 'POST'])
@login_required
def topic(unit):  
    print ('done', unit)


    return render_template('work/topic.html', unit=unit)



@app.route('/audioUpload', methods=['POST', 'GET'])
def audioUpload():

    title = request.form ['title']
    audio_string = request.form ['base64']    

    if title and base64:         
        audio = base64.b64decode(audio_string)
        newTitle = S3_LOCATION + current_user.username + title + '.mp3'
        filename = current_user.username + title + '.mp3'        
        print(S3_BUCKET_NAME)
        s3_resource.Bucket(S3_BUCKET_NAME).put_object(Key=filename, Body=audio)
        return jsonify({'title' : newTitle})
    
    return jsonify ({'error' : 'no upload'})








