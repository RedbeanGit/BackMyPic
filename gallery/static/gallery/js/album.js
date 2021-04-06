var currentSheet = 0, nbSheets = 0,
	oldStartSelectMode = window.startSelectMode,
	oldStopSelectMode = window.stopSelectMode,
	oldHideSelection = window.hideSelection,
	oldAddElement = window.addElement,
	oldDeleteSelection = window.deleteSelection,
	oldSelectElement = window.selectElement,
	oldShowElement = window.showElement,
	oldSendAction = window.sendAction,
	selectedPictures = new Set();

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
	}
}

function getNbSheets() {
	return document.querySelectorAll('.album__sheet').length;
}

/* actionnav functions */
window.startSelectMode = function() {
	oldStartSelectMode();
	let pictures = document.querySelectorAll('.album__picture');

	for (let picture of pictures)
		picture.classList.add('album__picture--selectable');
};

window.stopSelectMode = function() {
	let pictures = document.querySelectorAll('.album__picture');

	for (let pictureId of selectedPictures)
		selectElement(document.createEvent('Events'), pictureId);
	for (let picture of pictures)
		picture.classList.remove('album__picture--selectable');
	oldStopSelectMode();
};

window.hideSelection = function() {
	if (selectMode) {
		for (let pictureId of selectedPictures) {
			picture = document.getElementById('picture-' + pictureId);
			picture.remove();
		}
	}
	oldHideSelection();
};

window.addElement = function() {};

window.deleteSelection = function() {
	if (selectMode) {
		for (let pictureId of selectedPictures) {
			picture = document.getElementById('picture-' + pictureId);
			picture.remove();
		}
	}
	oldDeleteSelection();
};

window.selectElement = function(event, pictureId) {
	oldSelectElement(event, pictureId);

	if (selectMode) {
		event.stopPropagation();
		let picture = document.getElementById('picture-' + pictureId);

		if (selectedPictures.has(pictureId)) {
			selectedPictures.delete(pictureId);
			picture.classList.remove('album__picture--selected');
		} else {
			selectedPictures.add(pictureId);
			picture.classList.add('album__picture--selected');
		}
	}
};

window.showElement = function(pictureId, link) {
	oldShowElement(pictureId, link);
};

window.sendAction = function(actionName) {
	let inputContent = document.getElementById('actioncontent-input');
	
	if (inputContent) {
		inputContent.value = Array.from(selectedPictures).join();
	}
	oldSendAction(actionName);
};

(function() {
	nbSheets = getNbSheets();
})();