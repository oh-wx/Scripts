/*
	JavaScript for glossary.html
*/

// function test() { alert('this is a test'); }


function expand(id) {

	// show panel
	$(id).removeClass('hide');
	$(id).addClass('show');

	// expand and center panel
	$(id).animate({
		height: "300px",
		width: "1000px"}, 200);
}

function collapse(id) {
	
	// reset to origin
	$(id).css({
		height: "0px",
		width: "0px"});
	
	// hide panel
	$(id).removeClass("show");
	$(id).addClass("hide");
}

