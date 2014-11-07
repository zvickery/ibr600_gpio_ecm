int ledPin = 13;       // LED output
int relayPin = 7;      // Relay output
int buttonPin = 12;    // Pushbutton input
int ibrInputPin = 10;  // GPIO input on IBR
int ibrOutputPin = 11; // GPIO output on IBR

void setup() {
  Serial.begin(9600);
  
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT);
  pinMode(relayPin, OUTPUT);
  
  pinMode(ibrInputPin, OUTPUT);
  pinMode(ibrOutputPin, INPUT);
}

void loop() {  
  buttonCheck();
  ibrCheck();
  delay(10);
}

void buttonCheck()
{ 
  static int buttonState;
  static int lastButtonState = LOW;   // the previous reading from the input pin

  // the following variables are long's because the time, measured in miliseconds,
  // will quickly become a bigger number than can be stored in an int.
  static long lastDebounceTime = 0;  // the last time the output pin was toggled
  static long debounceDelay = 50;    // the debounce time; increase if the output flickers 
  
  int reading = digitalRead(buttonPin); 

  // If the switch changed, due to noise or pressing:
  if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
  } 
  
  if ((millis() - lastDebounceTime) > debounceDelay) {
    // whatever the reading is at, it's been there for longer
    // than the debounce delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;

      // only toggle the LED if the new button state is HIGH
      if (buttonState == HIGH) {
        Serial.print("Push button high transition\n");
        stateChange();
      }
    }
  }

  // save the reading.  Next time through the loop,
  // it'll be the lastButtonState:
  lastButtonState = reading;
}

void ibrCheck()
{
  static int previousState = LOW;
  
  int currentState = digitalRead(ibrOutputPin);
  if (previousState == HIGH && currentState == LOW)
  {
    Serial.print("IBR HIGH->LOW transition\n");
    stateChange();
  }
  
  previousState = currentState;
}

void stateChange()
{  
  static int state = LOW;
  state = !state;
  
  digitalWrite(ledPin, state);
  digitalWrite(ibrInputPin, state);
  digitalWrite(relayPin, state);
}
