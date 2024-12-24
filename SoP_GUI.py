import struct
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QMessageBox,
    QTableWidget, QTableWidgetItem, QLabel, QWidget, QScrollArea, QHeaderView
)
from PyQt5.QtCore import Qt


class ConfiguratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Structure Configuration GUI")
        self.setGeometry(100, 100, 1600, 900)  # Larger window to show full tables

        # Scrollable main layout
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.setCentralWidget(self.scroll_area)

        self.main_layout = QVBoxLayout(self.scroll_widget)

        # Add main heading
        self.add_main_heading("MARVEL SoP table Configurator")

        self.tables = {}

         # Predefined data for each table
        self.predefined_data = {
            "Continuous Charging Table Data": self.reshape_table_data(
                              [ 0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,
                                24,     24,     24,     24,     24,     24,     24,     24,     24,     24,     20,
                                60,     60,     60,     60,     60,     60,     60,     60,     60,     60,     40,
                                100,    100,    100,    100,    100,    100,    100,    100,    100,    100,    40,
                                200,    200,    200,    200,    200,    200,    200,    200,    200,    150,    60,
                                200,    200,    200,    200,    200,    200,    200,    200,    200,    160,    160,
                                200,    200,    200,    200,    200,    200,    200,    200,    200,    160,    160,
                                160,    160,    160,    160,    160,    160,    160,    160,    160,    160,    60,
                                60,     60,     60,     60,     60,     60,     60,     60,     60,     60,     40,
                                0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0 ], 
                                10, 11),

            "Continuous Discharging Table Data": self.reshape_table_data(
                               [40,        60,         80,         100,        100,        100,        100,        100,        100,        100,        100,
                                60,        100,        120,        160,        160,        160,        160,        160,        160,        160,        160,
                                60,        100,        120,        160,        160,        160,        160,        160,        160,        160,        160,
                                60,        100,        120,        160,        160,        160,        160,        160,        160,        160,        160,
                                60,        100,        120,        160,        160,        160,        160,        160,        160,        160,        160,
                                100,       120,        150,        200,        200,        200,        200,        200,        200,        200,        200,
                                100,       120,        150,        200,        200,        200,        200,        200,        200,        200,        200,
                                100,       120,        150,        200,        200,        200,        200,        200,        200,        200,        200,
                                100,       120,        150,        200,        200,        200,        200,        200,        200,        200,        200,
                                100,       120,        150,        200,        200,        200,        200,        200,        200,        200,        200,
                                100,       120,        150,        200,        200,        200,        200,        200,        200,        200,        200,
                                100,       120,        150,        200,        200,        200,        200,        200,        200,        200,        200,
                                60,        100,        120,        160,        160,        160,        160,        160,        160,        160,        160,
                                20,        30,         40,         60,         60,         60,         60,         60,         60,         60,         60,
                                0,         0,          0,          0,          0,          0,          0,          0,          0,          0,          0], 
                                15, 11),

            "Instantaneous Discharging Table Data": self.reshape_table_data(
                               [40,     60,     80,     200,    200,    200,    200,    200,    200,    200,    200,
                                60,     100,    120,    240,    240,    240,    240,    240,    240,    240,    240,
                                60,     100,    200,    300,    300,    300,    300,    300,    300,    300,    300,
                                60,     100,    200,    300,    300,    300,    300,    300,    300,    300,    300,
                                60,     100,    200,    300,    300,    300,    300,    300,    300,    300,    300,
                                100,    200,    240,    300,    300,    300,    300,    300,    300,    300,    300,
                                200,    200,    240,    300,    300,    300,    300,    300,    300,    300,    300,
                                200,    200,    300,    300,    300,    300,    300,    300,    300,    300,    300,
                                200,    200,    300,    300,    300,    300,    300,    300,    300,    300,    300,
                                200,    200,    300,    300,    300,    300,    300,    300,    300,    300,    300,
                                200,    200,    300,    300,    300,    300,    300,    300,    300,    300,    300,
                                200,    200,    300,    300,    300,    300,    300,    300,    300,    300,    300,
                                200,    200,    300,    300,    300,    300,    300,    300,    300,    300,    300,
                                20,     60,     120,    240,    240,    240,    240,    240,    240,    240,    240,
                                0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0 ], 
                                15, 11),

            "Instantaneous Charging Table Data": self.reshape_table_data(
                               [0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,
                                80,     80,     80,     80,     80,     80,     80,     80,     80,     80,     20,
                                160,    160,    160,    160,    160,    160,    160,    160,    160,    160,    40,
                                240,    240,    240,    240,    240,    240,    240,    240,    240,    240,    40,
                                300,    300,    300,    300,    300,    300,    300,    300,    300,    300,    60,
                                300,    300,    300,    300,    300,    300,    300,    300,    300,    300,    160,
                                300,    300,    300,    300,    300,    300,    300,    300,    300,    300,    160,
                                300,    300,    300,    300,    300,    300,    300,    300,    300,    300,    60,
                                240,    240,    240,    240,    240,    240,    240,    240,    240,    240,    40,
                                0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0 ], 
                                10, 11),
                                
            "SOC Data": [[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]],
            "Charging Temperature Data": [[0, 5, 10, 15, 20, 25, 45, 50, 55, 60]],
            "Discharging Temperature Data": [[-10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]],
            "Charging Max Elements": [[10, 11]],
            "Discharging Max Elements": [[15, 11]]
        }


        # Create labeled tables for all matrices
        for table_name in self.predefined_data.keys():
            self.create_table(table_name)

        # Add Generate Binary button
        self.generate_button = QPushButton("Generate Binary")
        self.generate_button.clicked.connect(self.generate_binary_file)
        self.generate_button.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 10px; border-radius: 5px;")
        self.main_layout.addWidget(self.generate_button)

        # Apply a black theme
        self.apply_black_theme()

    def reshape_table_data(self, flat_data, rows, cols):
        return [flat_data[i * cols:(i + 1) * cols] for i in range(rows)]

    def create_table(self, title):
        """Create a labeled table with resizable rows and columns."""
        if title in ["Continuous Charging Table Data", "Instantaneous Charging Table Data"]:
            row_labels = ["0°C", "5°C", "10°C", "15°C", "20°C", "25°C", "45°C", "50°C", "55°C", "60°C"]
            column_labels = ["0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
        elif title in ["Continuous Discharging Table Data", "Instantaneous Discharging Table Data"]:
            row_labels = ["-10°C", "-5°C", "0°C", "5°C", "10°C", "15°C", "20°C", "25°C", "30°C", "35°C", "40°C", "45°C", "50°C", "55°C", "60°C"]
            column_labels = ["0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
        else:
            row_labels = []
            column_labels = []


        label = QLabel(f"{title}:")
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.main_layout.addWidget(label)

        predefined_data = self.predefined_data.get(title, [])
        rows, cols = len(predefined_data), len(predefined_data[0]) if predefined_data else (10, 11)
        table = QTableWidget(rows, cols)
        table.setHorizontalHeaderLabels(column_labels[:cols])
        table.setVerticalHeaderLabels(row_labels[:rows])

        for i, row in enumerate(predefined_data):
            for j, value in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(value)))

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setMinimumSize(800, 300)

        self.main_layout.addWidget(table)
        self.tables[title] = table

    def add_main_heading(self, heading_text):
        """Add a bold main heading to the GUI."""
        main_heading = QLabel(heading_text)
        main_heading.setAlignment(Qt.AlignCenter)
        main_heading.setStyleSheet("font-weight: bold; font-size: 24px; color: #ffffff;")
        self.main_layout.addWidget(main_heading)

    def calculate_crc_sop(self, data):
        poly = 0xEDB88320
        crc = 0xFFFFFFFF

        for byte in data:
            crc ^= byte

            for _ in range(32):
                mask = -(crc & 1)
                crc = (crc >> 1) ^ (poly & mask)

        return ~crc & 0xFFFFFFFF

    def generate_binary_file(self):
        try:
            data = []
            for title, table in self.tables.items():
                for row in range(table.rowCount()):
                    for col in range(table.columnCount()):
                        item = table.item(row, col)
                        if item is not None:
                            value = int(item.text())
                            data.append(value)
                        else:
                            data.append(0)

            # Pack the data as signed 16-bit integers
            packed_data = struct.pack(f"{len(data)}h", *data)

            # Calculate CRC over the data
            crc = self.calculate_crc_sop(packed_data)
            packed_data_with_crc = packed_data + struct.pack("I", crc)

            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Binary File", "", "Binary Files (*.bin);;All Files (*)", options=options
            )
            if file_path:
                with open(file_path, "wb") as f:
                    f.write(packed_data_with_crc)
                QMessageBox.information(self, "Success", f"Binary file saved to: {file_path}")
                print(file_path)  # Output the file path to the console
                sys.exit(0)  # Exit with success and output the file path
            else:
                QMessageBox.warning(self, "Cancelled", "No file was saved.")

        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Invalid input: {e}")
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {ex}")

    def apply_black_theme(self):
        dark_theme = """
            QWidget {
                background-color: #1a1a1a;
                color: #e0e0e0;
                font-size: 14px;
                font-family: Arial, Helvetica, sans-serif;
            }
            QTableWidget {
                background-color: #2b2b2b;
                gridline-color: #444444;
                color: #e0e0e0;
                border: 1px solid #444444;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #3c3c3c;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
                padding: 6px;
                border: 1px solid #555555;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #3c3c3c;
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
            QScrollBar:vertical, QScrollBar:horizontal {
                background-color: #2b2b2b;
                border: none;
                width: 12px;
                height: 12px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background-color: #444444;
                border-radius: 6px;
            }
            QScrollBar::handle:hover {
                background-color: #555555;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
                border: none;
            }
        """
        self.setStyleSheet(dark_theme)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConfiguratorGUI()
    window.show()
    sys.exit(app.exec_())
