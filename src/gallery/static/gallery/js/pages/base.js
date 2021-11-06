var keyboardShortcuts = [],
	keyPressed = {};


function showMessage(msg, title) {
	var dialog = new Dialog('baseDialog');
	dialog.setTitle(title);
	dialog.setMessage(msg);
	dialog.setBlurSelector('body > *:not(#baseDialog)');
	dialog.show();
}

function alert(msg) {
	showMessage(msg, 'Message')
}

function alertError(msg) {
	showMessage(msg, 'Petit problème');
}

function alertExperimental() {
	showMessage('Cette fonctionnalité est encore expérimentale', 'Non disponible');
}

function addKeyboardShortcut(keys, fct, ...args) {
	keyboardShortcuts.push({
		fct: fct,
		keys: keys,
		args: args
	});
}

function removeKeyboardShortcut(keys, fct) {
	for (let i in keyboardShortcuts) {
		if (keyboardShortcuts[i].fct == fct && keyboardShortcuts[i].keys == keys) {
			keyboardShortcuts.splice(i, 1);
			i--;
		}
	}
}

function updateKeyboardShortcut(shortcut) {
	for (let key of shortcut.keys) {
		if (!keyPressed[key])
			return;
	}
	shortcut.fct(...shortcut.args);
}

function updateKeyboardShortcuts() {
	for (let shortcut of keyboardShortcuts) {
		updateKeyboardShortcut(shortcut);
	}
}

function resetKeyPressed() {
	keyPressed = {}
}



(function() {
	document.addEventListener('keydown', function(event) {   
		keyPressed[event.key] = true;
		keyPressed['Control'] = event.ctrlKey;
		updateKeyboardShortcuts();
	});
	document.addEventListener('keyup', function(event) {
		keyPressed[event.key] = false;
		keyPressed['Control'] = event.ctrlKey;
	});
})();