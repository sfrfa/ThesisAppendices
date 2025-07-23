import os
import pandas as pd
from glob import glob
from collections import defaultdict
from datetime import datetime
import logging

# Paths
input_folder = '10_RawDataMonthWithDistrict'
output_folder = '11_RawDataYear'
os.makedirs(output_folder, exist_ok=True)

# Setup logging
log_file_path = os.path.join(output_folder, "yearly_merge_log.log")
logging.basicConfig(filename=log_file_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Group files by year (from start date in filename)
year_groups = defaultdict(list)

for file in glob(os.path.join(input_folder, '*.csv')):
    file_name = os.path.basename(file)
    parts = file_name.split('_')
    
    if len(parts) < 4:
        logging.warning(f"Skipping file with unexpected format: {file_name}")
        continue

    try:
        start_date = parts[2]
        year = datetime.strptime(start_date, "%Y-%m-%d").year
    except ValueError:
        logging.warning(f"Invalid date format in filename: {file_name}")
        continue

    year_groups[year].append(file)

# Merge files per year
for year, files in year_groups.items():
    merged_df = pd.DataFrame()
    
    for file in files:
        try:
            df = pd.read_csv(file, sep=';', encoding='utf-8', on_bad_lines='skip',dtype={26: str}, low_memory=False)
            merged_df = pd.concat([merged_df, df], ignore_index=True)
            logging.info(f"Loaded {file} with {len(df)} rows.")
            print(f"Loaded {file} with {len(df)} rows.")
        except Exception as e:
            logging.error(f"Failed to process {file}: {e}")
            print(f"Failed to process {file}: {e}")

    output_file = f"csv_resultados_{year}.csv"
    output_path = os.path.join(output_folder, output_file)

    try:
        merged_df.to_csv(output_path, index=False, sep=';', encoding='utf-8')
        logging.info(f"Saved merged file: {output_file} with {len(merged_df)} rows.")
        print(f"Saved merged file: {output_file} with {len(merged_df)} rows.")
    except Exception as e:
        logging.error(f"Failed to save {output_file}: {e}")
        print(f"Failed to save {output_file}: {e}")
