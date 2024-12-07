import csv
def add_slashes_before_key_in_string(input_string, key_to_find, num_slashes):
    try:
        # Temporarily replace all occurrences of \\n and \\" with placeholders
        input_string = input_string.replace('\\n\\"', '__NEWLINE__').replace('\\"', '__QUOTE__')

        # Find the key in the string
        key_index = input_string.find(f'"{key_to_find}":')
        
        if key_index == -1:
            print(f"The key '{key_to_find}' was not found in the string.")
            return
        
        # Add the specified number of backslashes before the key
        new_key = "\\" * num_slashes + f'"{key_to_find}"'  # Add backslashes to the key
        
        # Replace the original key with the new key containing backslashes
        modified_string = input_string[:key_index] + new_key + input_string[key_index + len(f'"{key_to_find}":'):]
        
        # Restore the original \\n and \\" sequences
        # modified_string = modified_string.replace('__NEWLINE__', '\\n\\"').replace('__QUOTE__', '\\"')

        # Print the modified string
        print(modified_string)
    
    except Exception as e:
        print(f"An error occurred: {e}")

# the input string should be from the
input_string = '{\"csv_data\":\"13107712,2,18,167,3550,3127,3127,10,200,180000,1000,40,50,5,45,155,500,3420,3550,3380,120,60,103,185,180,185,180,500,500,500,80,90,400,100,200,55,52,50,55,52,50,0,2,5,0,2,5,95,92,90,95,92,90,0,2,5,0,2,5,200,100,2500,1,1250,4,2193279737\n\",\"binary_data\":\"AAAAAAAAAAAAAAAAAAAAAAAAAAAAABgAGAAYABgAGAAYABgAGAAYABgAFAA8ADwAPAA8ADwAPAA8ADwAPAA8ACgAZABkAGQAZABkAGQAZABkAGQAZAAoAMgAyADIAMgAyADIAMgAyADIAJYAPADIAMgAyADIAMgAyADIAMgAyACgAKAAyADIAMgAyADIAMgAyADIAMgAoACgAKAAoACgAKAAoACgAKAAoACgAKAAPAA8ADwAPAA8ADwAPAA8ADwAPAA8ACgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACgAPABQAGQAZABkAGQAZABkAGQAZAA8AGQAeACgAKAAoACgAKAAoACgAKAAPABkAHgAoACgAKAAoACgAKAAoACgADwAZAB4AKAAoACgAKAAoACgAKAAoAA8AGQAeACgAKAAoACgAKAAoACgAKAAZAB4AJYAyADIAMgAyADIAMgAyADIAGQAeACWAMgAyADIAMgAyADIAMgAyABkAHgAlgDIAMgAyADIAMgAyADIAMgAZAB4AJYAyADIAMgAyADIAMgAyADIAGQAeACWAMgAyADIAMgAyADIAMgAyABkAHgAlgDIAMgAyADIAMgAyADIAMgAZAB4AJYAyADIAMgAyADIAMgAyADIADwAZAB4AKAAoACgAKAAoACgAKAAoAAUAB4AKAA8ADwAPAA8ADwAPAA8ADwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACgAPABQAMgAyADIAMgAyADIAMgAyAA8AGQAeADwAPAA8ADwAPAA8ADwAPAAPABkAMgALAEsASwBLAEsASwBLAEsATwAZADIACwBLAEsASwBLAEsASwBLAE8AGQAyAAsASwBLAEsASwBLAEsASwBZADIAPAALAEsASwBLAEsASwBLAEsAcgAyADwACwBLAEsASwBLAEsASwBLAHIAMgALAEsASwBLAEsASwBLAEsASwByADIACwBLAEsASwBLAEsASwBLAEsAcgAyAAsASwBLAEsASwBLAEsASwBLAHIAMgALAEsASwBLAEsASwBLAEsASwByADIACwBLAEsASwBLAEsASwBLAEsAcgAyAAsASwBLAEsASwBLAEsASwBLAEUADwAeADwAPAA8ADwAPAA8ADwAPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABQAFAAUABQAFAAUABQAFAAUABQABQAoACgAKAAoACgAKAAoACgAKAAoAAoAPAA8ADwAPAA8ADwAPAA8ADwAPAAKAAsASwBLAEsASwBLAEsASwBLAEsATwALAEsASwBLAEsASwBLAEsASwBLAGgACwBLAEsASwBLAEsASwBLAEsASwBoAAsASwBLAEsASwBLAEsASwBLAEsATwA8ADwAPAA8ADwAPAA8ADwAPAA8AAoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoAFAAeACgAMgA8AEYAUABaAGQAAAAFAAoADwAUABkALQAyADcAPAD2//v/AAAFAAoADwAUABkAHgAjACgALQAyADcAPAAKAAsADwALADASEsA=\"}'
# Find the index of `"binary_data"`
x = input_string.find("\"binary_data\"")
print("Index of '\"binary_data\"':", x)
slashes = "\\" * 5
# To add a value at x-1 index, we can create a new string by slicing and concatenating
val = f"\\n\",{slashes}"
modified_string = input_string[:x-3] + val + input_string[x:]
# modified_string = input_string[:x-1] + "\\n" + input_string[x:]
string_val = modified_string.replace('"', '\\"')
save_path = "new.csv"

with open("output.txt", "w") as file:
    file.write(string_val)

print("Modified string:", string_val)

# add_slashes_before_key_in_string(input_string, key_to_find, num_slashes)
