function showError(msg) {
	var dialog = Dialog('baseDialog');
	dialog.setTitle('Petite problème');
	dialog.setMessage(msg);
	dialog.show();
}

(function() {
	addKeyboardShortcut(['Enter'], function(event){
		document.getElementById('register-form').submit();
	});
})();