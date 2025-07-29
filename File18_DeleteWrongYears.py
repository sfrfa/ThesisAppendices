import os
import pandas as pd
from glob import glob
from datetime import datetime

# Input and output folders
input_folder = '11_RawDataYear'
output_folder = '13_RawDataYearsCorrect'
os.makedirs(output_folder, exist_ok=True)

# Function to extract year from contract date string
def extract_year(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").year
    except Exception as e:
        print(f"Error extracting year from date string {date_str}: {e}")
        return None

# Process each file
for file_path in glob(os.path.join(input_folder, "*.csv")):
    file_name = os.path.basename(file_path)
    
    # Extract year from filename, e.g., csv_resultados_2015.csv → 2015
    try:
        year = int(file_name.split("_")[2].split(".")[0])
    except (IndexError, ValueError):
        print(f"Skipping file with unexpected name format: {file_name}")
        continue

    # Load file with proper encoding handling
    try:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8', on_bad_lines='skip', low_memory=False)
    except UnicodeDecodeError:
        print(f"Unicode decode error for {file_name}, trying ISO-8859-1 encoding.")
        try:
            df = pd.read_csv(file_path, sep=';', encoding='ISO-8859-1', on_bad_lines='skip', low_memory=False)
        except Exception as e:
            print(f"Error reading {file_name} with ISO-8859-1 encoding: {e}")
            continue
    except Exception as e:
        print(f"Error reading {file_name}: {e}")
        continue

    if 'Data de Celebração do Contrato' not in df.columns:
        print(f"'Data de Celebração do Contrato' column missing in {file_name}")
        continue

    # Ensure the 'Data de Celebração do Contrato' column is parsed as datetime
    try:
        df['Data de Celebração do Contrato'] = pd.to_datetime(df['Data de Celebração do Contrato'], errors='coerce', dayfirst=True)
    except Exception as e:
        print(f"Error converting 'Data de Celebração do Contrato' to datetime in {file_name}: {e}")
        continue

    # Filter rows where the contract year matches the filename year
    df['AnoContrato'] = df['Data de Celebração do Contrato'].dt.year
    df_filtered = df[df['AnoContrato'] == year].drop(columns=['AnoContrato'])

    # Check if filtered dataframe has rows
    if df_filtered.empty:
        print(f"No data found for year {year} in {file_name}. Skipping file.")
        continue

    # Save the cleaned file
    output_path = os.path.join(output_folder, file_name)
    
    # Check if the file already exists in the destination folder
    if os.path.exists(output_path):
        print(f"File {file_name} already exists in the output folder. Skipping saving.")
    else:
        df_filtered.to_csv(output_path, index=False, sep=';', encoding='utf-8')
        print(f"Saved {file_name} with {len(df_filtered)} valid rows.")
    
print("Processing completed.")
