import socket
import time
import serial

# Define the IP address and port to listen on
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 8080       # Port to listen on

# Set up serial connection to Arduino
SERIAL_PORT = '/dev/serial0'  # Change this if needed (e.g., /dev/ttyUSB0 if using USB)
BAUD_RATE = 9600

# Initialize serial connection
try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for the connection to initialize
    print("Serial connection established with Arduino.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# Define a time window for debouncing (e.g., 0.5 seconds)
DEBOUNCE_TIME = 0.5
last_sent_time = 0

def handle_command(command):
    """Send command to Arduino and log it."""
    global last_sent_time
    current_time = time.time()

    # Only send the command if enough time has passed since the last one
    if current_time - last_sent_time > DEBOUNCE_TIME:
        if arduino.is_open:
            arduino.write(command.encode())
            arduino.flush()  # Flush the output buffer
            last_sent_time = current_time  # Update the last sent time
            print(f"Command sent to Arduino: {command}")
        else:
            print("Serial connection to Arduino is closed.")
    else:
        print(f"Command '{command}' ignored due to debounce.")

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            try:
                while True:
                    data = conn.recv(1024)  # Buffer size of 1024 bytes
                    if not data:
                        print("No data received; closing connection.")
                        break
                    
                    # Decode command and handle it
                    command = data.decode('utf-8').strip()
                    print(f"Received command: {command}")
                    handle_command(command)

            except (ConnectionResetError, BrokenPipeError):
                print("Client disconnected unexpectedly.")
            except Exception as e:
                print(f"Error during connection handling: {e}")

            finally:
                conn.close()
                print("Connection closed.")

# Ensure serial port is closed when the program ends
if arduino.is_open:
    arduino.close()
    print("Serial connection to Arduino closed.")
