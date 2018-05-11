/*
	JQuery for glossary.html
*/

// function test() { alert('this is a test'); }


function expand(id) {

	// show panel
	$(id).removeClass('hide').addClass('show');

	// expand and center panel
	$(id).animate({
		height: "300px",
		width: "1000px"}, 200);
}

function collapse(id) {
	
	// reset size
	$(id).css({
		height: "0px",
		width: "0px"});
	
	// hide panel
	$(id).removeClass("show").addClass("hide");
}

