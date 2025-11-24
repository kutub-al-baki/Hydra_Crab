libcamera-vid -t 0 --inline -n --width 1280 --height 720 --framerate 30 \
--codec h264 -o - | gst-launch-1.0 fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! \
udpsink host=192.168.184.27 port=5000
