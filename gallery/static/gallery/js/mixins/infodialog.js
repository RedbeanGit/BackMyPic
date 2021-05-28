var cancelFunction = function(){},
	acceptFunction = function(){};

function infoDialogSetTitle(msg) {
	var title = document.querySelector('.infodialog__header p');
	title.innerText = msg;
}

function infoDialogSetMessage(msg) {
	var p = document.getElementById('infodialog-content');
	p.innerText = msg;
}

function infoDialogSetCancel(fct) {
	cancelFunction = fct;
}

function infoDialogSetAccept(fct) {
	acceptFunction = fct;
}

function infoDialogShow() {
	var infoDialog = document.querySelector('.infodialog');
	var back = document.querySelectorAll('header, footer, section > *:not(.infodialog)');
	
	infoDialog.style.height = 'auto';
	infoDialog.style.opacity = '1';
	infoDialog.style.transition = 'height 0s 0s, opacity 0.3s 0s';

	for (let element of back)
		element.style.filter = 'grayscale(80%) blur(5px)';
}

function infoDialogHide() {
	var infoDialog = document.querySelector('.infodialog');
	var back = document.querySelectorAll('header, footer, section > *:not(.infodialog)');

	infoDialog.style.height = '0';
	infoDialog.style.opacity = '0';
	infoDialog.style.transition = 'height 0s 0.2s, opacity 0.2s 0s';

	for (let element of back)
		element.style.filter = 'initial';
}

function infoDialogCancel() {
	cancelFunction();
	infoDialogHide();
}

function infoDialogAccept() {
	var p = document.getElementById('infodialog-content');
	acceptFunction(p.value);
	infoDialogHide();
}

function infoDialogRun(title, message, acceptFct, cancelFct) {
	infoDialogSetTitle(title);
	infoDialogSetMessage(message);
	infoDialogSetAccept(acceptFct);
	infoDialogSetCancel(cancelFct);
	infoDialogShow();
}

(function() {
	document.body.addEventListener('keyup', function(event) {
		event.preventDefault();
		if (event.keyCode === 13) {
			document.getElementById('infodialog-accept').click();
		}
	});
})();