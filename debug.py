import sys
import socket
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt

class MAVProxyClient(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.active_commands = []  # Store active commands

    def initUI(self):
        self.setWindowTitle("Chungi pungi")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()
        self.label = QLabel("Press keys to send RC commands:\n"
                            "W\n"
                            "A\n"
                            "D\n"
                            "S\n"
                            "↑\n"
                            "↓\n"
                            "Q (reset)")
        layout.addWidget(self.label)
        self.setLayout(layout)

    def send_command(self, command):
        """Send command to Raspberry Pi MAVProxy server"""
        HOST = "192.168.2.3"  # Change if necessary
        PORT = 7000

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, PORT))
                client_socket.sendall(command.encode())
                print(f"Sent: {command}")
        except Exception as e:
            print(f"Error: {e}")

    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard input"""
        key_map = {
            Qt.Key.Key_W: "rc 1 1000",
            Qt.Key.Key_A: "rc 2 1000",
            Qt.Key.Key_S: "rc 1 2000",
            Qt.Key.Key_D: "rc 2 2000",
            Qt.Key.Key_Up: "rc 3 2000",
            Qt.Key.Key_Up: "rc 3 2000",
            Qt.Key.Key_Down: "rc 3 1000",
        }

        if event.key() in key_map:
            command = key_map[event.key()]
            if command not in self.active_commands:
                self.active_commands.append(command)  # Store active command
            self.send_command(command)

        elif event.key() == Qt.Key.Key_Q:  # Reset command
            self.reset_commands()

    def reset_commands(self):
        reset_map = {
            "rc 1 1000": "rc 1 1500",
            "rc 2 1000": "rc 2 1500",
            "rc 2 2000": "rc 2 1500",
            "rc 3 2000": "rc 3 1500",
            "rc 3 1000": "rc 3 1500",
        }

        for command in reversed(self.active_commands):
            reset_command = reset_map.get(command)
            if reset_command:
                self.send_command(reset_command)

        self.active_commands.clear()  # Clear all active commands after reset

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MAVProxyClient()
    window.show()
    sys.exit(app.exec())
