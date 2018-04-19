/*
	Home.js
*/

/*
	TODO:
	-----
		implement expand/collapse
			must go from dual-panel to single panel for Main Tabs
			also need to determine how to handle MesoImg div for tabs

*/

var expanded = true;	// default is expanded Main Tab content

function set_defaults() {
	// hide all Main Tabs content, except for .default designated
	$("#MainTabsWrapper > div:not(.default)").addClass("hide");
	$("#MainTabsWrapper > div.default").addClass("show");
	
	// set active Main Tabs
	$("#MainTabsNav > li:eq(0)").addClass("active");
	$("#MainTabsNav > li:eq(1)").addClass("active");
	
	// hide all Info Tabs content
	$("#InfoTabsWrapper > div").addClass("hide");
	
	// hide on-hover link styling
	$("a.link > span").addClass("hide");
	
}


/*
	display SPC Meso img of field
	pre:	valid field key
	post:	MesoImg src set to value[0] of key/value pair
			MesoImg alt set to value[1] of key/value pair
*/
function meso_sel(field) {
	// big ole SPC Meso img dictionary
	let mesoimgs = {
		"obser":["bigsfc","Surface Observations","sfc_highlight.png"],
		"press":["pmsl","Mean Sea Level Pressure","sfc_highlight.png"],
		"poten":["mxth","Potential Temperature and Mixing Ratio","sfc_highlight.png"],
		"dewpt":["ttd","Surface Pressure/Winds/Temperature/Dew Point","sfc_highlight.png"],
		"925mb":["925mb","925mb Heights/Winds/Temperature/Dew Point","925mb_highlight.png"],
		"850mb":["850mb","850mb Heights/Winds/Temperature/Dew Point","850mb_highlight.png"],
		"700mb":["700mb","700mb Heights/Winds/Temperature/Relative Humidity","700mb_highlight.png"],
		"500mb":["500mb","500mb Heights/Winds/Temperature","500mb_highlight.png"],
		"300mb":["300mb","300mb Heights/Winds/Divergence","300mb_highlight.png"],
		"h8frt":["8fnt","850mb Heights/Winds/Temperature/Frontogenesis","850mb_highlight.png"],
		"h8adv":["tadv","850mb Heights/Winds/Temperature/Temp Advection","850mb_highlight.png"],
		"h7frt":["7fnt","700mb Heights/Winds/Temperature/Frontogenesis","700mb_highlight.png"],
		"h7adv":["7tad","700mb Heights/Winds/Temperature/Temp Advection","700mb_highlight.png"],
		"h5chg":["500mb_chg","500mb Heights/Winds/12hr 500mb Height Change","500mb_highlight.png"],
		"h5vrt":["vadv","500mb Heights/Vorticity/700-500mb Differential Cyclonic Vorticity Advection","500mb_highlight.png"],
		"h3crc":["ageo","300mb Heights/Ageostrophic Wind/700-500mb Lift","300mb_highlight.png"],
		"sbcap":["sbcp","Surface Based CAPE/CIN/Winds"],
		"mlcap":["mlcp","Mixed Layer CAPE/CIN/Surface Winds"],
		"mucap":["mucp","Most Unable Parcel CAPE/Lifted Parcel Level"],
		"mllap":["laps","700-500mb Lapse Rate"],
		"lllap":["lllr","0-3Km Lapse Rate"],
		"lclht":["lclh","Lifting Condensation Level"],
		"lfcht":["lfch","Level of Free Convection"],
		"1kmsh":["shr1","0-1Km Wind Shear Vector"],
		"6kmsh":["shr6","0-6Km Wind Shear Vector"],
		"8kmsh":["shr8","0-8Km Wind Shear Vector"],
		"911sh":["ulsr","9-11Km Storm Relative Winds"],
		"effsh":["eshr","Effective Wind Shear Vector"],
		"1kmsr":["srh1","0-1Km Storm Relative Helicity"],
		"3kmsr":["srh3","0-3Km Storm Relative Helicity"],
		"effsr":["effh","Effective Storm Relative Helicity"],
		"sbvrt":["dvvr","Surface Vertical Vorticity/Winds"]
	};
	
	
	param = mesoimgs[field][0];
	descr = mesoimgs[field][1];
	
	$("#MesoImg").attr("src", "http://www.spc.noaa.gov/exper/mesoanalysis/s20/" + param + "/" + param + ".gif");
	$("#MesoImg").attr("alt",descr);
	
	//alert( Object.keys(field).length );
	
	/* if available also set src to corresponding Supercell Schematic and Skew-T for the field selected */
	if ( mesoimgs[field].length == 3 ) {
		$("#SCDiagram").attr("src", "./img/"+mesoimgs[field][2]);
	}
}


/*
	shows Main Tab with id
	pre:	id must have prefix #
	post:	show content of Tab with id
*/
function maintab_sel(id) {
	/*** ugly conditionals, not sure if there's a better way ***/
	if (expanded) {
		// if Disc Tab is selected while expanded, do nothing
		if ( id == "#DiscTab" ) { return; }
		// otherwise don't hide Disc Tab
		else {
			$("#MainTabsWrapper > div:not(:first-of-type)").removeClass("show").addClass("hide");
		}
	}
	// when collapsed hide all content
	else {
		$("#MainTabsWrapper > div").removeClass("show").addClass("hide");
	
		// if collapsed and Disc tab selected only show Disc Tab content
		if ( id == "#DiscTab" ) {
			$("#DiscTab").removeClass("hide").addClass("show");
			return;
		}
	}
	
	// show active content
	$(id).removeClass("hide").addClass("show");
	$("#MesoImgWrapper").removeClass("hide").addClass("show");
}


function expand() {
	// hide Disc content if not active
	if ( !$("#MaintTabsNav li:first-of-type").hasClass("active") ) { $("#DiscTab").removeClass("show").addClass("hide"); }

	expanded = true;
}
function collapse() {
	
	
	expanded = false;
}


/*
	Callback function for when DOM is loaded
	pre:	Client request is received
	post:	event handlers are active
*/
$(document).ready(function() {
	
	/*
		on-click event for internal links
		pre:	DOM loaded
				link has id=[tab]-[param]
		post:	call maintab_sel(...) for content
				call meso_sel(...) for display
	*/
	$("a.link").click(function() {
		maintab_sel( "#"+$(this).attr("id").split("-")[0]+"Tab" );
		meso_sel( $(this).attr("id").split("-")[1] );
	});
	
	
	/*
		on-click event for Main Tabs Nav
		pre:	DOM loaded
		post:	call maintab_sel(...) for content id
				set clicked Tab active
	*/
	$("#MainTabsNav > li").click(function() {
		// if not active Tab clicked
		if ( !$(this).hasClass("active") )  {
			maintab_sel( "#"+$("#MainTabsWrapper > div:eq(" + $("#MainTabsNav > li").index(this) + ")").attr("id") )
			
			// remove active highlight, if expanded don't remove Disc Tab highlight
			if ( expanded ) { $("#MainTabsNav > li:not(:first-of-type)").removeClass("active"); }
			else { $("#MainTabsNav > li").removeClass("active"); }
			// highlight new active
			$(this).addClass("active");
		}
	});
	
	
	/*
		on-click event for Main Tabs content Navs
		pre:	DOM loaded
				li has id=[param]
		post:	call meso_sel(...) for meso param
	*/
	$("#MainTabsWrapper > div.content > ul > li").click(function() {
		meso_sel( $(this).attr("id") );
	});
});	// end doc.ready()

