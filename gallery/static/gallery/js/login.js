function showError(msg) {
	dialogSetTitle('Petite problème');
	dialogSetMessage(msg);
	dialogShow();
}

(function() {
	addKeyboardShortcut(['Enter'], function(event){
		document.getElementById('login-form').submit();
	});
})();