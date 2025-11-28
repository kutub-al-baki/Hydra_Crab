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

// List of valid commands
const String validCommands[] = {"up", "right", "left", "forward", "backward", "all", "stop", "start"};
String previousCommand = "";

unsigned long lastCommandTime = 0; // Track the last time a command was received
const unsigned long commandTimeout = 300; // Timeout period in milliseconds

// Function to validate commands
bool isValidCommand(String command) {
  for (String valid : validCommands) {
    if (command == valid) {
      return true;
    }
  }
  return false;
}

// Function to reduce repeated commands like "forwardforward" to "forward"
String reduceRepeatedCommand(String command) {
  for (String valid : validCommands) {
    if (command.indexOf(valid + valid) != -1) {
      // Replace all instances of the valid command repeated
      int repeatCount = command.length() / valid.length();
      return valid;  // Return only the first valid command
    }
  }
  return command; // Return the command as is if no repetition is found
}

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
  // Check if there is data available in the Serial buffer
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n'); // Read the command
    command.trim(); // Remove any leading/trailing whitespace

    // Reduce the command to a valid single input
    command = reduceRepeatedCommand(command);

    // Check if the command is valid and is not the same as the previous command
    if (isValidCommand(command)) {
      
      lastCommandTime = millis(); // Update the last command time

      Serial.print("First Last Command Time:");
      Serial.print(lastCommandTime);

      // Stop all motors before executing a new command
      stopAllMotors();

      // Process the command
      if (command == "up") {
        int motors[] = {0, 4}; // Channels for upward movement
        moveMotors(motors, 2, pwmFullThrottle);
      } else if (command == "right") {
        int motors[] = {2, 5}; // Channels for right movement
        moveMotors(motors, 2, pwmFullThrottle);
      } else if (command == "left") {
        int motors[] = {1, 3}; // Channels for left movement
        moveMotors(motors, 2, pwmFullThrottle);
      } else if (command == "forward") {
        int motors[] = {3, 5}; // Channels for forward movement
        moveMotors(motors, 2, pwmFullThrottle);
      } else if (command == "backward") {
        int motors[] = {1, 2}; // Channels for backward movement
        moveMotors(motors, 2, pwmFullThrottle);
      } else if (command == "all") {
        int motors[] = {0, 1, 2, 3, 4, 5}; // All motors
        moveMotors(motors, numMotors, pwmFullThrottle);
      } else if (command == "stop") {
        stopAllMotors();
      } else if (command == "start") {
        calibrateESCs();
      }

      // Update the previous command
      previousCommand = command;

      // Small delay to avoid multiple rapid inputs
      delay(100); // Adjust as needed for smoother command processing
    }
    else {
      // Print an error message for invalid commands
      Serial.print("Invalid command: ");
      Serial.println(command);
    }
  }

   // Check for command timeout
  if (millis() - lastCommandTime > commandTimeout) {
    Serial.print("Second Last Command Time:");
    Serial.print(lastCommandTime);
    stopAllMotors(); // Stop motors if no command is received within the timeout period
  }
  
}
