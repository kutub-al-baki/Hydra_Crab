#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Initialize PCA9685 driver
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Motor parameters
const int numMotors = 6;         // Number of motors
const int pwmFrequency = 50;    // Frequency for ESC (50 Hz)
const int pwmFullThrottle = 410; // Full forward throttle (2000 µs)
const int pwmNeutral = 307;      // Neutral throttle (1500 µs)
const int pwmStop = 205;         // Full reverse throttle (1000 µs)

// Function to move specific motors
void moveMotors(const int motors[], int numMotors, int pwmValue) {
  for (int i = 0; i < numMotors; i++) {
    pwm.setPWM(motors[i], 0, pwmValue);
  }
}

// Function to stop all motors
void stopAllMotors() {
  for (int motorChannel = 0; motorChannel < numMotors; motorChannel++) {
    pwm.setPWM(motorChannel, 0, pwmStop); // Ensure motors receive a stop signal
  }
}

// Function to calibrate ESCs
void calibrateESCs() {
  Serial.println("Calibrating ESCs...");

  // Step 1: Full throttle to enter calibration mode for all motors
  for (int motorChannel = 0; motorChannel < numMotors; motorChannel++) {
    pwm.setPWM(motorChannel, 0, pwmFullThrottle);
  }
  Serial.println("Sending Full Throttle...");
  delay(10); // Hold full throttle for 5 seconds

  // Step 2: Neutral throttle to set throttle range for all motors
  for (int motorChannel = 0; motorChannel < numMotors; motorChannel++) {
    pwm.setPWM(motorChannel, 0, pwmNeutral);
  }
  Serial.println("Setting Neutral Throttle...");
  delay(10); // Hold neutral for 3 seconds

  // Step 3: Explicitly stop all motors after calibration
  stopAllMotors();
  Serial.println("ESC Calibration Completed.");
}

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(pwmFrequency);
  delay(10);

  // Calibrate ESCs at startup
  calibrateESCs();
}

void loop() {
  // Check for serial commands
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n'); // Read the command from serial
    command.trim();                               // Remove trailing/leading whitespace

    // Recalibrate ESCs before executing a new command
    calibrateESCs();

    if (command == "up") {
      int motors[] = {1, 0}; // Channels for upward movement (M2 and M1)
      moveMotors(motors, 2, pwmFullThrottle);
      Serial.println("Moving Up...");
    } if (command == "right") {
      int motors[] = {3, 4}; // Channels for right movement (M4 and M5)
      moveMotors(motors, 2, pwmFullThrottle);
      Serial.println("Turning Right...");
    } if (command == "left") {
      int motors[] = {2, 5}; // Channels for left movement (M3 and M6)
      moveMotors(motors, 2, pwmFullThrottle);
      Serial.println("Turning Left...");
    } if (command == "forward") {
      int motors[] = {5, 4}; // Channels for forward movement (M6 and M5)
      moveMotors(motors, 2, pwmFullThrottle);
      Serial.println("Moving Forward...");
    } if (command == "backward") {
      int motors[] = {3, 2}; // Channels for backward movement (M4 and M3)
      moveMotors(motors, 2, pwmFullThrottle);
      Serial.println("Moving Backward...");
    } if (command == "all") {
      int motors[] = {0, 1, 2, 3, 4, 5}; // All channels for all motors
      moveMotors(motors, numMotors, pwmFullThrottle);
      Serial.println("Rotating All Motors...");
    } if (command == "stop") {
      stopAllMotors(); // Stop all motors
      Serial.println("Stopping All Motors...");
    } else {
      Serial.println("Invalid command. Use up, right, left, forward, backward, all, or stop.");
    }
  }
}
