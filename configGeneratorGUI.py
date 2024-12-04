import csv
import struct
from tkinter import Tk, Label, Entry, Button, filedialog, Frame, Scrollbar, Canvas, LEFT, RIGHT, Y, BOTH, VERTICAL
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
import subprocess

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

        print(f"Updated CSV saved to: {save_path}")
        
    
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
        
        # Print confirmation message
        print(f"New configuration saved to {csv_ref_file_path}")

    save_config_values(config_values, csv_file_path)

    close = messagebox.askyesno("Configuration details saved to successfully!!!, Do you wish to close?")
    
    if close:
            print("Process completed successfully... Shutting Down.....")
            root.quit()  # Close the GUI
    else:
            print("File saved... Proceed Further.....")

# Function to get values from the GUI and save them
def save_configs(entry_fields, parameter_names):
    config_values = []
    for i, entry in enumerate(entry_fields):
        config_values.append(entry.get())  
    
    # Save the reference CSV and config values
    save_all_configs(parameter_names, config_values)   # Reference CSV
    


# Function to load config values from a CSV file and populate the fields
def load_configs(entry_fields):
    load_configs_pass(entry_fields)

    
def load_configs_pass(entry_fields):
    file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    
    if file_path:
        with open(file_path, newline='') as file:
            csv_reader = csv.reader(file)
            config_values = next(csv_reader)
            
            # Populate the entry fields with the corresponding config values
            for i, entry in enumerate(entry_fields):
                entry.delete(0, 'end')
                entry.insert(0, config_values[i])

def flashConfigs():
    # Open file dialog to select a configuration file
    file_path = filedialog.askopenfilename(title="Select Configuration File", filetypes=[("CSV Files", "*.csv")])
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

def run_cota():
    clear_initial_buttons()
    heading = Label(root, text="MARVEL CONFIGURATION UPDATE INTERFACE", font=("Arial", 16, "bold"), bg="black", fg="white")
    heading.pack(pady=10)

    # Add a search bar at the top
    search_frame = Frame(root, bg="black")
    search_frame.pack(pady=10)
    Label(search_frame, text="Search Config:", font=("Arial", 12), bg="black", fg="white").pack(side=LEFT, padx=5)
    entry_search = Entry(search_frame, width=30)
    entry_search.pack(side=LEFT, padx=5)
    
    # Define the main frame and other required components
    main_frame = Frame(root, bg="grey", padx=20, pady=20)
    main_frame.pack(fill=BOTH, expand=1)

    canvas = Canvas(main_frame, bg="lightgrey", highlightthickness=0)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame = Frame(canvas, bg="lightgrey")
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Bind the search button to the search_config function with required parameters
    Button(search_frame, text="Search", command=lambda: search_config(entry_search.get(), frame, canvas)).pack(side=LEFT, padx=5)

    # Bind the Enter key to call the search function
    entry_search.bind("<Return>", lambda event: search_config(entry_search.get(), frame, canvas))

    def create_label_entry(parent, label_text, row):
        label = Label(parent, text=label_text, padx=10, pady=5, bg="lightgrey", fg="black", font=("Arial", 10, "bold"))
        label.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry = Entry(parent, width=50)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    # Enable mouse scrolling on Windows and Linux
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Enable mouse scrolling on macOS (delta is different)
    def on_mouse_wheel_mac(event):
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    # Bind the mouse scroll event globally to the root window for cross-GUI scrolling
    if root.tk.call("tk", "windowingsystem") == "aqua":  # macOS
        root.bind_all("<MouseWheel>", on_mouse_wheel_mac)
    else:  # Windows and Linux
        root.bind_all("<MouseWheel>", on_mouse_wheel)


    # Define labels and entries in the frame
    parameter_names = [
    "CONFIG_MAJOR_VERSION" ,
    "CONFIG_MINOR_VERSION" ,
    "NUMBER_OF_CMU" ,
    "CELL_IN_SERIES" ,
    "SHUNT_RESISTOR_uOhm" ,
    "CELL_MAX_VOLTAGE_THRESHOLD_mV" ,
    "CELL_MIN_VOLTAGE_THRESHOLD_mV" ,
    "CELL_BALANCING_START_VOLTAGE_mV" ,
    "CELL_IMBALANCE_THRESHOLD_mV",
    "PACK_MAX_CAPACITY_Ah" ,
    "PACK_MIN_CAPACITY_Ah" ,
    "PACK_USABLE_CAPACITY_mAh" ,
    "EEPROM_CAP_WRITE_mAh" ,
    "IR_WAIT_SOC" ,
    "IR_START_SOC" ,
    "IR_CYCLE_COUNT_THRESHOLD" ,
    "FAST_CHARGING_MAX_CURRENT_A" ,
    "ERROR_TIMEOUT_ms" ,
    "WARNING_TIMEOUT_ms" ,
    "RECOVERY_TIMEOUT_ms" ,
    "PRECHARGE_RETRY_TIMEOUT",
    "PRECHARGE_RETRY_LIMIT",
    "PRECHARGE_TIMEOUT",
    "BALANCING_DERATING_START_TEMP_C",
    "BALANCING_DERATING_END_TEMP_C",
    "BALANCING_MAX_ON_TIME_ms" ,
    "BALANCING_MIN_ON_TIME_ms" ,
    "BALANCING_MAX_OFF_TIME_ms" ,
    "BALANCING_MIN_OFF_TIME_ms" ,
    "MINIMUM_REQUIRED_CONFIG"  #TODO ADD RANGES FOR ALL PARAMS  ,OUT OF BOUNDS 
    ]

    entry_fields = []  

    for idx, param_name in enumerate(parameter_names):
        entry = create_label_entry(frame, f"{param_name} :", idx)
        entry_fields.append(entry) 
        pass
    # Save and Load Config Buttons
    button_save = Button(root, text="Save Config", command=lambda: save_configs(entry_fields, parameter_names))
    button_save.pack(pady=10)

    button_load = Button(root, text="Load Config", command=lambda: load_configs(entry_fields))
    button_load.pack(pady=10)

    button_flash = Button(root, text="Flash Config", command=flashConfigs)
    button_flash.pack(pady=10)

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





# Create the GUI window
root = Tk()
root.title("Config Parameter Input")

# Set the overall background color
root.configure(bg="black")

# Set the initial window size and make it resizable
root.geometry("750x700")
root.state('normal')

# Load the image and adjust its transparency
image = Image.open("D:/configGeneratorPython/background.png").convert("RGBA")
alpha = 200  # Set the transparency level (0 = fully transparent, 255 = fully opaque)
image.putalpha(alpha)

# Convert the image for Tkinter and create a label to display it
background_image = ImageTk.PhotoImage(image)
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set the overall background color (as a fallback)
root.configure(bg="black")

heading = Label(root, text="MARVEL UPDATE INTERFACE", font=("Arial", 16, "bold"), bg="black", fg="white")
heading.pack(pady=10)


#Select FOTA or COTA
fota_button = Button(root, text="FOTA", command=run_fota)
fota_button.pack(pady=10)

cota_button = Button(root, text="COTA", command=run_cota)
cota_button.pack(pady=10)



# Run the GUI loop
root.mainloop()



