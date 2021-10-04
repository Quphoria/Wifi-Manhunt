// Includes
#include <ESP8266WiFi.h>
#include <ArduinoWebsockets.h>

#include "config.h"

// Defines
#define LEDPin1 D0
#define LEDPin2 D4

// global vars
bool alive = 0;
bool game_running = 0;
bool ready = 0;
bool do_cal = 0;
bool do_ident = 0;


//function to return MAC address without semicolons
String getmacid(){
  String mac = WiFi.macAddress();
  for (int i=0; i<5; i++){
    mac.remove(2+i*2, 1);
  }
  return mac;
}


// Websocket Client pre-setup and callback
websockets::WebsocketsClient wsClient;
void onEventsCallback(websockets::WebsocketsEvent event, String data) {
    if(event == websockets::WebsocketsEvent::ConnectionOpened) {
        Serial.println("Connnection Opened");
    } else if(event == websockets::WebsocketsEvent::ConnectionClosed) {
        Serial.println("Connnection Closed");
    } else if(event == websockets::WebsocketsEvent::GotPing) {
        Serial.println("Got a Ping!");
    } else if(event == websockets::WebsocketsEvent::GotPong) {
        Serial.println("Got a Pong!");
    }
}
void wsMessageCallback(websockets::WebsocketsMessage message) {
  Serial.print("Got Message: "); Serial.println(message.data());
  String msgData = message.data();
  if (msgData.charAt(0) == 'S'){ //data valid if S exists
    alive = msgData.charAt(1);
    game_running = msgData.charAt(2);
    ready = msgData.charAt(3);
    do_cal = msgData.charAt(4);
    do_ident = msgData.charAt(5);
  }

}

bool ledsOn = 0;
//Invert LEDs
void ledInvert(){
  if (ledsOn == 0){
    digitalWrite(LEDPin1, LOW);
    digitalWrite(LEDPin2, LOW);
    ledsOn = 1;
  } else {
    digitalWrite(LEDPin1, HIGH);
    digitalWrite(LEDPin2, HIGH);
    ledsOn = 0;
  }
}

// send websocket payload
void sendWsPayload(String content, String method){
  String wsPayload = "{\"method\": \"" + method + "\", \"content\": " + content + "}";
  Serial.println(wsPayload);
  wsClient.send(wsPayload);
}



// setup   ####################################################################################



void setup()
{
  // IO Pins
  pinMode(LEDPin1, OUTPUT);
  pinMode(LEDPin2, OUTPUT);
  pinMode(0, INPUT_PULLUP);
  // Serial
  Serial.begin(115200);
  Serial.println();

  // WiFi Mode
  WiFi.mode(WIFI_AP_STA);
  
  // Start WiFi beacon
  Serial.print("Starting AP: "); Serial.println((GamePrefix + getmacid()));
  WiFi.softAP((GamePrefix + getmacid()));

  // Connect to WiFi Base
  WiFi.begin(BaseWiFiSSID, BaseWiFiPass); // base station WiFi network details
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    for(int i=0; i<4; i++){
      delay(125);
      ledInvert();
    }
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());

  //init callback for websockets
  wsClient.onMessage(wsMessageCallback);
  wsClient.onEvent(onEventsCallback);
  wsClient.connect(WebsocketServer);
  // websocket register with game server
  sendWsPayload(("{\"mac\": \"" + getmacid() + "\"}"), "join");

}


// functions for main loop   ##################################################################


// scan for nearby game devices
unsigned long interWiFiScan = 3000;
unsigned long lastWiFiScan = 0;
void WiFiScan(String method){
  if ((millis() - lastWiFiScan) > interWiFiScan){
    Serial.println("Scanning");
    int n = WiFi.scanNetworks();
    if(n==0){
      Serial.println("No Networks Found");
    } else {
      Serial.print(n); Serial.println(" Networks Found, showing game networks only");
      String wsPayload = "{\"mac\": \"" + getmacid() + "\", \"signals\":[";
      bool addComma = 0;
      for(int i=0; i<n; i++){
        if(WiFi.SSID(i).startsWith(GamePrefix)){
          if(addComma == 1){wsPayload = wsPayload + ", ";}
          Serial.print(i+1); Serial.print(". "); Serial.print(WiFi.SSID(i)); Serial.print(" "); Serial.print(WiFi.RSSI(i)); Serial.println("dBm");
          wsPayload = wsPayload + "{\"essid\": \"" + (WiFi.SSID(i).substring(5)) + "\", \"rssi\": " +  WiFi.RSSI(i) + " }";
          addComma = 1;
        }
      }
      wsPayload = wsPayload + "]}";
      sendWsPayload(wsPayload, method);
    }
    lastWiFiScan = millis();
  } 
}

// poll websocket server
void pollWs(){
  wsClient.poll();
}

//Connect WiFi if lost
void testWiFiConnection(){
  if(WiFi.status() != WL_CONNECTED){
    WiFi.begin(BaseWiFiSSID, BaseWiFiPass); // base station WiFi network details
    Serial.print("Connection Lost. Reconnecting");
    while(WiFi.status() != WL_CONNECTED){
      for(int i=0; i<4; i++){
        delay(125);
        ledInvert();
      }
    }
    Serial.print("Reconnected");
  }
}






// loop   #####################################################################################

void loop() {


if (do_cal){
  while(digitalRead(0)){ledInvert(); delay(50);}
  WiFiScan("cal");
  do_cal = 0;
}

while(game_running){
  testWiFiConnection();
  pollWs();
  if(!alive){
  WiFiScan("rssi");
  }

}

pollWs();
testWiFiConnection();

  
}