from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskApp.config import Config
from flask import current_app
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# setting a varibale to an instance of this Flask class
def create_app():
	app = Flask(__name__)

	return app


app = create_app()
app.app_context().push()

# a secret key will protect users against modifying cookies and forgery requests
app.config.from_object(Config)
# /// is a relative path which means the database will be created in this project folder
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)




# this new flask update is confusing
with app.app_context():
	db.create_all()

from flaskApp import routes