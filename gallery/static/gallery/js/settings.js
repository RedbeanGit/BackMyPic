function settingsDelete() {
	inputDialogRun(
		'Supprimer le compte',
		'Confirmer le mot de passe',
		function(value) {
			document.getElementById('input-confirm-password').value = value;
			sendAction('delete');
		},
		function() {}
	);
}

function settingsLogout() {
	infoDialogRun(
		'Se deconnecter',
		'Veux-tu vraiment te déconnecter ?',
		function(value) {
			sendAction('logout');
		},
		function() {}
	);
}

function settingsSave() {
	inputDialogSetType('password');
	inputDialogRun(
		'Modifier les données de connexion',
		'Confirmer l\'ancien mot de passe',
		function(value) {
			document.getElementById('input-confirm-password').value = value;
			sendAction('save');
		},
		function() {}
	);
}

function sendAction(actionName) {
	var input = document.getElementById('input-action');
	var form = document.getElementById('form-action');

	input.value = actionName;
	form.submit();
}