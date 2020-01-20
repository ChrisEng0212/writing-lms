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
SCHEMA = BaseConfig.SCHEMA
STUDENTID = []
     

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
        jload = None

    return jload
  
def putAWS(unit, data): 
    keyName = (str(unit) + '/')  #adding '/' makes a folder object
    jData = json.dumps(data)    
    print (keyName)    
    s3_resource.Bucket(S3_BUCKET_NAME).put_object(Key=keyName) 
    object = s3_resource.Object(S3_BUCKET_NAME, keyName + current_user.username + '.json')         
    object.put(Body=jData) 
    print('PUTAWS_ADDED: ' +  jData)  

    return keyName

def s3console(unit): 
    my_bucket = s3_resource.Bucket(S3_BUCKET_NAME)
    files = my_bucket.objects.all()         
    objs = my_bucket.objects.filter(Prefix=str(unit) + '/')        

    return objs

@app.route('/jCheck/<string:check>/<string:unit>', methods=['POST'])
def jChecker(check, unit):
    print('JCHECK ACTIVE')
    
    if check == 'work':
        file = current_user.username + '.json'
        obj = loadAWS(file, int(unit))  
        if obj == None:
            work = 'None'
        else:
            work = json.dumps(obj)
            print ('TRIED DUMP',  obj)   

        SOURCES = loadAWS('json_files/sources.json', 0)
        sources = json.dumps(SOURCES['sources'])  

    elif check == 'sources':
        SOURCES = loadAWS('json_files/sources.json', 0)
        sources = json.dumps(SOURCES['sources'])
        work = 'None' 

    #print('DATA', type(work),  str(work))
    return jsonify({'work' : work, 'sources' : sources})


def processRecord(unit, stage, count):
    ## make student_record
    record = jRecord.query.filter_by(username=current_user.username).first()  
    if record:
        student_record = ast.literal_eval(record.Midterm)
        print('1')
    else:
        student_record = {}
        start_record = jRecord(username=current_user.username, Midterm=str(student_record))
        db.session.add(start_record)
        record = jRecord.query.filter_by(username=current_user.username).first()  
        print('2')    

    if stage == "1":
        student_record[unit] = {
            'stage' : stage,
            'date_plan' : date.today(),
            'count' : 'none',
            'date_draft' : 'none',
            'date_revise' : 'none'
        }
    if stage == "2":
        student_record[unit]['stage'] = stage
        student_record[unit]['count'] = count
        student_record[unit]['date_draft'] = date.today()
    if stage == "3":
        student_record[unit]['stage'] = stage   

    record.Midterm = str(student_record)
    db.session.commit()
        


@app.route('/sendData', methods=['POST'])
def sendData():  
    unit = request.form ['unit']  
    obj = request.form ['obj'] 
    stage = request.form ['stage']
    count = request.form ['count']
    date_code = request.form ['date']  
    work = request.form ['work']        
    processRecord(unit, stage, count)

    name = current_user.username  

    dataDict = ast.literal_eval(obj) 
    userDict = {}
    #### check stage of adding data
    if work == 'plan':   
        userDict['meta'] = {
                'name' : name, 
                'unit' : unit,
                'date' : 'none',
                'avatar' : current_user.avatar, 
                'image' : S3_LOCATION + current_user.image_file, 
                'theme' : current_user.theme,
                'stage' : stage
                }        
    else:
        file = current_user.username + '.json'
        get_data = loadAWS(file, int(unit)) 
        userDict = ast.literal_eval(json.dumps(get_data))

    #### record the date of first draft-complete recorded
    if date_code == 'update':
        today = date.today()
        userDict['meta']['date'] = str(today)
    
    userDict[work] = dataDict 
    userDict['meta']['stage'] = stage
    
    print('UPDATED ', userDict)
    
    putAWS(int(unit), userDict)
    
    return jsonify({'name' : name, 'work' : work})


@app.route('/sendRevise', methods=['POST'])
def sendRevise():  
    unit = request.form ['unit']  
    html = request.form ['html']
    text = request.form ['text']
    stage = request.form ['stage']
    revised = request.form ['revised']
    work = 'revise'
    student = request.form ['student']     
    count = None

    processRecord(unit, stage, count)

    if int(stage) == 3:
        dataDict = {
            'html' : html, 
            'text' : text, 
            'revised' : revised
        } 
        file = student + '.json'
        get_data = loadAWS(file, int(unit)) 
        userDict = ast.literal_eval(json.dumps(get_data))    
        
        userDict[work] = dataDict 
        userDict['meta']['stage'] = stage

    if int(stage) == 4:
        file = current_user.username + '.json'
        get_data = loadAWS(file, int(unit)) 
        userDict = ast.literal_eval(json.dumps(get_data)) 

        userDict[work]['revised'] = revised
        userDict['meta']['stage'] = stage
        
    print('UPDATED ', userDict)    
    putAWS(int(unit), userDict)
    
    return jsonify({'name' : student, 'work' : work})


