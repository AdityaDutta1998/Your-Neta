
//populate all states
$.getJSON( "/static/js/AllStates.json", function( data ) {
	var states = '';
	data.forEach(function(state){
		states = states + "<option value='"+ state + "'>" + state + "</option>";
	})

	$('#state_select').append(states);

});




// get the constituencies
var constituencies = {};

$.getJSON( "/static/js/AllSeats.json", function(data) {
	constituencies = data;
});



function updateConstituencies(){
	var selected_state = document.getElementById('state_select').value;

	var selected_constituencies = constituencies[selected_state];

	$('#constituencies_select').find('option').remove();

	var tmp = "<option value='Constituency'>Constituency</option>";

	if(selected_state == "State"){
		$('#constituencies_select').append(tmp);
		return;
	}

	selected_constituencies.sort();

	selected_constituencies.forEach(function(constituency){
		tmp = tmp + "<option value='"+ constituency + "'>" + constituency + "</option>";
	})

	$('#constituencies_select').append(tmp);
}



function showError(){
	$("#error_header").show();
	$("#error_header").text("Please provide both fields");
}


function submitDetails(){
	var selected_state = document.getElementById('state_select').value;
	var selected_constituency = document.getElementById('constituencies_select').value;

	if(selected_state == "State" || selected_constituency == "Constituency"){
		showError()
		return;
	}

	localStorage.setItem('state', selected_state);
	localStorage.setItem('constituency', selected_constituency);

	var base_url = window.location.origin;
	location.href = base_url+"/interests";

}
