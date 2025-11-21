#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  150 // Minimum pulse length out of 4096
#define SERVOMAX  600 // Maximum pulse length out of 4096

void setup() {
  Serial.begin(9600);  // Initialize serial communication
  pwm.begin();
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz
}

void loop() {
  if (Serial.available() > 0) { // Check if data is available
    char command = Serial.read(); // Read the incoming byte
    processCommand(command);
  }
}

// Function to process received commands
void processCommand(char command) {
  switch (command) {
    case 'a':
      moveStandardServo(0, 180); // Rotate servo 0 to 180 degrees
      break;
    case '1':
      moveStandardServo(0, 0); // Return servo 0 to 0 degrees
      break;
    case 'b':
      moveStandardServo(1, 180); // Rotate servo 1 to 180 degrees
      break;
    case '2':
      moveStandardServo(1, 0); // Return servo 1 to 0 degrees
      break;
  }
}

// Function to move standard servos (like on channels 0 and 1)
void moveStandardServo(int channel, int position) {
  int pulse = map(position, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(channel, 0, pulse);   // Move the servo to the desired position
  delay(1000);                     // Wait for the servo to reach the position
}
