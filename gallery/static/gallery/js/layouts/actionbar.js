var selectMode = false,
	searchMode = false,
	selectableClass = 'itemClass',
	idBaseName = 'item',
	selectedIds = new Set();

// Select
function actionSelect() {
	if (selectMode)
		actionStopSelectMode();
	else
		actionStartSelectMode();
}

function actionStartSelectMode() {
	selectMode = true;
	var selActions = document.querySelectorAll('.actionbar__element--selectable');
	var items = document.querySelectorAll('.' + selectableClass);

	for (let selAction of selActions)
		selAction.classList.remove('actionbar__element--disabled');
	for (let item of items)
		item.classList.add(selectableClass + '--selectable');

	addKeyboardShortcut(['Delete'], actionDelete);
	addKeyboardShortcut(['Shift', 'A'], actionSelectAllItems);
	addKeyboardShortcut(['Shift', 'S'], actionDownload);
	addKeyboardShortcut(['Shift', 'N'], actionAdd);
	addKeyboardShortcut(['Shift', 'H'], actionHide);
}

function actionStopSelectMode() {
	var selActions = document.querySelectorAll('.actionbar__element--selectable');
	var items = document.querySelectorAll('.' + selectableClass);

	for (let selAction of selActions)
		selAction.classList.add('actionbar__element--disabled');
	for (let itemId of selectedIds)
		actionSelectItem(itemId);
	for (let item of items)
		item.classList.remove(selectableClass + '--selectable');
	selectMode = false;

	removeKeyboardShortcut(['Delete'], actionDelete);
	removeKeyboardShortcut(['Shift', 'A'], actionSelectAllItems);
	removeKeyboardShortcut(['Shift', 'S'], actionDownload);
	removeKeyboardShortcut(['Shift', 'N'], actionAdd);
	removeKeyboardShortcut(['Shift', 'H'], actionHide);
}

function actionActiveSelection(event, itemId, link) {
	event.stopPropagation();
	if (selectMode)
		actionSelectItem(itemId);
	else
		actionShowItem(itemId, link);
}

function actionSelectItem(itemId) {
	if (selectMode) {
		var item = document.getElementById(idBaseName + '-' + itemId);

		if (selectedIds.has(itemId)) {
			selectedIds.delete(itemId);
			item.classList.remove(selectableClass + '--selected');
		} else {
			selectedIds.add(itemId);
			item.classList.add(selectableClass + '--selected');
		}
	}
}

function actionSelectAllItems() {
	var items = document.querySelectorAll('.' + selectableClass);

	for (let item of items) {
		var itemId = parseInt(item.id.split('-')[1]);

		if (!selectedIds.has(itemId)) {
			selectedIds.add(itemId);
			item.classList.add(selectableClass + '--selected');
		}
	}
}

function actionShowItem(itemId, link) {
	window.location.href = link;
}

// Upload
function actionUpload(formId) {
	document.getElementById(formId).click();
}

// Download
function actionDownload() {
	if (selectMode)
		actionSend('download', Array.from(selectedIds).join());
}

// Add
function actionAdd() {}

// Delete
function actionDelete() {
	if (selectMode) {
		for (let itemId of selectedIds) {
			item = document.getElementById(idBaseName + '-' + itemId);
			item.remove();
		}
		actionSend('delete', Array.from(selectedIds).join());
	}
}

// Share
function actionShare() {
	if (selectMode) {
		alertExperimental();
		//actionSendAction('share', Array.from(selectedIds).join());
	}
}

// Hide
function actionHide() {}

// Search
function actionSearch() {
	if (searchMode)
		actionStopSearchBar();
	else
		actionStartSearchBar();
}

function actionStartSearchBar() {
	searchMode = true;
	document.querySelector('input.search-bar').classList.remove('disabled');
}

function actionStopSearchBar() {
	searchMode = false;
	document.querySelector('input.search-bar').classList.add('disabled');
}

// send action to the server
function actionSend(actionName, content) {
	resetKeyPressed();
	
	let inputType = document.getElementById('actiontype-input');
	let inputContent = document.getElementById('actioncontent-input');
	let form = document.getElementById('action-form');
	
	if (inputType)
		inputType.value = actionName;
	if (inputContent)
		inputContent.value = content;
	if (form)
		form.submit();
}

// API
function actionSetSelectableClass(clsName) {
	selectableClass = clsName;
}

function actionSetIdBaseName(name) {
	idBaseName = name;
}

(function() {
	document.addEventListener('click', e => {
		let searchBar = document.querySelector('input.search-bar');

		if (searchBar) {
			if (!searchBar.contains(e.target) && searchMode) {
				actionStopSearchBar();
			}
		}
	}, true);
})();