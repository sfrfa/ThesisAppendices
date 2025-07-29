import os
import pandas as pd
from glob import glob
import logging

# Path settings
input_folder = '07_RawDataFinalMonthFixed'
output_folder = '08_RawDataMonthWithTipo'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Logger configuration
log_file_path = os.path.join(output_folder, "processing_log.log")
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Group files by (start_date, end_date, distrito, concelho)
from collections import defaultdict
file_groups = defaultdict(list)

# Organize files by group
for file in glob(os.path.join(input_folder, '*.csv')):
    file_name = os.path.basename(file)
    parts = file_name.split('_')
    
    if len(parts) < 11:
        logging.warning(f"Skipping file with unexpected format: {file_name}")
        continue

    desdedata = parts[2]
    atedata = parts[4]
    distrito = parts[6]
    concelho = parts[8]
    tipo = parts[10].split('.')[0]

    key = (desdedata, atedata, distrito, concelho)
    file_groups[key].append((file, tipo))

# Process each group
for (desdedata, atedata, distrito, concelho), files in file_groups.items():
    combined_df = pd.DataFrame()

    for file, tipo in files:
        file_name = os.path.basename(file)
        try:
            df = pd.read_csv(file, sep=';', encoding='utf-8', on_bad_lines='skip')
            df['Tipo'] = tipo
            combined_df = pd.concat([combined_df, df], ignore_index=True)
            logging.info(f"Loaded {file_name} with {len(df)} rows.")
            print(f"Loaded {file_name} with {len(df)} rows.")
        except Exception as e:
            logging.error(f"Failed to process {file_name}: {e}")
            print(f"Failed to process {file_name}: {e}")
            continue

    output_filename = f"csv_resultados_{desdedata}_a_{atedata}_distrito_{distrito}_concelho_{concelho}.csv"
    output_path = os.path.join(output_folder, output_filename)

    try:
        combined_df.to_csv(output_path, index=False, sep=';', encoding='utf-8')
        logging.info(f"Saved combined file: {output_filename} with {len(combined_df)} rows.")
        print(f"Saved combined file: {output_filename} with {len(combined_df)} rows.")
    except Exception as e:
        logging.error(f"Failed to save {output_filename}: {e}")
        print(f"Failed to save {output_filename}: {e}")
