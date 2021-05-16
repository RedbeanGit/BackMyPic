function showInputDialog(msg, fct) {
	sheet = document.getElementById('input-sheet');

	if (sheet) {
		sheet.querySelector('label').textContent = msg + ' :';
		sheet.querySelector('input[type=submit]').onclick =	function(){
			fct(document.getElementById('input-sheet__input').value);
		};
		sheet.classList.add('input-sheet--visible');
	}
}

function hideInputDialog() {
	sheet = document.getElementById('input-sheet');

	if (sheet) {
		sheet.querySelector('label').textContent = '';
		sheet.querySelector('input[type=submit]').onclick =	function(){	};
		sheet.classList.remove('input-sheet--visible');
	}
}