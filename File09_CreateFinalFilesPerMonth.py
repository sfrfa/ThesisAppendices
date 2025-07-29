import os
import shutil
import logging
import sys

# Define folder paths
RAW_DATA_FOLDER = '01_RawData'
FIXED_MONTH_FOLDER = '04_FixedRawDataMonth'
FINAL_MONTH_FOLDER = '05_RawDataFinalMonth'
LOG_FOLDER = 'Logs'

# Ensure the destination folder exists
os.makedirs(FINAL_MONTH_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# Log files
COPY_LOG = os.path.join(LOG_FOLDER, "copy_overwrite_log.log")
COPIED_FILES_LOG = os.path.join(LOG_FOLDER, "copied_files.log")

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(COPY_LOG, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)  # Logs to console
    ]
)

def log_copied_file(file_name, action):
    log_message = f"{file_name} - {action}"
    
    # Log to the copied files log
    with open(COPIED_FILES_LOG, "a", encoding="utf-8") as log_file:
        log_file.write(log_message + "\n")
    
    # Log to console and main log file
    logging.info(log_message)

def copy_files(source_folder, destination_folder, overwrite=False):
    files = os.listdir(source_folder)
    for file_name in files:
        source_file = os.path.join(source_folder, file_name)
        destination_file = os.path.join(destination_folder, file_name)
        
        if not os.path.isfile(source_file):
            continue
        
        if os.path.exists(destination_file):
            if overwrite:
                action = "Overwritten"
            else:
                action = "Skipped (Already Exists)"
                log_copied_file(file_name, action)
                continue
        else:
            action = "Copied"

        try:
            shutil.copy2(source_file, destination_file)
            log_copied_file(file_name, action)
        except Exception as e:
            logging.error(f"Error copying {file_name}: {e}")

if __name__ == "__main__":
    logging.info("Starting file copying process...")

    # Clear the copied files log before each run
    open(COPIED_FILES_LOG, "w").close()
    
    # Step 1: Copy all files from 01_RawData to 05_RawDataFinalMonth
    logging.info("Copying files from 01_RawData to 05_RawDataFinalMonth...")
    copy_files(RAW_DATA_FOLDER, FINAL_MONTH_FOLDER, overwrite=False)
    
    # Step 2: Copy all files from 04_FixedRawDataMonth to 05_RawDataFinalMonth (Overwriting)
    logging.info("Copying files from 04_FixedRawDataMonth to 05_RawDataFinalMonth (Overwriting)...")
    copy_files(FIXED_MONTH_FOLDER, FINAL_MONTH_FOLDER, overwrite=True)
    
    logging.info("File copying process completed successfully.")
