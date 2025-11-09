import RPi.GPIO as GPIO
import time

# Motor GPIO definitions
motors = {
    "1": {"rpwm": 17, "lpwm": 27},
    "2": {"rpwm": 22, "lpwm": 23},
    "3": {"rpwm": 5,  "lpwm": 6},
    "4": {"rpwm": 13, "lpwm": 19},
}

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup all pins
for motor in motors.values():
    GPIO.setup(motor["rpwm"], GPIO.OUT)
    GPIO.setup(motor["lpwm"], GPIO.OUT)

def rotate_clockwise(motor_id):
    m = motors[motor_id]
    GPIO.output(m["rpwm"], GPIO.HIGH)
    GPIO.output(m["lpwm"], GPIO.LOW)

def rotate_anticlockwise(motor_id):
    m = motors[motor_id]
    GPIO.output(m["rpwm"], GPIO.LOW)
    GPIO.output(m["lpwm"], GPIO.HIGH)

def stop_motor(motor_id):
    m = motors[motor_id]
    GPIO.output(m["rpwm"], GPIO.LOW)
    GPIO.output(m["lpwm"], GPIO.LOW)

try:
    while True:
        cmd = input("Enter command (e.g., 1c / 2ac / 3stop): ").strip()
        if len(cmd) >= 2:
            motor_id = cmd[0]
            action = cmd[1:]

            if motor_id not in motors:
                print("Invalid motor ID. Use 1 to 4.")
                continue

            if action == "c":
                rotate_clockwise(motor_id)
                print(f"Motor {motor_id} rotating clockwise.")
            elif action == "ac":
                rotate_anticlockwise(motor_id)
                print(f"Motor {motor_id} rotating anticlockwise.")
            elif action == "stop":
                stop_motor(motor_id)
                print(f"Motor {motor_id} stopped.")
            else:
                print("Invalid command. Use c / ac / stop.")

except KeyboardInterrupt:
    GPIO.cleanup()
