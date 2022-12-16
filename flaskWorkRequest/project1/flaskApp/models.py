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
	profilePicture = db.Column(db.String(60), default='dafault.png')
	# this will be generated in the UserRequestform Table
	requestForm = db.relationship('UserRequestForm', backref='user') 
	userStaffExtension = db.relationship('StaffExtension', backref='staffExtension', uselist=False)

	def __repr__(self): # this will print 
		return f"User({self.id}, {self.userName}, {self.userType})"

# For User Staffs
class StaffExtension(db.Model):
	__tablename__ = 'userstaff'
	id = db.Column(db.Integer, primary_key=True)
	staffId = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
	staffName = db.Column(db.String(20), nullable=False)
	staffAge = db.Column(db.String(20), nullable=False)
	staffGender = db.Column(db.String(20), nullable=False)
	staffOccupation = db.Column(db.String(20), nullable=False)
	staffRating = db.Column(db.Integer, default=0)
	staffComments = db.relationship('StaffExtensionComment', backref='staffComment')

	staffAssignment = db.relationship('UserRequestForm', backref='staffAssignment') # one to many relationship

	def __repr__(self): # this will print 
		return f"User({self.id}, {self.staffId}, {self.staffName})"

# Staff Comments
class StaffExtensionComment(db.Model):
	__tablename__ = 'staffcomment'
	id = db.Column(db.Integer, primary_key=True)
	commentId = db.Column(db.Integer, db.ForeignKey('userstaff.id'), unique=True)
	comment = db.Column(db.String(500))

	def __repr__(self): # this will print 
		return f"User({self.id}, {self.commentId}, {self.comment})"

# Requestor Form table for UserRequestors
class UserRequestForm(db.Model):
	__tablename__ = 'userRequestForm'

	id = db.Column(db.Integer, primary_key=True)
	requestorName = db.Column(db.String(500), nullable=False)
	requestTitle = db.Column(db.String(500), nullable=False)
	requestedWork = db.Column(db.String(500), nullable=False)
	roomNumber = db.Column(db.String(20), nullable=False)
	avilabilityOfMaterials = db.Column(db.String(10), nullable=False)
	priorityLevel = db.Column(db.Integer, default=0) # change this to integer in the future 0 - pending 1 - high 2 - medium 3 - low
	status = db.Column(db.String(20), default='Pending')
	dateApproved = db.Column(DateTime, default=datetime.now(), nullable=False)
	dateLimit = db.Column(DateTime, default=datetime.now(), nullable=False)
	requestFormId = db.Column(db.Integer, db.ForeignKey('user.id'))

	assignedStaff = db.Column(db.Integer, db.ForeignKey('userstaff.id'), unique=True)

	def __repr__(self): # this will print 
		return f"User({self.requestorName},{self.requestTitle}, {self.requestedWork}, {self.roomNumber}, {self.requestFormId}, {self.priorityLevel}, {self.avilabilityOfMaterials}, {self.status})"


