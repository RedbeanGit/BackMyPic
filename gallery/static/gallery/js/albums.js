var oldStartSelectMode = window.startSelectMode,
	oldStopSelectMode = window.stopSelectMode,
	oldHideSelection = window.hideSelection,
	oldAddElement = window.addElement,
	oldDeleteSelection = window.deleteSelection,
	oldSelectElement = window.selectElement,
	oldShowElement = window.showElement,
	oldSendAction = window.sendAction,
	selectedAlbums = new Set();

/* actionnav functions */
window.startSelectMode = function() {
	oldStartSelectMode();
	let albums = document.querySelectorAll('.album');

	for (let album of albums)
		album.classList.add('album--selectable');
};

window.stopSelectMode = function() {
	oldStopSelectMode();
	let albums = document.querySelectorAll('.album');

	for (let albumId of selectedAlbums)
		selectAlbum(albumId);
	for (let album of albums)
		album.classList.remove('album--selectable');
};

window.hideSelection = function() {};

window.addElement = function() {
	alertExperimental();
};

window.deleteSelection = function() {
	if (selectMode) {
		for (let albumId of selectedAlbums) {
			album = document.getElementById('album-' + albumId);
			album.remove();
		}
	}
	oldDeleteSelection();
};

window.selectElement = function(event, albumId) {
	oldSelectElement(event, albumId);

	if (selectMode) {
		event.stopPropagation();
		let album = document.getElementById('album-' + albumId);

		if (selectedAlbums.has(albumId)) {
			selectedAlbums.delete(albumId);
			album.classList.remove('album--selected');
		} else {
			selectedAlbums.add(albumId);
			album.classList.add('album--selected');
		}
	}
};

window.showElement = function(albumId) {
	oldShowElement(albumId);
	let album = document.getElementById('album-' + albumId);
};

window.sendAction = function(actionName) {
	let inputContent = document.getElementById('actioncontent-input');
	
	if (inputContent) {
		inputContent.value = Array.from(selectedAlbums).join();
	}
	oldSendAction(actionName);
};