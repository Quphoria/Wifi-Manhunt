const api_url = "http://localhost:8080";

function get_state() {
  $.getJSON(api_url + "/state", (data) => {
    console.log(data);
    $("#game_running").toggle(data.game_running);
    $("#game_stopped").toggle(!data.game_running);
  })
  $.getJSON(api_url + "/clients", (data) => {
    console.log(data);
    load_clients(data.clients);
  })
}

$(function () {
  // This code runs after the document ready.
  setInterval(function () {
    get_state();
    //code goes here that will be run every second.    
  }, 1000);

 
});

/*
  Calling the error modal
  $('#errorModalBody').html("body html");
  $('#errorModal').modal('show');
*/