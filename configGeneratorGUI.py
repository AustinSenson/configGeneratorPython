import csv
import struct
import json
import base64
from tkinter import Tk, Label, Entry, Button, filedialog, Frame, Scrollbar, Canvas, LEFT, RIGHT, Y, BOTH, VERTICAL
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QFileDialog, QWidget, QScrollArea, QFrame, QMessageBox, QGridLayout)
from PyQt5.QtCore import Qt
import tempfile
import os

def clear_initial_buttons():
    fota_button.pack_forget()
    cota_button.pack_forget()

def search_config(search_term, frame, canvas):  
    search_term = search_term.lower()
    for widget in frame.winfo_children():
        if isinstance(widget, Label):
            if search_term in widget.cget("text").lower():
                # Scroll to the widget using its absolute position within the canvas
                canvas.yview_moveto(widget.winfo_y() / frame.winfo_height())
                return  # Stop searching after the first match

            
def read_string_as_uint64_array(data_input):
    uint64_array = []
    
    # Convert to a string if the input is a list
    if isinstance(data_input, list):
        data_string = ','.join(str(item) for item in data_input)
    else:
        data_string = data_input
    
    # Split the string by commas
    values = data_string.split(',')
    
    # Parse each value as uint64 and combine the first two values
    combined_value = None
    for i, value in enumerate(values):
        try:
            # Convert the value to an integer
            int_value = int(value.strip())  # Assuming input values are in hex
            
            if i == 0:
                # Store the first value separately
                combined_value = int_value
            elif i == 1:
                # Combine the first and second values
                combined_value = (combined_value << 8) | int_value 
                combined_value <<= 8   # adding 0x00 to the last byte as minor config version is not being used    
            else:
                # Pack and unpack as uint64
                uint64_array.append(struct.unpack('<Q', struct.pack('<Q', int_value))[0])
        
        except ValueError:
            print(f"Invalid value: {value.strip()}")
    
    if combined_value is not None:
        uint64_array.insert(0, combined_value)
    
    return uint64_array

