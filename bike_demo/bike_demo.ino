const int encoderPin = 5;

void setup() {
  pinMode(encoderPin, INPUT);
  digitalWrite(encoderPin, HIGH); // set the encoder pin to pull-up
  TCCR1A = 0;
  Serial.begin(9600);
}

int lastButtonState = 0;
const int samplePeriod = 10;

void loop() {
  // stop counting
  TCCR1B = 0;
  int count = TCNT1;
  // reset the counter
  TCNT1 = 0;
  
  // start counting
  bitSet(TCCR1B, CS12); // Counter clock source is external pin
  bitSet(TCCR1B, CS11); // Clock the rising edge
  delay(samplePeriod);
  Serial.println(count);
}
