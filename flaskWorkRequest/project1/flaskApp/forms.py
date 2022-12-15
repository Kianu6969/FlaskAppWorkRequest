from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length, Email

# Registration Form Requestor
class Requestor_Registration(FlaskForm):

	userName = StringField('departmentName', 
							validators=[DataRequired(),
							Length(min=2, max=20)])

	passWord = PasswordField('password',
							validators=[DataRequired()])

	submitReq = SubmitField('Register')

# Work Request Approval
class RequestApproval(FlaskForm):
	priorityLevel = RadioField('Level', choices=[1,2,3])
	submitApproval = SubmitField('Approve')

# Registration Form Staff
class Staff_Registration(FlaskForm):

	userName = StringField('Staff Name', 
							validators=[DataRequired(),
							Length(min=2, max=20)])

	age = IntegerField('Age', validators=[DataRequired()])
	
	gender = RadioField('Gender', choices=['Male','Female'])
	occupation = StringField('Occupation', 
							validators=[DataRequired(),
							Length(min=2, max=20)])

	passWord = PasswordField('password', validators=[DataRequired()])

	submitStaff = SubmitField('Register')

# Login Form
class LoginForm(FlaskForm):
	userName = StringField('departmentName', 
							validators=[DataRequired(),
							Length(min=2, max=20)])

	passWord = PasswordField('password',
							validators=[DataRequired()])

	remember = BooleanField('Remember Me')

	submit = SubmitField('Login')

# Requestor Work Request Form
class WorkRequestForm(FlaskForm):

	requestTitle = StringField('requestTitle', validators=[DataRequired(), Length(min=5, max=100)])
	requestRoomNumber = StringField('requestRoomNumber', validators=[DataRequired()])
	others = StringField('others')
	workOrder = RadioField('WorkOrder', choices=['Repair',
												 'Replacement',
												 'Fabrication', 
												 'Installation', 
												 'Construction', 
												 'Landscaping',
												 'Cleaning',
												 'Hauling',
												 'Plumbing',
												 'Painting/Repainting'])
	materialAvailability = RadioField('materialAvialability', choices=['Yes', 'No'])
	submit = SubmitField('Submit Request')

