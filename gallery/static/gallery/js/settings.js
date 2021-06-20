function settingsDelete() {
	dialogSetTitle('Supprimer le compte');
	dialogSetInput('password', '', '', 'Confirmer le mot de passe', 'current-password');
	dialogAddAcceptFunction(function(value){
		document.getElementById('password-input').value = value;
		settingsSend('delete');
	});
	dialogShow();
}

function settingsLogout() {
	dialogSetTitle('Se déconnecter');
	dialogSetMessage('Veux-tu vraiment te déconnecter ?');
	dialogAddAcceptFunction(function(value){
		settingsSend('logout');
	});
	dialogShow();
}

function settingsSave() {
	function confirm() {
		dialogSetTitle('Confirme ton identité');
		dialogSetInput('password', '', '', 'Confirme ton ancien mot de passe', 'current-password');
		dialogAddAcceptFunction(function(value){
			document.getElementById('old-password-input').value = value;
			settingsSend('save');
		});
		dialogShow();
	}

	newPassword = document.getElementById('new-password-input');

	if (newPassword.value) {
		dialogSetTitle('Modifie tes données de connexion');
		dialogSetInput('password', '', '', 'Confirme ton nouveau mot de passe', 'new-password');
		dialogAddAcceptFunction(function(value) {
			dialogClearAcceptFunctions();
			document.getElementById('confirm-password-input').value = value;
			confirm();
		});
		dialogShow();
	} else {
		confirm();
	}
}

function settingsSend(actionName) {
	var input = document.getElementById('action-input');
	var form = document.getElementById('action-form');

	input.value = actionName;
	form.submit();
}

function showError(msg) {
	dialogSetTitle('Petite problème');
	dialogSetMessage(msg);
	dialogShow();
}