var selectMode = false, hideMode = false,
	selectedPictures = new Set(),
	picturelist, inputUpload;

// Selection Mode
function switchSelectMode() {
	if (selectMode)
		stopSelectMode();
	else
		startSelectMode();
}

function startSelectMode() {
	selectMode = true;
	enableSelActions();

	pictures = document.querySelectorAll('.picture-box');

	for (let picture of pictures) {
		picture.classList.add('selectable');
	}
}

function stopSelectMode() {
	selectMode = false;
	disableSelActions();

	pictures = document.querySelectorAll('.picture-box');

	for (let picture of pictures) {
		picture.classList.remove('selectable');
	}

	unselectPictures();
	hideMode = false;
}

function enableSelActions() {
	var selActions = document.querySelectorAll('.sel-action');

	for (let selAction of selActions)
		selAction.classList.remove('disabled');
}

function disableSelActions() {
	var selActions = document.querySelectorAll('.sel-action');

	for (let selAction of selActions)
		selAction.classList.add('disabled');
}

// Hide mode
function switchHideMode() {
	if (selectMode) {
		if (hideMode)
			stopHideMode();
		else
			startHideMode();
	}
}

function startHideMode() {
	hideMode = true;

	for (let pictureId of selectedPictures) {
		picture = document.getElementById('picture-' + pictureId);
		picture.classList.add('hidden');
	}
	alert('Cette fonctionnalité n\'est pas encore disponible!');
}

function stopHideMode() {
	hideMode = false;

	for (let pictureId of selectedPictures) {
		picture = document.getElementById('picture-' + pictureId);
		picture.classList.remove('hidden');
	}
}

// Delete
function deletePictures() {
	if (selectMode) {
		for (let pictureId of selectedPictures) {
			picture = document.getElementById('picture-' + pictureId);
			picture.remove();
		}

		let input = document.getElementById('delete-input');

		if (input) {
			input.value = Array.from(selectedPictures).join();
			let form = document.getElementById('delete-form');

			if (form)
				form.submit();
		}
		stopSelectMode();
	}
}

// Share
function sharePictures() {
	if (selectMode) {
		alert('Cette fonctionnalité n\'est pas encore disponible!');
	}
}

// Uploading and downloading
function downloadPictures() {
	if (selectMode) {
		alert('Cette fonctionnalité n\'est pas encore disponible!');
	}
}

// Scroll
function horizontalScroll(e) {
	e.preventDefault();
	pictureList.scrollBy(e.deltaY * 0.8, 0); 
}

// when a picture is clicked
function activePicture(pictureId) {
	if (selectMode)
		selectPicture(pictureId);
	else
		showPicture(pictureId);
}

function selectPicture(pictureId) {
	let picture = document.getElementById('picture-' + pictureId);

	if (selectedPictures.has(pictureId)) {
		selectedPictures.delete(pictureId);
		picture.classList.remove('selected');
	} else {
		selectedPictures.add(pictureId);
		picture.classList.add('selected');
	}
}

function unselectPictures() {
	for (let pictureId of selectedPictures) {
		selectPicture(pictureId);
	}
}

function showPicture(pictureId) {
	let picture = document.getElementById('picture-' + pictureId);
}

(function() {
	pictureList = document.getElementById('picturelist');
	inputUpload = document.getElementById('input-upload');

	if (pictureList)
		pictureList.addEventListener('wheel', horizontalScroll);
	if (inputUpload)
		inputUpload.addEventListener('change', e => {uploadPictures();});
})();