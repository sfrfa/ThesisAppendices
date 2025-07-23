import os
import shutil

# Source and destination folders
SOURCE_FOLDER = '02_RawDataDay'
DESTINATION_FOLDER = '03_FixedRawDataDay'

# Ensure destination folder exists
os.makedirs(DESTINATION_FOLDER, exist_ok=True)

# List all files in the source folder
files = os.listdir(SOURCE_FOLDER)

for file_name in files:
    if not file_name.endswith('.csv'):
        continue

    original_file_path = os.path.join(SOURCE_FOLDER, file_name)

    if file_name.endswith('_fixed.csv'):
        # Remove '_fixed' from the filename for the fixed file
        new_file_name = file_name.replace('_fixed', '')

        # Construct destination path
        destination_file_path = os.path.join(DESTINATION_FOLDER, new_file_name)

        # Overwrite the existing file with the fixed version
        shutil.copy2(original_file_path, destination_file_path)
        print(f'Overwritten {new_file_name} with fixed version from {file_name}')
    
    else:
        # For non-fixed files, use the original name
        new_file_name = file_name

        # Construct destination path for non-fixed files
        destination_file_path = os.path.join(DESTINATION_FOLDER, new_file_name)

        # Copy non-fixed files (no overwrite)
        if not os.path.exists(destination_file_path):
            shutil.copy2(original_file_path, destination_file_path)
            print(f'Copied {file_name} to {new_file_name}')
        else:
            print(f'Skipping {file_name} as {new_file_name} already exists')

print('File copying process completed.')
