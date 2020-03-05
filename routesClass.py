import sys, boto3, random, base64, os, secrets, httplib2, json, ast, datetime
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

# IN THIS FILE
# STUDENTS 
# ATT_TEAM
# ATT_DASH
# ATT_LOG 
# DISPLAY TEAMS
# REMOVE STUDENTS 

@app.route ("/students")
@login_required 
def students():
    if current_user.id != 1:
        return abort(403)  
    
    students = User.query.order_by(asc(User.studentID)).all()    
    
    return render_template('instructor/students.html', S3_LOCATION=S3_LOCATION, students=students, title='students')  


######## Attendance //////////////////////////////////////////////
@app.route("/team_maker", methods = ['GET', 'POST'])
@login_required
def att_team():

    #legend = 'Attendance: ' + time.strftime('%A %b, %d %Y %H:%M')
    legend = 'None'
    # check if attendance is open 
    openData = Attendance.query.filter_by(username='Chris').first()
    if openData:
        openCheck = openData.teamnumber
        if openCheck == 98 or openCheck == 50:  # 98 open in normal state, 50 open in midterm state - all units can be done
            form = Attend()  
        elif openCheck == 99:  # switch to late form
            form = AttendLate() 
        elif openCheck == 100:   # delete all rows
            db.session.query(Attendance).delete()
            db.session.commit()
            attendance = Attendance(username = 'Chris', 
            attend='Notice', teamnumber=97, studentID='100000000')      
            db.session.add(attendance)
            db.session.commit()
            flash('Attendance is not open yet, please try later', 'danger')
            return redirect(url_for('home')) 
        else: # openData has return None
            flash('Attendance is not open yet, please try later', 'danger')
            return redirect(url_for('home'))  
    else:
        flash('Attendance is not open yet, please try later', 'danger')
        return redirect(url_for('home'))  

        
    # set up page data 
    teamcount = openData.teamcount
    teamsize = openData.teamsize 
    print('teamsizexxxxxxxx', teamsize) 
    notice = openData.attend     

    # set up student data   
    count = Attendance.query.filter_by(username=current_user.username).count()
    fields = Attendance.query.filter_by(username=current_user.username).first()     
    
    # set teamnumber to be zero by default (or not Zero in the case of solo classes)
    if teamsize == 0:
        teamNumSet = current_user.id + 100
    else:
        teamNumSet = 0 

    # set up team info 
    users = {}
    if count == 1: 
        teammates = Attendance.query.filter_by(teamnumber=fields.teamnumber).all()        
        for teammate in teammates:            
            image = User.query.filter_by(username=teammate.username).first().image_file
            users[teammate.username] = [teammate.username, S3_LOCATION + image]
    else:        
        users = None     

    # prepare initial form
    if count == 0:               
        if form.validate_on_submit():            
            # check last id for AttendLog 
            lastID = AttendLog.query.order_by(desc(AttendLog.id)).first().id   
            # team maker
            attendance = Attendance(username = form.name.data, 
            attend=form.attend.data, teamnumber=form.teamnumber.data, 
            teamcount=form.teamcount.data, studentID=form.studentID.data, unit=lastID+1)      
            db.session.add(attendance)
            db.session.commit()
            # long term log 
            if form.attend.data == 'On time':
                attScore = 3
            elif form.attend.data == 'Late': 
                attScore = 2
            else:
                attScore = 1          
            attendLog = AttendLog(username = form.name.data, 
            attend=form.attend.data,teamnumber=form.teamnumber.data, 
            studentID=form.studentID.data, attScore=attScore)
            db.session.add(attendLog)
            # commit both
            db.session.commit()
            return redirect(url_for('att_team'))
        else:
            form.name.data = current_user.username
            form.studentID.data = current_user.studentID
            form.teamcount.data = 0
            form.teamnumber.data = teamNumSet  
    
    #after attendance is complete teamnumber 0 is reassigned to a team  
    elif fields.teamnumber == 0: 
        # { 1 : 1,  2 : 1  ,  3 :  0 }
        teamDict = {}  
        for i in range (1,teamcount+1):
            count = Attendance.query.filter_by(teamnumber=i).count()
            if count: 
                teamDict[i] = count
            else:   
                teamDict[i] = 0
        print (teamDict)

        # all teams are full so make a new team
        if teamDict[teamcount] == teamsize:
            countField = Attendance.query.filter_by(username='Chris').first()
            countField.teamcount = teamcount +1            
            db.session.commit() 
            return redirect(url_for('att_team'))
        # all teams have the same number (first and last) of students so start from beginning
        elif teamDict[1] == teamDict[teamcount]:
            fields.teamnumber = 1
            db.session.commit()
            flash('Your attendance has been recorded', 'info')
            return redirect(url_for('att_team'))
        else:
            for key in teamDict:
                # search each group until one needs to be filled
                if teamDict[key] > teamDict[key+1]:
                    fields.teamnumber = key+1
                    db.session.commit()
                    flash('Your attendance has been recorded', 'info')
                    return redirect(url_for('att_team'))                 
                else: 
                    pass
    
    return render_template('instructor/att_team.html', legend=legend, count=count, fields=fields, 
    teamcount=teamcount, form=form, notice=notice, users=users)  


