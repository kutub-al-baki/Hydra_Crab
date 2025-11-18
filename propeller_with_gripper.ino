#include <Servo.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Function prototypes
void processCommand(char command);
void stopMotors();
void moveServo(int position);

// Servo constants
#define SERVOMIN  150  // Minimum pulse length out of 4096
#define SERVOMAX  600  // Maximum pulse length out of 4096

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
const int motor1LPWM = 6;
const int motor1RPWM = 3;
const int motor2LPWM = 5;
const int motor2RPWM = 9;

void setup() {
  Wire.begin();
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60); // Set PWM frequency for servos

  pinMode(motor1LPWM, OUTPUT);
  pinMode(motor1RPWM, OUTPUT);
  pinMode(motor2LPWM, OUTPUT);
  pinMode(motor2RPWM, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    Serial.flush();  // Clear buffer after reading the command
    if (command != '\n' && command != '\r') {
      // Stop motors
      digitalWrite(motor1RPWM, LOW);
      digitalWrite(motor1LPWM, LOW);
      digitalWrite(motor2RPWM, LOW);
      digitalWrite(motor2LPWM, LOW);
      
      // Handle motor commands
      switch (command) {
        case 'a':
          analogWrite(motor1RPWM, 50);
          analogWrite(motor2RPWM, 50);
          break;
        case 'b':
          analogWrite(motor1LPWM, 50);
          analogWrite(motor2LPWM, 50);
          break;
        case 'c':
          analogWrite(motor1RPWM, 30);
          analogWrite(motor2LPWM, 50);
          break;
        case 'd':
          analogWrite(motor1RPWM, 50);
          analogWrite(motor2LPWM, 30);
          break;
        case 'q':
          Serial.println("quit");
          stopMotors(); // Stop motors if 'q' is pressed
          break;
        case 'x': // Move servo to 100 degrees
          moveServo(100);
          break;
        case 'y': // Move servo back to 0 degrees
          moveServo(0);
          break;
        default:
          Serial.println("Invalid Command");
          break;
      }
    }
  }
}

// Function to move the servo to the desired position
void moveServo(int position) {
  int pulse = map(position, 0, 100, SERVOMIN, SERVOMAX);
  pwm.setPWM(0, 0, pulse); // Set the PWM signal for channel 0
  delay(15);               // Wait for the servo to reach the position
}

// Function to stop all motors
void stopMotors() {
  digitalWrite(motor1RPWM, LOW);
  digitalWrite(motor1LPWM, LOW);
  digitalWrite(motor2RPWM, LOW);
  digitalWrite(motor2LPWM, LOW);
}
