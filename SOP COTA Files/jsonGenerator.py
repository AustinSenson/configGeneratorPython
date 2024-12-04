import json
import base64
from tkinter import Tk, filedialog

def prepare_data_for_transmission(csv_data, binary_data):
    # Encode binary data as Base64
    binary_base64 = base64.b64encode(binary_data).decode('utf-8')
    
    # Ensure null termination for csv_data (replace newline with null byte)
    # csv_data = csv_data.rstrip('\n') + '\0'  # Add null terminator at the end
    # csv_data = csv_data.rstrip('\n') + '\0'  # Add null terminator at the end

    # Prepare a dictionary to hold both CSV data and binary data
    data = {
        "csv_data": csv_data,
        "binary_data": binary_base64
    }

    # Convert the dictionary to a JSON string without spaces after commas and colons
    json_data = json.dumps(data, separators=(',', ':'))

    # Escape double quotes in the JSON string for use in C code
    json_data_c_style = json_data.replace('"', '\\"')

    return json_data_c_style

def select_file(file_type):
    # Open file dialog for selecting files
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title=f"Select {file_type} file", filetypes=[("All Files", "*.*")])
    return file_path

# Ask the user to select a CSV file and a binary file
csv_file = select_file("CSV")
binary_file = select_file("binary")

# Read the CSV file
with open(csv_file, 'r') as f:
    csv_data = f.read()

# Read the binary file
with open(binary_file, 'rb') as f:
    binary_data = f.read()

# Prepare the data for transmission
transmission_data = prepare_data_for_transmission(csv_data, binary_data)
print("Transmission Data:", transmission_data)
