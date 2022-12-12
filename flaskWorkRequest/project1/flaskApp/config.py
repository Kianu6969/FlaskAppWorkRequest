import os 
from flask import current_app

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'the-key'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///workRequest2.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False