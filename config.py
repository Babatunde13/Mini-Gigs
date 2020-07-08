'''Module for creating configuration object just like settings.py in Django'''

import os

basedir =  os.path.abspath(os.path.dirname(__file__ ))

class Config:
    '''Common configuration that is used duriin development, production and testing'''
    SECRET_KEY=os.environ.get('SECRET_KEY') or '302669542ecbae5d1d7a744ea10380d7'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    MAIL_SUBJECT='[Mini Gigs]'
    MINI_GIGS_ADMIN=os.environ.get('MINI_GIGS__ADMIN')
    MAIL_PORT=587
    MAIL_USERNAME=os.environ.get('EMAIL_USER')
    MAIL_PASSWORD=os.environ.get('EMAIL_PASS')
    MAIL_SERVER='smtp.googlemail.com'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    '''Development configurations'''
    DEBUG=True
    MAIL_USE_TLS=True
    SQLALCHEMY_DATABASE_URI=os.environ.get('DEV_DATABASE_URL') or \
         'sqlite:///' + os.path.join(basedir, 'site.db')

class TestingConfig(Config):
    '''Testing configurations'''
    TESTING=True
    SQLALCHEMY_DATABASE_URI=os.environ.get('TEST_DATABASE_URL') or \
         'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    '''Production configurations'''
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
         'sqlite:///' + os.path.join(basedir, 'data.sqlite')
        
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': Config
}