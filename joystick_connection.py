import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QGridLayout
from PyQt6.QtCore import Qt, QTimer
import pygame

class PrototypeSoftware(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle('Prototype Software For Hydra')
        self.resize(1200, 800)

        # Main layout of the window
        main_layout = QVBoxLayout()

        # Add a heading
        heading = QLabel("Prototype Software For Hydra", self)
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(heading)

        # Horizontal line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        main_layout.addSpacing(20)
        horizontal_section = QHBoxLayout()

        # Left section (3D image)
        left_section = QVBoxLayout()
        label_3d_image = QLabel("Video Captured From Raspberry Pi", self)
        label_3d_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_3d_image.setStyleSheet("border: 1px solid black;")
        label_3d_image.setFixedSize(500, 400)
        left_section.addWidget(label_3d_image)

        # # Right section (Camera feed)
        # right_section = QVBoxLayout()
        # label_camera = QLabel("3D Image Of The Video We Got", self)
        # label_camera.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # label_camera.setStyleSheet("border: 1px solid black;")
        # label_camera.setFixedSize(500, 400)
        # right_section.addWidget(label_camera)

        horizontal_section.addLayout(left_section)
        # horizontal_section.addLayout(right_section)
        main_layout.addLayout(horizontal_section)

        main_layout.addSpacing(20)
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line2)
        main_layout.addSpacing(20)

        # Controls sections
        controls_section = QHBoxLayout()

        # Robotics Arm Controls
        robotics_arm_section = QVBoxLayout()
        robotics_arm_layout = QGridLayout()

        robotics_arm_label = QLabel("Robotics Arm Controls", self)
        robotics_arm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create joystick buttons as instance attributes
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

        thruster_label = QLabel("Thrusters Control", self)
        thruster_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create thruster buttons as instance attributes
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

        # Grip Button
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

        # Initialize Pygame Joystick
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick connected: {self.joystick.get_name()}")
        else:
            self.joystick = None
            print("No joystick detected")

        # Timer to poll joystick
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.poll_joystick)
        self.timer.start(100)  # Poll every 100ms

    def poll_joystick(self):
        if self.joystick:
            pygame.event.pump()  # Process events

            # Get joystick axes and buttons
            axes = [self.joystick.get_axis(i) for i in range(self.joystick.get_numaxes())]
            buttons = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]

            # Log buttons and axes for debugging
            print(f"Axes: {axes}")
            print(f"Buttons: {buttons}")

            # Example binding for axis and button control
            if buttons[0]:  # Button 0 pressed
                print("Button A pressed: Arm Moving Down")
                self.thruster_down.setStyleSheet("background-color: yellow")
            else:
                self.thruster_down.setStyleSheet("")

            if buttons[1]:  # Button 1 pressed
                print("Button B pressed: Arm Moving Right")
                self.thruster_right.setStyleSheet("background-color: yellow")
            else:
                self.thruster_right.setStyleSheet("")

            if buttons[4]:  # Button 1 pressed
                print("Button Y pressed: Arm Moving Arm Moving Up")
                self.thruster_up.setStyleSheet("background-color: yellow")
            else:
                self.thruster_up.setStyleSheet("")

            if buttons[3]:  # Button 1 pressed
                print("Button X pressed: Arm Moving Left")
                self.thruster_left.setStyleSheet("background-color: yellow")
            else:
                self.thruster_left.setStyleSheet("")

            # Start Motors

            if buttons[10]: 
                print("Starting...")          
            else:
               pass

            # Stop all motors

            if buttons[11]: 
                print("Stopping...")          
            else:
               pass

            # Start all thrusters

            if buttons[8] and buttons[9]:
                print("Rotating all thrusters")
            else:
                pass




        # Axis-based control for Up/Down (axis 1) and Left/Right (axis 0)
        if axes[1] < -0.5:  # Move Up if axis 1 is less than -0.5
            print("Axis moved: Moving Up")
            self.joystick_up.setStyleSheet("background-color: yellow")
        elif axes[1] > 0.5:  # Move Down if axis 1 is greater than 0.5
            print("Axis moved: Moving Down")
            self.joystick_down.setStyleSheet("background-color: yellow")
        else:
            self.joystick_up.setStyleSheet("")
            self.joystick_down.setStyleSheet("")

        if axes[0] < -0.5:  # Move Left if axis 0 is less than -0.5
            print("Axis moved: Moving Left")
            self.joystick_left.setStyleSheet("background-color: yellow")
        elif axes[0] > 0.5:  # Move Right if axis 0 is greater than 0.5
            print("Axis moved: Moving Right")
            self.joystick_right.setStyleSheet("background-color: yellow")
        else:
            self.joystick_left.setStyleSheet("")
            self.joystick_right.setStyleSheet("")

        # Grip Control
        if buttons[6] and buttons[7]:
            print("Yo Griped!")
            self.grip_button.setStyleSheet("background-color: yellow")
        else:
            self.grip_button.setStyleSheet("")




# Main function to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of the window
    window = PrototypeSoftware()
    window.show()

    # Execute the app
    sys.exit(app.exec())