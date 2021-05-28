/* All features implemented in this file:
	- select
	- download
	- add
	- delete
	- share
	- hide
	- searchbar
*/

var selectMode = false,
	searchMode = false;

// Select
function actionSelect() {
	if (selectMode)
		stopSelectMode();
	else
		startSelectMode();
}

function startSelectMode() {
	selectMode = true;
	let selActions = document.querySelectorAll('.actionbar__element--selectable');

	for (let selAction of selActions)
		selAction.classList.remove('actionbar__element--disabled');
}

function stopSelectMode() {
	selectMode = false;
	let selActions = document.querySelectorAll('.actionbar__element--selectable');

	for (let selAction of selActions)
		selAction.classList.add('actionbar__element--disabled');
}

function activeSelection(event, elementId, link) {
	event.stopPropagation();
	if (selectMode)
		selectElement(elementId);
	else
		showElement(elementId, link);
}

function selectElement(elementId) {}

function showElement(elementId, link) {
	window.location.href = link;
}

// Upload
function actionUpload(formId) {
	document.getElementById(formId).click();
}

// Download
function actionDownload() {}

// Add
function actionAdd() {}

// Delete
function actionDelete() {}

// Share
function actionShare() {
	if (selectMode) {
		alertExperimental();
	}
}

// Hide
function actionHide() {
	if (selectMode) {
		alertExperimental();
	}
}

// Search
function actionSearch() {
	if (searchMode) {
		stopSearchBar();
	} else {
		startSearchBar();
	}
}

function startSearchBar() {
	searchMode = true;
	document.querySelector('input.search-bar').classList.remove('disabled');
}

function stopSearchBar() {
	searchMode = false;
	document.querySelector('input.search-bar').classList.add('disabled');
}

// send action to the server
function sendAction(actionName, content) {
	let inputType = document.getElementById('actiontype-input');
	let inputContent = document.getElementById('actioncontent-input');
	let form = document.getElementById('action-form');
	
	if (inputType)
		inputType.value = actionName;
	if (inputContent)
		inputContent.value = content;
	if (form)
		form.submit();

	stopSelectMode();
}

(function() {
	document.addEventListener('click', e => {
		let searchBar = document.querySelector('input.search-bar');

		if (searchBar) {
			if (!searchBar.contains(e.target) && searchMode) {
				stopSearchBar();
			}
		}
	}, true);
})();