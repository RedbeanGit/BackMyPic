function Dialog(id) {
	this.htmlElement = document.getElementById(id);
	this.cancelFunctions = [];
	this.acceptFunctions = [];
	this.blurSelector = 'header, footer, section > *:not(.dialog)';

	this.cancelButton = this.htmlElement.querySelector('.dialog__button--cancel');
	this.acceptButton = this.htmlElement.querySelector('.dialog__button--accept');
	
	this.setTitle = function(msg) {
		var title = this.htmlElement.querySelector('.dialog__header p');
		title.innerText = msg;
	};
	this.setInput = function(type, name, value, placeholder, autocomplete) {
		this.setContent('<input type="' + type + '" name="' + name + '" value="' + value + '" placeholder="' + placeholder + '" autocomplete="' + autocomplete + '" class="input dialog__content">');
	};
	this.setMessage = function(message) {
		this.setContent('<p class="dialog__content">' + message + '</p>');
	};
	this.setContent = function(html) {
		var body = this.htmlElement.querySelector('.dialog__body');

		if (body.firstElementChild.classList.contains('dialog__content'))
			body.firstElementChild.remove();
		body.insertAdjacentHTML('afterbegin', html);
	};
	this.addCancelFunction = function(fct) {
		this.cancelFunctions.push(fct);
	};
	this.addAcceptFunction = function(fct) {
		this.acceptFunctions.push(fct);
	};
	this.show = function() {
		var dialog = this.htmlElement;
		var back = document.querySelectorAll(this.blurSelector);
		var content = this.htmlElement.querySelector('.dialog__content');

		dialog.style.height = 'auto';
		dialog.style.opacity = '1';
		dialog.style.transition = 'height 0s 0s, opacity 0.3s 0s';

		for (let element of back)
			element.style.filter = 'grayscale(80%) blur(5px)';
		content.focus();

		addKeyboardShortcut(['Enter'], this.accept);
		addKeyboardShortcut(['Escape'], this.cancel);
	};
	this.hide = function() {
		var dialog = this.htmlElement;
		var back = document.querySelectorAll(this.blurSelector);

		dialog.style.height = '0';
		dialog.style.opacity = '0';
		dialog.style.transition = 'height 0s 0.2s, opacity 0.2s 0s';

		for (let element of back)
			element.style.filter = 'initial';

		removeKeyboardShortcut(['Enter'], this.accept);
		removeKeyboardShortcut(['Escape'], this.cancel);
	};
	this.cancel = function() {
		this.hide();
		for (let fct of this.cancelFunctions)
			fct();
	};
	this.accept = function() {
		this.hide();
		var input = this.htmlElement.querySelector('.dialog__content');
	
		for (let fct of this.acceptFunctions)
			fct(input.value);
	};
	this.clearCancelFunctions = function() {
		this.cancelFunctions = [];
	};
	this.clearAcceptFunctions = function() {
		this.acceptFunctions = [];
	};
	this.setBlurSelector = function(selector) {
		this.blurSelector = selector;
	};

	this.cancelButton.onclick = this.cancel.bind(this);
	this.acceptButton.onclick = this.accept.bind(this);
}