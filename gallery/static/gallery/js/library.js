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
	let albums = document.querySelectorAll('.album');

	for (let albumId of selectedAlbums)
		selectElement(document.createEvent('Events'), albumId);
	for (let album of albums)
		album.classList.remove('album--selectable');
	oldStopSelectMode();
};

window.hideSelection = function() {};

window.addElement = function() {
	showUserInput('Nom de l\'album', function(value){
		let inputContent = document.getElementById('actioncontent-input');
	
		if (inputContent) {
			inputContent.value = value;
		};
		oldSendAction('add');
	});
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

window.showElement = function(albumId, link) {
	oldShowElement(albumId, link);
};

window.sendAction = function(actionName) {
	let inputContent = document.getElementById('actioncontent-input');
	
	if (inputContent) {
		inputContent.value = Array.from(selectedAlbums).join();
	}
	oldSendAction(actionName);
};