const int encoderPin = 3;

void setup() {
  pinMode(encoderPin, INPUT);
  digitalWrite(encoderPin, HIGH); // set the encoder pin to pull-up
  Serial.begin(9600);
}

int lastButtonState = 0;

void loop() {
  int buttonState = digitalRead(encoderPin);
  if (buttonState != lastButtonState) {
    Serial.println("c");
    lastButtonState = buttonState;
  } else {
    Serial.println("n");
  }
}
