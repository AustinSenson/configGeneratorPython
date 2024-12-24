from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
import configGeneratorGUI
import sys

class ConfigGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MARVEL CONFIGURATION UPDATE INTERFACE")
        self.setGeometry(400, 200, 600, 400)

        # Main Widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Layout
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Add main heading
        self.add_main_heading("MARVEL Firmware and Configuration Update Interface")

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # FOTA Button
        self.fota_button = QPushButton("FOTA")
        self.fota_button.clicked.connect(self.run_fota)
        self.fota_button.setStyleSheet("background-color: #007bff; color: white; font-weight: bold; padding: 10px; border-radius: 5px;")
        self.layout.addWidget(self.fota_button)

        # COTA Button
        self.cota_button = QPushButton("COTA")
        self.cota_button.clicked.connect(self.open_cota_window)
        self.cota_button.setStyleSheet("background-color: #007bff; color: white; font-weight: bold; padding: 10px; border-radius: 5px;")
        self.layout.addWidget(self.cota_button)

        # Add CAN Live View button
        self.can_live_view_button = QPushButton("CAN Live View")
        self.can_live_view_button.clicked.connect(self.open_can_live_view)
        self.can_live_view_button.setStyleSheet("background-color: #007bff; color: white; font-weight: bold; padding: 10px; border-radius: 5px;")
        self.layout.addWidget(self.can_live_view_button)

        # Apply black theme
        self.apply_black_theme()

    def add_main_heading(self, heading_text):
        """Add a bold main heading to the GUI."""
        main_heading = QLabel(heading_text)
        main_heading.setAlignment(Qt.AlignCenter)
        main_heading.setStyleSheet("font-weight: bold; font-size: 28px; color: #ffffff; margin-bottom: 20px;")
        self.layout.addWidget(main_heading)

    def run_fota(self):
        QMessageBox.information(self, "FOTA", "Run FOTA functionality here.")

    def open_cota_window(self):
        self.cota_window = configGeneratorGUI.RunCOTA()
        self.cota_window.show()

    def open_can_live_view(self):
        QMessageBox.information(self, "CAN Live View", "Launch CAN Live View functionality here.")

    def apply_black_theme(self):
        dark_theme = """
            QWidget {
                background-color: #1a1a1a;
                color: #e0e0e0;
                font-size: 14px;
                font-family: 'Times New Roman', serif;
            }
            QPushButton {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #606060;
            }
        """
        self.setStyleSheet(dark_theme)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConfigGeneratorGUI()
    window.show()
    sys.exit(app.exec_())
