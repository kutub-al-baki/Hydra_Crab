import smbus
import time

# PCA9685 I2C Address
PCA9685_ADDR = 0x40
MODE1 = 0x00
PRESCALE = 0xFE
LED0_ON_L = 0x06  # Base address for channel 0 (Change for other channels)

# Servo PWM Range (Adjust these based on your servo's specs)
SERVO_MIN = 130  # PWM for backward rotation
SERVO_MAX = 670  # PWM for forward rotation
SERVO_STOP = 400  # PWM for stopping (center position)

# Initialize I2C bus
bus = smbus.SMBus(1)

# Function to set PWM for a given channel
def set_pwm(channel, on, off):
    reg = LED0_ON_L + 4 * channel
    bus.write_byte_data(PCA9685_ADDR, reg, on & 0xFF)
    bus.write_byte_data(PCA9685_ADDR, reg + 1, on >> 8)
    bus.write_byte_data(PCA9685_ADDR, reg + 2, off & 0xFF)
    bus.write_byte_data(PCA9685_ADDR, reg + 3, off >> 8)

# Set PCA9685 Frequency to 50Hz (standard servo freq)
def init_pca9685():
    bus.write_byte_data(PCA9685_ADDR, MODE1, 0x10)  # Sleep
    prescale = int(round(25000000.0 / (4096 * 50)) - 1)
    bus.write_byte_data(PCA9685_ADDR, PRESCALE, prescale)
    bus.write_byte_data(PCA9685_ADDR, MODE1, 0x80)  # Restart

# Initialize PCA9685
init_pca9685()

# Move servo on Channel 1 (adjust the channel as needed)
channel = 1  # For Channel 1

# Function to rotate the servo based on key input
def handle_key_input():
    while True:
        key = input("Press 'f' to move forward, 'b' to move backward, 'q' to stop: ").lower()
        if key == 'f':  # Move forward
            print("Moving Forward...")
            set_pwm(channel, 0, SERVO_MAX)  # Move to forward position
        elif key == 'b':  # Move backward
            print("Moving Backward...")
            set_pwm(channel, 0, SERVO_MIN)  # Move to backward position
        elif key == 'q':  # Stop
            print("Stopping...")
            set_pwm(channel, 0, SERVO_STOP)  # Stop at center (90 degrees)
        else:
            print("Invalid key pressed! Press 'f', 'b', or 'q'.")

# Start the key input loop
handle_key_input()
