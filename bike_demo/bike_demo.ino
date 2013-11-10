const int encoderPin = 3;

void setup() {
  pinMode(encoderPin, INPUT);
  digitalWrite(encoderPin, HIGH);
  Serial.begin(9600);
}

int lastButtonState = 0;

void loop() {
  int buttonState = digitalRead(encoderPin);
  if (lastButtonState != buttonState) {
    lastButtonState = buttonState;
    Serial.println("c");
  } else {
    Serial.println("n");
  }
  // Serial.println(curCount);
}
