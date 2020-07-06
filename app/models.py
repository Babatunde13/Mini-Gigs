'''Models needed for the full functionality of the app'''

# Third party imports
from datetime import datetime
import hashlib
from flask import request
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# local imports
from app import db, app, login_manager


@login_manager.user_loader
def load_user(user_id):
    '''Dynamically gets the details of the user for easy use in the client side'''
    return User.query.get(int(user_id))

#Association table for user and job models
users_jobs = db.Table('users_jobs',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('job_id', db.Integer, db.ForeignKey('job.id'))
)

#Association table for user and interests models
users_interests = db.Table('users_interests',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'))
)

#Association table for user and skills models
users_skills = db.Table('users_skills',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
)

class User(db.Model, UserMixin):
    '''User representation in the database, it is connected to Job, 
        Interest and Skill models in a many-to many relationship.
        It is connected toEducation and Work Experience models in a one-to-many relationship.'''
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    fname=db.Column(db.String(20), nullable=False)
    lname=db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True ,nullable=False)
    profile_picture=db.Column(db.String, default='default.jpg')
    resume=db.Column(db.String)
    address=db.Column(db.Text)
    is_super_admin=db.Column(db.Boolean, default=False)
    is_confirmed=db.Column(db.Boolean, default=False)
    is_recruiter=db.Column(db.Boolean, default=False)
    is_actively_interviewing=db.Column(db.Boolean, default=False)
    education_details=db.relationship('Education', backref='author', lazy=True)
    work_experience=db.relationship('WorkExperience', backref='author', lazy=True)
    facebook_link=db.Column(db.String)
    twitter_link=db.Column(db.String)
    linkedin_link=db.Column(db.String)
    salary_expt=db.Column(db.Integer)
    password=db.Column(db.String(60), nullable=False)
    jobs=db.relationship('Job', #connects the user to the jobs model
                        secondary=users_jobs,
                        backref=db.backref('users', lazy='dynamic'),
                        lazy='dynamic')
    interests=db.relationship('Interest', #connects the user to the interest model
                        secondary=users_interests,
                        backref=db.backref('users', lazy='dynamic'),
                        lazy='dynamic')
    skills=db.relationship('Skill', #connects the user to the skill model
                        secondary=users_skills,
                        backref=db.backref('users', lazy='dynamic'),
                        lazy='dynamic')

    def get_reset_token(self, expires_sec=1800):
        '''Generates a timed token to reset password/confirm account'''
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def gravatar(self, size=100, default='identicon', rating='g'):
        '''Generates a profile image url and sends it to the client side
         if user doesn't set a profile picture'''
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash_ = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash_}?s={size}&d={default}&r={rating}'.format(
                                                            url=url, 
                                                            hash_=hash_, 
                                                            size=size, 
                                                            default=default, 
                                                            rating=rating)
    
    @staticmethod 
    def verify_reset_token(token):
        '''Verifies the timed token generated in the function above'''
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"User('{self.username}', '{self.email}')"

class Job(db.Model):
    '''Job representation in the database. The many side of a many-to-many relationship with user model'''
    id = db.Column(db.Integer, primary_key=True)
    company=db.Column(db.String)
    title=db.Column(db.String)
    description=db.Column(db.Text)
    expiry_date=db.Column(db.DateTime, default=datetime.utcnow)
    date_posted=db.Column(db.DateTime, default=datetime.utcnow)
    is_visible=db.Column(db.Boolean, default=True)
    creator_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"User('{self.company}', '{self.expiry_date}')"
    

class WorkExperience(db.Model):
    '''Work Experience representation in the database. The many side of a one-to-many relationship with user model'''
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(30), nullable=False)
    description=db.Column(db.Text, nullable=False)
    start_date=db.Column(db.DateTime, default=datetime.utcnow)
    end_date=db.Column(db.DateTime, default=datetime.utcnow)
    impact=db.Column(db.String)
    company=db.Column(db.String(30), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"User('{self.title}', '{self.end_date}')"

class Education(db.Model):
    '''Education representation in the database. The many side of a one-to-many relationship with user model'''
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(30), nullable=False)
    description=db.Column(db.Text, nullable=False)
    school=db.Column(db.String(30), nullable=False)
    start_date=db.Column(db.DateTime, default=datetime.utcnow)
    end_date=db.Column(db.DateTime, default=datetime.utcnow)
    impact=db.Column(db.String)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"User('{self.title}', '{self.end_date}')"

class Interest(db.Model):
    '''Interest representation in the database. The many side of a one-to-many relationship with user model'''
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30), nullable=False)

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"User('{self.name}')"

class Skill(db.Model):
    '''Skill representation in the database. The many side of a one-to-many relationship with user model'''
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30), nullable=False)

    def __repr__(self):
        '''This functions describes how the user model will be displayed'''
        return f"User('{self.name}')"

