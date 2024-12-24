import can
from time import sleep
import sys
import os

OTA_COMM = 0x6FA
XAVIER_FOTA_INIT = [9, 2, 1, 2, 2]
XAVIER_COTA_INIT = [9, 2, 1, 4, 2]
XAVIER_FOTA_DONE = [9, 2, 1, 5, 2]
XAVIER_COTA_DONE = [0, 2, 1, 0xA, 2]


def transfer_file(file_path, local_temp_file):
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as source_file:
                file_content = source_file.read()

            with open(local_temp_file, "wb") as target_file:
                target_file.write(file_content)
            # print("temp file created")
            return True
        except Exception as e:
            print(f"Error reading or writing the file: {e}")
            return False
    else:
        print(f"File not found: {file_path}")
        return False

def is_executable(file_path):

    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return False
    if not os.access(file_path, os.X_OK):
        print(f"Error: {file_path} is not executable or doesn't have execute permissions.")
        return False
    return True
    
def send_can(arbitration_id, message):
    with can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=250_000) as bus:
        msg = can.Message(arbitration_id=arbitration_id, data=message, is_extended_id=False)
        try:
            bus.send(msg)
        except can.CanError:
            print(f"CAN message:{message} not sent")

def receive_can(arbitration_id):
    can_filter = [{"can_id": arbitration_id, "can_mask": 0xFFFFFFFF, "extended": False}]
    while True:
        with can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=250_000, can_filters=can_filter) as bus:
            msg = bus.recv()
            if msg.arbitration_id == arbitration_id:
                return True, msg.data

def upgradeMarvel_FOTA(bin_file_path, version_input):
    if bin_file_path:
        version_components = version_input.split('.')
        version_numbers = [int(component, 16) for component in version_components]
        major = version_numbers[0]
        minor = version_numbers[1]
        patch = version_numbers[2]
        
        while True:
            received_msg = receive_can(0x7A1)
            if received_msg[0]:
                if received_msg[1][-8] == 2:
                    if (received_msg[1][-5] == patch and received_msg[1][-6] == minor and received_msg[1][-7] == major):
                        return "Already on the same version"
                    print(received_msg[1][-1])
                    if received_msg[1][-1] == 1:
                        app_name = "marvel3-appSecondary.bin"
                    else:
                        app_name = "marvel3-appPrimary.bin"
                    break

        if os.path.exists(bin_file_path):
            with open(bin_file_path, "rb") as source_file:
                app_bin_content = source_file.read()

            local_bin_file_path = "app.bin"
            with open(local_bin_file_path, "wb") as target_file:
                target_file.write(app_bin_content)

            print(f"Got {app_name} file")
            send_can(OTA_COMM, XAVIER_FOTA_INIT)
            status = receive_can(0x6FA)
            if status:
                sleep(1)
                os.system(f"app.exe app.bin")
                print("Update done, Switching Partition")
                send_can(OTA_COMM, XAVIER_FOTA_DONE)
                os.remove(local_bin_file_path)
            else:
                print("ECU didn't respond")
        else:
            print(f"{app_name} file not found.")
    else:
        print("No folder selected")

def upgradeMarvel_COTA(file_path):
                    #    , config_version):
    print(file_path)
    print(config_version)
    while True:
        received_msg = receive_can(0x7A1)
        if received_msg[0]:
            if received_msg[1][-8] == 2:
                if received_msg[1][-3] == config_version:
                    return "Already on the same version"
                else:
                    print(f"Marvel on Config Version: {received_msg[1][-3]}")
                    config_name = os.path.basename(file_path)
                    break
    
    config_name = os.path.basename(file_path)
    local_txt_file = "conf.txt"
    if transfer_file(file_path, local_txt_file):
        # print(f"Got {config_name} file")
        send_can(OTA_COMM, XAVIER_COTA_INIT)
        sleep(1)
        if not is_executable("cota.exe"):
            print("executable invalid")
            return
        os.system(f"cota.exe {local_txt_file}") #check local bin file path
        print("COTA Done")
        send_can(OTA_COMM, XAVIER_COTA_DONE) 
        print("Update DONE")
        os.remove(local_txt_file)
        received_msg = receive_can(0x7A1)
        if received_msg[0]:
           if received_msg[1][-8] == 2:
                print(f"Marvel on Config Version: {received_msg[1][-3]}")

    else:
        print(f"{config_name} file not found.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: upgradeMarvel.py <task> <file_path> [<config_version>] [<bin_file_path> <version_input>]")
        sys.exit(1)

    task = sys.argv[1]
    if task == "COTA":
        if len(sys.argv) != 3:
            print("Usage for COTA: upgradeMarvel.py COTA <file_path> <config_version>")
            sys.exit(1)
        file_path = sys.argv[2]
        try:
            config_version_str = file_path.replace('D:/configGeneratorRepo/configGeneratorPython/v', '').replace('.00.00.csv', '')
            config_version = int(config_version_str)
        except ValueError:
            print("Error: Unable to parse configuration version from the file path. Please check the file name format.")
            config_version = None
            sys.exit(1)
        print("COTA START")
        print(file_path)
        upgradeMarvel_COTA(file_path)
        sys.exit(0)
                        #    , config_version)

    elif task == "FOTA":        #TODO test FOTA
        if len(sys.argv) != 4:
            print("Usage for FOTA: upgradeMarvel.py FOTA <bin_file_path> <version_input>")
            sys.exit(1)
        bin_file_path = sys.argv[2]
        version_input = sys.argv[3]
        print("FOTA START")
        upgradeMarvel_FOTA(bin_file_path, version_input)
        sys.exit(0)
