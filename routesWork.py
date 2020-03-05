import sys, boto3, random, base64, os, secrets, httplib2, json, ast
from sqlalchemy import asc, desc 
from datetime import datetime, timedelta, date
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

    

"""S3 CONNECTIONS """
def loadAWS(file, unit):   
    if unit == 0 :
        key = file
        content_object = s3_resource.Object(  S3_BUCKET_NAME, key  )
        print('LOAD_AWS_SEARCH', content_object)
    else:
        key = str(unit) + '/' + file        
        content_object = s3_resource.Object(  S3_BUCKET_NAME, key   )
        print('LOAD_AWS_SEARCH', content_object)
    try:
        file_content = content_object.get()['Body'].read().decode('utf-8')
        jload = json.loads(file_content)
        print(type(jload))
    except:
        print('AWS return NONE')
        jload = None

    return jload
  
        
''' new style '''
@app.route('/storeData', methods=['POST'])
def storeData():  
    unit = request.form ['unit']  
    obj = request.form ['obj'] 
    stage = request.form ['stage']
    work = request.form ['work']  

    if work == 'edit':
        student = request.form ['student']         
    else:
        student = current_user.username

    print('STAGE WORK OBJ', stage, work, obj)
    classModel = Info.ass_mods_dict[unit]
    entry = classModel.query.filter_by(username=student).first()
    info = json.loads(entry.info)

    if work == 'plan':                
        if int(stage) == 0: 
            info[work + "_date_start"] = str(date.today())           
        if int(stage) == 1:            
            info[work + "_date_finish"] = str(date.today())
        info['stage'] = stage
        entry.info = json.dumps(info)
        entry.plan = obj
        entry.grade = stage
        db.session.commit() 

    if work == 'draft':        
        if int(stage) == 1: 
            info[work + "_date_start"] = str(date.today())           
        if int(stage) == 2:            
            info[work + "_date_finish"] = str(date.today())
        info['stage'] = stage
        entry.info = json.dumps(info)
        entry.draft = obj
        entry.grade = stage
        db.session.commit() 

    if work == 'edit': 
        dataDict = {
            'html' : request.form ['html'], 
            'text' : request.form ['text'], 
            'revised' : None, 
        } 
        info['stage'] = stage
        entry.info = json.dumps(info)
        entry.revise = json.dumps(dataDict)
        entry.grade = 3
        db.session.commit() 

    if work == 'revise':   
        info[work + "_date_finish"] = str(date.today())
        info['stage'] = stage
        entry.info = json.dumps(info)
        dataDict = json.loads(entry.revise)
        dataDict['revised'] = obj ## actuall a string
        entry.revise = json.dumps(dataDict)
        entry.grade = 4
        db.session.commit() 
    
    if work == 'publish':   
        info[work + "_date_finish"] = str(date.today())
        info['stage'] = stage
        entry.info = json.dumps(info)
        dataDict = {
            'title' :  request.form ['title'],
            'imageLink' :  request.form ['imageLink'],
            'final' :  request.form ['final'],
        }
        entry.publish = json.dumps(dataDict)
        entry.grade = 5
        db.session.commit() 
        

    name = current_user.username  
    
    return jsonify({'name' : name, 'work' : work})


@app.route('/sendImage', methods=['POST'])
def sendImage(): 
    b64String = request.form ['b64String'] 
    print(b64String)
    print('SENDIMAGE ACTIVE') 
    unit = request.form ['unit']  
    fileType = request.form ['fileType']  
    print (b64String, fileType)

    image = base64.b64decode(b64String)
    imageLink = S3_LOCATION + 'images/' + unit + '/' + current_user.username + '.' + fileType
    filename = 'images/' + unit + '/' + current_user.username + '.' + fileType
    s3_resource.Bucket(S3_BUCKET_NAME).put_object(Key=filename, Body=image)

    return jsonify({'name' : current_user.username, 'imageLink' : imageLink})


""" ### TOPICS ### """

@app.route("/topic_list", methods = ['GET', 'POST'])
@login_required
def topic_list():
    topDict = {}   
    
    with open('static/json_files/sources.json', 'r') as f:
        srcJSON = json.load(f)
        
    sources = srcJSON['sources']

    pprint(sources)

    for unit in sources:        
        src = sources[unit]       
        if src['Set'] == 1:
            ## add to topics list
            topDict[unit] = {
                'Title' : src['Title'], 
                'Deadline' : src['Deadline']
            }
            model = Info.ass_mods_dict[unit]
            user = model.query.filter_by(username=current_user.username).first()
            ## add info details if available            
            if user:
                infoDict = json.loads(user.info) 
                topDict[unit]['Theme'] = infoDict['theme']       
                topDict[unit]['Stage'] = int(infoDict['stage'])       
                topDict[unit]['Avatar'] = infoDict['avatar'] 
            else: 
                topDict[unit]['Theme'] = 'white'      
                topDict[unit]['Stage'] = 0      
                topDict[unit]['Avatar'] = 'none'
                
    print('DICT', topDict)
    topJS = json.dumps(topDict)  

    return render_template('work/topic_list.html', topJS=topJS)