def imageAWS(data, unit):   
    # S3_Location / 1 / 1 / mark 
    _ , f_ext = os.path.splitext(data.filename) # _  replaces f_name which we don't need #f_ext  file extension     
    data_filename =  int(unit) + '/' + current_user.username + f_ext 
    s3_filename =  S3_LOCATION + data_filename     
    s3_resource.Bucket(S3_BUCKET_NAME).put_object(Key=data_filename, Body=data) 

    return s3_filename


@app.route('/sendImage', methods=['POST'])
def sendImage(): 
    print('SENDIMAGE ACTIVE') 
    unit = request.form ['unit']  
    image_string = request.form ['selectedFile']   
    image_dict = json.loads(image_string) 
    work = 'publish'    

    print (image_dict)

    imageLink = imageAWS(image_dict, unit)

    file = current_user.username + '.json'
    get_data = loadAWS(file, int(unit)) 
    userDict = ast.literal_eval(json.dumps(get_data)) 

    if userDict[work]:
        userDict[work]['image'] = imageLink
    else:
        userDict[work] = {}
        userDict[work]['image'] = imageLink   
      
    putAWS(int(unit), userDict[work])
    
    return jsonify({'name' : student, 'imageLink' : imageLink})


""" ### TOPICS ### """

@app.route("/topic_list", methods = ['GET', 'POST'])
@login_required
def topic_list():
    topDict = {}        

    SOURCES = loadAWS('json_files/sources.json', 0)
    sources = SOURCES['sources']
    for unit in sources:
        src = sources[unit]       
        if src['Set'] == 1:
            ## add to topics list
            topDict[unit] = {
                'Title' : src['Title'], 
                'Deadline' : src['Deadline']
            }
            ## add meta details if available
            file = current_user.username + '.json'
            obj = loadAWS(file, int(unit)) 
            print('obj', obj)
            if obj:
                topDict[unit]['Theme'] = obj['meta']['theme']       
                topDict[unit]['Stage'] = int(obj['meta']['stage'])       
                topDict[unit]['Avatar'] = obj['meta']['avatar']      
                  
            else: 
                topDict[unit]['Theme'] = 'white'      
                topDict[unit]['Stage'] = 0      
                topDict[unit]['Avatar'] = 'none'
                
    print('DICT', topDict)
    topJS = json.dumps(topDict)  

    return render_template('work/topic_list.html', topJS=topJS)

@app.route('/topicCheck/<string:unit>', methods=['POST'])
def topicCheck(unit):
    print('TOPIC CHECK ACTIVE')
    
    stage = 0    
    dataList =  []    
    objs = s3console(int(unit))
    print(objs)    
    for item in objs:
        jload = loadAWS(item.key, 0)  
        print('TEST', item.key)
        if jload: # becasue None would be the folder search '1/'
            if jload['meta']['name'] == current_user.username:
                
                stage = jload['meta']['stage']
                print('CURRENT USER FOUND', stage)
            else:
                dataList.append(  json.dumps(jload) )              
            
            if int(jload['meta']['stage']) > 0:
                print('PLAN FINISHED')
            if int(jload['meta']['stage']) > 1:
                print('WORK FINISHED')   

    random.shuffle(dataList)      

    SOURCES = loadAWS('json_files/sources.json', 0)
    sources = json.dumps(SOURCES['sources'])    

    #print('DATA', type(dataList), dataList)
    return jsonify({'dataList' : dataList, 'sources' : sources, 'stage' : stage})


""" ### PLAN/WORK/REVISE/PUBLISH ### """

@app.route("/work/<string:part>/<string:unit>", methods = ['GET', 'POST'])
@login_required
def part(part, unit):  
    
    return render_template('work/' + part + '.html', unit=unit)


""" ### INSTRUCTOR DASHBOARD ### """

@app.route("/dashboard", methods = ['GET', 'POST'])
@login_required
def dashboard():

    recList = {}    
    records = jRecord.query.all()
    for rec in records:
        stuDict = ast.literal_eval(rec.Midterm)
        recList[rec.username] = stuDict

    recOBJ = json.dumps(recList)

    return  render_template('instructor/dashboard.html', recOBJ=recOBJ)

@app.route("/editor/<string:student>/<string:unit>", methods = ['GET', 'POST'])
@login_required
def editor(student, unit):

    file = student + '.json'
    obj = loadAWS(file, int(unit)) 

    print(obj)
    
    text = ''
    for part in obj['draft']:
        text += obj['draft'][part]
    

    return  render_template('instructor/editor.html', text=text, student=student, unit=unit)




