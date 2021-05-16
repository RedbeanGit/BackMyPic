/* Dependencies:
	- mixins/actionbar.js
	- mixins/inputdialog.js
*/

var oldStartSelectMode = window.startSelectMode,
	oldStopSelectMode = window.stopSelectMode,
	oldDownloadSelection = window.downloadSelection,
	oldAddElement = window.addElement,
	oldDeleteSelection = window.deleteSelection,
	oldShareSelection = window.shareSelection,
	oldSelectElement = window.selectElement,
	oldShowElement = window.showElement;
var selectedAlbums = new Set();
var currentAlbum = 0,
	nbAlbums;

///////////////////////////////////////////////////////////////////////////////////////////////////
/// Actionbar features ////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

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

window.downloadSelection = function() {
	if (selectMode)
		sendAction('download', Array.from(selectedAlbums).join());
	oldDownloadSelection();
};

window.addElement = function() {
	showInputDialog('Nom de l\'album', function(value){
		let inputContent = document.getElementById('actioncontent-input');
	
		if (inputContent) {
			inputContent.value = value;
		};
		sendAction('add', Array.from(selectedAlbums).join());
	});
	oldAddElement();
};

window.deleteSelection = function() {
	if (selectMode) {
		for (let albumId of selectedAlbums) {
			album = document.getElementById('album-' + albumId);
			album.remove();
		}
		sendAction('delete', Array.from(selectedAlbums).join());
	}
	oldDeleteSelection();
};

window.shareSelection = function() {
	if (selectMode)
		sendAction('share', Array.from(selectedAlbums).join());
	oldShareSelection();
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
				previousAlbum();
			else if (i == currentAlbum)
				oldShowElement(albumId, link);
			else
				nextAlbum();
		}
	}
};

///////////////////////////////////////////////////////////////////////////////////////////////////
/// LibraryView features //////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

function nextAlbum() {
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
}

function previousAlbum() {
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
}

(function() {
	nbAlbums = document.querySelectorAll('.library .album').length;
})();