const burger_button = document.querySelector('.dropdown-toggle');
const burger_menu = document.querySelector('.dropdown-items');

burger_button.addEventListener('click', function(){
	burger_menu.classList.toggle('show');
});