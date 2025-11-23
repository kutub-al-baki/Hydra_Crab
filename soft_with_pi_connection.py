import sys
import socket
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QGridLayout
from PyQt6.QtCore import Qt

class PrototypeSoftware(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle('Prototype Software For Hydra')

        # Resize the window to make it larger
        self.resize(1200, 800)

        # Main layout of the window
        main_layout = QVBoxLayout()

        # Add a heading
        heading = QLabel("Prototype Software For Hydra", self)
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(heading)

        # Add a horizontal line under the heading
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        main_layout.addSpacing(20)

        # Create two horizontal sections (left for 3D image, right for camera feed)
        horizontal_section = QHBoxLayout()

        # Left section (3D image)
        left_section = QVBoxLayout()
        label_3d_image = QLabel("Video Captured From Raspberry Pi", self)
        label_3d_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_3d_image.setStyleSheet("border: 1px solid black;")
        label_3d_image.setFixedSize(500, 400)
        left_section.addWidget(label_3d_image)

        # Right section (Camera feed)
        right_section = QVBoxLayout()
        label_camera = QLabel("3D Image Of The Video We Got", self)
        label_camera.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_camera.setStyleSheet("border: 1px solid black;")
        label_camera.setFixedSize(500, 400)
        right_section.addWidget(label_camera)

        # Add both sections to the horizontal layout
        horizontal_section.addLayout(left_section)
        horizontal_section.addLayout(right_section)

        # Add the horizontal section to the main layout
        main_layout.addLayout(horizontal_section)
        main_layout.addSpacing(20)

        # Add another horizontal line below the two sections
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line2)
        main_layout.addSpacing(20)

        # Create two sections for the Robotics Arm and Thrusters controls
        controls_section = QHBoxLayout()

        # Left section (Robotics Arm Controls)
        robotics_arm_section = QVBoxLayout()
      
        # Create joystick-like buttons using QGridLayout for Robotics Arm Controls
        robotics_arm_layout = QGridLayout()

        # Add joystick buttons in a grid layout (Up, Down, Left, Right)
        robotics_arm_label = QLabel("Robotics Arm Controls", self)
        robotics_arm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        joystick_up = QPushButton("Up", self)
        joystick_down = QPushButton("Down", self)
        joystick_left = QPushButton("Left", self)
        joystick_right = QPushButton("Right", self)

        # Connect buttons to commands for controlling the Raspberry Pi
        joystick_up.clicked.connect(lambda: self.send_command('arm_up'))
        joystick_down.clicked.connect(lambda: self.send_command('arm_down'))
        joystick_left.clicked.connect(lambda: self.send_command('arm_left'))
        joystick_right.clicked.connect(lambda: self.send_command('arm_right'))

        # Positioning buttons like a joystick
        robotics_arm_layout.addWidget(joystick_up, 0, 1)
        robotics_arm_layout.addWidget(joystick_left, 1, 0)
        robotics_arm_layout.addWidget(robotics_arm_label, 1, 1)
        robotics_arm_layout.addWidget(joystick_right, 1, 2)
        robotics_arm_layout.addWidget(joystick_down, 2, 1)

        # Add the joystick layout to the arm section
        robotics_arm_section.addLayout(robotics_arm_layout)

        # Right section (Thruster Controls)
        thrusters_section = QVBoxLayout()

        # Create joystick-like buttons using QGridLayout for Thruster Controls
        thrusters_layout = QGridLayout()

        # Add joystick buttons in a grid layout (Up, Down, Left, Right)
        thruster_up = QPushButton("Up", self)
        thruster_down = QPushButton("Down", self)
        thruster_left = QPushButton("Left", self)
        thruster_right = QPushButton("Right", self)

        # Connect buttons to commands for controlling the Raspberry Pi
        thruster_up.clicked.connect(lambda: self.send_command('thruster_up'))
        thruster_down.clicked.connect(lambda: self.send_command('thruster_down'))
        thruster_left.clicked.connect(lambda: self.send_command('thruster_left'))
        thruster_right.clicked.connect(lambda: self.send_command('thruster_right'))

        # Positioning buttons like a joystick
        thruster_label = QLabel("Thrusters Control", self)
        thruster_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        thrusters_layout.addWidget(thruster_up, 0, 1)
        thrusters_layout.addWidget(thruster_left, 1, 0)
        thrusters_layout.addWidget(thruster_label, 1, 1)
        thrusters_layout.addWidget(thruster_right, 1, 2)
        thrusters_layout.addWidget(thruster_down, 2, 1)

        # Add the joystick layout to the thruster section
        thrusters_section.addLayout(thrusters_layout)

        # Add both control sections to the layout
        controls_section.addLayout(robotics_arm_section)
        controls_section.addLayout(thrusters_section)

        # Add the controls section to the main layout
        main_layout.addLayout(controls_section)
        main_layout.addSpacing(30)

        # Add a centered "Grip" button below the controls section
        grip_button_layout = QHBoxLayout()
        grip_button = QPushButton("Grip Open/Close", self)
        grip_button.setFixedSize(150, 50)
        grip_button.clicked.connect(lambda: self.send_command('grip_toggle'))  # Add grip button command
        grip_button_layout.addStretch(1)
        grip_button_layout.addWidget(grip_button)
        grip_button_layout.addStretch(1)
        main_layout.addLayout(grip_button_layout)

        # Add some blank space under the sections
        spacer = QLabel("", self)
        main_layout.addWidget(spacer)

        # Set the layout for the main window
        self.setLayout(main_layout)

    def send_command(self, command):
        """Send command to Raspberry Pi using sockets."""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('10.42.0.174', 8080))  # Replace 'raspberry_pi_ip' with actual IP
            client_socket.sendall(command.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Response: {response}")
            client_socket.close()
        except Exception as e:
            print(f"Error: {e}")

# Main function to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrototypeSoftware()
    window.show()
    sys.exit(app.exec())
