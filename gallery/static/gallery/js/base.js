var searchMode = false;

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