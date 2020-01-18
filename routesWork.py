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

    print('DATA', type(work),  str(work))
    return jsonify({'work' : work, 'sources' : sources})


def processRecord(unit, stage):
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
    
    ### how to keep stage record?
    try: 
        if student_record[unit]['stage'] == stage:
            pass
        else: 
            student_record[unit]['stage'] = stage 
        print('3')
    except:
        student_record[unit] = {}
        student_record[unit]['stage'] = stage  
        print('4')

    record.Midterm = str(student_record)
    db.session.commit()

        


@app.route('/sendData', methods=['POST'])
def sendData():  
    unit = request.form ['unit']  
    stage = request.form ['stage']
    date = 'date variable not set' #request.form ['date']  
    obj = request.form ['obj'] 
    work = request.form ['work'] 
    name = current_user.username
    user = User.query.filter_by(username=name).first() 
    processRecord(unit, stage) 
    
    
    dataDict = ast.literal_eval(obj) 
    userDict = {}
    #### check stage of adding data
    if work == 'plan':                 
        
        userDict['meta'] = {
                'name' : name, 
                'unit' : unit,
                'date' : date,
                'avatar' : user.avatar, 
                'image' : S3_LOCATION + user.image_file, 
                'theme' : user.theme,
                'stage' : stage
                }        
    else:
        file = current_user.username + '.json'
        get_data = loadAWS(file, int(unit)) 
        userDict = ast.literal_eval(json.dumps(get_data))

    userDict[work] = dataDict 
    userDict['meta']['stage'] = stage
    print('UPDATED ', userDict)
    
    putAWS(int(unit), userDict)
    
    return jsonify({'name' : name, 'work' : work})


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






