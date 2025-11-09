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
   # cmd = f"libcamera-vid -t 0 -o - | gst-launch-1.0 fdsrc ! h264parse ! rtph264pay ! udpsink host=192.168.241.27 port=5000"
    cmd = f"libcamera-vid -t 0 --inline -o - | ffmpeg -i - -c:v copy -f mpegts udp://192.168.241.27:5000"
    os.system(cmd)

# Capture video and stream for different cameras
def main():
    print('Start testing the camera A')
    i2c = "i2cset -y 1 0x70 0x00 0x04"
    os.system(i2c)
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
    stream(1)  # Stream camera A

    print('Start testing the camera B') 
    i2c = "i2cset -y 1 0x70 0x00 0x05"
    os.system(i2c)
    gp.output(7, True)
    gp.output(11, False)
    gp.output(12, True)
    stream(2)  # Stream camera B

    print('Start testing the camera C')
    i2c = "i2cset -y 1 0x70 0x00 0x06"
    os.system(i2c)
    gp.output(7, False)
    gp.output(11, True)
    gp.output(12, False)
    stream(3)  # Stream camera C

    print('Start testing the camera D')
    i2c = "i2cset -y 1 0x70 0x00 0x07"
    os.system(i2c)
    gp.output(7, True)
    gp.output(11, True)
    gp.output(12, False)
    stream(4)  # Stream camera D

if __name__ == "__main__":
    main()

    # Reset GPIO pins after streaming
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
