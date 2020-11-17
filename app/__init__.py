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

#Initalising the db
db = SQLAlchemy(app)
login_manager = LoginManager(app) #Initialising the login manager for authentication
login_manager.login_view='login'
login_manager.login_message='You need to login first to access this page'
login_manager.login_message_category='info'
login_manager.session_protection='strong'

from config import config
app.config.from_object(config['production'])

mail= Mail(app)
migrate = Migrate(app, db)

# Calling the view functions
from app import routes
