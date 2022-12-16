console.log('Hey');

// Modal pupop

var assignStaffBtn = document.querySelector('.assign-btn');
var modal = document.querySelector('.modal-wrapper');
var staffName = document.querySelectorAll('#staffName');
var closeBtn = document.getElementById('close-btn');
var assignStaff = document.querySelector('.assignStaff');

console.log(assignStaff.value);
console.log(staffName.textContent);

// opening the modal
assignStaffBtn.addEventListener('click', function(){
	modal.style.display = 'flex';
});

// closing the modal
closeBtn.addEventListener('click', function(){
	modal.style.display = 'none';
});

for (let i = 0; i < staffName.length; i++){
	staffName[i].addEventListener('click', function(){
		assignStaff.value = staffName[i].textContent;
		modal.style.display = 'none';
	});
	console.log(staffName[i].textContent);
}

