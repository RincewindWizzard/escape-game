
#define TX_PIN 12
#define RX_PIN 0
#define LED 13
#define NETWORK 0b00100


#define THRESHOLD_UPPER 70
#define THRESHOLD_LOWER 30
void setup() {
  pinMode(TX_PIN, OUTPUT);
  pinMode(RX_PIN, INPUT);
  Serial.begin(9600);
  
}


void loop() {
  if (Serial.available() > 3) {
    uint8_t network = Serial.read();
    uint8_t btn     = Serial.read();
    
    // on or off
    uint8_t state   = Serial.read();
    
    
    digitalWrite(13, HIGH);
    for(uint8_t i = 0; i < 3; i++) {
      send_code(network, btn, state);
      delay(100);
    }
    digitalWrite(13, LOW);
  }
}

void send_code(byte network, byte btn, boolean state) {
  network = network & 0b11111;
  btn = (1 << btn) & 0b11111;
  byte state_seq = 0;
  if(state)
    state_seq = 0b10;
  else
    state_seq = 0b01;
  unsigned int data = (state_seq << 10) | (btn << 5) | network;
  
  for(byte i=0; i< 7; i++)
    rfsend(data, 12);


}

void rfsend(int data, byte length) {
  byte digit;
  for(byte i=0; i < length; i++) {
    digit = data & 1;
    data = data >> 1;
    if(digit) {
      digitalWrite(TX_PIN, HIGH);
      wait(1);
      digitalWrite(TX_PIN, LOW);
      wait(3);
      digitalWrite(TX_PIN, HIGH);
      wait(1);
      digitalWrite(TX_PIN, LOW);
      wait(3);
    }
    else {
      digitalWrite(TX_PIN, HIGH);
      wait(1); //da die Pausen x*350us lang sind, machen wir daraus eine Funktion
      digitalWrite(TX_PIN, LOW);
      wait(3);
      digitalWrite(TX_PIN, HIGH);
      wait(3);
      digitalWrite(TX_PIN, LOW);
      wait(1);      
    }
  }
  rfsync();
}

void rfsync() {
  digitalWrite(TX_PIN,HIGH);
  wait(1);
  digitalWrite(TX_PIN,LOW);
  wait(31);
}

void wait(int x) {
  delayMicroseconds(x*350); //warte x*350us
}

