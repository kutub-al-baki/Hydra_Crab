//#include <Wire.h>
//#include <Adafruit_PWMServoDriver.h>
//
//// Initialize PCA9685 driver
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
//
//const int motorChannel = 0;       // Motor connected to channel 0
//const int pwmFrequency = 50;      // Frequency for ESC (50 Hz)
//const int pwmFullThrottle = 410; // Full forward throttle (2000 µs)
//const int pwmNeutral = 307;      // Neutral throttle (1500 µs)
//const int pwmStop = 205;         // Full reverse throttle (1000 µs)
//
//void setup() {
//  Serial.begin(9600);
//  pwm.begin();
//  pwm.setPWMFreq(pwmFrequency);
//  delay(10);
//
//  Serial.println("Calibrating ESC...");
//
//  // Step 1: Full throttle to enter calibration mode
//  pwm.setPWM(motorChannel, 0, pwmFullThrottle);
//  Serial.println("Sending Full Throttle...");
//  delay(5000);  // Hold full throttle for 5 seconds
//
//  // Step 2: Neutral throttle to set throttle range
//  pwm.setPWM(motorChannel, 0, pwmNeutral);
//  Serial.println("Setting Neutral Throttle...");
//  delay(3000);  // Hold neutral for 3 seconds
//
//  Serial.println("ESC Calibration Completed.");
//  delay(2000);
//}
//
//void loop() {
//  // Step 3: Test backward movement
//  Serial.println("Testing Backward...");
//  pwm.setPWM(motorChannel, 0, pwmStop);1
//  delay(3000);
//
//  // Step 4: Test forward movement
//  Serial.println("Testing Forward...");
//  pwm.setPWM(motorChannel, 0, pwmFullThrottle);
//  delay(3000);
//
//  // Return to neutral
//  Serial.println("Returning to Neutral...");
//  pwm.setPWM(motorChannel, 0, pwmNeutral);
//  delay(2000);
//}

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

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(pwmFrequency);
  delay(10);

  Serial.println("Calibrating ESCs...");

  // Step 1: Full throttle to enter calibration mode for all motors
  for (int motorChannel = 0; motorChannel < numMotors; motorChannel++) {
    pwm.setPWM(motorChannel, 0, pwmFullThrottle);
  }
  Serial.println("Sending Full Throttle...");
  delay(5000); // Hold full throttle for 5 seconds

  // Step 2: Neutral throttle to set throttle range for all motors
  for (int motorChannel = 0; motorChannel < numMotors; motorChannel++) {
    pwm.setPWM(motorChannel, 0, pwmNeutral);
  }
  Serial.println("Setting Neutral Throttle...");
  delay(3000); // Hold neutral for 3 seconds

  Serial.println("ESC Calibration Completed.");
  delay(2000);
}

void loop() {
  Serial.println("Testing all motors...");

  // Step 1: Test backward movement for all motors
  for (int motorChannel = 0; motorChannel < numMotors; motorChannel++) {
    pwm.setPWM(motorChannel, 0, pwmStop);
  }
  Serial.println("Testing Backward...");
  delay(3000);

  // Step 2: Test forward movement for all motors
  for (int motorChannel = 0; motorChannel < numMotors; motorChannel++) {
    pwm.setPWM(motorChannel, 0, pwmFullThrottle);
  }
  Serial.println("Testing Forward...");
  delay(3000);

  // Step 3: Return to neutral for all motors
  for (int motorChannel = 0; motorChannel < numMotors; motorChannel++) {
    pwm.setPWM(motorChannel, 0, pwmNeutral);
  }
  Serial.println("Returning to Neutral...");
  delay(2000);

  Serial.println("All motors tested. Restarting loop...");
  delay(5000); // Pause before restarting the loop
}
