import struct
import numpy as np

# SOP Table 155Ah
def calculate_crc_sop(data):

    poly = 0xEDB88320
    crc = 0xFFFFFFFF
    
    for byte in data:
        crc ^= byte
        
        for _ in range(32):
            mask = -(crc & 1)
            crc = (crc >> 1) ^ (poly & mask)
    
    return ~crc & 0xFFFFFFFF

continuousChargingTableData_raw = [ #110
                0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,
                20.64,  20.64,  20.64,  20.64,  20.64,  20.64,  20.64,  20.64,  20.64,  20.64,  17.2,
                51.6,   51.6,   51.6,   51.6,   51.6,   51.6,   51.6,   51.6,   51.6,   51.6,   34.4,
                86,     86,     86,     86,     86,     86,     86,     86,     86,     86,     51.6,
                172,    172,    172,    172,    172,    172,    172,    172,    172,    172,    137.6,
                172,    172,    172,    172,    172,    172,    172,    172,    172,    172,    51.6,
                172,    172,    172,    172,    172,    172,    172,    172,    172,    172,    51.6,
                137.6,  137.6,  137.6,  137.6,  137.6,  137.6,  137.6,  137.6,  137.6,  137.6,  51.6,
                51.6,   51.6,   51.6,   51.6,   51.6,   51.6,   51.6,   51.6,   51.6,   51.6,   34.4,
                0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0]


            
continuousDischargingTableData_raw = [ #165
                34,     51,     51,     86,     86,     86,     86,     86,     86,     86,     86,
                50,     86,     86,     137,    137,    137,    137,    137,    137,    137,    137,
                50,     86,     86,     137,    137,    137,    137,    137,    137,    137,    137,
                50,     86,     86,     137,    137,    137,    137,    137,    137,    137,    137,
                50,     86,     86,     137,    137,    137,    137,    137,    137,    137,    137,
                86,     103,    129,    172,    172,    172,    172,    172,    172,    172,    172,
                86,     103,    129,    172,    172,    172,    172,    172,    172,    172,    172,
                86,     103,    129,    172,    172,    172,    172,    172,    172,    172,    172,
                86,     103,    129,    172,    172,    172,    172,    172,    172,    172,    172,
                86,     103,    129,    172,    172,    172,    172,    172,    172,    172,    172,
                86,     103,    129,    172,    172,    172,    172,    172,    172,    172,    172,
                86,     103,    129,    172,    172,    172,    172,    172,    172,    172,    172,
                50,     86,     111,    137,    137,    137,    137,    137,    137,    137,    137,
                34,     34,     51,     51,     51,     51,     51,     51,     51,     51,     51,
                0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0]



instantaneousChargingTableData_raw = [
                0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0,
                68.8,   68.8,   68.8,   68.8,   68.8,   68.8,   68.8,   68.8,   68.8,   68.8,   51.6,
                137.6,  137.6,  137.6,  137.6,  137.6,  137.6,  137.6,  137.6,  137.6,  137.6,  103.2,
                206.4,  206.4,  206.4,  206.4,  206.4,  206.4,  206.4,  206.4,  206.4,  206.4,  137.6,
                258,    258,    258,    258,    258,    258,    258,    258,    258,    258,    172,
                258,    258,    258,    258,    258,    258,    258,    258,    258,    258,    172,
                258,    258,    258,    258,    258,    258,    258,    258,    258,    258,    172,
                258,    258,    258,    258,    258,    258,    258,    258,    258,    258,    172,
                206.4,  206.4,  206.4,  206.4,  206.4,  206.4,  206.4,  206.4,  206.4,  206.4,  137.6,
                0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0]
            
            
instantaneousDischargingTableData_raw = [ #165
                34,     51,     68.8,   172,    172,    172,    172,    172,    172,    172,    172,
                50,     86,     103.2,  206.4,  206.4,  206.4,  206.4,  206.4,  206.4,  206.4,  206.4,
                50,     86,     172,    258,    258,    258,    258,    258,    258,    258,    258,
                50,     86,     172,    258,    258,    258,    258,    258,    258,    258,    258,
                50,     86,     172,    258,    258,    258,    258,    258,    258,    258,    258,
                86,     103.2,  206.4,  258,    258,    258,    258,    258,    258,    258,    258,
                86,     103.2,  206.4,  258,    258,    258,    258,    258,    258,    258,    258,
                86,     120.4,  258,    258,    258,    258,    258,    258,    258,    258,    258,
                86,     120.4,  258,    258,    258,    258,    258,    258,    258,    258,    258,
                86,     120.4,  258,    258,    258,    258,    258,    258,    258,    258,    258,
                86,     120.4,  258,    258,    258,    258,    258,    258,    258,    258,    258,
                86,     120.4,  258,    258,    258,    258,    258,    258,    258,    258,    258,
                50,     86,     172,    258,    258,    258,    258,    258,    258,    258,    258,
                34,     51.6,   103.2,  206.4,  206.4,  206.4,  206.4,  206.4,  206.4,  206.4,  206.4,
                0,      0,      0,      0,      0,      0,      0,      0,      0,      0,      0]


continuousChargingTableData = np.array([int(f) for f in continuousChargingTableData_raw], dtype=np.int16)
continuousDischargingTableData = np.array([int(f) for f in continuousDischargingTableData_raw], dtype=np.int16)
instantaneousChargingTableData = np.array([int(f) for f in instantaneousChargingTableData_raw], dtype=np.int16)
instantaneousDischargingTableData = np.array([int(f) for f in instantaneousDischargingTableData_raw], dtype=np.int16)

chargingTemperatureData = [ 0, 5, 10, 15, 20, 25, 45, 50, 55, 60 ]  
chargingMaxElements = [ 10, 11 ]

dischargingTemperatureData = [-10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60] 
dischargingMaxElements = [15, 11]

socData = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100] 


data = continuousChargingTableData + continuousDischargingTableData + instantaneousDischargingTableData + instantaneousChargingTableData +socData + chargingTemperatureData + dischargingTemperatureData + chargingMaxElements + dischargingMaxElements

# Pack the data
packed_data = struct.pack(f'{len(data)}h', *data)

# Calculate CRC over the data (not including the CRC itself)
crc = calculate_crc_sop(packed_data)
print(crc)

# Write data to file
with open("battery_data.bin", "wb") as f:
    f.write(packed_data)
    f.write(struct.pack('I', crc))

