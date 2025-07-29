import os
import logging

# Base folder where the CSV files are stored
BASE_FOLDER = "01_RawData"

# Log files for different categories
LARGE_FILES_LOG = "large_files.log"  # Files with more than 500 rows
SMALL_FILES_LOG = "small_files.log"  # Files with 500 rows or less

# Configure logging to log both to a file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("file_check.log"),  # Save logs to a file
        logging.StreamHandler()  # Also print logs to the console
    ]
)

# Function to check the number of rows in CSV files
def check_files():
    if not os.path.exists(BASE_FOLDER):
        logging.error(f"[ERROR] Folder not found: {BASE_FOLDER}")
        print(f"[ERROR] Folder not found: {BASE_FOLDER}")
        return

    print("Checking files for row count...\n")
    logging.info("Starting file row count check...")

    # Open logs in append mode so they persist between runs
    with open(LARGE_FILES_LOG, "a", encoding="utf-8") as large_log, open(SMALL_FILES_LOG, "a", encoding="utf-8") as small_log:
        for file_name in os.listdir(BASE_FOLDER):
            file_path = os.path.join(BASE_FOLDER, file_name)

            # Ensure it's a file and a CSV
            if not os.path.isfile(file_path) or not file_name.endswith(".csv"):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    row_count = sum(1 for line in f)

                if row_count > 500:
                    message = f"[LARGE] {file_name} has {row_count} rows."
                    print(message)
                    logging.info(message)
                    large_log.write(f"{file_name} - {row_count} rows\n")
                    large_log.flush()
                else:
                    message = f"[SMALL] {file_name} has {row_count} rows."
                    print(message)
                    logging.info(message)
                    small_log.write(f"{file_name} - {row_count} rows\n")
                    small_log.flush()

            except Exception as e:
                error_message = f"[ERROR] Failed to read {file_name}: {e}"
                print(error_message)
                logging.error(error_message)

    print("\nFile verification completed.")
    logging.info("File verification completed.")

# Run the check
check_files()
