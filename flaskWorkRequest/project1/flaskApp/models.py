from datetime import datetime
from flaskApp import db, loginManager
from flask_login import UserMixin
from flaskApp.forms import LoginForm
from sqlalchemy.types import DateTime

@loginManager.user_loader
def loadUser(userId):
	return User.query.get(int(userId))



# Database Table Models
# user table =============================================
class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	userName = db.Column(db.String(20), unique=True, nullable=False)
	userType = db.Column(db.String(20), default='Admin')
	passWord = db.Column(db.String(60), nullable=False)

	# this will be generated in the UserRequestform Table
	requestForm = db.relationship('UserRequestForm', backref='user') 

	def __repr__(self): # this will print 
		return f"User({self.id}, {self.userName}, {self.userType})"

# Requestor Form table for UserRequestors
class UserRequestForm(db.Model):
	__tablename__ = 'userRequestForm'

	id = db.Column(db.Integer, primary_key=True)
	requestorName = db.Column(db.String(500), nullable=False)
	requestTitle = db.Column(db.String(500), nullable=False)
	requestedWork = db.Column(db.String(500), nullable=False)
	roomNumber = db.Column(db.Integer(), nullable=False)
	avilabilityOfMaterials = db.Column(db.String(10), nullable=False)
	priorityLevel = db.Column(db.Integer, default=0) # change this to integer in the future 0 - pending 1 - high 2 - medium 3 - low
	status = db.Column(db.String(20), default='Pending')
	dateApproved = db.Column(DateTime, default=datetime.now(), nullable=False)
	dateLimit = db.Column(DateTime, default=datetime.now(), nullable=False)
	requestFormId = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self): # this will print 
		return f"User({self.requestorName},{self.requestTitle}, {self.requestedWork}, {self.roomNumber}, {self.requestFormId}, {self.priorityLevel}, {self.avilabilityOfMaterials}, {self.status})"


