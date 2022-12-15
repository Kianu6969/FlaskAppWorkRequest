var addBtn = document.querySelector('.request-work-btn');
var closeBtn = document.querySelector('.request-form-close');
var modal = document.querySelector('.modal-popup-request-form');

var input1 = document.querySelector('.requestTitle');
var input2 = document.querySelector('.requestRoomNumber');

addBtn.addEventListener('click', function(){
	modal.classList.add('modal-popup-request-form-active');
});

closeBtn.addEventListener('click', function(){
	modal.classList.remove('modal-popup-request-form-active');
	input1.value = "";
	input2.value = "";
});