def write_csv_with_crc(data, crc_value, save_path):
    # Append CRC value to the data array
    data.append(crc_value)
    
    # Ask the user where to save the new CSV file
    # save_path = asksaveasfilename(title="Save CSV with CRC", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if save_path:
        # Write the updated data to the new CSV file
        with open(save_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            # Write the data as a single row in the CSV
            csv_writer.writerow(data)

        with open(save_path, 'r') as file:
            file_content = file.read()
        # character_count = len(file_content)  # Calculate the total length of the file

        print(f"Updated CSV saved to: {save_path}")
        # print(f"Total number of characters in the CSV: {character_count}")
        
    
    else:
        print("No file selected for saving.")
    

# Function to calculate CRC
def calculate_flash_crc(data):
    poly = 0xEDB88320
    crc = 0xFFFFFFFF
    
    for value in data:
        crc ^= value
        for _ in range(32):
            mask = -(crc & 1)
            crc = (crc >> 1) ^ (poly & mask)
    
    return ~crc & 0xFFFFFFFF
# Function to save the config values to a CSV file
def save_config_values(values,csv_file_path):
        
        data_array = read_string_as_uint64_array(values)

        # CRC calculation and appending can be added here
        crc_result = calculate_flash_crc(data_array)
        print(f"Calculated CRC: {crc_result}")

        # Step 3: Write the updated CSV with CRC as the last element
        write_csv_with_crc(data_array, crc_result,csv_file_path)
        


def save_all_configs(parameter_names, config_values):    
    # Ask the user for the file path and append "_reference" to the filename

    """ uncomment for entering file name manually """
    # csv_file_path = asksaveasfilename(title="Save CSV with config names", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

    """ File name based on Major Config Version """
    print(config_values)
    config_version = int(config_values[0])
    base_filename = f"v{config_version:02d}.00.00"
    csv_file_path = f"{base_filename}.csv"

    if csv_file_path:
        if not csv_file_path.endswith("_reference.csv"):
            csv_ref_file_path = csv_file_path.replace(".csv", "_reference.csv")

        with open(csv_ref_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Parameter Name', 'Value'])
            # Write parameter names and values
            for name, value in zip(parameter_names, config_values):
                csv_writer.writerow([name, value])
        # print(f"New configuration saved to {csv_ref_file_path}")

        #Load file for that particular config to be saved
        csv_load_file_path = csv_file_path.replace(".csv", "_load.csv")
        with open(csv_load_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)       
            csv_writer.writerow(config_values)
        # print(f"New configuration values saved to {csv_load_file_path}")

    save_config_values(config_values, csv_file_path)

    close = messagebox.askyesno("Configuration details saved successfully!\nDo you wish to close?")
    
    if close:
            print("Process completed successfully... Shutting Down.....")
            root.quit()  # Close the GUI
    else:
            print("File saved... Proceed Further.....")

# Function to get values from the GUI and save them
def save_configs(entry_fields, parameter_names):
    config_values = []
    for i, entry in enumerate(entry_fields):
        config_values.append(entry.text())  # Use text() to get the text from QLineEdit    
    # Save the reference CSV and config values
    save_all_configs(parameter_names, config_values)   # Reference CSV
    
from tkinter import Tk, filedialog

def select_file(file_type):
    """
    Open file dialog for selecting files based on the provided file type.
    :param file_type: The type of file to select ("binary" or "CSV").
    :return: The selected file path.
    """
    # Set up the prompt based on the file type
    if file_type.lower() == "binary":
        prompt = "Select binary file for SoP structure"
    elif file_type.lower() == "csv":
        prompt = "Select configuration SoP"
    else:
        prompt = f"Select {file_type} file"
    
    # Open file dialog
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title=prompt, filetypes=[("All Files", "*.*")])
    return file_path

def add_slashes_before_key_in_string(csv_file, input_string, num_slashes):

    x = input_string.find("\"binary_data\"")
    print("Index of '\"binary_data\"':", x)
    slashes = "\\" * num_slashes
    # print(input_string[x:])
    modified_string = input_string[:x] + slashes + input_string[x:]
    string_val = modified_string.replace('"', '\\"')
    string_val = string_val.replace('n\\', '\\n\\')
    with open(csv_file, "w") as file:
        file.write(string_val)
    # print("Modified string:", string_val)
    
    return string_val
    # print("Modified string:", string_val)
        

# Function to load config values from a CSV file and populate the fields
def load_configs(entry_fields):
    load_configs_pass(entry_fields)

    
def load_configs_pass(entry_fields):
    file_path = QFileDialog.getOpenFileName(
        caption="Open CSV File",
        filter="CSV files (*.csv);;All files (*)"
    )[0]  # Get the file path

    if file_path:
        with open(file_path, newline='') as file:
            csv_reader = csv.reader(file)
            config_values = next(csv_reader)  # Read the first row of the CSV file

            # Populate the entry fields with the corresponding config values
            for i, entry in enumerate(entry_fields):
                entry.clear()  # Clear the existing text
                if i < len(config_values):
                    entry.setText(config_values[i])  # Set the new text


def prepare_data_for_transmission(csv_file, csv_data, binary_data,character_count):
    # Encode binary data as Base64
    binary_base64 = base64.b64encode(binary_data).decode('utf-8')
    
    # Ensure null termination for csv_data (replace newline with null byte)
    # csv_data = csv_data.rstrip('\n') + '\0'  # Add null terminator at the end
    # csv_data = csv_data.rstrip('\n') + '\0'  # Add null terminator at the end
    # Prepare a dictionary to hold both CSV data and binary data
    data = \
    {
        "csv_data": csv_data,
        "binary_data": binary_base64
    }
  
    # Convert the dictionary to a JSON string without spaces after commas and colons
    json_data = json.dumps(data, separators=(',', ':'))
    # Escape double quotes in the JSON string for use in C code
    json_data_c_style = json_data.replace('"', '\\"')
    num_slashes = 4 - ((character_count + 2) % 4)                                          # considering the /n/ also
    json_data_c_style = json_data_c_style.replace("\\", "")
    json_data_new = add_slashes_before_key_in_string(csv_file, json_data_c_style, num_slashes)
    # print(json_data_new)
    return json_data_new

def jsonGenerator(csv_file, binary_file):
    # Ask the user to select a CSV file and a binary file
    
    # Read the CSV file
    with open(csv_file, 'r') as f:
        csv_data = f.read()
    character_count = len(csv_data)
    print(character_count)
    # Read the binary file
    with open(binary_file, 'rb') as f:
        binary_data = f.read()

    transmission_data = prepare_data_for_transmission(csv_file, csv_data, binary_data,character_count)
    print("Transmission Data:", transmission_data)


def flashConfigs():
    # Open file dialog to select a configuration file
    csv_file = select_file("CSV")

    binary_file = select_binary_from_gui()

    jsonGenerator(csv_file, binary_file)
    file_path = csv_file
    # config_version = file_path.replace('v', '').replace('.csv', '')
    
    # Confirm with the user if they want to proceed with flashing
    response = messagebox.askyesno("Confirm Flash", "Are you sure you want to flash the configuration?")
    
    if file_path:
        if response:
            try:
                task = "COTA"
                command = ["python", "upgradeMarvel.py",task, file_path]
                        #    , config_version]
                result = subprocess.run(command, capture_output=True, text=True, check=True)

                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                
                # Check the output for specific messages
                if "Already on the same version" in result.stdout.strip():
                    messagebox.showinfo("Info", "The device is already on the same CONFIG version.")
                elif "Update done" in result.stdout.strip():
                    messagebox.showinfo("Success", "Configuration flashed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Subprocess error: {e}")
                print(f"STDOUT: {e.stdout}")
                print(f"STDERR: {e.stderr}")
                messagebox.showerror("Error", f"Failed to flash firmware: {e}")
            except Exception as ex:
                messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {ex}")
        else:
            messagebox.showinfo("Cancelled", "Flash COTA canceled.")
    else:
        print("Flash COTA canceled.")
        messagebox.showinfo("Restricted Action")

# Function to select the binary file
def select_binary_from_gui():
    response = messagebox.askyesno("Select Binary", "Do you want to generate the binary file using the GUI?")
    if response:
        # Call the GUI script to generate the binary file
        result = subprocess.run(
            ["python", "SoP_GUI.py"],  # Replace with the actual path to your GUI script
            capture_output=True,
            text=True,
            check=True
        )
        binary_path = result.stdout.strip()
        return binary_path
    else:
        # Select the binary file manually
        file_path = filedialog.askopenfilename(
            title="Select Binary File",
            filetypes=[("Binary Files", "*.bin"), ("All Files", "*.*")]
        )
        return file_path

class RunCOTA(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MARVEL CONFIGURATION UPDATE INTERFACE")
        self.setGeometry(100, 100, 750, 700)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Add heading
        self.heading = QLabel("MARVEL CONFIGURATION UPDATE INTERFACE")
        self.heading.setAlignment(Qt.AlignCenter)
        self.heading.setStyleSheet("font-size: 16px; font-weight: bold; color: white; background-color: black;")
        self.layout.addWidget(self.heading)

        self.search_bar_layout = QHBoxLayout()
        self.search_label = QLabel("Search Config:")
        self.search_label.setStyleSheet("font-size: 12px; color: white; background-color: black;")
        self.search_bar_layout.addWidget(self.search_label)
        self.search_entry = QLineEdit()
        self.search_bar_layout.addWidget(self.search_entry)
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_config)
        self.search_bar_layout.addWidget(self.search_button)
        self.layout.addLayout(self.search_bar_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        self.scroll_layout = QGridLayout()
        self.scroll_widget.setLayout(self.scroll_layout)

        self.parameter_names =[
        "CONFIG_MAJOR_VERSION",
        "CONFIG_MINOR_VERSION",
        "NUMBER_OF_CMU",
        "CELL_IN_SERIES",
        "SHUNT_RESISTOR_uOhm",
        "CELL_MAX_VOLTAGE_THRESHOLD_mV",
        "CELL_MIN_VOLTAGE_THRESHOLD_mV",
        "CELL_BALANCING_START_VOLTAGE_mV",
        "CELL_IMBALANCE_THRESHOLD_mV",
        "PACK_MAX_CAPACITY_Ah",
        "PACK_USABLE_CAPACITY_mAh",
        "EEPROM_CAP_WRITE_mAh",
        "IR_WAIT_SOC",
        "IR_START_SOC",
        "IR_CYCLE_COUNT_THRESHOLD",
        "SLOW_CHARGING_MAX_CURRENT_A",
        "FAST_CHARGING_MAX_CURRENT_A",
        "CHARGE_CURRENT_DETECTION_THRESHOLD_mA",
        "SLOW_CHARGING_TARGET_mV",
        "FAST_CHARGING_TARGET_mV",
        "CV_TRANSITION_mV",
    
        #Scale it *100
        "FAST_CHARGING_SCALING_FACTOR",
        "SLOW_CHARGING_CV_SCALING_FACTOR",
        "SLOW_CHARGING_CC_SCALING_FACTOR",

        "OCC_ERROR_CURRENT_A",
        "OCC_WARNING_CURRENT_A",
        "OCD_ERROR_CURRENT_A",
        "OCD_WARNING_CURRENT_A",
        "ERROR_TIMEOUT_ms",
        "WARNING_TIMEOUT_ms",
        "RECOVERY_TIMEOUT_ms",
        "BALANCING_DERATING_START_TEMP_C",
        "BALANCING_DERATING_END_TEMP_C",
        "BALANCING_MAX_ON_TIME_ms",
        "BALANCING_MIN_ON_TIME_ms",
        "BALANCING_MAX_OFF_TIME_ms",
        "OTC_ERROR_TEMPERATURE_GROUP_1",
        "OTC_WARNING_TEMPERATURE_GROUP_1",
        "OTC_RECOVERY_TEMPERATURE_GROUP_1",
        "OTD_ERROR_TEMPERATURE_GROUP_1",
        "OTD_WARNING_TEMPERATURE_GROUP_1",
        "OTD_RECOVERY_TEMPERATURE_GROUP_1",
        "UTC_ERROR_TEMPERATURE_GROUP_1",
        "UTC_WARNING_TEMPERATURE_GROUP_1",
        "UTC_RECOVERY_TEMPERATURE_GROUP_1",
        "UTD_ERROR_TEMPERATURE_GROUP_1",
        "UTD_WARNING_TEMPERATURE_GROUP_1",
        "UTD_RECOVERY_TEMPERATURE_GROUP_1",
        "OTC_ERROR_TEMPERATURE_GROUP_2",
        "OTC_WARNING_TEMPERATURE_GROUP_2",
        "OTC_RECOVERY_TEMPERATURE_GROUP_2",
        "OTD_ERROR_TEMPERATURE_GROUP_2",
        "OTD_WARNING_TEMPERATURE_GROUP_2",
        "OTD_RECOVERY_TEMPERATURE_GROUP_2",
        "UTC_ERROR_TEMPERATURE_GROUP_2",
        "UTC_WARNING_TEMPERATURE_GROUP_2",
        "UTC_RECOVERY_TEMPERATURE_GROUP_2",
        "UTD_ERROR_TEMPERATURE_GROUP_2",
        "UTD_WARNING_TEMPERATURE_GROUP_2",
        "UTD_RECOVERY_TEMPERATURE_GROUP_2",
        "HIGH_IMBALANCE_ERROR_mV",
        "CONTACTOR_CUT_OFF_TIME_ms",    
        "PRECHARGE_RETRY_TIMEOUT",
        "PRECHARGE_RETRY_LIMIT",
        "PRECHARGE_TIMEOUT",   
        "MINIMUM_REQUIRED_CONFIG",                     
        ]

        self.entry_fields = []
        for idx, param_name in enumerate(self.parameter_names):
            label = QLabel(f"{param_name}:")
            label.setStyleSheet("font-size: 10px; color: black;")
            entry = QLineEdit()
            self.scroll_layout.addWidget(label, idx, 0)
            self.scroll_layout.addWidget(entry, idx, 1)
            self.entry_fields.append(entry)

        # Add Save, Load, and Flash buttons
        self.button_save = QPushButton("Save Config")
        self.button_save.clicked.connect(self.save_configs_test)
        self.layout.addWidget(self.button_save)

        self.button_load = QPushButton("Load Config")
        self.button_load.clicked.connect(self.load_configs)
        self.layout.addWidget(self.button_load)

        self.button_flash = QPushButton("Flash Config")
        self.button_flash.clicked.connect(self.flash_configs)
        self.layout.addWidget(self.button_flash)

    def search_config(self):
        search_term = self.search_entry.text().lower()
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if isinstance(widget, QLabel) and search_term in widget.text().lower():
                self.scroll_area.verticalScrollBar().setValue(widget.y())
                break

    def save_configs_test(self):
        config_values = save_configs(self.entry_fields, self.parameter_names)
        if config_values:
            QMessageBox.information(self, "Success", "Configurations saved successfully!")

    def load_configs(self):
        load_configs(self.entry_fields)
        # QMessageBox.information(self, "Load", "Load Config functionality here.")

    def flash_configs(self):

        flashConfigs()
        # QMessageBox.information(self, "Flash", "Flash Config functionality here.")

def run_fota():
    # Incorporate FOTA under this function
    clear_initial_buttons()
    heading = Label(root, text="MARVEL FIRMWARE UPDATE INTERFACE", font=("Arial", 16, "bold"), bg="black", fg="white")
    heading.pack(pady=10)

    # Prompt the user to select the firmware binary file
    bin_folder_path = filedialog.askopenfilename(title="Select Firmware Binary File", filetypes=[("BIN Files", "*.bin")])
    
    # Prompt the user to enter the firmware version
    if bin_folder_path:
        version_input = simpledialog.askstring("Firmware Version", "Enter the firmware version:")
        
        # Ask for confirmation before flashing
        if version_input:
            response = messagebox.askyesno("Confirm Flash", "Are you sure you want to flash the firmware?")
            if response:
                try:
                    # Pass the selected file path and version to the script
                    task = "FOTA"
                    flash_response = subprocess.run(
                        ["python", "upgradeMarvel.py", task, bin_folder_path, version_input],
                        capture_output=True,
                        text=True,
                        check=True
                    )

                    # Print stdout and stderr for debugging
                    print("STDOUT:", flash_response.stdout)
                    print("STDERR:", flash_response.stderr)

                    if flash_response.returncode != 0:
                        messagebox.showerror("Error", "Failed to flash firmware. Check the console for details.")
                    else:
                        if "Already on the same version" in flash_response.stdout.strip():
                            messagebox.showinfo("Info", "The device is already on the same version.")
                        else:
                            messagebox.showinfo("Success", "Firmware flashed successfully.")

                except subprocess.CalledProcessError as e:
                    print(f"Subprocess error: {e}")
                    print(f"STDOUT: {e.stdout}")
                    print(f"STDERR: {e.stderr}")
                    messagebox.showerror("Error", f"Failed to flash firmware: {e}")
            else:
                messagebox.showinfo("Cancelled", "Firmware flashing canceled.")
        else:
            messagebox.showinfo("Cancelled", "No version entered. Flashing canceled.")
    else:
        messagebox.showinfo("Cancelled", "No file selected. Flashing canceled.")