## AJAX
@app.route('/topicCheck/<string:unit>', methods=['POST'])
def topicCheck(unit):
    print('TOPIC CHECK ACTIVE')
    
    stage = 0    
    dataList =  [] 

    model = Info.ass_mods_dict[unit]
    entries = model.query.all() 
    
    for entry in entries:
        info = json.loads(entry.info)
        if info['name'] == current_user.username:               
            stage = info['stage']
            print('CURRENT USER FOUND', current_user.username, stage)
        else:
            try:
                plan = json.loads(entry.plan)
            except:
                plan = {}
            try:
                draft = json.loads(entry.draft)
            except:
                draft = {}
            try:
                publish = json.loads(entry.publish)
            except:
                publish = {}

            entryDict = {
                'info' : json.loads(entry.info),
                'plan' : plan,
                'draft' : draft,
                'publish' : publish,
            }
            
            dataList.append( json.dumps(entryDict)  ) 
    
    #print('XXXXXX', dataList)
    random.shuffle(dataList)    
      

    with open('static/json_files/sources.json', 'r') as f:        
        srcJSON = json.load(f)
        
        
    sources = json.dumps(srcJSON['sources'])  

    #print('DATA', type(dataList), dataList)
    return jsonify({'dataList' : dataList, 'sources' : sources, 'stage' : stage})

## AJAX
@app.route('/getHTML/<string:unit>', methods=['POST'])
def getHTML(unit):
    print('GET HTML ACTIVE')
    
    
    model = Info.ass_mods_dict[unit]
    entry = model.query.filter_by(username=current_user.username).first() 
    info = entry.info
    revise = entry.revise 
    stage = entry.grade   

    #print('DATA', type(dataList), dataList)
    return jsonify({'revise' : revise, 'stage' : stage, 'info' : info})


""" ### PLAN/WORK/REVISE/PUBLISH ### """

@app.route("/work/<string:part>/<string:unit>", methods = ['GET', 'POST'])
@login_required
def part(part, unit): 

    classModel = Info.ass_mods_dict[unit]
    entryCount = classModel.query.filter_by(username=current_user.username).count()
    if entryCount == 0:
        info = {
            'avatar' : current_user.avatar, 
            'theme' : current_user.theme,
            'name' : current_user.username, 
            'image' : S3_LOCATION + current_user.image_file, 
            'stage' : 0
        }
        entry = classModel(username=current_user.username, info=json.dumps(info))
        db.session.add(entry)
        db.session.commit()
    
    
    entry = classModel.query.filter_by(username=current_user.username).first()    

    fullDict = {
        'info' : entry.info,
        'plan' : entry.plan,
        'draft' : entry.draft,
        'revise' : entry.revise,
        'publish' : entry.publish,
    }    
    
    #print(fullDict)

    #SOURCES = loadAWS('json_files/sources.json', 0)
    #sources = json.dumps(SOURCES['sources']) 
    with open('static/json_files/sources.json', 'r') as f:
        srcJSON = json.load(f)
        
    sources = json.dumps(srcJSON['sources']) 
    
    return render_template('work/' + part + '.html', unit=unit, fullDict=json.dumps(fullDict), sources=sources)


""" ### INSTRUCTOR DASHBOARD ### """

@app.route("/dashboard", methods = ['GET', 'POST'])
@login_required
def dashboard():

    recDict = {} 

    for model in Info.ass_mods_dict:
        recDict[model] = {}
        print(recDict)
        for entry in Info.ass_mods_dict[model].query.all():           
            recDict[str(model)][entry.username] = json.loads(entry.info)

    
    

    return  render_template('instructor/dashboard.html', recOBJ=str(json.dumps(recDict)))

@app.route("/editor/<string:student>/<string:unit>", methods = ['GET', 'POST'])
@login_required
def editor(student, unit):

    model = Info.ass_mods_dict[unit]
    print(model)
    jString = model.query.filter_by(username=student).first()
    print(jString.draft)
    student_draft = json.loads(jString.draft)

            
    text = ''
    for part in student_draft:
        text += student_draft[part]
    

    return  render_template('instructor/editor.html', text=text, student=student, unit=unit)




