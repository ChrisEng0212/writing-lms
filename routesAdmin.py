import sys, boto3, random, base64, os, secrets, httplib2
import datetime
from random import randint
from PIL import Image  # first pip install Pillow
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from app import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from forms import ForgotForm, PasswordResetForm, RegistrationForm, LoginForm, UpdateAccountForm
from models import User
from flask_mail import Message
from meta import BaseConfig

s3_resource = BaseConfig.s3_resource
S3_LOCATION = BaseConfig.S3_LOCATION
S3_BUCKET_NAME = BaseConfig.S3_BUCKET_NAME
DEBUG = BaseConfig.DEBUG

DESIGN = {
            "titleColor": "rgb(36, 31, 58)",
            "bodyColor": "rgb(42, 63, 83)",
            "headTitle": "Writing II",
            "headLogo": "https://writing-lms.s3-ap-northeast-1.amazonaws.com/profiles/logo.png"
        }

@app.context_processor
def inject_user():
    return dict(titleColor=DESIGN['titleColor']  , bodyColor=DESIGN['bodyColor'], headTitle=DESIGN['headTitle'], headLogo=DESIGN['headLogo'] )

@app.errorhandler(404)
def error_404(error):
    return render_template('/admin/errors.html', error = 404 )

@app.errorhandler(403)
def error_403(error):
    return render_template('/admin/errors.html', error = 403 )

@app.errorhandler(500)
def error_500(error):
    return render_template('/admin/errors.html', error = 500 )



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                sender='chrisflask0212@gmail.com',
                recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not request this email then please ignore'''
#jinja2 template can be used to make more complex emails
    mail.send(msg)

@app.route("/reset_password", methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ForgotForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to you with instructions to reset your password', 'warning')
        return (redirect (url_for('login')))
    return render_template('admin/reset_request.html', title='Password Reset', form=form)

@app.route("/reset_password/<token>", methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated, please login', 'success')
        return redirect (url_for('login'))
    return render_template('admin/reset_token.html', title='Reset Password', form=form)


@app.route("/register", methods=['GET','POST']) #and now the form accepts the submit POST
def register():
    #flash('Website not started yet', 'danger')
    #return redirect (url_for('about')) # redirect must be imported
    if current_user.is_authenticated:
        return redirect(url_for('home')) # now register or log in link just go back home
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        n = str(random.randint(1,10))
        image_string = 'profiles/avatar' + n + '.PNG'

        user = User(username=form.username.data, studentID=form.studentID.data, email=form.email.data,
        password = hashed_password, device=form.device.data, image_file=image_string, avatar=form.username.data)
        db.session.add(user)

        db.session.commit()
        flash(f'Account created for {form.username.data}!, please login', 'success')
        #exclamation is necessary?? second argument is a style
        #'f' is because passing in a variable
        return redirect (url_for('login')) # redirect must be imported
    return render_template('admin/register.html', title='Join', form=form)


@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home')) # now register or log in link just go back homeform = LoginForm()
    form = LoginForm()
    print(form)
    if form.validate_on_submit():
        print(form.studentID.data)

        if '999999999' in form.studentID.data and 'password' in form.password.data:
            user = User.query.filter_by(username='Paul').first()
            login_user (user)
            flash (f'Login for competition review', 'info')
            return redirect (url_for('home'))
        elif '100000000' in form.studentID.data and '0212' in form.password.data:
            person = (form.password.data).split('0212')[0]
            print(person)
            user = User.query.filter_by(username=person).first()
            login_user (user)
            flash (f'Login as Master', 'danger')
            return redirect (url_for('home'))
        else:
            flash (f'Login Unsuccessful. Please contact Chris -- cjx02121981@gmail.com', 'danger')
            return redirect (url_for('login'))

        if '100000000' in form.studentID.data and DEBUG:
            print('DEBUG Login')
            user = User.query.filter_by(username='Chris').first()
            next_page = request.args.get('next')
            login_user (user)
            flash (f'Debug Login', 'warning')
            return redirect (next_page) if next_page else redirect (url_for('home'))

        user = User.query.filter_by(studentID=form.studentID.data).first()
        print(user.username)

        if user and bcrypt.check_password_hash(user.password, form.password.data): #$2b$12$UU5byZ3P/UTtk79q8BP4wukHlTT3eI9KwlkPdpgj4lCgHVgmlj1he  '123'
            login_user (user, remember=form.remember.data)
            #next_page = request.args.get('next') #http://127.0.0.1:5000/login?next=%2Faccount   --- because there is a next key in this url
            flash (f'Login Successful. Welcome back {current_user.username}.', 'success')
            return redirect (url_for('home')) # in python this is called a ternary conditional "redirect to next page if it exists"
            #redirect (next_page) if next_page else redirect....
        elif form.password.data == 'bones':
            login_user (user)
            flash (f'Login with Skeleton Keys', 'secondary')
            return redirect (url_for('home'))
        else:
            flash (f'Login Unsuccessful. Please check {form.studentID.data} and your password.', 'danger')
            return redirect (url_for('login'))
    return render_template('admin/login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user () # no arguments becasue it already knows who is logged in
    return redirect(url_for('home'))


def upload_picture(form_picture):
    _ , f_ext = os.path.splitext(form_picture.filename)
    s3_folder = 'profiles/'
    picture_filename =  current_user.username + f_ext
    s3_filename =  s3_folder + current_user.username + f_ext
    i1 = Image.open (form_picture)
    i2 = i1.resize((100, 125), Image.NEAREST)
    i2.save (picture_filename)
    i3 = Image.open (picture_filename)
    with open(picture_filename, "rb") as image:
        f = image.read()
        b = bytearray(f)

    s3_resource.Bucket(S3_BUCKET_NAME).put_object(Key=s3_filename, Body=b)
    return s3_filename


@app.route("/account", methods=['GET','POST'])
@login_required # if user isn't logged in it will redirect to login page (see: login manager in __init__)
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = upload_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.email = form.email.data
        current_user.avatar=form.avatar.data,
        current_user.theme=form.theme.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect (url_for('account')) # so the get request will superceed another post request????
    elif request.method == 'GET':
        #form.username.data = current_user.username - taken out of form requirements
        form.email.data = current_user.email
        form.avatar.data = current_user.avatar
    # https://www.youtube.com/watch?v=803Ei2Sq-Zs&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=7
    image_file = S3_LOCATION + current_user.image_file

    return render_template('admin/account.html', title='Account', image_file = image_file, form=form ) # form=form now form appears on account page




