const home_btn = document.querySelector('.nav-home');
const staff_btn = document.querySelector('.nav-staff');
const request_btn = document.querySelector('.nav-requests');
const showInfo_btn = document.querySelector('.show-info');

const home = document.querySelector('.feed-home');
const staff = document.querySelector('.feed-staff');
const requestor = document.querySelector('.feed-requestor');
const request = document.querySelector('.feed-request');

console.log('yeah');
home_btn.style.background = "var(--blueGreen)";

// =======================================
// ======== THIS IS FOR NAVIGATION =======
// =======================================

// for navigating to home
home_btn.addEventListener('click', function(){
	home_btn.style.background = "var(--blueGreen)";
	staff_btn.style.background = "var(--white)";
	// requestor_btn.style.background = "var(--white)";
	request_btn.style.background = "var(--white)";

	home.style.display = "grid";
	staff.style.display = "none";
	// requestor.style.display = "none";
	request.style.display = "none";
});


// for navigating to staff
staff_btn.addEventListener('click', function(){
	home_btn.style.background = "var(--white)";
	staff_btn.style.background = "var(--blueGreen)";
	// requestor_btn.style.background = "var(--white)";
	request_btn.style.background = "var(--white)";

	home.style.display = "none";
	staff.style.display = "grid";
	// requestor.style.display = "none";
	request.style.display = "none";
});


// for navigating to requests
request_btn.addEventListener('click', function(){
	home_btn.style.background = "var(--white)";
	staff_btn.style.background = "var(--white)";
	// requestor_btn.style.background = "var(--white)";
	request_btn.style.background = "var(--blueGreen)";

	home.style.display = "none";
	staff.style.display = "none";
	// requestor.style.display = "none";
	request.style.display = "grid";
});

// ==================================================
// ======== THIS IS FOR THE PROGRESS BAR =======
// ==================================================

var element = document.querySelectorAll('.approved');
var elementOngoing = document.querySelectorAll('.ongoing')
var elementFinished = document.querySelectorAll('.finished')

var progress_bar = document.querySelectorAll('.progress-bar');


// this will load automatocally when the page refreshes or loads
function progress(){
	for (var i = 0; i < progress_bar.length; i++){
		var percent = element[i];
		var ongoing = elementOngoing[i];
		var finised = elementFinished[i];
		
		if (percent.value == 50 || percent.value == 90){
			ongoing.style.background = '#87C0CD';
			ongoing.style.color = '#F3F9FB';
			ongoing.innerText = 'check';
			progress_bar[i].style.width = percent.value+'%';

			if(percent.value == 90){
				finised.style.background = '#87C0CD';
				finised.innerText = 'check';
				finised.style.color = '#F3F9FB';
			}
		}
		
		console.log(ongoing.style.background);
		console.log('innerText: ', percent.value);
	}
}
 	




