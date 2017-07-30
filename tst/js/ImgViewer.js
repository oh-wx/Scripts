/*
	JavaScript
*/

class ImgViewer {

	constructor(imgs, id) {
		this.imgs = imgs;
		this.id = id;
		this.index = 0;
		this.playing;
	}
	
	frst() {
		this.index = 0;
		document.getElementById(this.id).src = this.imgs[this.index];
	}

	back() {
		if (this.index > 1) { this.index -= 1; }
		else { this.index = this.imgs.length-1; }
		document.getElementById(this.id).src = this.imgs[this.index];
	}

	play() {
		var interval = 500; // in milliseconds
		this.playing = setInterval(this.fore.bind(this), interval);
	}

	paus() {
		clearInterval(this.playing);
	}

	fore() {
		if (this.index < this.imgs.length-1) { this.index += 1; }
		else { this.index = 0; }
		document.getElementById(this.id).src = this.imgs[this.index];
	}

	last() {
		this.index = this.imgs.length-1;
		document.getElementById(this.id).src = this.imgs[this.index];
	}

	/*test() {
		alert( 'this is a test' );
	}*/
}