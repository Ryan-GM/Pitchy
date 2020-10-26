from flask.app import Flask
from ..models import User
from flask_wtf import FlaskForm
from wtforms import ValidationError,PasswordField,BooleanField,StringField,SubmitField
from wtforms.validators import Required,Email,EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[Required()])
    password = PasswordField('Password',validators=[Required()])
    remember = BooleanField('Remember Me!')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Your username',validators=[Required()])
    email = StringField('Your email',validators=[Required()])
    password = PasswordField('Password',validators=[Required(),EqualTo('password_confirm',message = 'Passwords need to match')])
    password_confirm = PasswordField('Confirm password',validators=[Required()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError("Email already taken!!")

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError("Username already taken!!")
