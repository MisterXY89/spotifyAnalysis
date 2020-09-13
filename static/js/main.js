
/*
Author: Virendra
http://www.jquerybyexample.net/2012/06/get-url-parameters-using-jquery.html
*/
function getURLParameter(sParam) {
	var sPageURL = window.location.search.substring(1);
	var sURLVariables = sPageURL.split('&');

	for (var i = 0; i < sURLVariables.length; i++) {
		var sParameterName = sURLVariables[i].split('=');
		if (sParameterName[0] == sParam) {
			return sParameterName[1];
		}
	}
}


function setDefaults() {
  const limit_field = document.getElementById("limit");
  const time_range_field = document.getElementById("time_range");

  let time_range = getURLParameter("time_range");
  let limit = getURLParameter("limit");


  if (time_range !== undefined) {
    time_range_field.value = time_range;
  } else {
    time_range_field.value = "short_term";
  }

  if (limit !== undefined) {
    limit_field.value = limit;
  } else {
    limit_field.value = 10;
  }
}

function generateHtmlForDisplay(item) {
  return "<tr>"
          + "<td> <img src='"
          +  item.album.images[2].url
          + "' alt='album cover'/> </td>"
          + "<td>"
          +  item.name
          + "</td>"
          + "<td>"
          +   item.artists[0].name
          + "</td>"
          + "<td>"
          +  item.album.name
          + "</td>"
					+ "<td>"
					+ "<button type='button' class='btn _box _success' onclick='analyseTrackFromQuery(this);' id='"+item.uri+"'> Analyse </button>"
					+ "</td>"
        + "</tr>";
}

function displayQueryResults(json) {
  const queryResultTable = document.getElementById("queryResultTable");
  const queryResults = document.getElementById("queryResults");
  json.forEach(item => {
    queryResults.innerHTML += generateHtmlForDisplay(item);
  });
  queryResultTable.style.display = "block";
}

function analyseTrackFromQuery(el) {
	let uri = el.id;
	document.getElementById("trackURI").value = uri;
	document.trackAnalyseForm.submit();
}

document.addEventListener("DOMContentLoaded", event => {

	let els = Array.from(document.getElementsByClassName("analyseUserPlaylistButton"));
	els.forEach(el => {
		el.addEventListener("click", event => {
			let uri = el.id;
			document.getElementById("playlistURI").value = uri;
			document.playlistAnalyseForm.submit();
		})
	});

	let searchBtn = document.getElementById("searchSong");

	if (searchBtn !== null) {

		searchBtn.addEventListener("click", event => {

			let trackInput = document.getElementById("trackURI");
			let searchTerm = trackInput.value;

			if (searchTerm != "") {

				fetch("/searchSong", {
					method: "post",
					headers: {
						'Accept': 'application/json',
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						query: searchTerm
					})
				})
				.then(response => {
					console.log(response);
					return response.json();
				})
				.then(json => {
					console.log(json);
					displayQueryResults(json.result);
				})
				.catch(error => {
					console.log(error);
				});

			} else {
				alert("Please enter a query :)");
			}


		});

	}

});
