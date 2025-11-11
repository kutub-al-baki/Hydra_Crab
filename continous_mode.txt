#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

const int numMotors = 6;         
const int pwmFrequency = 50;    
const int pwmFullThrottle = 410; 
const int pwmNeutral = 307;      
const int pwmStop = 205;         

const String validCommands[] = {"up", "right", "left", "forward", "backward", "all", "stop", "calibrate"};
unsigned long lastCommandTime = 0; 
const unsigned long commandTimeout = 500; 
bool isMoving = false;  
String previousCommand = "";

bool isValidCommand(String command) {
  for (String valid : validCommands) {
    if (command == valid) return true;
  }
  return false;
}

void moveMotors(const int motors[], int numMotors, int pwmValue) {
  for (int i = 0; i < numMotors; i++) {
    pwm.setPWM(motors[i], 0, pwmValue);
  }
}

void stopAllMotors() {
  for (int motorChannel = 0; motorChannel < numMotors; motorChannel++) {
    pwm.setPWM(motorChannel, 0, pwmStop);
  }
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


void calibrateESCs() {
  Serial.println("Calibrating ESCs...");
  
  for (int motorChannel = 0; motorChannel < numMotors; motorChannel++) {
    pwm.setPWM(motorChannel, 0, pwmFullThrottle);
  }
  delay(10); 

  for (int motorChannel = 0; motorChannel < numMotors; motorChannel++) {
    pwm.setPWM(motorChannel, 0, pwmNeutral);
  }
  delay(10); 

  stopAllMotors();
  Serial.println("ESC Calibration Completed.");
}

void setup() {
  
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(pwmFrequency);
  delay(10);

  calibrateESCs();
  stopAllMotors();
}

void loop() {
  while (Serial.available()>0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

      // Reduce the command to a valid single input
    command = reduceRepeatedCommand(command);

    if (isValidCommand(command)) {
      lastCommandTime = millis();
      isMoving = true;
      Serial.print("First last command line: ");
      Serial.print(lastCommandTime);

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
      } else if (command == "calibrate") {
        calibrateESCs();
      }

      // Update the previous command
      previousCommand = command;
    }
  }

  if (millis() - lastCommandTime > commandTimeout && isMoving) {
    stopAllMotors();
    isMoving = false;
    Serial.flush();
    Serial.print(" Last Command Time: ");
    Serial.print(lastCommandTime);
  }
}
