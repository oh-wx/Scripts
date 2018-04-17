/*
	Home.js
*/

var mesoimgs = {
	"obser": ["bigsfc","Surface Observations"],
	"press": ["pmsl","Mean Sea Level Pressure"],
	"poten": ["mxth","Potential Temperature and Mixing Ratio"],
	"dewpt": ["ttd","Surface Pressure/Winds/Temperature/Dew Point"],
	"925mb": ["925mb","925mb Heights/Winds/Temperature/Dew Point"],
	"850mb": ["850mb","850mb Heights/Winds/Temperature/Dew Point"],
	"700mb": ["700mb","700mb Heights/Winds/Temperature/Relative Humidity"],
	"500mb": ["500mb","500mb Heights/Winds/Temperature"],
	"300mb": ["300mb","300mb Heights/Winds/Divergence"]
};

function meso_sel(field) {
	param = mesoimgs[field][0];
	descr = mesoimgs[field][1];
	
	$("#MesoImg").attr("src", "http://www.spc.noaa.gov/exper/mesoanalysis/s20/" + param + "/" + param + ".gif");
	$("#MesoImg").attr("alt",descr);
	
	/* also set src to corresponding Supercell Schematic and Skew-T for the field selected */
	// document.getElementById(id+"Schematic").src = "...";
}


function maintab_sel(sel) {
	// remove active highlight
	$("#MainTabsNav > li").removeClass("active");
	// hide all content
	$("#MainTabsWrapper > div:not(:first-of-type)").removeClass("show").addClass("hide");
	// highlight active tab
	$(document).click(function(event) {
		$("#MainTabsNav > " + event.target).addClass("active");
	});
	// show selected content
	$(sel).removeClass("hide").addClass("show");
}


/*
$(document).ready(function() {

		alert("ready");

	$("#MainTabsNav > li").click(function() {
		
		alert("clicked");
		
		if ( !$(this).hasClass("active") )  {
			// remove active highlighting
			$("#MainTabsNav > li").removeClass("active");
			// hide content
			$("#MainTabsWrapper > div").removeClass("show").addClass("hide");
			// highlight new active
			$(this).addClass("active");
			// show active content
			//$("#MainTabsWrapper > div:eq(" + $("#MainTabsNav > li").index(this) + ")").removeClass("hide").addClass("show");
		}
	});

});
*/