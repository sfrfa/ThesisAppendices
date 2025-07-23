import os
import requests
import logging
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import urlencode
import sys

# Folders
DAILY_FOLDER = "06_RawDataDayMissingData"
LOG_FOLDER = "Logs"

# Ensure folders exist
os.makedirs(DAILY_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# Log files
LARGE_FILES_LOG = "error_files.log"
DAILY_LOG = os.path.join(LOG_FOLDER, "error_files.log")

# Base URL
BASE_URL = "https://www.base.gov.pt/Base4/pt/resultados/"

# HTTP headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
}

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_FOLDER, "script_log.log"), encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Generate daily date ranges within a given month
def generate_daily_dates(month_start):
    start = datetime.strptime(month_start, "%Y-%m-%d")
    end = start.replace(day=1) + timedelta(days=32)
    end = end.replace(day=1) - timedelta(days=1)

    return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]

# Fetch data

def fetch_data(params, output_path):
    try:
        url = BASE_URL + "?" + urlencode(params)
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200 and "text/csv" in response.headers.get("Content-Type", ""):
            with open(output_path, "wb") as f:
                f.write(response.content)
            return True
        else:
            logging.warning(f"Failed to download: {output_path}")
            return False
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return False

# Main function to process daily downloads

def process_daily_downloads():
    files_to_process = [
        "csv_resultados_2020-02-01_a_2020-03-01_distrito_13_concelho_182_tipo_1.csv",
        "csv_resultados_2022-01-01_a_2022-02-01_distrito_12_concelho_164_tipo_1.csv"
    ]

    for file in files_to_process:
        parts = file.replace(".csv", "").split("_")
        start_date = parts[2]
        end_date = parts[4]
        district = parts[6]
        municipality = parts[8]
        tipo = parts[10]

        daily_dates = generate_daily_dates(start_date)

        for day in daily_dates:
            output_file = os.path.join(DAILY_FOLDER, f"csv_resultados_{day}_a_{day}_distrito_{district}_concelho_{municipality}_tipo_{tipo}.csv")

            if os.path.exists(output_file):
                logging.info(f"File already exists: {output_file}")
                continue

            query_params = {
                "type": "csv_contratos",
                "tipo": tipo,
                "distrito": district,
                "concelho": municipality,
                "desdedatacontrato": day,
                "atedatacontrato": day,
            }

            success = fetch_data(query_params, output_file)
            if success:
                logging.info(f"Successfully downloaded: {output_file}")

# Run the script
if __name__ == "__main__":
    process_daily_downloads()
