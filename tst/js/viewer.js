function frst(id) {
	index = 0;
	document.getElementById(id).src = imgs[index];
}

function back(id) {
	if (index > 0) { index -= 1; }
	else { index = imgs.length-1; }
	document.getElementById(id).src = imgs[index];
}

function play(id) {
	var interval = 500; // in milliseconds
	playing = setInterval(fore, interval, id);
}

function paus() {
	clearInterval(playing)
}

function fore(id) {
	if (index < imgs.length-1) { index += 1; }
	else { index = 0; }
	document.getElementById(id).src = imgs[index];
}

function last(id) {
	index = imgs.length-1;
	document.getElementById(id).src = imgs[index];
}

function test() {
	alert( 'this is a test' );
}