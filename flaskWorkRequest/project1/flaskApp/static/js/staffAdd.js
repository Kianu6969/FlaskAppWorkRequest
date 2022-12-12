
// Modal variables requestor
var addStaffbtn = document.querySelector('.registerStaff-btn');
var modalBgStaff = document.querySelector('.modal-bg-staff');
var closeBtnStaff = document.getElementById('close-btn-staff');



// Form variables requestor
var userNameStaff = document.querySelector('.username-staff');
var passStaff = document.querySelector('.password-staff');
// var rePass = document.querySelector('.re-password');

// Open the modal pop-up for requestor
addStaffbtn.addEventListener('click', function(){
	modalBgStaff.classList.add('modalbg-active-staff');

});
// Close the modal pop-up requestor
closeBtnStaff.addEventListener('click', function(){
	modalBgStaff.classList.remove('modalbg-active-staff');
	userNameStaff.value = "";
	passStaff.value = "";
	// rePass.value = "";

});

