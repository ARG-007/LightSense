// include the library code:
#include <LiquidCrystal.h>

// Creates an LCD object. Parameters: (rs, enable, d4, d5, d6, d7)
LiquidCrystal lcd(2, 3, 4, 5, 6, 7);



const byte Lamp[] = { B01110, B11011, B10001, B11011, B11111, B01010, B01010, B01010 };
const byte Environment[] = { B11111, B10001, B10101, B10101, B01110, B00100, B01110, B11111 };
const byte MQTT_Connect[] = { B00000, B00001, B01010, B00100, B10001, B11011, B10101, B10001 };
const byte MQTT_Disconnect[] = { B01010, B00100, B01010, B00000, B10001, B11011, B10101, B10001 };
const byte MQTT_Upload[] = { B00100, B01110, B10101, B00100, B10001, B11011, B10101, B10001 };

enum SYMBOL {
  LAMP,
  ENV,
  MQC,
  MQNC,
  MQU
};

int i = 0;
void setup() 
{
	// set up the LCD's number of columns and rows:
	lcd.begin(16, 2);
  lcd.createChar(0, Lamp);
  lcd.createChar(1, Environment);
  lcd.createChar(2, MQTT_Connect);
  lcd.createChar(3, MQTT_Disconnect);
  lcd.createChar(4, MQTT_Upload);

	// Clears the LCD screen
	lcd.clear();

	lcd.print("Project Boomer");
  // lcd.print("34");

	lcd.setCursor(0, 1);


  lcd.write(LAMP);
  lcd.write(ENV);
  lcd.write(MQC);
  lcd.write(MQNC);
  lcd.write(MQU);

}

void loop() 
{
// 	// Print a message to the LCD.
//   analogWrite(A5, i);
// 	// set the cursor to column 0, line 1
// 	// (note: line 1 is the second row, since counting begins with 0):
// 	lcd.setCursor(0, 1);
// 	// Print a message to the LCD.
// 	lcd.print(i);
//   i++;

  delay(250);
}
