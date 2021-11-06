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
	var albums = document.querySelectorAll('.cover');

	for (let i = 0; i < nbAlbums; i++) {
		if (albums[i].id == 'cover-' + albumId) {
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
	var dialog = new Dialog('libraryDialog');
	dialog.setTitle('Créer un nouvel album');
	dialog.setInput('text', 'album-name', '', 'Nom de l\'album', 'on');
	dialog.addAcceptFunction(function(value){actionSend('add', value);});
	dialog.setBlurSelector('body > *:not(#libraryDialog)');
	dialog.show();
	oldActionAdd();
};


///////////////////////////////////////////////////////////////////////////////////////////////////
/// Contentnav features ///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

window.contentnavNext = function() {
	if (currentAlbum < nbAlbums-1) {
		var albums = document.querySelectorAll('.cover');

		if (currentAlbum == 0)
			document.querySelector('.contentnav__element--previous').classList.remove('contentnav__element--disabled');

		if (currentAlbum > 0)
			albums[currentAlbum-1].classList.remove('cover--previous');
		albums[currentAlbum].classList.remove('cover--current');
		albums[currentAlbum+1].classList.remove('cover--next');

		currentAlbum++;

		albums[currentAlbum-1].classList.add('cover--previous');
		albums[currentAlbum].classList.add('cover--current');
		if (currentAlbum < nbAlbums - 1)
			albums[currentAlbum+1].classList.add('cover--next');

		if (currentAlbum == nbAlbums - 1)
			document.querySelector('.contentnav__element--next').classList.add('contentnav__element--disabled');
	}
};

window.contentnavPrevious = function() {
	if (currentAlbum > 0) {
		var albums = document.querySelectorAll('.cover');

		if (currentAlbum == nbAlbums - 1)
			document.querySelector('.contentnav__element--next').classList.remove('contentnav__element--disabled');

		albums[currentAlbum-1].classList.remove('cover--previous');
		albums[currentAlbum].classList.remove('cover--current');
		if (currentAlbum < nbAlbums - 1)
			albums[currentAlbum+1].classList.remove('cover--next');

		currentAlbum--;

		if (currentAlbum > 0)
			albums[currentAlbum-1].classList.add('cover--previous');
		albums[currentAlbum].classList.add('cover--current');
		albums[currentAlbum+1].classList.add('cover--next');

		if (currentAlbum == 0)
			document.querySelector('.contentnav__element--previous').classList.add('contentnav__element--disabled');
	}
};

///////////////////////////////////////////////////////////////////////////////////////////////////
/// LibraryView features //////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

(function() {
	nbAlbums = document.querySelectorAll('.cover').length;

	if (currentAlbum == 0)
		document.querySelector('.contentnav__element--previous').classList.add('contentnav__element--disabled');
	if (currentAlbum == nbAlbums - 1)
		document.querySelector('.contentnav__element--next').classList.add('contentnav__element--disabled');
	
	actionSetSelectableClass('cover');
	actionSetIdBaseName('cover');
})();