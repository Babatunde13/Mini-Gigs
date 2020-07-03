'''Module for configuration of the flask app, flask extensions and some helper libraries'''

#Third party imports
import os

#Importing flask and needed flask extensions
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand

# Creating the flask app
app = Flask(__name__)
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY') or 'andjjsdnmsmdms'
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('Database') or 'sqlite:///site.db'

#Initalising the db
db = SQLAlchemy(app)
login_manager = LoginManager(app) #Initialising the login manager for authentication
login_manager.login_view='login'
login_manager.login_message='You need to login first to access this page'
login_manager.login_message_category='info'


# Some important configuration, a better practice is to use a different file for configurations
# the file should contain different object dlike testing config, development config and production config
login_manager.session_protection='strong'
app.config['MAIL_SERVER']=os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD']=os.environ.get('EMAIL_PASS') 
app.config['MAIL_SUBJECT']='Mini Gigs'
mail= Mail(app)
migrate = Migrate(app, db)

# Calling the view functions
from app import routes
