
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QGridLayout
from PyQt6.QtCore import Qt
import cv2
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap


class CameraThread(QThread):
    update_frame = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) 
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Flip the frame to correct mirror effect
                frame = cv2.flip(frame, 1)

                frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.update_frame.emit(qt_image)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
        self.cap.release()

class PrototypeSoftware(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle('Prototype Software For Hydra')

        # Resize the window to make it larger
        self.resize(1200, 800)  # Set width to 1200px and height to 800px

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


        main_layout.addSpacing(20)  # Add 20 pixels of space after the line
        # Create two horizontal sections (left for 3D image, right for camera feed)
        horizontal_section = QHBoxLayout()

        # Left section (Video feed from Raspberry Pi)
        left_section = QVBoxLayout()
        self.label_3d_image = QLabel("Video Captured From Raspberry Pi", self)
        self.label_3d_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3d_image.setStyleSheet("border: 1px solid black;")
        self.label_3d_image.setFixedSize(640, 360)  # Adjusted size
        left_section.addWidget(self.label_3d_image)

        # Right section (Camera feed)
        right_section = QVBoxLayout()
        label_camera = QLabel("3D Image Of The Video We Got", self)
        label_camera.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_camera.setStyleSheet("border: 1px solid black;")
        label_camera.setFixedSize(640, 360)  # Adjusted size
        right_section.addWidget(label_camera)

        # Add both sections to the horizontal layout
        horizontal_section.addLayout(left_section)
        horizontal_section.addLayout(right_section)

        # Add the horizontal section to the main layout
        main_layout.addLayout(horizontal_section)
        main_layout.addSpacing(20)  # Add 20 pixels of space after the line

        # Add another horizontal line below the two sections
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line2)
        main_layout.addSpacing(20)  # Add 20 pixels of space after the line

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

        # Positioning buttons like a joystick
        robotics_arm_layout.addWidget(joystick_up, 0, 1)
        robotics_arm_layout.addWidget(joystick_left, 1, 0)
        robotics_arm_layout.addWidget(robotics_arm_label, 1,1)
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
        main_layout.addSpacing(30)  # Add 20 pixels of space after the line

        # Add a centered "Grip" button below the controls section
        grip_button_layout = QHBoxLayout()
        grip_button = QPushButton("Grip Open/Close", self)
        grip_button.setFixedSize(150, 50)  # Set button size
        grip_button_layout.addStretch(1)  # Add stretch to center the button
        grip_button_layout.addWidget(grip_button)
        grip_button_layout.addStretch(1)  # Add stretch to center the button
        main_layout.addLayout(grip_button_layout)

        # Add some blank space under the sections
        spacer = QLabel("", self)
        main_layout.addWidget(spacer)

        # Set the layout for the main window
        self.setLayout(main_layout)


        # Initialize the camera thread and connect to label
        self.camera_thread = CameraThread()
        self.camera_thread.update_frame.connect(self.update_video_frame)
        self.camera_thread.start()

    def update_video_frame(self, qt_image):
        self.label_3d_image.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        self.camera_thread.stop()
        event.accept()

# Main function to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of the window
    window = PrototypeSoftware()
    window.show()

    # Execute the app
    sys.exit(app.exec())
