from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed, FileRequired # what kind of files are allowed to be uploaded
from flask_login import current_user # now we can use this for the account update
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, HiddenField, validators, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from models import *  #you forgot this and it took forever to notice the mistake!!!

#python classes will be forms
#then converted into forms in our html

class Attend(FlaskForm):
    attend = RadioField('Attendance', choices = [('On time', 'On time'), ('Late', 'Late')])
    name =  StringField ('Name in English', validators=[DataRequired(), Length(min=2, max=20)])
    studentID = StringField ('Student ID (9 numbers)', validators=[DataRequired(), Length(9)])                  
    teamnumber = IntegerField ('Team Number')
    teamcount = IntegerField ('Team Count')                                                  
    submit = SubmitField('Join Class')

class AttendLate(FlaskForm):
    attend = RadioField('Attendance', choices = [('Late', 'Late'), ('2nd Class', '2nd Class')])
    name =  StringField ('Name in English', validators=[DataRequired(), Length(min=2, max=20)])
    studentID = StringField ('Student ID (9 numbers)', validators=[DataRequired(), Length(9)])                  
    teamnumber = IntegerField ('Team Number')
    teamcount = IntegerField ('Team Count')                                                  
    submit = SubmitField('Join')

class AttendInst(FlaskForm):
    attend = StringField ('Notice')   
    username =  StringField ('Name in English', validators=[DataRequired(), Length(min=2, max=20)])
    studentID = StringField ('Student ID', validators=[DataRequired(), Length(9)])                  
    teamnumber = IntegerField ('Status (50-review; 97-disabled; 98-open; 99-late; 100-clear)') 
    #RadioField('Status', choices = [(97, 'disabled'), (98, 'open'), (99, 'late'), (100, 'clear')])
    teamcount = IntegerField ('Team Count')   
    teamsize = IntegerField ('Team Size (0 for no teams)')  
    #RadioField('Size', choices = [(0, '0'), (2, '2'), (3, '3'), (4, '4')]) 
    unit = StringField ('unit(2) eg 01 or MT', validators=[DataRequired(), Length(min=2, max=20)])                                         
    submit = SubmitField('Join')

class RegistrationForm(FlaskForm):

    username = StringField ('Name in English', validators=[DataRequired(), Length(min=2, max=20)])    
    studentID = StringField ('Student ID (9 numbers)', validators=[DataRequired(), Length(9)])
    email = StringField('Email', validators=[DataRequired(), Email()] )  
    device = RadioField('Main Device', choices = [('Apple', 'Apple iphone'), ('Android', 'Android Phone'), ('Win', 'Windows Phone')]) 
    password = PasswordField('Password', validators=[DataRequired()] )
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')] )
    
    submit = SubmitField('Join')

    def validate_username(self, username):  # the field is username
        user = User.query.filter_by(username=username.data).first()  #User was imported at the top # first means just find first instance?
        if user:  # meaning if True
            raise ValidationError('Another student has that username, please add family name')  # ValidationError needs to be imported from wtforms
    
    def validate_email(self, email): 
        user = User.query.filter_by(email=email.data).first()  
        if user:  
            raise ValidationError('That email has an account already, did you forget your password?') 

    def validate_studentID(self, studentID): 
        try:
            int(studentID.data)
        except:
            raise ValidationError('9 numbers; no S') 
        user = User.query.filter_by(studentID=studentID.data).first()  
        if user:           
            raise ValidationError('That student ID already has an account, did you forget your password?')  

class LoginForm(FlaskForm):
    studentID = StringField ('Student ID', validators=[DataRequired(), Length(9)])     
    password = PasswordField('Password', validators=[DataRequired()]) 
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_studentID(self, studentID): 
        try:
            print(studentID.data)
            int(studentID.data)
            pass
        except:
            raise ValidationError('This should be your ID with no `s`') 

class ForgotForm(FlaskForm):
    email = StringField ('Email', validators=[DataRequired(), Email()])         
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email): 
        user = User.query.filter_by(email=email.data).first()  
        if user is None:  
            raise ValidationError('There is no account with that email, contact your instructor') 

class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()] )
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')] )
    submit = SubmitField('Set New Password')

class UpdateAccountForm(FlaskForm):
    #username = StringField ('Username', validators=[DataRequired(), Length(min=2, max=20)])    
    email = StringField('Email', validators=[DataRequired(), Email()] )   
    picture = FileField ('Change Profile Picture', validators=[FileAllowed(['jpg', 'png', 'heic'])]) 
    theme = RadioField('Personal Theme', choices = [('aqua', 'Blue' ), ('springgreen', 'Green' ), ('Orange', 'Orange'), ('violet', 'Pink' )]) 
    avatar = StringField('Pen Name (used for writing)', validators=[DataRequired(), Length(min=2, max=20)] )   
    submit = SubmitField('Update')

    def validate_username(self, avatar):  # the field is username
        if avatar.data != current_user.username: # if the updated one is the same then no need to validate
            user = User.query.filter_by(avatar=avatar.data).first()  #User was imported at the top # first means just find first instance?
            if user:  # meaning if True
                raise ValidationError('That pen name is being used already, please try another')  # ValidationError needs to be imported from wtforms
    
    def validate_email(self, email):  
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()  
            if user:  
                raise ValidationError('That email has an account already, did you forget your password?')      
     



