/* Dependencies:
	- mixins/actionbar.js
	- mixins/contentnav.js
	- mixins/inputdialog.js
*/

var oldStartSelectMode = window.startSelectMode,
	oldStopSelectMode = window.stopSelectMode,
	oldSelectElement = window.selectElement,
	oldShowElement = window.showElement,
	oldActionDownload = window.actionDownload,
	oldActionAdd = window.actionAdd,
	oldActionDelete = window.actionDelete,
	oldActionShare = window.actionShare;
var oldContentnavNext = window.contentnavNext,
	oldContentnavPrevious = window.contentnavPrevious;
var selectedAlbums = new Set();
var currentAlbum = 0,
	nbAlbums;

///////////////////////////////////////////////////////////////////////////////////////////////////
/// Actionbar features ////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

// Select
window.startSelectMode = function() {
	let albums = document.querySelectorAll('.album');

	for (let album of albums)
		album.classList.add('album--selectable');
	oldStartSelectMode();
};

window.stopSelectMode = function() {
	let albums = document.querySelectorAll('.album');

	for (let albumId of selectedAlbums)
		selectElement(albumId);
	for (let album of albums)
		album.classList.remove('album--selectable');
	oldStopSelectMode();
};

window.selectElement = function(albumId) {
	if (selectMode) {
		let album = document.getElementById('album-' + albumId);

		if (selectedAlbums.has(albumId)) {
			selectedAlbums.delete(albumId);
			album.classList.remove('album--selected');
		} else {
			selectedAlbums.add(albumId);
			album.classList.add('album--selected');
		}
	}
	oldSelectElement(albumId);
};

window.showElement = function(albumId, link) {
	var albums = document.querySelectorAll('.library .album');

	for (let i = 0; i < nbAlbums; i++) {
		if (albums[i].id == 'album-' + albumId) {
			if (i < currentAlbum)
				contentnavPrevious();
			else if (i == currentAlbum)
				oldShowElement(albumId, link);
			else
				contentnavNext();
		}
	}
};

// Download
window.actionDownload = function() {
	if (selectMode)
		sendAction('download', Array.from(selectedAlbums).join());
	oldActionDownload();
};

// Add
window.actionAdd = function() {
	inputDialogRun(
		'Créer un nouvel album',
		'Nom de l\'album', 
		function(value){
			sendAction('add', value);
		},
		function(){}
	);
	oldActionAdd();
};

// Delete
window.actionDelete = function() {
	if (selectMode) {
		for (let albumId of selectedAlbums) {
			album = document.getElementById('album-' + albumId);
			album.remove();
		}
		sendAction('delete', Array.from(selectedAlbums).join());
	}
	oldActionDelete();
};

// Share
window.actionShare = function() {
	if (selectMode)
		sendAction('share', Array.from(selectedAlbums).join());
	oldActionShare();
};

///////////////////////////////////////////////////////////////////////////////////////////////////
/// Contentnav features ///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

window.contentnavNext = function() {
	if (currentAlbum < nbAlbums-1) {
		var albums = document.querySelectorAll('.library .album');

		if (currentAlbum == 0)
			document.querySelector('.contentnav__element--previous').classList.remove('contentnav__element--disabled');

		if (currentAlbum > 0)
			albums[currentAlbum-1].classList.remove('album--previous');
		albums[currentAlbum].classList.remove('album--current');
		albums[currentAlbum+1].classList.remove('album--next');

		currentAlbum++;

		albums[currentAlbum-1].classList.add('album--previous');
		albums[currentAlbum].classList.add('album--current');
		if (currentAlbum < nbAlbums - 1)
			albums[currentAlbum+1].classList.add('album--next');

		if (currentAlbum == nbAlbums - 1)
			document.querySelector('.contentnav__element--next').classList.add('contentnav__element--disabled');
	}
};

window.contentnavNext = function previousAlbum() {
	if (currentAlbum > 0) {
		var albums = document.querySelectorAll('.library .album');

		if (currentAlbum == nbAlbums - 1)
			document.querySelector('.contentnav__element--next').classList.remove('contentnav__element--disabled');

		albums[currentAlbum-1].classList.remove('album--previous');
		albums[currentAlbum].classList.remove('album--current');
		if (currentAlbum < nbAlbums - 1)
			albums[currentAlbum+1].classList.remove('album--next');

		currentAlbum--;

		if (currentAlbum > 0)
			albums[currentAlbum-1].classList.add('album--previous');
		albums[currentAlbum].classList.add('album--current');
		albums[currentAlbum+1].classList.add('album--next');

		if (currentAlbum == 0)
			document.querySelector('.contentnav__element--previous').classList.add('contentnav__element--disabled');
	}
};

///////////////////////////////////////////////////////////////////////////////////////////////////
/// LibraryView features //////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

(function() {
	nbAlbums = document.querySelectorAll('.library .album').length;

	if (currentAlbum == 0)
		document.querySelector('.contentnav__element--previous').classList.add('contentnav__element--disabled');
	if (currentAlbum == nbAlbums - 1)
		document.querySelector('.contentnav__element--next').classList.add('contentnav__element--disabled');
})();