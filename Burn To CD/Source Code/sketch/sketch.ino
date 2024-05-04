#define TINY_GSM_MODEM_SIM800
#define SerialMon Serial
#define TINY_GSM_DEBUG SerialMon
#define LOGGING

#define GSM_AUTOBAUD_MIN 9600
#define GSM_AUTOBAUD_MAX 115200

#include <SoftwareSerial.h>


//SIM800L GSM Constants
const byte gsmTX = 8;
const byte gsmRX = 9;
const byte gsmReset = 10;

SoftwareSerial gsm(gsmTX,gsmRX);

#define GSM_PIN ""

const char apn[]      = "YourAPN"; // Do nOt Leave at Default Value
const char gprsUser[] = "";
const char gprsPass[] = "";

const char *MQTT_SERVER = "broker.mqttdashboard.com";
const char *USER = "";
const char *PASS = "";
const char *CLIENT_ID = "ABDTG_LS";
const char *TOPIC = "ABDTG_LightSense";
const int MQTT_PORT = 1883;

#include <TinyGsmClient.h>
#include <PubSubClient.h>

#ifdef DUMP_AT_COMMANDS
#include <StreamDebugger.h>
StreamDebugger debugger(gsm, SerialMon);
TinyGsm        modem(debugger);
#else
TinyGsm        modem(gsm);
#endif

TinyGsmClient gsmclient(modem);
PubSubClient mqtt(gsmclient);

enum state {WORKING=1, SLEEPING, FAULT};


// LDR COnstants
const byte lampID = 24;
const byte lampPin = A0;
const byte envPin = A1;

short adc, env;
byte state;



// LCD Character Constants
#include <LiquidCrystal.h>

enum LCD_CHARACTERS {
    LAMP,
    ENVIRONMENT,
    MQTT_CONNECT,
    MQTT_DISCONNECT,
    MQTT_UPLOAD 
};

const byte Lamp[] = { B01110, B11011, B10001, B11011, B11111, B01010, B01010, B01010 };
const byte Environment[] = { B11111, B10001, B10101, B10101, B01110, B00100, B01110, B11111 };
const byte MQTT_Connect[] = { B00000, B00001, B01010, B00100, B10001, B11011, B10101, B10001 };
const byte MQTT_Disconnect[] = { B01010, B00100, B01010, B00000, B10001, B11011, B10101, B10001 };
const byte MQTT_Upload[] = { B00100, B01110, B10101, B00100, B10001, B11011, B10101, B10001 };

LiquidCrystal LCD(2,3,4,5,6,7);

void drawLine(char c, int times){
    for(int i=0;i<times;i++){
        Serial.print(c);
    }
    Serial.println();
}

bool connectGPRS(){
    drawLine('+',80);
    Serial.print(F("Connecting To APN :"));
    Serial.println(apn);

    if(!modem.gprsConnect(apn, gprsUser, gprsPass)){
        Serial.println(F("Status: Failed"));
    } else {
        Serial.println(F("Status: Success"));
    }
    drawLine('+',80);
    return modem.isGprsConnected();

}

bool connectMQTT(){
    int retries = 0, max = 5;
    drawLine('=',80);
    Serial.println(F("Connecting To MQTT Server"));

    while(!mqtt.connected() && retries < max) {
        if(mqtt.connect(CLIENT_ID, USER, PASS)){
            Serial.println(F("MQTT Server Connected Successfully!!"));
            drawLine('=',80);
            return true;
        } else {
            Serial.print(F("Connection Failed With State :"));
            Serial.println(mqtt.state());
            Serial.println(F("Retrying"));
            retries++;
            drawLine('-',80);
        }
    }
    drawLine('=',80);
    return false;
}

unsigned long mask(int id, int ldr, int global, int state){
    unsigned long data = id;
    data <<= 10;
    data |= ldr;
    data <<= 10;
    data |= global;
    data <<=2;
    data |= state;

    return data;
}

void unmask(unsigned long masked){
    // drawLine('-',80);
    Serial.print(F("State : "));
    Serial.println(masked & 3);
    masked >>= 2;
    Serial.print(F("Global : "));
    Serial.println(masked & 1023);
    masked >>= 10;
    Serial.print(F("LDR : "));
    Serial.println(masked & 1023);
    masked >>= 10;
    Serial.print(F("ID : "));
    Serial.println(masked & 1023);
}

void setup(){
    Serial.begin(115200);
    // LCD.
    LCD.begin(16,2);

    LCD.createChar(LAMP, Lamp);
    LCD.createChar(ENVIRONMENT, Environment);



    pinMode(13, OUTPUT);

    // pinMode(lampPin, INPUT);
    // pinMode(envPin, INPUT);
    
    // Serial.println(F("Initializing GSM Serial"));
    // TinyGsmAutoBaud(gsm, GSM_AUTOBAUD_MIN, GSM_AUTOBAUD_MAX);
    // gsm.begin(115200);
    // delay(6000);
    // modem.init();

    // Serial.print(F("Modem Info : "));
    // Serial.println(modem.getModemInfo());

    // Set Server
    // mqtt.setServer(MQTT_SERVER, MQTT_PORT);

    // if(connectMQTT()==false){
    //     return;
    // }
    // if(connectGPRS()){
    //     Serial.println(F("GPRS Connected Successfully"));
    // } else {
    //     Serial.println(F("GPRS Connection Failed"));
    // }
}

void loop(){
    digitalWrite(13, HIGH);

    // if(!mqtt.connected()){
    //     connectMQTT();
    // }

    adc = analogRead(lampPin);
    env = analogRead(envPin);

    LCD.clear(); 

    LCD.setCursor(0, 0);
    LCD.write(LAMP);

    LCD.setCursor(0, 1);
    LCD.write(ENVIRONMENT);

    LCD.setCursor(2, 0);
    LCD.print(adc);
    LCD.setCursor(2, 1);
    LCD.print(env);
    
    state = ((adc < env) || adc < 600) ? ((env > 600)? SLEEPING : FAULT) : WORKING;


    unsigned long data =  mask(lampID, adc, env, state);
    unmask(data);

    String hexData = String(data, HEX).c_str();

    LCD.setCursor(8, 0 );
    switch(state) {
      case 1: LCD.print(F("WORKING"));break;
      case 2: LCD.print(F("SLEEPING"));break;
      case 3: LCD.print(F("BROKEN"));break;
    }
    
    Serial.print("Hex Data: ");
    Serial.println(hexData);


    // if(mqtt.publish(TOPIC, hexData)){
    //     Serial.println(F("Published"));
    // } else {
    //     Serial.println(F("Not Published"));
    // }

   
    drawLine('+', 80);
    digitalWrite(13, LOW);
    delay(3000);
}

