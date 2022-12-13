from flask import render_template, url_for, flash, redirect
from flaskApp import app, db, bcrypt
 # this is our forms
from flaskApp.forms import Requestor_Registration, Staff_Registration, LoginForm, WorkRequestForm, RequestApproval
from flaskApp.models import User, UserRequestForm # this is our database model
from flask_login import login_user, current_user, logout_user # these are for handling sessions
from sqlalchemy import desc


# dummy data
requestsData = [
	{
		'department': 'CCSIT',
		'workRequest': 'Cleaning',
		'date': 'October 15, 2022',
		'level': 'High'
	},
	{
		'department': 'OSAS',
		'workRequest': 'Plumbing',
		'date': 'September 17, 2022'
	},
	{
		'department': 'Lab 1',
		'workRequest': 'Computer Maintenance',
		'date': 'September 07, 2022',
		'level': 'High'
	},
	{
		'department': 'Office 2',
		'workRequest': 'Wifi Installation',
		'date': 'October 25, 2022',
		'level': 'Medium'
	},
	{
		'department': 'MSIT',
		'workRequest': 'Aircondition Repair',
		'date': 'November 1, 2022',
		'level': 'Low'
	},
	{
		'department': 'Oracle',
		'workRequest': 'Tiles Repair',
		'date': 'October 28, 2022',
		'level': 'High'
	}
]
# no idea what this does
# @app.shell_context_processor
# def make_shell_context():
# 	return {'db': db, 'User': User}


# ADMINISTRATOR PAGE===================================

@app.route('/adminPage', methods=['GET', 'POST']) 
def adminPage():
	formStaff = Staff_Registration()
	formRequestor = Requestor_Registration()
	workRequest = UserRequestForm.query.order_by(desc(UserRequestForm.id))
	requestsCount = UserRequestForm.query.filter_by(status='unApproved').count()
	pendingRequest = UserRequestForm.query.filter_by(status='unApproved')
	staffCount = User.query.filter_by(userType='Staff').count()
	# usersRequestor = User.query.filter_by(userType='Requestor')

	if current_user.is_authenticated == False:
		return redirect(url_for('loginPage'))
	
	
	# ----- Requestor Registration -----
	if formRequestor.submitReq.data and formRequestor.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(formRequestor.passWord.data).decode('utf-8')
		userReq = User(userName=formRequestor.userName.data, passWord=hashed_pass, userType='Requestor')
		db.session.add(userReq)
		db.session.commit()
		flash(f'Account Requestor Created for {formRequestor.userName.data}!')
		return redirect(url_for('adminPage'))

	# ----- Staff Regstration ------
	elif formStaff.submitStaff.data and formStaff.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(formStaff.passWord.data).decode('utf-8')
		userStaff = User(userName=formStaff.userName.data, passWord=hashed_pass, userType='Staff')
		db.session.add(userStaff)
		db.session.commit()
		flash(f'Account Staff Created for {formStaff.userName.data}!')
		return redirect(url_for('adminPage'))

	return render_template('adminDashboard.html',
							requestsData=requestsData,
	  						title='Admin Page',
	  						user=current_user.userName, 
	  						form2=formStaff,
	    					form=formRequestor, 
	    					workRequest=workRequest, 
	    					countReq=requestsCount,
	    					countStaff=staffCount,
	    					pendingRequest=pendingRequest)
# reject a request
@app.route('/adminPage/reject/<name>/<int:ids>')
def reject(name, ids):
	_name = name
	_id = ids
	reqFormRemoved = UserRequestForm.query.filter_by(requestTitle=_name).first()
	flash(f'{reqFormRemoved.requestorName} : {reqFormRemoved.requestTitle} Removed')
	return redirect(url_for('adminPage'))

# ADMIN APPROVAL PAGE - This is where the admin can approve a pending work request
@app.route('/adminPage/requestApproval/<name>/<int:idNum>', methods=['POST', 'GET'])
def adminPageApproval(name, idNum):
	name_ = name
	idNum_ = idNum
	formApprove = RequestApproval()
	user = UserRequestForm.query.filter_by(requestorName=name_, id=idNum_).first()
	if formApprove.submitApproval.data and formApprove.validate_on_submit():
		user.status = 'Approved'
		db.session.commit()
		return redirect(url_for('adminPage'))

	return render_template('adminApproval.html',id=idNum_, userName=name_, title='Admin Approval Page', user=current_user.userName, form=formApprove, user2=user)



# home page / login page ===============================
@app.route('/', methods=['GET', 'POST']) 
@app.route('/loginPage', methods=['GET', 'POST']) 
def loginPage():
	form = LoginForm()

	user = User.query.filter_by(userName=form.userName.data).first()
	# staff = User.query.filter_by(userName=form.userName.data).first()
	# admin = User.query.filter_by(userName=form.userName.data).first()


	if form.validate_on_submit():
		# bcrypt.check_password_hash(user.passWord, form.passWord.data
		# user Admin Authentication ===========
		if user and bcrypt.check_password_hash(user.passWord, form.passWord.data):
			# db.session.commit()
			login_user(user,remember=form.remember.data)
			# Redirect to the users specified usertype dashboard
			if user.userType == 'Admin':
				if current_user.is_authenticated:
					return redirect(url_for('adminPage'))
			elif user.userType == 'Requestor':
				if current_user.is_authenticated:
					return redirect(url_for('requestorPage'))
			elif user.userType == 'Staff':
				if current_user.is_authenticated:
					return redirect(url_for('staffPage'))

		else:
			flash('Invalid Account!!')
			return redirect(url_for('loginPage'))
						

	return render_template('login.html', title='Login Page', form=form)

# REQUESTOR PAGE===============================
@app.route('/requestorPage', methods=['GET', 'POST'])
def requestorPage():
	if current_user.is_authenticated == False:
		return redirect(url_for('loginPage'))
	form = WorkRequestForm()
	user = User.query.filter_by(userName=current_user.userName).first()
	userRequestForms = UserRequestForm.query.filter_by(requestFormId=user.id).order_by(desc(UserRequestForm.id))

	if form.submit.data and form.validate_on_submit():
		requestForm = UserRequestForm(requestorName=current_user.userName, requestedWork=form.workOrder.data, roomNumber=form.requestRoomNumber.data, avilabilityOfMaterials=form.materialAvailability.data,requestTitle = form.requestTitle.data, user=user)
		db.session.add(requestForm)
		db.session.commit()
	# user = User()
	# user.query.get(1).userName
	return render_template('requestorDashboard.html', title='Requestor Page', user=current_user.userName, form=form, userFrom=userRequestForms)

# STAFF PAGE===============================
@app.route('/staffPage', methods=['GET', 'POST'])
def staffPage():
	if current_user.is_authenticated == False:
		return redirect(url_for('loginPage'))
	return render_template('staffDashboard.html', title='Staff Page', user=current_user.userName)


# LOGOUT PAGE (this will logout the current user session)===================
@app.route('/logout', methods=['GET', 'POST'])
def logout():
	if current_user.is_authenticated == False:
		return redirect(url_for('loginPage'))
	logout_user()
	return redirect('loginPage')





