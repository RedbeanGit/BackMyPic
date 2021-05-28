var cancelFunction = function(){},
	acceptFunction = function(){};

function inputDialogSetTitle(msg) {
	var title = document.querySelector('.inputdialog__header p');
	title.innerText = msg;
}

function inputDialogSetPlaceholder(msg) {
	var input = document.getElementById('inputdialog-content');
	input.placeholder = msg;
}

function inputDialogSetCancel(fct) {
	cancelFunction = fct;
}

function inputDialogSetAccept(fct) {
	acceptFunction = fct;
}

function inputDialogSetType(type) {
	var input = document.getElementById('inputdialog-content');
	input.type = type;
}

function inputDialogShow() {
	var inputDialog = document.querySelector('.inputdialog');
	var back = document.querySelectorAll('header, footer, section > *:not(.inputdialog)');
	var input = document.getElementById('inputdialog-content');

	inputDialog.style.height = 'auto';
	inputDialog.style.opacity = '1';
	inputDialog.style.transition = 'height 0s 0s, opacity 0.3s 0s';

	for (let element of back)
		element.style.filter = 'grayscale(80%) blur(5px)';
	input.focus();
}

function inputDialogHide() {
	var inputDialog = document.querySelector('.inputdialog');
	var back = document.querySelectorAll('header, footer, section > *:not(.inputdialog)');

	inputDialog.style.height = '0';
	inputDialog.style.opacity = '0';
	inputDialog.style.transition = 'height 0s 0.2s, opacity 0.2s 0s';

	for (let element of back)
		element.style.filter = 'initial';
}

function inputDialogCancel() {
	cancelFunction();
	inputDialogHide();
}

function inputDialogAccept() {
	var input = document.getElementById('inputdialog-content');
	acceptFunction(input.value);
	inputDialogHide();
}

function inputDialogRun(title, placeholder, acceptFct, cancelFct) {
	inputDialogSetTitle(title);
	inputDialogSetPlaceholder(placeholder);
	inputDialogSetAccept(acceptFct);
	inputDialogSetCancel(cancelFct);
	inputDialogShow();
}

(function() {
	document.body.addEventListener('keyup', function(event) {
		event.preventDefault();
		if (event.keyCode === 13) {
			document.getElementById('inputdialog-accept').click();
		}
	});
})();