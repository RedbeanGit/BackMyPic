var selectMode = false,
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
	let selActions = document.querySelectorAll('.sel-action');
	let pictures = document.querySelectorAll('.picture-box');

	for (let selAction of selActions)
		selAction.classList.remove('disabled');
	for (let picture of pictures)
		picture.classList.add('selectable');
}

function stopSelectMode() {
	selectMode = false;
	let selActions = document.querySelectorAll('.sel-action');
	let pictures = document.querySelectorAll('.picture-box');

	for (let selAction of selActions)
		selAction.classList.add('disabled');
	for (let pictureId of selectedPictures)
		selectPicture(pictureId);
	for (let picture of pictures)
		picture.classList.remove('selectable');
	hideMode = false;
}

// Hide
function hidePictures() {
	if (selectMode) {
		for (let pictureId of selectedPictures) {
			picture = document.getElementById('picture-' + pictureId);
			picture.remove();
		}
		sendAction('hide');
	}
}

// Delete
function deletePictures() {
	if (selectMode) {
		for (let pictureId of selectedPictures) {
			picture = document.getElementById('picture-' + pictureId);
			picture.remove();
		}
		sendAction('delete');
	}
}

// Share
function sharePictures() {
	if (selectMode) {
		sendAction('share');
		alert('Cette fonctionnalité n\'est pas encore disponible !')
	}
}

// Download
function downloadPictures() {
	if (selectMode) {
		sendAction('download');
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

function showPicture(pictureId) {
	let picture = document.getElementById('picture-' + pictureId);
}

// send action to the server
function sendAction(actionName) {
	let inputType = document.getElementById('actiontype-input');
	let inputContent = document.getElementById('actioncontent-input');

	if (inputType && inputContent) {
		inputType.value = actionName;
		inputContent.value = Array.from(selectedPictures).join();
		let form = document.getElementById('action-form');

		if (form)
			form.submit();
	}
	stopSelectMode();
}

(function() {
	pictureList = document.getElementById('picturelist');

	if (pictureList)
		pictureList.addEventListener('wheel', horizontalScroll);
})();