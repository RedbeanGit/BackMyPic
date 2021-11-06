function settingsDelete() {
	var dialog = new Dialog('oldPasswordDialog');
	dialog.setTitle('Supprimer le compte');
	dialog.setInput('password', 'old_password', '', 'Confirmer le mot de passe', 'current-password');
	dialog.addAcceptFunction(function(value){
		settingsSend('delete');
	});
	dialog.setBlurSelector('header, .sectiontitle, .form__content > *:not(#oldPasswordDialog), footer');
	dialog.show();
}

function settingsLogout() {
	var dialog = new Dialog('logoutDialog');
	dialog.setTitle('Se déconnecter');
	dialog.setMessage('Veux-tu vraiment te déconnecter ?');
	dialog.addAcceptFunction(function(value){
		settingsSend('logout');
	});
	dialog.setBlurSelector('header, .sectiontitle, .form__content > *:not(#logoutDialog), footer');
	dialog.show();
}

function settingsSave() {
	var dialog = new Dialog('oldPasswordDialog');
	dialog.setTitle('Confirme ton identité');
	dialog.setInput('password', 'old_password', '', 'Confirme ton ancien mot de passe', 'current-password');
	dialog.addAcceptFunction(function(value){settingsSend('save');});
	dialog.setBlurSelector('header, .sectiontitle, .form__content > *:not(#oldPasswordDialog), footer');
	dialog.show();
}

function settingsSend(actionName) {
	var input = document.getElementById('action-input');
	var form = document.getElementById('action-form');

	input.value = actionName;
	form.submit();
}