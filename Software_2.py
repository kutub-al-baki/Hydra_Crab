import sys
import pygame
import cv2
import socket
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QGridLayout
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
import torch  # Import torch for YOLOv5

# class VideoThread(QThread):
#     update_frame = pyqtSignal(QImage)

#     def __init__(self, stream_url):
#         super().__init__()
#         self.stream_url = stream_url
#         self.running = False
#         self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Load YOLOv5 model

#     def run(self):
#         self.running = True
#         cap = cv2.VideoCapture(self.stream_url)

#         while self.running:
#             ret, frame = cap.read()
#             if ret:
#                 # Perform object detection
#                 results = self.model(frame)  # Run YOLOv5 inference
#                 # Render results on the frame
#                 frame = results.render()[0]  # Render the frame with detections

#                 rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 height, width, channel = rgb_image.shape
#                 bytes_per_line = 3 * width
#                 qt_image = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
#                 resized_image = qt_image.scaled(500, 400, Qt.AspectRatioMode.KeepAspectRatio)
#                 self.update_frame.emit(resized_image)

#         cap.release()

#     def stop(self):
#         self.running = False
#         self.quit()
#         self.wait()

class PrototypeSoftware(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Hydra Software 1')
        self.resize(1200, 800)

        main_layout = QVBoxLayout()
        heading = QLabel("Hydra Software 2", self)
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(heading)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        main_layout.addSpacing(20)
        horizontal_section = QHBoxLayout()

        # Left section (Camera feed)
        left_section = QVBoxLayout()
        self.label_3d_image = QLabel("Video captured from Raspberry Pi", self)
        self.label_3d_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3d_image.setStyleSheet("border: 1px solid black;")
        self.label_3d_image.setFixedSize(500, 400)
        left_section.addWidget(self.label_3d_image)

        horizontal_section.addLayout(left_section)
        main_layout.addLayout(horizontal_section)

        main_layout.addSpacing(20)
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line2)
        main_layout.addSpacing(20)

        controls_section = QHBoxLayout()

        # Robotics Arm Controls
        robotics_arm_section = QVBoxLayout()
        robotics_arm_layout = QGridLayout()

        robotics_arm_label = QLabel("Thruster PWM Control", self)
        robotics_arm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.joystick_up = QPushButton("Up", self)
        self.joystick_down = QPushButton("Down", self)
        self.joystick_left = QPushButton("Left", self)
        self.joystick_right = QPushButton("Right", self)

        robotics_arm_layout.addWidget(self.joystick_up, 0, 1)
        robotics_arm_layout.addWidget(self.joystick_left, 1, 0)
        robotics_arm_layout.addWidget(robotics_arm_label, 1, 1)
        robotics_arm_layout.addWidget(self.joystick_right, 1, 2)
        robotics_arm_layout.addWidget(self.joystick_down, 2, 1)

        robotics_arm_section.addLayout(robotics_arm_layout)

        # Thruster Controls
        thrusters_section = QVBoxLayout()
        thrusters_layout = QGridLayout()

        thruster_label = QLabel("Thrusters Fixed Control", self)
        thruster_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.thruster_up = QPushButton("Up", self)
        self.thruster_down = QPushButton("Down", self)
        self.thruster_left = QPushButton("Left", self)
        self.thruster_right = QPushButton("Right", self)

        thrusters_layout.addWidget(self.thruster_up, 0, 1)
        thrusters_layout.addWidget(self.thruster_left, 1, 0)
        thrusters_layout.addWidget(thruster_label, 1, 1)
        thrusters_layout.addWidget(self.thruster_right, 1, 2)
        thrusters_layout.addWidget(self.thruster_down, 2, 1)

        thrusters_section.addLayout(thrusters_layout)

        controls_section.addLayout(robotics_arm_section)
        controls_section.addLayout(thrusters_section)
        main_layout.addLayout(controls_section)

        grip_button_layout = QHBoxLayout()
        self.grip_button = QPushButton("Grip Open/Close", self)
        self.grip_button.setFixedSize(150, 50)
        grip_button_layout.addStretch(1)
        grip_button_layout.addWidget(self.grip_button)
        grip_button_layout.addStretch(1)
        main_layout.addLayout(grip_button_layout)

        spacer = QLabel("", self)
        main_layout.addWidget(spacer)
        self.setLayout(main_layout)

        #Initialize Pygame
        #Initialize Joystick
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick connected: {self.joystick.get_name()}")
        else:
            self.joystick = None
            print("No joystick detected")

        # self.video_thread = None
        # self.video_url = "http://192.168.131.173:8000"

         # Initialize socket connection to Raspberry Pi
        self.raspberry_pi_ip = '10.42.0.126'  # Replace with your Raspberry Pi's IP address
        self.raspberry_pi_port = 8080  # Ensure this matches the port in the Raspberry Pi code
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_pi()

        # Timer to check joystick events
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_joystick)
        self.timer.start(100)

    def connect_to_pi(self):
        try:
            self.socket.connect((self.raspberry_pi_ip, self.raspberry_pi_port))
            print("Connected to Raspberry Pi")
        except Exception as e:
            print(f"Connection error: {e}")

    # def start_video_stream(self):
    #     if not self.video_thread:
    #         self.video_thread = VideoThread(self.video_url)
    #         self.video_thread.update_frame.connect(self.display_video_stream)
    #         self.video_thread.start()

    # def stop_video_stream(self):
    #     if self.video_thread:
    #         self.video_thread.stop()
    #         self.video_thread = None

    # def display_video_stream(self, qt_image):
    #     self.label_3d_image.setPixmap(QPixmap.fromImage(qt_image))

    def check_joystick(self):
        if self.joystick:
            pygame.event.pump()
            # Get joystick axes and buttons
            axes = [self.joystick.get_axis(i) for i in range(self.joystick.get_numaxes())]
            buttons = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]

            # Log buttons and axes for debugging
            print(f"Axes: {axes}")
            print(f"Buttons: {buttons}")

            # Axis-based control for Up/Down (axis 1) and Left/Right (axis 0)
            if axes[1] < -0.5:  # Move Up if axis 1 is less than -0.5
                print("Axis moved: Moving Up")
                self.send_command('forward')
                self.joystick_up.setStyleSheet("background-color: yellow")
                QTimer.singleShot(100, lambda: self.joystick_right.setStyleSheet(""))   

                
            elif axes[1] > 0.5:  # Move Down if axis 1 is greater than 0.5
                print("Axis moved: Moving Down")
                self.send_command('backward')
                self.joystick_down.setStyleSheet("background-color: yellow")
                QTimer.singleShot(100, lambda: self.joystick_right.setStyleSheet(""))   

            else:
                self.joystick_up.setStyleSheet("")
                self.joystick_down.setStyleSheet("")

            if axes[0] < -0.5:  # Move Left if axis 0 is less than -0.5
                print("Axis moved: Moving Left")
                self.send_command('c')
                self.joystick_right.setStyleSheet("background-color: yellow")
                QTimer.singleShot(100, lambda: self.joystick_right.setStyleSheet(""))   

            elif axes[0] > 0.5:
                print("Axis moved: Moving Right")
                self.send_command('d')
                self.joystick_right.setStyleSheet("background-color: yellow")
                QTimer.singleShot(100, lambda: self.joystick_right.setStyleSheet(""))   

            else:
                self.joystick_left.setStyleSheet("")
                self.joystick_right.setStyleSheet("")

            # Button control
            if buttons[0]: 
                print("Button A pressed: Arm Moving Down")
                self.thruster_down.setStyleSheet("background-color: yellow")
                self.send_command('down')
            else:
                self.thruster_down.setStyleSheet("")

            if buttons[1]:  
                print("Button B pressed: Arm Moving Right")
                self.thruster_right.setStyleSheet("background-color: yellow")
                self.send_command('right')
            else:
                self.thruster_right.setStyleSheet("")

            if buttons[4]: 
                print("Button Y pressed: Arm Moving Arm Moving Up")
                self.thruster_up.setStyleSheet("background-color: yellow")
                self.send_command('up')
            else:
                self.thruster_up.setStyleSheet("")

            if buttons[3]: 
                print("Button X pressed: Arm Moving Left")
                self.thruster_left.setStyleSheet("background-color: yellow")
                self.send_command('left')
            else:
                self.thruster_left.setStyleSheet("")

            # Start Motors
            if buttons[10]: 
                print("Starting...")
                self.send_command('start')          
            else:
               pass

            # Stop all motors
            if buttons[11]: 
                print("Stopping...")
                self.send_command('stop')          
            else:
               pass

            # Start all thrusters
            if buttons[8] and buttons[9]:
                print("Rotating all thrusters")
                self.send_command('q')
            else:
                pass

    def send_command(self, command):
        try:
            self.socket.sendall(command.encode('utf-8'))
            print(f"Command sent: {command}")
        except Exception as e:
            print(f"Error sending command: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PrototypeSoftware()
    window.show()
    sys.exit(app.exec())
