import os
import pandas as pd
import logging
import sys

# Source and destination folders
SOURCE_FOLDER = '05_RawDataFinalMonth'
DESTINATION_FOLDER = '07_RawDataFinalMonthFixed'
LOG_FOLDER = 'Logs'
FAILED_LOG_FILE = os.path.join(LOG_FOLDER, 'failed_files.log')

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

# Helper function to log failed files
def log_failed_file(file_name, error_message):
    with open(FAILED_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"Failed to process {file_name}: {error_message}\n")

# Verify and fix CSV using pandas
def fix_csv(file_path, output_path, file_name):
    try:
        # Read the CSV using pandas, attempting with 'utf-8' encoding first
        df = pd.read_csv(file_path, sep=';', on_bad_lines='skip', encoding="utf-8")  # Try 'utf-8' first
        
        # Write the fixed CSV to the destination folder, maintaining the original title
        df.to_csv(output_path, index=False, sep=';', encoding="utf-8")  # Save in 'utf-8' encoding
        
        logging.info(f"Fixed and saved file: {output_path}")
        
    except UnicodeDecodeError:
        # If a UnicodeDecodeError occurs, try with 'latin1' encoding
        logging.warning(f"Unicode decode error for {file_name}. Trying 'latin1' encoding.")
        try:
            df = pd.read_csv(file_path, sep=';', on_bad_lines='skip', encoding="latin1")
            df.to_csv(output_path, index=False, sep=';', encoding="utf-8")
            logging.info(f"Fixed and saved file with 'latin1' encoding: {output_path}")
        except Exception as e:
            error_message = f"Error processing {file_name}: {e}"
            logging.error(error_message)
            log_failed_file(file_name, error_message)  # Log the failed file

    except Exception as e:
        error_message = f"Error processing {file_name}: {e}"
        logging.error(error_message)
        log_failed_file(file_name, error_message)  # Log the failed file

# Main function to process files
def process_files():
    files = os.listdir(SOURCE_FOLDER)

    for file_name in files:
        if not file_name.endswith('.csv'):
            continue

        source_file_path = os.path.join(SOURCE_FOLDER, file_name)
        destination_file_path = os.path.join(DESTINATION_FOLDER, file_name)

        logging.info(f"Processing file: {file_name}")

        try:
            # Process and save the fixed file, overwriting if it already exists
            fix_csv(source_file_path, destination_file_path, file_name)
        except Exception as e:
            # In case of failure, log the file name and error
            log_failed_file(file_name, str(e))

    logging.info('File processing completed.')

# Run the script
if __name__ == "__main__":
    process_files()
