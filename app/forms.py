'''Forms needed for the full functionality of the app'''

# Third party imports
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (
    StringField, PasswordField, 
    SelectField, IntegerField, FormField,
    SubmitField, BooleanField, TextAreaField)
from wtforms.validators import (
    DataRequired, Length, url,
    Email, EqualTo, ValidationError)
from flask_wtf.file import FileField, FileAllowed

# local imports
from app.models import User

class LoginForm(FlaskForm):
    '''Login form'''
    email=StringField('Email', validators=[DataRequired(),
                                                Email()])
    password=PasswordField('Password', validators=[DataRequired(), 
                                                Length(8, 16)])
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    '''Registration form'''
    username=StringField('Username', validators=[DataRequired(),
                                                Length(2, 20)])
    email=StringField('Email', validators=[DataRequired(),
                                            Email()])
    fname=StringField('First Name', validators=[DataRequired(),
                                                Length(2, 20)])
    lname=StringField('Last Name', validators=[DataRequired(),
                                                Length(2, 20)])
    password=PasswordField('Password', validators=[DataRequired(), 
                                                    Length(8, 16)])
    is_recruiter=BooleanField('Are you a recruiter')
    confirm_password=PasswordField('Confirm Password', 
                                    validators=[EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        '''Ensures that the username chosen by the user hasn't been registered to the database.'''
        user=User.query.filter_by(username=username.data).first()

        # If the username has been registered to the db, an error will be raised in the html form
        if user:
            raise ValidationError('Username is taken, please choose another')

    def validate_email(self, email):
        '''Ensures that the email chosen by the user hasn't been registered to the database.'''
        user=User.query.filter_by(email=email.data).first()

        # If the email has been registered to the db, an error will be raised in the html form
        if user: 
            raise ValidationError('Email is taken, please choose another')

class ResetPasswordForm(FlaskForm):
    '''Form to fill to get reset password link in email'''
    email=StringField('Email', validators=[DataRequired(),
                                            Email()])
    submit = SubmitField('Reset Password')

    def validate_email(self, email):
        '''Ensures that the email chosen by the user hasn't been registered to the database.'''
        user=User.query.filter_by(email=email.data).first()

        # If the email has been registered to the db, an error will be raised in the html form
        if user is None: 
            raise ValidationError('Email is not registered')

class NewPasswordForm(FlaskForm):
    '''Form to fill to change password'''
    password=PasswordField('Password', validators=[DataRequired(), 
                                                    Length(8, 16)])
    confirm_password=PasswordField('Confirm Password', 
                                    validators=[EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Reset Password')
                                        
class UpdateAccountForm(FlaskForm):
    '''Update Account form'''
    username=StringField('Username', validators=[DataRequired(),
                                                Length(2, 20)])
    email=StringField('Email', validators=[DataRequired(),
                                            Email()])
    fname=StringField('First Name', validators=[DataRequired(),
                                                Length(2, 20)])
    lname=StringField('Last Name', validators=[DataRequired(),
                                                Length(2, 20)])
    profile_picture=FileField('Upload Profile Picture', validators=[ 
                                FileAllowed(['png', 'jpg'])])
    resume=FileField('Upload Profile Picture', validators=[ 
                                                         FileAllowed(['pdf', 'docx'])])
    is_admin=BooleanField('Are you an Admin')
    is_actively_interviewing=BooleanField('Are you actively in search for job')
    facebook_link=StringField('Facebook url', validators=[url()])
    twitter_link=StringField('Twitter url', validators=[url()])
    linkedin_link=StringField('Linkedin url', validators=[url()])
    is_recruiter=BooleanField('Are you a recruiter')
    salary=IntegerField('Expected sslary')
    submit = SubmitField('Update profile')

    def validate_username(self, username):
        '''Ensures that the username chosen by the user hasn't been registered to the database.'''

        # If the username has been registered to the db, an error will be raised in the html form
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username taken. Please choose another.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken, please choose another')