char dataString[50] = {0};
int a = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int in = Serial.readStringUntil('\n').toInt();
  Serial.println(in);
  
  delay(100);
}
