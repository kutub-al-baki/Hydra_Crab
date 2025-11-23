#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10);  // CE, CSN
const byte address[6] = "00001";

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_LOW);
  radio.stopListening();  // Set module as transmitter
}

void loop() {
  const char text[] = "Hello World";
  bool success = radio.write(&text, sizeof(text));
  
  if (success) {
    Serial.println("Sent: Hello World");
  } else {
    Serial.println("Send failed");
  }

  delay(1000);
}
