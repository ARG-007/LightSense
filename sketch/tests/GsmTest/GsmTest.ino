#include <SoftwareSerial.h>

const byte gsmTx = 8;
const byte gsmRx = 9;
const byte gsmReset = 10;

SoftwareSerial gsm(gsmTx, gsmRx);

String buffer = "";

void serialExchange() {
  // delay(50);
  if (Serial.available()) {
    buffer = Serial.readString();
    gsm.println(buffer);
  }

  while(gsm.available()) {
    Serial.write(gsm.read());
  }
}

void setup() {
  Serial.begin(115200);
  gsm.begin(9600);

  Serial.println("Initializing GSM");
  gsm.println("AT");
  serialExchange();
  gsm.println("AT+CSQ");
  serialExchange();
  gsm.println("AT+CCID");
  serialExchange();
  gsm.println("AT+CREG?");
  serialExchange();

  Serial.println("Give AT Commands Now");
}

void loop() {
  // delay(500);
  serialExchange();
}
