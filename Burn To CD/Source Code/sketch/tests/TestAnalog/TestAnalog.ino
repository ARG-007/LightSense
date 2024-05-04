
void setup() {
analogReference(INTERNAL);
  Serial.begin(115200);

  // pinMode(A0, INPUT);
  // pinMode(A1, INPUT);
  // pinMode(A2, INPUT);
  // pinMode(A3, INPUT);
  // pinMode(A4, INPUT);
  // pinMode(A5, INPUT);

  // pinMode(A0, OUTPUT);
  // pinMode(A1, OUTPUT);
  // pinMode(A2, OUTPUT);
  // pinMode(A3, OUTPUT);
  // pinMode(A4, OUTPUT);
  // pinMode(A5, OUTPUT);

  analogWrite(A0, LOW);
  analogWrite(A1, LOW);
  // analogWrite(A2, LOW);
  analogWrite(A3, LOW);
  analogWrite(A4, LOW);
  analogWrite(A5, LOW);

}

void loop() {
  // put your main code here, to run repeatedly:
  delay(1000);
  Serial.println("===========================================");
  Serial.print("A0: ");
  Serial.println(analogRead(A0));
  delay(250);
  Serial.print("A1: ");
  Serial.println(analogRead(A1));
  delay(250);
  Serial.print("A2: ");
  Serial.println(analogRead(A2));
  delay(250);
  Serial.print("A3: ");
  Serial.println(analogRead(A3));
  delay(250);
  Serial.print("A4: ");
  Serial.println(analogRead(A4));
  delay(250);
  Serial.print("A5: ");
  Serial.println(analogRead(A5));
  delay(250);
}
