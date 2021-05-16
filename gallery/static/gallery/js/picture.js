/* Dependencies:
	- mixins/actionbar.js
*/

var oldDownloadSelection = window.downloadSelection,
	oldDeleteSelection = window.deleteSelection,
	oldShareSelection = window.shareSelection,
	oldHideSelection = window.hideSelection;

///////////////////////////////////////////////////////////////////////////////////////////////////
/// Actionbar features ////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

window.downloadSelection = function() {
	sendAction('download', null);
	oldDownloadSelection();
};

window.deleteSelection = function() {
	sendAction('delete', null);
	oldDeleteSelection();
};

window.shareSelection = function() {
	sendAction('share', null);
	oldShareSelection();
};

window.hideSelection = function() {
	sendAction('hide', null);
	oldHideSelection();
};