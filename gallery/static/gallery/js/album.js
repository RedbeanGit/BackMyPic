/* Dependencies:
	- mixins/actionbar.js
	- mixins/contentnav.js
*/

var oldActionHide = window.actionHide;
var oldContentnavNext = window.contentnavNext,
	oldContentnavPrevious = window.contentnavPrevious;
var currentSheet = -1,
	nbSheets = 0;

///////////////////////////////////////////////////////////////////////////////////////////////////
/// Actionbar features ////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

// Hide
window.actionHide = function() {
	if (selectMode) {
		for (let pictureId of selectedIds) {
			picture = document.getElementById(idBaseName + '-' + pictureId);
			picture.remove();
		}
		actionSend('hide', Array.from(selectedIds).join());
	}
	oldActionHide();
};

///////////////////////////////////////////////////////////////////////////////////////////////////
/// Contentnav features ///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

window.contentnavNext = function() {
	if (currentSheet < nbSheets - 1) {
		currentSheet++;
		var pages = document.querySelectorAll('.album__page');
		pages[(nbSheets - currentSheet - 1) * 2].classList.add('album__page--rotated');
		pages[currentSheet * 2 + 1].classList.add('album__page--rotated');

		if (currentSheet == 0)
			document.querySelector('.contentnav__element--previous').classList.remove('contentnav__element--disabled');
		if (currentSheet == nbSheets - 1)
			document.querySelector('.contentnav__element--next').classList.add('contentnav__element--disabled');
	}
};

window.contentnavPrevious = function() {
	if (currentSheet > -1) {
		var pages = document.querySelectorAll('.album__page');
		pages[(nbSheets - currentSheet - 1) * 2].classList.remove('album__page--rotated');
		pages[currentSheet * 2 + 1].classList.remove('album__page--rotated');
		currentSheet--;

		if (currentSheet == nbSheets - 2)
			document.querySelector('.contentnav__element--next').classList.remove('contentnav__element--disabled');
		if (currentSheet == -1)
			document.querySelector('.contentnav__element--previous').classList.add('contentnav__element--disabled');
	}
};

///////////////////////////////////////////////////////////////////////////////////////////////////
/// AlbumView features ////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

function getNbSheets() {
	return document.querySelectorAll('.album__page').length / 2;
}


(function() {
	nbSheets = getNbSheets();
	actionSetSelectableClass('album__picture');
	actionSetIdBaseName('picture');
})();