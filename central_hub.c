#include <SoftwareSerial.h>
#define RX 6
#define TX 5

SoftwareSerial ESP01 (RX,TX); // RX | TX

String ssid = "138SL-Residents";
String password = "resident2020@138sl";
String host = "10.10.4.124";
String PORT = "5500";
String Command  = "";
String post = "";
String body = "";
int id = 1;
int countTrueCommand;
int countTimeCommand; 
boolean found = false; 

void setup() {
  randomSeed(analogRead(0));
  Serial.begin(115200);
  ESP01.begin(115200);
  sendCommand("AT",5,"OK"); // check if connection is okay
  sendCommand("AT+CWMODE=1",5,"OK"); // set client mode
  sendCommand("AT+CWJAP=\""+ ssid +"\",\""+ password +"\"",20,"OK");
  
}

void loop() {
   sendCommand("AT+CIPSTART=\"TCP\",\""+ host +"\"," + PORT,15,"OK");
   body = "";
    body = "{\"sensor_id\":"+ String(getsensor_id());
    body+= ",\"moisture\":" +String(getmoisture());
    body+= "}";
    post="";
    post = "POST /sensor HTTP/1.1\r\nHost: ";
    post += host;
    post += "\r\nContent-Type: application/json\r\nContent-Length:";
    post += body.length();
    post += "\r\n\r\n";
    post += body;
    post += "\r\n";
    Command = "AT+CIPSEND=";
    Command+= String(post.length());
    sendCommand(Command, 10, "OK");
    sendCommand(post, 10,"OK");
    sendCommand("AT+CIPCLOSE=0", 15, "OK");
    delay(5000);
}


void sendCommand(String command, int maxTime, char readReplay[]) {
  Serial.print(countTrueCommand);
  Serial.print(". at command => ");
  Serial.print(command);
  Serial.print(" ");
  while(countTimeCommand < (maxTime*1))
  {
    ESP01.println(command);//at+cipsend
    if(ESP01.find(readReplay))//ok
    {
      found = true;
      break;
    }
  
    countTimeCommand++;
  }
  
  if(found == true)
  {
    Serial.println("Successful");
    countTrueCommand++;
    countTimeCommand = 0;

  }
  
  if(found == false)
  {
    Serial.println("Unsuccessful");
    countTrueCommand = 0;
    countTimeCommand = 0;
  }
  
  found = false;
 }

 int getmoisture() {
  return random(0,2);
 }

 int getsensor_id() {
  return random(1,3);
 }