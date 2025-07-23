import os
import pandas as pd
import logging
import sys
from datetime import datetime
from collections import defaultdict

# Source and destination folders
SOURCE_FOLDER = '03_FixedRawDataDay'
DESTINATION_FOLDER = '04_FixedRawDataMonth'
LOG_FOLDER = 'Logs'

# Ensure folders exist
os.makedirs(DESTINATION_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_FOLDER, "monthly_concat_log.log"), encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Group files by month, district, municipality, and type
def group_files_by_month(files):
    grouped_files = defaultdict(list)
    
    for file_name in files:
        if not file_name.endswith('.csv'):
            continue
        
        parts = file_name.replace(".csv", "").split("_")
        
        if len(parts) != 11:  # Checking for exactly 11 parts
            logging.warning(f"Skipping file with unexpected format: {file_name}")
            continue

        # Extract relevant information
        start_date = parts[2]
        district = parts[6]
        municipality = parts[8]
        data_type = parts[10]
        
        try:
            # Get the month and year from the start date
            month_year = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m")
            
            # Group by month, district, municipality, and type
            key = (month_year, district, municipality, data_type)
            grouped_files[key].append(file_name)
        
        except ValueError:
            logging.warning(f"Skipping file with invalid date format: {file_name}")

    return grouped_files

# Concatenate CSV files by group and save them
def process_groups(grouped_files):
    for (month_year, district, municipality, data_type), files in grouped_files.items():
        data_frames = []
        
        for file_name in files:
            file_path = os.path.join(SOURCE_FOLDER, file_name)
            try:
                df = pd.read_csv(file_path, sep=';', encoding="utf-8")
                data_frames.append(df)
                logging.info(f"Loaded file: {file_name}")
            except Exception as e:
                logging.error(f"Failed to read file {file_name}: {e}")
        
        if data_frames:
            # Concatenate all DataFrames
            merged_df = pd.concat(data_frames, ignore_index=True)

            # Generate output file name
            start_date = f"{month_year}-01"
            end_date = (pd.to_datetime(start_date) + pd.DateOffset(months=1)).strftime("%Y-%m-%d")
            output_file_name = f"csv_resultados_{start_date}_a_{end_date}_distrito_{district}_concelho_{municipality}_tipo_{data_type}.csv"
            output_file_path = os.path.join(DESTINATION_FOLDER, output_file_name)
            
            # Save the concatenated file
            merged_df.to_csv(output_file_path, index=False, sep=';', encoding="utf-8")
            logging.info(f"Saved merged file: {output_file_name}")

# Main function
def process_files():
    files = os.listdir(SOURCE_FOLDER)
    
    grouped_files = group_files_by_month(files)
    process_groups(grouped_files)
    
    logging.info('Monthly file processing completed.')

# Run the script
if __name__ == "__main__":
    process_files()
