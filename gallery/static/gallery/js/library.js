/* Dependencies:
	- mixins/actionbar.js
	- mixins/contentnav.js
	- mixins/inputdialog.js
*/

var	oldActionShowItem = window.actionShowItem,
	oldActionAdd = window.actionAdd;
var oldContentnavNext = window.contentnavNext,
	oldContentnavPrevious = window.contentnavPrevious;
var currentAlbum = 0,
	nbAlbums;

///////////////////////////////////////////////////////////////////////////////////////////////////
/// Actionbar features ////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

window.actionShowItem = function(albumId, link) {
	var albums = document.querySelectorAll('.library .album');

	for (let i = 0; i < nbAlbums; i++) {
		if (albums[i].id == 'album-' + albumId) {
			if (i < currentAlbum)
				contentnavPrevious();
			else if (i == currentAlbum)
				oldActionShowItem(albumId, link);
			else
				contentnavNext();
		}
	}
};

// Add
window.actionAdd = function() {
	dialogSetTitle('Créer un nouvel album');
	dialogSetInput('text', 'album-name', '', 'Nom de l\'album', 'on');
	dialogAddAcceptFunction(function(value){actionSend('add', value);});
	dialogShow();
	oldActionAdd();
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

window.contentnavPrevious = function() {
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

function showError(msg) {
	dialogSetTitle('Petite problème');
	dialogSetMessage(msg);
	dialogShow();
}

(function() {
	nbAlbums = document.querySelectorAll('.library .album').length;

	if (currentAlbum == 0)
		document.querySelector('.contentnav__element--previous').classList.add('contentnav__element--disabled');
	if (currentAlbum == nbAlbums - 1)
		document.querySelector('.contentnav__element--next').classList.add('contentnav__element--disabled');
	
	actionSetSelectableClass('album');
	actionSetIdBaseName('album');
})();