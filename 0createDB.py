
from app import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from pprint import pprint
from models import *
import json

#db.drop_all()
#db.create_all()
#db.session.commit()

def main(): 
    host = User(username='Chris', avatar='jimbob', theme='lightblue', studentID='100000000', email='cjx02121981@gmail.com', image_file='profiles/avatar1.PNG', password='tc0212', device='Heroku')
    db.session.add(host)
    db.session.commit()
    
    test = User(username='Test1', avatar='AMANA', theme='red', studentID='100000001', email='cjx02181@gmail.com', image_file='profiles/avatar2.PNG', password='tc0212', device='Heroku')
    db.session.add(test)
    db.session.commit()

    test = User(username='Test2', avatar='transndA', theme='pink', studentID='100000002', email='cjx0981@gmail.com', image_file='profiles/avatar3.PNG', password='tc0212', device='Heroku')
    db.session.add(test)
    db.session.commit()

    test = User(username='Test3', avatar='xdrtpoi', theme='yellow', studentID='100000003', email='c81@gmail.com', image_file='profiles/avatar4.PNG', password='tc0212', device='Heroku')
    db.session.add(test)
    db.session.commit()

    test = User(username='Test4', avatar='poerylu', theme='lightgreen', studentID='100000004', email='cj1@gmail.com', image_file='profiles/avatar5.PNG', password='tc0212', device='Heroku')
    db.session.add(test)
    db.session.commit()

    
def work():
    entry = A01A(username='Test1', info=json.dumps({
        "name": "Jill",
        "unit": "01",
        "avatar": "Ariel",
        "image": "https://writing-lms.s3.ap-northeast-1.amazonaws.com/profiles/avatar4.png",
        "theme": "springgreen",
        "stage": "1"
    }), plan=json.dumps({
        "Topic": "Lorum ",
        "Thesis": "Lorem ipsum dolor sit amet",
        "Idea_1": "Lorem ipsum dolor sit amet",
        "Details_1": "Lorem, ipsum, dolor, sit amet",
        "Idea_2": "Lorem ipsum dolor sit amet",
        "Details_2": "Lorem, ipsum, dolor, sit amet",
        "Idea_3": "Lorem ipsum dolor sit amet",
        "Details_3": "Lorem, ipsum, dolor, sit amet"
    }), draft=json.dumps({
        "Intro": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Part_1": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Part_2": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Part_3": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Closing": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
    }) 
    )
    db.session.add(entry)
    db.session.commit()

    entry = A01A(username='Test2', info=json.dumps({
        "name": "Bob",
        "unit": "01",
        "avatar": "MAxim",
        "image": "https://writing-lms.s3.ap-northeast-1.amazonaws.com/profiles/avatar4.png",
        "theme": "red",
        "stage": "2"
    }), plan=json.dumps({
        "Topic": "Lorum ",
        "Thesis": "Lorem ipsum dolor sit amet",
        "Idea_1": "Lorem ipsum dolor sit amet",
        "Details_1": "Lorem, ipsum, dolor, sit amet",
        "Idea_2": "Lorem ipsum dolor sit amet",
        "Details_2": "Lorem, ipsum, dolor, sit amet",
        "Idea_3": "Lorem ipsum dolor sit amet",
        "Details_3": "Lorem, ipsum, dolor, sit amet"
    }), draft=json.dumps({
        "Intro": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Part_1": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Part_2": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Part_3": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Closing": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
    }), grade=2 
    )
    db.session.add(entry)
    db.session.commit()
    entry = A01A(username='Test4', info=json.dumps({
        "name": "Jeff",
        "unit": "01",
        "avatar": "jelly",
        "image": "https://writing-lms.s3.ap-northeast-1.amazonaws.com/profiles/avatar4.png",
        "theme": "yellow",
        "stage": "2"
    }), plan=json.dumps({
        "Topic": "Lorum ",
        "Thesis": "Lorem ipsum dolor sit amet",
        "Idea_1": "Lorem ipsum dolor sit amet",
        "Details_1": "Lorem, ipsum, dolor, sit amet",
        "Idea_2": "Lorem ipsum dolor sit amet",
        "Details_2": "Lorem, ipsum, dolor, sit amet",
        "Idea_3": "Lorem ipsum dolor sit amet",
        "Details_3": "Lorem, ipsum, dolor, sit amet"
    }), draft=json.dumps({
        "Intro": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Part_1": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Part_2": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Part_3": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Closing": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
    }), grade=2
    )
    db.session.add(entry)
    db.session.commit()
    entry = A01A(username='Test3', info=json.dumps({
        "name": "Petite",
        "unit": "01",
        "avatar": "Pretty",
        "image": "https://writing-lms.s3.ap-northeast-1.amazonaws.com/profiles/avatar4.png",
        "theme": "pink",
        "stage": "2"
    }), plan=json.dumps({
        "Topic": "Lorum ",
        "Thesis": "Lorem ipsum dolor sit amet",
        "Idea_1": "Lorem ipsum dolor sit amet",
        "Details_1": "Lorem, ipsum, dolor, sit amet",
        "Idea_2": "Lorem ipsum dolor sit amet",
        "Details_2": "Lorem, ipsum, dolor, sit amet",
        "Idea_3": "Lorem ipsum dolor sit amet",
        "Details_3": "Lorem, ipsum, dolor, sit amet"
    }), draft=json.dumps({
        "Intro": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Part_1": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Part_2": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Part_3": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Closing": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
    }), grade=2 
    )
    db.session.add(entry)
    db.session.commit()

    

action = work() #main()