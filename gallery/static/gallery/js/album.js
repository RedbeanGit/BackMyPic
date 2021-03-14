var currentSheet = 0, nbSheets = 0;

function next() {
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

function previous() {
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

(function() {
	nbSheets = getNbSheets();
})();