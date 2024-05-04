// Hacky solution for VOltmeter, as I don't have one
#include <LiquidCrystal.h>

//LCD PINS
const byte rs = 2;
const byte en = 3;
const byte d4 = 4;
const byte d5 = 5;
const byte d6 = 6;
const byte d7 = 7;

const int VOLT_METER_PIN = A2;

const float R1 = 10000;
const float R2 = 1000;
const float VOLT_REF = 5;
const float RESISTOR_RATIO = R2 / (R1 + R2); 

LiquidCrystal LCD(rs, en, d4, d5, d6, d7);

int steps = 20;

float mesureVoltage(int steps) {
  float adc = 0;
  for(int i=0; i<steps; i++){
    adc += analogRead(VOLT_METER_PIN);
    delay(5);
  }
  adc /= steps;
  Serial.println(adc);
  return ((adc * VOLT_REF) / 1024 ) / RESISTOR_RATIO;
}

void setup() {
  Serial.begin(115200);
  digitalWrite(13, LOW);
  // analogReference(INTERNAL);

  analogWrite(A0, LOW);
  analogWrite(A1, LOW);
  // analogWrite(A2, LOW);
  analogWrite(A3, LOW);
  analogWrite(A4, LOW);
  analogWrite(A5, LOW);

  LCD.begin(16, 2);
  LCD.clear();
  LCD.setCursor(3, 0);
  LCD.print("VOLTMETER");

}

void loop() {
  Serial.print("Aproximating Voltage: ");
  float volts = mesureVoltage(steps); 
  Serial.print(volts);
  Serial.println(" V");

  LCD.setCursor(3, 1);
  LCD.print(volts);
  LCD.print(" V");
  delay(1000);
  // put your main code here, to run repeatedly:
}
