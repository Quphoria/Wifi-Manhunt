const api_url = "http://localhost:8080"

function get_state() {
  $.getJSON(api_url + "/state", (data) => {
    console.log(data);
    $("#game_status").text(data.status);
  })
}

function set_nickname(event) {
  console.log(event);
  const nick = prompt("Nickname");

}

function create_row(data) {
  var template = $("#clientrow").html();
  var new_row = $(template);
  new_row.appendTo("#clienttablebody");
  new_row.find('[class*="client-set-nick"]').first().click(set_nickname);
}

$(function(){
    // This code runs after the document ready.
    setInterval(function(){ 
      get_state();
      //code goes here that will be run every second.    
    }, 1000);

    create_row();
});

/*
const body = 'Cannot access projects.json<br>' +
          "<code>" + e.status + ": " + e.statusText + "</code>";
        $('#errorModalBody').html(body);
        $('#errorModal').modal('show');
   */

    