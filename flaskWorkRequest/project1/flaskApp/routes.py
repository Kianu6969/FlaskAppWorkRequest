import os
import secrets
from flask import render_template, url_for, flash, redirect
from flaskApp import app, db, bcrypt
 # this is our forms
from flaskApp.forms import Requestor_Registration, Staff_Registration, LoginForm, WorkRequestForm, RequestApproval, RequestOngoing, ProfileForm, RateStaff
from flaskApp.models import User, UserRequestForm, StaffExtension # this is our database model
from flask_login import login_user, current_user, logout_user, login_required # these are for handling sessions
from sqlalchemy import desc, asc
from datetime import datetime, timedelta
from PIL import Image


# no idea what this does
# @app.shell_context_processor
# def make_shell_context():
# 	return {'db': db, 'User': User}


# ADMINISTRATOR PAGE===================================

@app.route('/adminPage', methods=['GET', 'POST']) 
@login_required
def adminPage():
	if current_user.is_authenticated == False:
		return redirect(url_for('loginPage'))

	formStaff = Staff_Registration()
	formRequestor = Requestor_Registration()
	workRequest = UserRequestForm.query.order_by(UserRequestForm.priorityLevel)
	requestsCount = UserRequestForm.query.filter_by(status='Pending').count()
	pendingRequest = UserRequestForm.query.filter_by(status='Pending').order_by(desc(UserRequestForm.dateApproved))
	staffCount = User.query.filter_by(userType='Staff').count()
	
	staffs = StaffExtension.query.order_by(desc(StaffExtension.staffRating)).all()
	# staffProfilePic = User.query.filter_by(id=staffs.staffId)

	profileImage = url_for('static', filename='profilePic/'+current_user.profilePicture)
	# usersRequestor = User.query.filter_by(userType='Requestor')

	
	
	
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
		staffExtend = StaffExtension(staffName=formStaff.userName.data, staffExtension=userStaff, staffAge = formStaff.age.data, staffGender = formStaff.gender.data, staffOccupation = formStaff.occupation.data)
		db.session.add(userStaff)
		db.session.add(staffExtend)
		db.session.commit()
		flash(f'Account Staff Created for {formStaff.userName.data}!')
		return redirect(url_for('adminPage'))

	return render_template('adminDashboard.html',
	  						title='Admin Page',
	  						user=current_user.userName, 
	  						form2=formStaff,
	    					form=formRequestor, 
	    					workRequest=workRequest, 
	    					countReq=requestsCount,
	    					countStaff=staffCount,
	    					pendingRequest=pendingRequest,
	    					profileImage=profileImage,
	    					staff=staffs)
# reject a request
@app.route('/adminPage/reject/<name>/<int:ids>')
def reject(name, ids):
	_name = name
	_id = ids
	reqFormRemoved = UserRequestForm.query.filter_by(requestTitle=_name).first()
	db.session.delete(reqFormRemoved)
	db.session.commit()
	flash(f'{reqFormRemoved.requestorName} : {reqFormRemoved.requestTitle} - Removed')
	return redirect(url_for('adminPage'))



# ADMIN FINAL CONFIRMATION
@app.route('/adminPage/finalConfirmation/<name>/<int:idNum>', methods=['POST', 'GET'])
def adminFinalConfirm(name, idNum):
	name_ = name
	id_ = idNum

	user = UserRequestForm.query.filter_by(requestorName = name_, id = id_).first()
	user.status = 'Finished'
	db.session.commit()

	return redirect(url_for('adminPage'))


# ADMIN APPROVAL PAGE - This is where the admin can approve a pending work request
@app.route('/adminPage/requestApproval/<name>/<int:idNum>', methods=['POST', 'GET'])
def adminPageApproval(name, idNum):
	if current_user.is_authenticated == False:
		return redirect(url_for('loginPage'))

	name_ = name
	idNum_ = idNum
	formApprove = RequestApproval()
	user = UserRequestForm.query.filter_by(requestorName=name_, id=idNum_).first()
	approvedDate = datetime.now()
	userStaff = StaffExtension.query.all()
	# this will assign the specific staff
	

	profileImage = url_for('static', filename='profilePic/'+current_user.profilePicture)

	if formApprove.submitApproval.data and formApprove.validate_on_submit():
		staffAssigned = StaffExtension.query.filter_by(staffName=formApprove.assignStaff.data).first()
		user.staffAssignment = staffAssigned
		# set different time limits based on priority levels
		if formApprove.priorityLevel.data == '1':
			user.dateLimit = datetime.now() + timedelta(days=3)

		elif formApprove.priorityLevel.data == '2':
			user.dateLimit = datetime.now() + timedelta(days=14)

		elif formApprove.priorityLevel.data == '3':
			user.dateLimit = datetime.now() + timedelta(days=30)

		user.status = 'Approved'
		user.priorityLevel = formApprove.priorityLevel.data
		db.session.commit()
		return redirect(url_for('adminPage'))

	return render_template('adminApproval.html',id=idNum_, userName=name_, title='Admin Approval Page', user=current_user.userName, form=formApprove, user2=user, profileImage=profileImage, userStaff=userStaff)



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
	countRequests = UserRequestForm.query.filter_by(requestorName=current_user.userName).count()
	userRequestForms = UserRequestForm.query.filter_by(requestFormId=user.id).order_by(UserRequestForm.priorityLevel)
	profileImage = url_for('static', filename='profilePic/'+current_user.profilePicture)

	if form.submit.data and form.validate_on_submit():
		requestForm = UserRequestForm(requestorName=current_user.userName, requestedWork=form.workOrder.data, roomNumber=form.requestRoomNumber.data, avilabilityOfMaterials=form.materialAvailability.data,requestTitle = form.requestTitle.data, user=user, dateApproved=datetime.now())
		db.session.add(requestForm)
		db.session.commit()
	# user = User()
	# user.query.get(1).userName
	return render_template('requestorDashboard.html', title='Requestor Page', user=current_user.userName, form=form, userForm=userRequestForms, count=countRequests, profileImage=profileImage)

