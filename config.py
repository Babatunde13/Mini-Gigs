'''Module for creating configuration object just like settings.py in Django'''

import os

basedir =  os.path.abspath(os.path.dirname(__file__ ))

class Config:
    '''Common configurations that is used during development, production and testing'''
    SECRET_KEY=os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    MAIL_SUBJECT='[Mini Gigs]'
    MINI_GIGS_ADMIN=['koikibabatunde14@gmail.com']
    MAIL_PORT=587
    MAIL_USERNAME=os.environ.get('MAIL_USER')
    MAIL_PASSWORD=os.environ.get('MAIL_PASS') 
    MAIL_SERVER=os.environ.get('MAIL_SERVER')

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
         'sqlite:///' + os.path.join(basedir, 'data-test.db')

class ProductionConfig(Config):
    '''Production configurations'''
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
         'sqlite:///' + os.path.join(basedir, 'prod.db')
        
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': Config
}