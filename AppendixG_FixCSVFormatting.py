import os
import pandas as pd
import logging
import sys

# Source and destination folders
SOURCE_FOLDER = '05_RawDataFinalMonth'
DESTINATION_FOLDER = '07_RawDataFinalMonthFixed'
LOG_FOLDER = 'Logs'

# Ensure folders exist
os.makedirs(DESTINATION_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_FOLDER, "fixing_script_month_log.log"), encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Verify and fix CSV using pandas
def fix_csv(file_path, output_path):
    try:
        # Read the CSV using pandas, attempting with 'latin1' or 'utf-8' encoding
        df = pd.read_csv(file_path, sep=';', on_bad_lines='skip', encoding="utf-8")  # Try 'utf-8' first
        
        # Write the fixed CSV to the destination folder, maintaining the original title
        df.to_csv(output_path, index=False, sep=';', encoding="utf-8")  # Save in 'utf-8' encoding
        
        logging.info(f"Fixed and saved file: {output_path}")
        
    except UnicodeDecodeError:
        # If a UnicodeDecodeError occurs, try with 'latin1' encoding
        logging.warning(f"Unicode decode error for {file_path}. Trying 'latin1' encoding.")
        try:
            df = pd.read_csv(file_path, sep=';', on_bad_lines='skip', encoding="latin1")
            df.to_csv(output_path, index=False, sep=';', encoding="utf-8")
            logging.info(f"Fixed and saved file with 'latin1' encoding: {output_path}")
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")
    
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")

# Main function to process files
def process_files():
    files = os.listdir(SOURCE_FOLDER)

    for file_name in files:
        if not file_name.endswith('.csv'):
            continue

        source_file_path = os.path.join(SOURCE_FOLDER, file_name)
        destination_file_path = os.path.join(DESTINATION_FOLDER, file_name)

        # Check if the file has already been processed
        if os.path.exists(destination_file_path):
            logging.info(f"File {file_name} already exists in the destination folder. Skipping processing.")
            continue  # Skip processing this file

        logging.info(f"Processing file: {file_name}")

        # Process and save the fixed file
        fix_csv(source_file_path, destination_file_path)

    logging.info('File processing completed.')

# Run the script
if __name__ == "__main__":
    process_files()
