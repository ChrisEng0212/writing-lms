from datetime import datetime, timedelta
from app import app, db, login_manager
from flask_login import UserMixin, current_user # this imports current user, authentication, get id (all the login attributes)
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


#login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)     
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, unique=True, nullable=False)
    studentID = db.Column(db.String(9), unique=True, nullable=False)
    attend = db.Column(db.String)
    teamnumber = db.Column(db.Integer)
    teamsize = db.Column(db.Integer)
    teamcount = db.Column(db.Integer)
    unit = db.Column(db.String(9))    
 
class AttendLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)     
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, nullable=False)
    studentID = db.Column(db.String(9), nullable=False)
    attend = db.Column(db.String)
    teamnumber = db.Column(db.Integer)
    attScore = db.Column(db.Integer)
    extraStr = db.Column(db.String)
    extraInt = db.Column(db.Integer)
   
class User(db.Model, UserMixin): #import the model
    id = db.Column(db.Integer, primary_key=True) #kind of value and the key unique to the user
    date_added = db.Column(db.DateTime, default=datetime.now)
    username =  db.Column(db.String(20), unique=True, nullable=False) #must be a unique name and cannot be null    
    avatar =  db.Column(db.String(20), unique=True, nullable=False)
    studentID = db.Column(db.String(9), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(), nullable=False, default='profiles/avatar1.PNG') #images will be hashed to 20 and images could be the same
    password = db.Column(db.String(60), nullable=False)    
    device = db.Column (db.String(), nullable=False)        
    theme = db.Column (db.String(20), default='ghostwhite')
    extraStr = db.Column(db.String)
    extraInt = db.Column(db.Integer)

    def get_reset_token(self, expires_sec=1800):
        expires_sec = 1800        
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod #tell python not to expect that self parameter as an argument, just accepting the token
    def verify_reset_token(token):
        expires_sec = 1800 
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None 
        return User.query.get(user_id)

    def __repr__(self):  # double underscore method or dunder method, marks the data, this is how it is printed
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"




    
############### UNIT MODELS ###################################

class jLibrary (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username = db.Column(db.String)    
    Unit01 = db.Column(db.String)
    Unit02 = db.Column(db.String)
    Unit03 = db.Column(db.String)
    Unit04 = db.Column(db.String)
    Unit05 = db.Column(db.String) 
    Unit06 = db.Column(db.String)
    Unit07 = db.Column(db.String)
    Unit08 = db.Column(db.String) 
    extraStr = db.Column(db.String)
    extraInt = db.Column(db.Integer)


class aControl (db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    deadline = db.Column(db.DateTime) 
    Unit = db.Column(db.String)
    Set = db.Column(db.Integer)
    extraStr = db.Column(db.String)
    extraInt = db.Column(db.Integer)

    
    

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.id == 1:
                return True
            else:
                return False
        else:
            return False

    #https://danidee10.github.io/2016/11/14/flask-by-example-7.html


admin = Admin(app)

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Attendance, db.session))
admin.add_view(MyModelView(AttendLog, db.session))
admin.add_view(MyModelView(jLibrary, db.session))
admin.add_view(MyModelView(aControl, db.session))

