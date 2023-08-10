#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "SingStar";
const char* password = "SingStar";

int pushButton = 4;
int buttonStatePrev = 1;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200); 
  // make the pushbutton's pin an input:
  pinMode(pushButton, INPUT_PULLUP);
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input pin:
  int buttonState = digitalRead(pushButton);
  // print out the state of the button:
  if (buttonState != buttonStatePrev && buttonState == 0){
    Serial.println("Pressed");
    if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;
      http.begin("http://192.168.137.1:5000/screenshot");
      int httpResponseCode = http.GET();
      if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        Serial.println(payload);
      }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      // Free resources
      http.end();
    }else{
      Serial.println("WiFi Disconnected");
    }
  }
  buttonStatePrev = buttonState;
  delay(10);        // delay in between reads for stability
}
