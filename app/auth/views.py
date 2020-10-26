from . import auth
from ..models import User
from .forms import RegistrationForm,LoginForm
from flask import render_template,url_for,request,flash,redirect
from flask_login import login_required,login_user,logout_user
from ..email import mail_message
from .. import db

@auth.route('/signup', methods = ["GET","POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        user.save_u()
        mail_message("Welcome to Pitch-IT","email/welcome_user",user.email,user=user)
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', r_form = form)

@auth.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user != None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or Password')
    return render_template('auth/login.html', loginform = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))