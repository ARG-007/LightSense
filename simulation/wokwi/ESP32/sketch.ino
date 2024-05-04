#include <WiFi.h>
#include <PubSubClient.h>

typedef struct {
    int id;
    int lamp;
    int env;
    bool previousState;
} LDR;

enum state {WORKING=1, SLEEPING, FAULT};

const LDR ldr[]={{1,32,33,true},{3,34,35,true}};
int adc, env;

const char *MQTT_SERVER = "broker.mqttdashboard.com";
const char *USER = "";
const char *PASS = "";
const char *CLIENT_ID = "ABDTG_LS_ESP32PUB";
const char *TOPIC = "ABDTG_LightSense";
const int MQTT_PORT = 1883;

WiFiClient wificlient;
PubSubClient client(wificlient);

void drawLine(char c, int times){
    for(int i=0;i<times;i++){
        Serial.print(c);
    }
    Serial.println();
}

bool connectWifi(){
    int retries = 0, max=100;
    drawLine('=',80);
    Serial.println("Connecting Wifi");
    WiFi.mode(WIFI_STA);
    WiFi.begin("Wokwi-GUEST","",6);
    while(WiFi.status()!=WL_CONNECTED && retries<max) {
        delay(100);
        Serial.print(".");
        retries++;
    }
    Serial.println();
    
    if(retries>max){
        drawLine('=',80);
        Serial.println("Wifi Connection Failed!");
        return false;
    } else {
        Serial.println("Wifi Connected");
        drawLine('=',80);
        return true;
    }
}

bool connectMQTT(){
    int retries = 0, max = 5;
    drawLine('=',80);
    Serial.println("Connecting To MQTT Server");
    client.setServer(MQTT_SERVER, MQTT_PORT);
    while(!client.connected() && retries < max) {
        if(client.connect(CLIENT_ID, USER, PASS)){
            Serial.println("MQTT Server Connected Successfully!!");
            drawLine('=',80);
            return true;
        } else {
            Serial.print("Connection Failed With State :");
            Serial.println(client.state());
            Serial.println("Retrying");
            retries++;
            drawLine('-',80);
        }
    }
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
    drawLine('-',80);
    Serial.print("State : ");
    Serial.println(masked & 3);
    masked >>= 2;
    Serial.print("Global : ");
    Serial.println(masked & 1023);
    masked >>= 10;
    Serial.print("LDR : ");
    Serial.println(masked & 1023);
    masked >>= 10;
    Serial.print("ID : ");
    Serial.println(masked & 1023);
}

void setup(){
    Serial.begin(115200);
    if(connectWifi()==false){
        return;
    }
    if(connectMQTT()==false){
        return;
    }
}

void loop(){
    if(WiFi.status()!=WL_CONNECTED) {
        connectWifi();
    }
    if(!client.connected()){
        connectMQTT();
    }

    for(int i=0;i<2;i++){

        adc = analogRead(ldr[i].lamp);
        env = analogRead(ldr[i].env);
        int state = adc<env?(env>600 ? SLEEPING : FAULT ) : WORKING;
        unsigned long data =  mask(ldr[i].id, adc, env, state);
        unmask(data);
        if(client.publish(TOPIC,String(data).c_str())){
            Serial.println("Published");
        } else {
            Serial.println("Not Published");
        }
        drawLine('-',80);
    }

    delay(1000);
}

