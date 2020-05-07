from datetime import datetime, timedelta
from app import app, db, login_manager
from flask_login import UserMixin, current_user # this imports current user, authentication, get id (all the login attributes)
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



modDictAss = {}

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



class BaseAss(db.Model):
    __abstract__ = True
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String)
    number = db.Column(db.Integer, unique=True)
    info = db.Column(db.String)
    plan = db.Column(db.String)
    draft = db.Column(db.String)
    revise = db.Column(db.String)
    publish = db.Column(db.String) 
    grade = db.Column(db.Integer) 
    comment = db.Column(db.String)
    extra = db.Column(db.String)

class A01A (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss['01'] = A01A

class A02A (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss['02'] = A02A

class A03A (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss['03'] = A03A

class A04A (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss['04'] = A04A

class A05A (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss['05'] = A05A

class A06A (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss['06'] = A06A

class A07A (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss['07'] = A07A

class A08A (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss['08'] = A08A

class A09A (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss['09'] = A09A



##############################3
listAss = []
for elements in modDictAss.values():
    listAss.append(elements)

class Info ():
    ass_mods_dict = modDictAss
    ass_mods_list = listAss
 
    
    

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.id > 0:
                return True
            else:
                return False
        else:
            return True

    #https://danidee10.github.io/2016/11/14/flask-by-example-7.html


admin = Admin(app)

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Attendance, db.session))
admin.add_view(MyModelView(AttendLog, db.session))

for ass in listAss:
    admin.add_view(MyModelView(ass, db.session))