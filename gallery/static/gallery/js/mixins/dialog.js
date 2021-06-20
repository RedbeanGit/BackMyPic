var cancelFunctions = [],
	acceptFunctions = [],
	blurSelector = 'header, footer, section > *:not(.dialog)';

function dialogSetTitle(msg) {
	var title = document.querySelector('.dialog__header p');
	title.innerText = msg;
}

function dialogSetInput(type, name, value, placeholder, autocomplete) {
	dialogSetContent('<input type="' + type + '" name="' + name + '" value="' + value + '" placeholder="' + placeholder + '" autocomplete="' + autocomplete + '" class="input" id="dialog-content">');
}

function dialogSetMessage(message) {
	dialogSetContent('<p id="dialog-content">' + message + '</p>');
}

function dialogSetContent(html) {
	var body = document.querySelector('.dialog__body');

	if (body.firstElementChild.id == 'dialog-content')
		body.firstElementChild.remove();
	body.insertAdjacentHTML('afterbegin', html);
}

function dialogAddCancelFunction(fct) {
	cancelFunctions.push(fct);
}

function dialogAddAcceptFunction(fct) {
	acceptFunctions.push(fct);
}

function dialogShow() {
	var dialog = document.querySelector('.dialog');
	var back = document.querySelectorAll(blurSelector);
	var content = document.getElementById('dialog-content');

	dialog.style.height = 'auto';
	dialog.style.opacity = '1';
	dialog.style.transition = 'height 0s 0s, opacity 0.3s 0s';

	for (let element of back)
		element.style.filter = 'grayscale(80%) blur(5px)';
	content.focus();

	addKeyboardShortcut(['Enter'], dialogAccept);
	addKeyboardShortcut(['Escape'], dialogCancel);
}

function dialogHide() {
	var dialog = document.querySelector('.dialog');
	var back = document.querySelectorAll(blurSelector);

	dialog.style.height = '0';
	dialog.style.opacity = '0';
	dialog.style.transition = 'height 0s 0.2s, opacity 0.2s 0s';

	for (let element of back)
		element.style.filter = 'initial';

	removeKeyboardShortcut(['Enter'], dialogAccept);
	removeKeyboardShortcut(['Escape'], dialogCancel);
}

function dialogCancel() {
	dialogHide();
	for (let fct of cancelFunctions)
		fct();
}

function dialogAccept() {
	dialogHide();
	var input = document.getElementById('dialog-content');
	
	for (let fct of acceptFunctions)
		fct(input.value);
}

function dialogClearCancelFunctions() {
	cancelFunctions = [];
}

function dialogClearAcceptFunctions() {
	acceptFunctions = [];
}

function dialogSetBlurSelector(selector) {
	blurSelector = selector;
}