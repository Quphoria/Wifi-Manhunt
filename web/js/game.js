const api_url = "http://localhost:8080"

function get_state() {
  $.getJSON(api_url + "/state", (data) => {
    console.log(data);
    $("#game_status").text(data.status);
  })
  $.getJSON(api_url + "/clients", (data) => {
    console.log(data);
    // load_clients(data.clients);
    // $("#game_status").text(data.status);
  })
}

function set_nickname(event) {
  console.log(event);
  const mac = $(event.target).data("mac");
  const nick = prompt("Nickname");
  post_req("/nick", {
    "mac": mac,
    "nick": nick
  });
}

function cal_client(event) {
  console.log(event);
  const mac = $(event.target).data("mac");
  post_req("/startcal", {
    "mac": mac
  });
}

function load_clients(data) {
  $("#clienttablebody").empty();
  for (client of data) {
    create_row(client);
  }
}

function create_row(data) {
  var template = $("#clientrow").html();
  var new_row = $(template);
  new_row.appendTo("#clienttablebody");
  new_row.find('[class*="client-mac"]').first().text(data.mac);
  new_row.find('[class*="client-nick"]').first().text(data.nick);
  new_row.find('[class*="client-rssi-t"]').first().text(data.cal_rssi_threshold);
  new_row.find('[class*="client-alive"]').first().text(data.alive ? "Yes" : "No");

  sn_b = new_row.find('[class*="client-set-nick"]').first();
  sn_b.data("mac", data.mac);
  sn_b.click(set_nickname);
  nr_b = new_row.find('[class*="client-cal"]').first();
  nr_b.data("mac", data.mac);
  nr_b.click(cal_client);
}

async function post_req(path, data) {
  const response = await fetch(api_url + path, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return response.json();
}



$(function(){
    // This code runs after the document ready.
    setInterval(function(){ 
      get_state();
      //code goes here that will be run every second.    
    }, 1000);

    create_row({
      "mac": "BCFF4D82538E",
      "nick": "TestPLZ",
      "cal_rssi_threshold": -21,
      "alive": true
    });

    $("#game_start").click(() => {
      post_req("/start", {"imposters": [
        "BCFF4D82538F"
      ]});
    });

    $("#game_stop").click(() => {
      post_req("/stop", {});
    });
});

/*
const body = 'Cannot access projects.json<br>' +
          "<code>" + e.status + ": " + e.statusText + "</code>";
        $('#errorModalBody').html(body);
        $('#errorModal').modal('show');
   */

    