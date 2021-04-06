var selectMode = false;

// Selection Mode
function switchSelectMode() {
	if (selectMode)
		stopSelectMode();
	else
		startSelectMode();
}

function startSelectMode() {
	selectMode = true;
	let selActions = document.querySelectorAll('.actionnav__element--selectable');

	for (let selAction of selActions)
		selAction.classList.remove('actionnav__element--disabled');
}

function stopSelectMode() {
	selectMode = false;
	let selActions = document.querySelectorAll('.actionnav__element--selectable');

	for (let selAction of selActions)
		selAction.classList.add('actionnav__element--disabled');
}

// Hide
function hideSelection() {
	if (selectMode) {
		sendAction('hide');
	}
}

// Add
function addElement() {
	
}

// Delete
function deleteSelection() {
	if (selectMode) {
		sendAction('delete');
	}
}

// Share
function shareSelection() {
	if (selectMode) {
		sendAction('share');
		alertExperimental();
	}
}

// Download
function downloadSelection() {
	if (selectMode) {
		sendAction('download');
	}
}

// when a picture is clicked
function activeSelection(event, elementId, link) {
	if (selectMode)
		selectElement(event, elementId);
	else
		showElement(elementId, link);
}

function selectElement(event, elementId) {
	
}

function showElement(elementId, link) {
	window.location.href = link;
}

// send action to the server
function sendAction(actionName) {
	let inputType = document.getElementById('actiontype-input');
	
	if (inputType) {
		inputType.value = actionName;
		let form = document.getElementById('action-form');

		if (form)
			form.submit();
	}
	stopSelectMode();
}