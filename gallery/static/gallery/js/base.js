var searchMode = false,
	asked = [];

function activeSearch() {
	if (searchMode) {

	} else {
		enableSearchBar();
	}
}

function enableSearchBar() {
	searchMode = true;
	document.querySelector('input.search-bar').classList.remove('disabled');
}

function disableSearchBar() {
	searchMode = false;
	document.querySelector('input.search-bar').classList.add('disabled');
}

function alertExperimental() {
	alert('Cette fonctionnalité n\'est pas encore disponible !');
}

function showUserInput(msg, fct) {
	sheet = document.getElementById('input-sheet');

	if (sheet) {
		sheet.querySelector('label').textContent = msg + ' :';
		sheet.querySelector('input[type=submit]').onclick =	function(){
			fct(document.getElementById('input-sheet__input').value);
		};
		sheet.classList.add('input-sheet--visible');
	}
}

function hideUserInput() {
	sheet = document.getElementById('input-sheet');

	if (sheet) {
		sheet.querySelector('label').textContent = '';
		sheet.querySelector('input[type=submit]').onclick =	function(){	};
		sheet.classList.remove('input-sheet--visible');
	}
}


(function() {
	document.addEventListener('click', e => {
		let searchBar = document.querySelector('input.search-bar');

		if (searchBar) {
			if (!searchBar.contains(e.target) && searchMode) {
				disableSearchBar();
			}
		}
	}, true);
})();