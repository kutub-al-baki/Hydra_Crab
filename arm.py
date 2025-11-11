import smbus
import time

# PCA9685 Default I2C address
PCA9685_ADDRESS = 0x40
# Registers
MODE1 = 0x00
PRESCALE = 0xFE
LED0_ON_L = 0x06

# Servo Settings for continuous servo
SERVO_NEUTRAL = 307  # Neutral position (stopped) ~1.5ms pulse
SERVO_OPEN = 500      # Open gripper (Clockwise rotation)
SERVO_CLOSE = 150     # Close gripper (Counterclockwise rotation)
SERVO_CHANNEL = 1     # Channel where the servo is connected

# Initialize I2C bus
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

def set_pwm(channel, on, off):
    """Sends PWM signal to PCA9685 for the given channel."""
    bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L + 4 * channel, on & 0xFF)
    bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L + 4 * channel + 1, on >> 8)
    bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L + 4 * channel + 2, off & 0xFF)
    bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L + 4 * channel + 3, off >> 8)

def set_pwm_freq(freq):
    """Sets the frequency of the PWM signal (typically 50Hz for servos)."""
    prescale_val = int(25000000.0 / (4096 * freq) - 1)
    old_mode = bus.read_byte_data(PCA9685_ADDRESS, MODE1)
    new_mode = (old_mode & 0x7F) | 0x10  # Sleep mode
    bus.write_byte_data(PCA9685_ADDRESS, MODE1, new_mode)
    bus.write_byte_data(PCA9685_ADDRESS, PRESCALE, prescale_val)
    bus.write_byte_data(PCA9685_ADDRESS, MODE1, old_mode)
    time.sleep(0.005)
    bus.write_byte_data(PCA9685_ADDRESS, MODE1, old_mode | 0x80)

def move_servo(command):
    """Moves the gripper based on the command."""
    if command == "open":
        print("Opening gripper...")
        set_pwm(SERVO_CHANNEL, 0, SERVO_OPEN)  # Open the gripper (rotate clockwise)
        time.sleep(2)  # Allow the gripper to open
        set_pwm(SERVO_CHANNEL, 0, SERVO_NEUTRAL)  # Stop the gripper (neutral)
    elif command == "close":
        print("Closing gripper...")
        set_pwm(SERVO_CHANNEL, 0, SERVO_CLOSE)  # Close the gripper (rotate counterclockwise)
        time.sleep(2)  # Allow the gripper to close
        set_pwm(SERVO_CHANNEL, 0, SERVO_NEUTRAL)  # Stop the gripper (neutral)
    elif command == "stop":
        print("Stopping gripper...")
        set_pwm(SERVO_CHANNEL, 0, SERVO_NEUTRAL)  # Immediate stop

def main():
    set_pwm_freq(50)  # Set frequency to 50Hz for servo
    print("Commands: 'open', 'close', 'stop', 'exit'")

    while True:
        command = input("Command: ").strip().lower()
        if command in ["open", "close", "stop"]:
            move_servo(command)
        elif command == "exit":
            break
        else:
            print("Invalid command. Use 'open', 'close', 'stop'.")

if __name__ == "__main__":
    main()
