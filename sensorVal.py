import smbus
import time

# I2C bus 0 (used in your case)
bus = smbus.SMBus(0)

# BMP388 I2C address
BMP388_ADDR = 0x77

# Registers for BMP388
BMP388_TEMP_REG = 0x04
BMP388_PRESS_REG = 0x07
BMP388_ALT_REG = 0x08
BMP388_PWR_CTRL_REG = 0x1B  # Corrected the missing variable
BMP388_OSR_REG = 0x1C
BMP388_CONFIG_REG = 0x1F

# BMP388 conversion constants
TEMP_CONV_FACTOR = 16384.0
TEMP_OFFSET = 25.0  # Sensor calibration offset

# Initialize the sensor
def initialize_sensor():
    # Reset the sensor
    bus.write_byte_data(BMP388_ADDR, 0x1B, 0xB6)  # Soft reset
    time.sleep(0.5)

    # Enable pressure and temperature sensor
    bus.write_byte_data(BMP388_ADDR, 0x1B, 0x33)  # Normal mode (Temp & Pressure enabled)
    time.sleep(0.5)

    # Set oversampling and filtering
    bus.write_byte_data(BMP388_ADDR, 0x1C, 0x03)  # Temperature oversampling x2
    bus.write_byte_data(BMP388_ADDR, 0x1D, 0x03)  # Pressure oversampling x2
    bus.write_byte_data(BMP388_ADDR, 0x1F, 0x02)  # IIR filter setting
    time.sleep(0.5)

# Function to read raw I2C data
def read_data(register):
    return bus.read_i2c_block_data(BMP388_ADDR, register, 3)

# Function to read temperature
def read_temperature():
    temp_data = bus.read_i2c_block_data(BMP388_ADDR, BMP388_TEMP_REG, 2)
    raw_temp = (temp_data[1] << 8) | temp_data[0]  # Combine MSB and LSB

    # Convert to Celsius
    temperature = raw_temp / 256.0  # Datasheet formula

    print(f"Raw Temp Data: {raw_temp} | Converted Temp: {temperature:.2f} °C")
    return temperature

# Function to get pressure
def read_pressure():
    data = read_data(BMP388_PRESS_REG)
    pressure_raw = (data[0] | (data[1] << 8) | (data[2] << 16))
    pressure = pressure_raw / 256.0  # Adjust based on datasheet
    return pressure

# Function to get altitude
def read_altitude():
    data = read_data(BMP388_ALT_REG)
    altitude_raw = (data[0] | (data[1] << 8) | (data[2] << 16))
    altitude = altitude_raw / 100.0  # Adjust based on datasheet
    return altitude

def main():
    try:
        initialize_sensor()  # Initialize BMP388 sensor

        while True:
            # Read temperature, pressure, and altitude
            temperature = read_temperature()
            pressure = read_pressure()
            altitude = read_altitude()

            # Print the sensor data
            print(f"Temperature: {temperature:.2f} °C")
            print(f"Pressure: {pressure:.2f} Pa")
            print(f"Altitude: {altitude:.2f} m")

            time.sleep(1)  # Wait before reading again

    except KeyboardInterrupt:
        print("Program terminated.")

if __name__ == "__main__":
    main()
