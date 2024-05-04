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

}

void loop(){
    digitalWrite(13, HIGH);

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
    
    if(adc > 600 || adc > env){
      state = WORKING;
    }
    else {
      if(env > 600)
        state = SLEEPING;
      else
        state = FAULT;
    }
    // state = ((adc < env) || adc < 600) ? ((env > 600)? SLEEPING : FAULT) : WORKING;


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

    LCD.setCursor(8,1);
    LCD.print(lampID);

    drawLine('+', 80);
    digitalWrite(13, LOW);
    delay(3000);
}

