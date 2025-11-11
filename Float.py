import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QGroupBox, QTableWidget, QTableWidgetItem, QGridLayout,
    QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MATE Float Dashboard")
        self.setGeometry(100, 100, 1920, 1080)
        self.setStyleSheet("background-color: #1e1e1e;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title and Start Button
        title_bar = QHBoxLayout()
        title_label = QLabel("MATE FLOAT DASHBOARD")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: orange;")
        title_bar.addWidget(title_label)

        start_button = QPushButton("START TELEMETRY")
        start_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #bbb;
                border: 1px solid #900;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #900;
                color: white;
            }
        """)
        title_bar.addStretch()
        title_bar.addWidget(start_button)
        main_layout.addLayout(title_bar)

        # Graph Area
        graph_layout = QHBoxLayout()

        # Pressure Graph Box
        pressure_box = self.create_graph_box("Live Pressure Graph")
        graph_layout.addWidget(pressure_box)

        # Depth Graph Box
        depth_box = self.create_graph_box("Live Depth Graph")
        graph_layout.addWidget(depth_box)

        # Status Box
        status_box = self.create_status_box()
        graph_layout.addWidget(status_box)

        main_layout.addLayout(graph_layout)

        # Table Area
        data_label = QLabel("Live Data From Sensors")
        data_label.setStyleSheet("color: #ccc; font-size: 16px;")
        main_layout.addWidget(data_label)

        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Team ID", "Time", "Depth", "Pressure"])
        table.setStyleSheet("""
            QTableWidget {
                background-color: #2b2b2b;
                color: #ccc;
                border: 1px solid #004050;
            }
            QHeaderView::section {
                background-color: #222;
                color: #aaa;
            }
        """)
        table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(table)

        self.setLayout(main_layout)

    def create_graph_box(self, title):
        group_box = QGroupBox(title)
        group_box.setStyleSheet("""
            QGroupBox {
                color: #aaa;
                border: 1px solid #004050;
                font-size: 14px;
            }
        """)
        layout = QVBoxLayout()
        graph_frame = QFrame()
        graph_frame.setFixedHeight(250)
        graph_frame.setStyleSheet("background-color: #111; border: 1px solid #555;")
        layout.addWidget(graph_frame)
        group_box.setLayout(layout)
        return group_box

    def create_status_box(self):
        status_group = QGroupBox("FLOAT COMMUNICATION STATUS")
        status_group.setStyleSheet("""
            QGroupBox {
                color: #aaa;
                border: 1px solid #004050;
                font-size: 10px;
            }
        """)
        status_layout = QVBoxLayout()

        connected_label = QLabel("CONNECTED")
        connected_label.setFont(QFont("Arial", 16))
        connected_label.setStyleSheet("color: orange;")
        connected_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ip_label = QLabel("IP ADDRESS: 192.168.2.3")
        ip_label.setStyleSheet("color: #999; font-size: 10px;")
        ip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        status_layout.addWidget(connected_label)
        status_layout.addWidget(ip_label)

        status_group.setLayout(status_layout)
        status_group.setFixedWidth(200)
        status_group.setFixedHeight(100)
        return status_group


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())
