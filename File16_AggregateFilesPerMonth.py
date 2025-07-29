import os
import pandas as pd
from glob import glob
from collections import defaultdict
import logging
from datetime import datetime

# Input and output folders
input_folder = '09_RawDataMonthWithCounty'
output_folder = '10_RawDataMonthWithDistrict'
os.makedirs(output_folder, exist_ok=True)

# Setup logging
log_file_path = os.path.join(output_folder, "processing_log.log")
logging.basicConfig(filename=log_file_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Distrito mapping
distrito_names = {
    "0": "Todos",
    "2": "Aveiro",
    "3": "Beja",
    "4": "Braga",
    "5": "Braganca",
    "6": "Castelo Branco",
    "7": "Coimbra",
    "8": "Évora",
    "9": "Faro",
    "10": "Guarda",
    "11": "Leiria",
    "12": "Lisboa",
    "13": "Portalegre",
    "14": "Porto",
    "15": "Santarém",
    "16": "Setúbal",
    "17": "Viana do Castelo",
    "18": "Vila Real",
    "19": "Viseu",
    "20": "Região Autónoma dos Açores",
    "21": "Região Autónoma da Madeira",
    "22": "Portugal Continental",
    "23": "Distrito não determinado",
    "24": "Consulado situados no estrangeiro"
}

# Group files by (start_date, end_date)
file_groups = defaultdict(list)

for file in glob(os.path.join(input_folder, '*.csv')):
    file_name = os.path.basename(file)
    file_stem = os.path.splitext(file_name)[0]  # Remove .csv
    parts = file_stem.split('_')

    if len(parts) < 7:
        logging.warning(f"Skipping file with unexpected format: {file_name}")
        continue

    desdedata = parts[2]
    atedata = parts[4]

    # Validate dates
    try:
        datetime.strptime(desdedata, "%Y-%m-%d")
        datetime.strptime(atedata, "%Y-%m-%d")
    except ValueError:
        logging.warning(f"Invalid date format in filename: {file_name}")
        continue

    distrito = parts[6]

    key = (desdedata, atedata)
    file_groups[key].append(file)

# Merge files per month
for (desdedata, atedata), files in file_groups.items():
    merged_df = pd.DataFrame()

    for file in files:
        file_name = os.path.basename(file)
        try:
            df = pd.read_csv(file, sep=';', encoding='utf-8', on_bad_lines='skip')

            # Get district ID from filename (remove .csv)
            district_id_str = os.path.splitext(file_name.split('_')[-1])[0]

            if district_id_str not in distrito_names:
                logging.warning(f"Invalid or unknown district ID in file: {file_name}")
                continue

            df['DistritoId'] = district_id_str
            df['DistritoNome'] = distrito_names[district_id_str]

            merged_df = pd.concat([merged_df, df], ignore_index=True)
            logging.info(f"Loaded {file_name} with {len(df)} rows.")
            print(f"Loaded {file_name} with {len(df)} rows.")
        except Exception as e:
            logging.error(f"Failed to process {file_name}: {e}")
            print(f"Failed to process {file_name}: {e}")

    # Save merged file without distrito in filename
    output_filename = f"csv_resultados_{desdedata}_a_{atedata}.csv"
    output_path = os.path.join(output_folder, output_filename)

    try:
        merged_df.to_csv(output_path, index=False, sep=';', encoding='utf-8')
        logging.info(f"Saved merged file: {output_filename} with {len(merged_df)} rows.")
        print(f"Saved merged file: {output_filename} with {len(merged_df)} rows.")
    except Exception as e:
        logging.error(f"Failed to save {output_filename}: {e}")
        print(f"Failed to save {output_filename}: {e}")
