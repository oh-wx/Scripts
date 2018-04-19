/*
	GeoLocate Forecast
*/
/*
function get_latlon() {
	if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(function success(position) {
				alert( 'Lat: ' + position.coords.latitude.toString() + '\nLon: ' + position.coords.longitude.toString() );},
			function error() {
				alert('An error occurred retrieving Lat/Lon');
			});
	}
	else {
		alert('GeoLocate is no enabled');
	}
}*/




var Location = {};

if (navigator.geolocation) {
	navigator.geolocation.getCurrentPosition(success, error);
}
else {
	alert('GeoLocate not supported');
}

function error() {
	alert('GeoLocate enabled, but unable to determine Lat/Lon')
}

function success(position) {
	Location.lat = position.coords.latitude;
	Location.lon = position.coords.longitude;
	
	alert( 'Lat:' + Location.lat.toString() + '\nLon:' + Location.lon.toString() )
}