# STAFF PAGE===============================
@app.route('/staffPage', methods=['GET', 'POST'])
def staffPage():
	if current_user.is_authenticated == False:
		return redirect(url_for('loginPage'))

	#this returns a Staffextention from the user that has a type of staff
	userStaffAssigned = StaffExtension.query.filter_by(staffName=current_user.userName).first()
	user = StaffExtension.query.filter_by(staffId=current_user.id).first()
	profileImage = url_for('static', filename='profilePic/'+current_user.profilePicture)

	return render_template('staffDashboard.html', title='Staff Page', user=current_user.userName, userStaff=user, profileImage=profileImage, userStaffAssigned=userStaffAssigned.staffAssignment)

# This is where the finished requests go 
@app.route('/staffPage/finished/<name>/<int:id>', methods=['POST', 'GET'])
def staffFinishedPage(name, id):
	_name = name
	_id = id
	form = UserRequestForm.query.filter_by(requestTitle=_name, id = _id).first()
	form.status = 'Semi Final'
	form.dateApproved = datetime.now()
	db.session.commit()

	return redirect(url_for('staffPage'))

# Rate staff
@app.route('/staffPage/rateStaff/<reqId>/<idNum>', methods=['GET', 'POST'])
def rateStaff(reqId, idNum):

	form = RateStaff()
	name_= reqId
	id_ = idNum
	user = UserRequestForm.query.filter_by(assignedStaff=id_, id=name_).first()
	count = UserRequestForm.query.filter_by(assignedStaff=id_).count()
	user.requestRating = 3
	# db.session.commit()
	# f"{user.requestTitle}, {user.staffAssignment.staffName}, {count}"

	return render_template('rateStaff.html', title='Rate Staff', name=user.requestTitle, work=user.staffAssignment.staffName)


# Staff ongoing page - where the staff can change the status of the form
@app.route('/staffPage/Ongoing/<name>/<idNum>', methods=['GET', 'POST'])
def staffOngoingPage(name, idNum):
	if current_user.is_authenticated == False:
		return redirect(url_for('loginPage'))

	_name = name
	_id = idNum
	profileImage = url_for('static', filename='profilePic/'+current_user.profilePicture)
	form = UserRequestForm.query.filter_by(requestorName=_name, id=_id).first()
	
	formSubmit = RequestOngoing()

	if formSubmit.submit.data and formSubmit.validate_on_submit():
		form.status = 'OnGoing'
		db.session.commit()
		return redirect(url_for('staffPage'))

	return render_template('staffOngoing.html', name=_name, title='Staff Ongoing Page', profileImage=profileImage, user=current_user.userName, form=form, formSubmit=formSubmit)

# Save Picture 
def savePic(formPic):
	randomHex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(formPic.filename)
	picFileName = randomHex + f_ext
	fpath = os.path.join(app.root_path, 'static/profilePic', picFileName)

	outputSize = (500, 500)
	i = Image.open(formPic)
	i.thumbnail(outputSize)

	i.save(fpath)

	return picFileName

# PROFILE PAGE FOR USERS
@app.route('/profilePage', methods=['GET', 'POST'])
def profilePage():
	if current_user.is_authenticated == False:
		return redirect(url_for('loginPage'))

	profileImage = url_for('static', filename='profilePic/'+current_user.profilePicture)
	profile = User.query.filter_by(id=current_user.id).first()
	form = ProfileForm()
	currentProfile = current_user.profilePicture
	ratingView = User.query.filter_by(id=current_user.id).first()
	page = 'None'
	pageTemplate = 'profilePage.html'

	# changing pages for different users
	if current_user.userType == 'Admin':
		page = 'adminPage'
		pageTemplate = 'profilePageAdmin.html'

	elif current_user.userType == 'Staff':
		
		page = 'staffPage'
		pageTemplate = 'profilePageStaff.html'

	elif current_user.userType == 'Requestor':
		page = 'requestorPage'
		pageTemplate = 'profilePageRequestor.html'

	if form.submit.data and form.validate_on_submit():
		if form.profilePic.data:
			updatedProfilePic = savePic(form.profilePic.data)
			current_user.profilePicture = updatedProfilePic
			db.session.commit()

		return redirect(url_for('profilePage'))


	return render_template(pageTemplate, title='Profile Page', user=current_user.userName, profileImage=profileImage, page=page, profile=profile, form=form, currentProfile=currentProfile, ratingView=ratingView)


# LOGOUT PAGE (this will logout the current user session)===================
@app.route('/logout', methods=['GET', 'POST'])
def logout():
	if current_user.is_authenticated == False:
		return redirect(url_for('loginPage'))
	logout_user()
	return redirect('loginPage')





