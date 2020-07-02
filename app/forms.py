from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (
    StringField, PasswordField, SelectField,
    SubmitField, BooleanField, TextAreaField)
from wtforms.validators import (
    DataRequired, Length, 
    Email, EqualTo, ValidationError)
from flask_wtf.file import FileField, FileAllowed
from flask_pagedown.fields import PageDownField
from app.models import User

class LoginForm(FlaskForm):
    username=StringField('Username', validators=[
        DataRequired(),
        Length(2, 20)
    ])
    password=PasswordField('Password', validators=[DataRequired(), Length(8, 16)])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user=User.query.filter_by(username=username.data).first()
        if user is None:
            return ValidationError('Username is not registered')

class RegisterForm(FlaskForm):
    username=StringField('Username', validators=[
        DataRequired(),
        Length(2, 20)
    ])
    email=StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    fname=StringField('First Name', validators=[
        DataRequired(),
        Length(2, 20)
    ])
    lname=StringField('Last Name', validators=[
        DataRequired(),
        Length(2, 20)
    ])
    password=PasswordField('Password', validators=[DataRequired(), Length(8, 16)])
    confirm_password=PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            return ValidationError('Username is taken')

    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user is not None:
            return ValidationError('Email is taken')

