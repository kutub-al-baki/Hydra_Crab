import RPi.GPIO as gp
import os

gp.setwarnings(False)
gp.setmode(gp.BOARD)

# Set up GPIO pins for camera selection
gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

# Stream video to laptop over UDP
def stream(cam):
    # Command to stream video from the selected camera
    cmd = f"libcamera-vid -t 0 --inline -o - | ffmpeg -i - -c:v copy -f mpegts udp://192.168.241.27:5000"
    os.system(cmd)

# Set GPIO for each camera
def setup_camera(cam):
    if cam == 'A':
        i2c = "i2cset -y 1 0x70 0x00 0x04"
        os.system(i2c)
        gp.output(7, False)
        gp.output(11, False)
        gp.output(12, True)
    elif cam == 'B':
        i2c = "i2cset -y 1 0x70 0x00 0x05"
        os.system(i2c)
        gp.output(7, True)
        gp.output(11, False)
        gp.output(12, True)
    elif cam == 'C':
        i2c = "i2cset -y 1 0x70 0x00 0x06"
        os.system(i2c)
        gp.output(7, False)
        gp.output(11, True)
        gp.output(12, False)
    elif cam == 'D':
        i2c = "i2cset -y 1 0x70 0x00 0x07"
        os.system(i2c)
        gp.output(7, True)
        gp.output(11, True)
        gp.output(12, False)
    else:
        print("Invalid camera selection. Please choose A, B, C, or D.")
        return False
    return True

def main():
    print("Select a camera to stream (A, B, C, or D):")
    selected_cam = input().strip().upper()  # Take user input

    # Validate the user input and stream video from the selected camera
    if setup_camera(selected_cam):
        print(f'Starting to stream Camera {selected_cam}')
        stream(selected_cam)  # Stream the selected camera
    else:
        print("Camera selection failed. Exiting.")

if __name__ == "__main__":
    main()

    # Reset GPIO pins after streaming
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
orchi@orchi:~ $ 