# set up the attendence for the day
@app.route("/att_dash", methods = ['GET', 'POST'])
@login_required
def att_dash():
    if current_user.id != 1:
        return abort(403)
    form = AttendInst()

    openData = Attendance.query.filter_by(username='Chris').first()

    if openData:    
        if form.validate_on_submit():            
            openData.attend = form.attend.data 
            openData.teamnumber = form.teamnumber.data 
            openData.teamsize = form.teamsize.data 
            openData.teamcount = form.teamcount.data 
            openData.unit =  form.unit.data        
            db.session.commit()    
            
            flash('Attendance has been updated', 'secondary') 
            return redirect(url_for('att_team')) 
        else:
            form.username.data = 'Chris'
            form.studentID.data = '100000000'
            try:
                form.attend.data = openData.attend
                form.teamnumber.data = openData.teamnumber
                form.teamsize.data = openData.teamsize
                form.teamcount.data = openData.teamcount
                form.unit.data = openData.unit                
            except: 
                pass 
    else:
        flash('Attendance not started', 'secondary') 
        return redirect(request.referrer)  

    return render_template('instructor/att_dash.html', form=form, status=openData.teamnumber, title='controls')  

# see historical attendance
@app.route ("/att_log")
@login_required
def att_log():  
    if current_user.id != 1:
        return abort(403)
    
    IDLIST = IDLIST

    ## create a list of all course dates
    course = Course.query.order_by(asc(Course.date)).all()   
    dateList = []
    for c in course:
        date = c.date
        dateList.append(date.strftime("%m/%d"))    
    print('dateList', dateList)   
    
    ## log all dates when attendance was complete (and show total att score)
    attLogDict = {}    
    for number in IDLIST:        
        attLogDict[number] = []
    for attLog in attLogDict:
        logs = AttendLog.query.filter_by(studentID=str(attLog)).all() 
        attGrade = 0        
        if logs:                        
            for log in logs:
                d = log.date_posted
                dStr = d.strftime("%m/%d")                
                attLogDict[attLog].append(dStr) 
                attGrade = attGrade + log.attScore
            attLogDict[attLog].insert(0, attGrade) 
        
    print('attLogDict', attLogDict)

    ##get names for all student IDs
    userDict = {}
    users = User.query.all()
    for user in users:
        userDict[int(user.studentID)] = user.username

    today = datetime.now()
    todayDate = today.strftime("%m/%d")  

    return render_template('instructor/att_log.html', title='att_log', attLogDict=attLogDict, dateList=dateList, todayDate=todayDate, userDict=userDict)  


# see teams
@app.route ("/teams")
@login_required 
def teams():  
    if current_user.id != 1:
        return abort(403)       

    try:
        teamcount = Attendance.query.filter_by(username='Chris').first().teamcount
    except:
        flash('Attendance not open yet', 'danger')
        return redirect(url_for('home')) 
    
    if teamcount > 0: 
        attDict = {}  #  teamnumber = fields, 1,2,3,4 names
        for i in range(1, teamcount+1):
            teamCall = Attendance.query.filter_by(teamnumber=i).all()
            attDict[i] = teamCall    
    # if team count set to zero ---> solo joining
    else:
        attDict = {}
        users = User.query.order_by(asc(User.studentID)).all()        
        for user in users:
            attStudent = Attendance.query.filter_by(username=user.username).first() 
            if attStudent:
                attDict[user.username] = [user.studentID, attStudent.date_posted]
            else:
                attDict[user.username] = [user.studentID, 0]
    print(attDict)

    tablesDict = {}
    
    return render_template('instructor/teams.html', attDict=attDict, teamcount=teamcount, title='teams')  


# remove person from team and att_log
@app.route ("/studentRemove/<string:name>", methods = ['GET', 'POST'])
@login_required 
def studentRemove(name):
    if current_user.id != 1:
        return abort(403)   

    findSt = Attendance.query.filter_by(username=name).first()    
    
    #delete the attendances entries using ids
    Attendance.query.filter_by(id=findSt.id).delete()
    db.session.commit()

    AttendLog.query.filter_by(id=findSt.unit).delete()
    db.session.commit()
    
    #find the team work today
    todaysUnit = Attendance.query.filter_by(username='Chris').first().unit   
    studentTeam = Attendance.query.filter_by(username=name).first().teamnumber
    
    idNum = 0 
    for model in Info.modListUnits:
        # ie search for u061u
        if todaysUnit + '1' in str (model):
            try:
                idNum = model.query.filter_by(teamnumber=studentTeam).first().id
            except:
                pass
            

    return jsonify({'removed' : name, 'unit' : todaysUnit, 'idNum' : idNum})





