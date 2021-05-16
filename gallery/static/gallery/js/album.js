/* Dependencies:
	- mixins/actionbar.js
*/

var oldStartSelectMode = window.startSelectMode,
	oldStopSelectMode = window.stopSelectMode,
	oldDownloadSelection = window.downloadSelection,
	oldDeleteSelection = window.deleteSelection,
	oldShareSelection = window.shareSelection,
	oldHideSelection = window.hideSelection,
	oldSelectElement = window.selectElement,
	oldSendAction = window.sendAction,
	selectedPictures = new Set();
var currentSheet = 0,
	nbSheets = 0;

///////////////////////////////////////////////////////////////////////////////////////////////////
/// Actionbar features ////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

window.startSelectMode = function() {
	let pictures = document.querySelectorAll('.album__picture');

	for (let picture of pictures)
		picture.classList.add('album__picture--selectable');
	oldStartSelectMode();
};

window.stopSelectMode = function() {
	let pictures = document.querySelectorAll('.album__picture');

	for (let pictureId of selectedPictures)
		selectElement(pictureId);
	for (let picture of pictures)
		picture.classList.remove('album__picture--selectable');
	oldStopSelectMode();
};

window.downloadSelection = function() {
	if (selectMode)
		sendAction('download', Array.from(selectedPictures).join());
	oldDownloadSelection();
};

window.deleteSelection = function() {
	if (selectMode) {
		for (let pictureId of selectedPictures) {
			picture = document.getElementById('picture-' + pictureId);
			picture.remove();
		}
		sendAction('delete', Array.from(selectedPictures).join());
	}
	oldDeleteSelection();
};

window.shareSelection = function() {
	if (selectMode)
		sendAction('share', Array.from(selectedPictures).join());
	oldShareSelection();
};

window.hideSelection = function() {
	if (selectMode) {
		for (let pictureId of selectedPictures) {
			picture = document.getElementById('picture-' + pictureId);
			picture.remove();
		}
		sendAction('hide', Array.from(selectedPictures).join());
	}
	oldHideSelection();
};

window.selectElement = function(pictureId) {
	if (selectMode) {
		let picture = document.getElementById('picture-' + pictureId);

		if (selectedPictures.has(pictureId)) {
			selectedPictures.delete(pictureId);
			picture.classList.remove('album__picture--selected');
		} else {
			selectedPictures.add(pictureId);
			picture.classList.add('album__picture--selected');
		}
	}
	oldSelectElement(pictureId);
};

///////////////////////////////////////////////////////////////////////////////////////////////////
/// AlbumView features ////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

function nextSheet() {
	if (currentSheet < nbSheets) {
		currentSheet++;
		var visibles = document.querySelectorAll('.album__sheet--visible');

		for (let sheet of visibles) {
			if (!sheet.classList.contains('album__sheet--rotated')) {
				if (sheet.previousElementSibling)
					sheet.previousElementSibling.classList.remove('album__sheet--visible');
				
				sheet.classList.add('album__sheet--rotated');

				if (sheet.nextElementSibling)
					sheet.nextElementSibling.classList.add('album__sheet--visible');
			}
		}

		if (currentSheet == 1)
			document.querySelector('.contentnav__element--previous').classList.remove('contentnav__element--disabled');

		if (currentSheet == nbSheets)
			document.querySelector('.contentnav__element--next').classList.add('contentnav__element--disabled');
	}
}

function previousSheet() {
	if (currentSheet > 0) {
		currentSheet--;
		var visibles = document.querySelectorAll('.album__sheet--visible');

		for (let i = visibles.length - 1; i >= 0; i--) {
			var sheet = visibles[i];
			if (sheet.classList.contains('album__sheet--rotated')) {
				if (sheet.nextElementSibling)
					sheet.nextElementSibling.classList.remove('album__sheet--visible');
				
				sheet.classList.remove('album__sheet--rotated');

				if (sheet.previousElementSibling)
					sheet.previousElementSibling.classList.add('album__sheet--visible');
			}
		}

		if (currentSheet == nbSheets - 1)
			document.querySelector('.contentnav__element--next').classList.remove('contentnav__element--disabled');

		if (currentSheet == 0)
			document.querySelector('.contentnav__element--previous').classList.add('contentnav__element--disabled');
	}
}

function getNbSheets() {
	return document.querySelectorAll('.album__sheet').length;
}


(function() {
	nbSheets = getNbSheets();
})();