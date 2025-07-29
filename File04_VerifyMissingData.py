import os
import requests
import logging
from datetime import datetime, timedelta
from urllib.parse import urlencode

# Basic configuration
BASE_FOLDER = "05_RawDataFinalMonth"
os.makedirs(BASE_FOLDER, exist_ok=True)

log_file = os.path.join("", "missing_files.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Base URL
BASE_URL = "https://www.base.gov.pt/Base4/pt/resultados/"

# HTTP headers with User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
}

# Value ranges for district and municipality
distritos_concelhos = {
    2: range(3, 22), 3: range(23, 37), 4: range(38, 52), 5: range(53, 65),
    6: range(66, 77), 7: range(78, 95), 8: range(96, 110), 9: range(111, 127),
    10: range(128, 142), 11: range(143, 159), 12: range(160, 176),
    13: range(177, 192), 14: range(193, 211), 15: range(212, 233),
    16: range(234, 247), 17: range(248, 258), 18: range(259, 273),
    19: range(274, 298), 20: range(299, 318), 21: range(319, 330),
    22: [0], 23: [0], 24: [0]
}

# Types of information from the portal
tipos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

# Function to generate monthly dates
def generate_monthly_dates(data_inicio, data_fim):
    datas = []
    data_atual = data_inicio
    while data_atual <= data_fim:
        prox_data = data_atual + timedelta(days=31)
        prox_data = prox_data.replace(day=1)
        datas.append((data_atual.strftime("%Y-%m-%d"), prox_data.strftime("%Y-%m-%d")))
        data_atual = prox_data
    return datas

datas_pesquisa = generate_monthly_dates(
    data_inicio=datetime(2015, 1, 1),
    data_fim=datetime(2024, 12, 1)
)

# Function to download data
def fetch_data(params):
    try:
        url = BASE_URL + "?" + urlencode(params)
        response = requests.get(url, headers=headers)

        if 300 <= response.status_code < 400:
            redirect_url = response.headers.get('Location')
            response = requests.get(redirect_url, headers=headers)

        debug_file_path = os.path.join(BASE_FOLDER, "debug_file_missingdata.csv")
        with open(debug_file_path, "wb") as f:
            f.write(response.content)

        return response, url
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        print(f"Fatal error: {e}")
        return None, None

# Loop to check each file
for desdedata, atedata in datas_pesquisa:
    for distrito, concelhos in distritos_concelhos.items():
        for concelho in concelhos:
            for tipo in tipos:
                file_name = f"csv_resultados_{desdedata}_a_{atedata}_distrito_{distrito}_concelho_{concelho}_tipo_{tipo}.csv"
                file_path = os.path.join(BASE_FOLDER, file_name)

                if os.path.exists(file_path):
                    print(f"[OK] File exists: {file_name}")
                else:
                    print(f"[FALTA] File missing: {file_name}. Starting download...")
                    logging.warning(f"File missing: {file_name}. Download...")

                    params = {
                        "type": "csv_contratos",
                        "tipo": tipo,
                        "tipocontrato": "",
                        "sel_price": "price_c1",
                        "sel_date": "date_c1",
                        "pais": "187",
                        "distrito": distrito,
                        "concelho": concelho,
                        "desdedatacontrato": desdedata,
                        "atedatacontrato": atedata,
                    }

                    response, url = fetch_data(params)

                    if response and response.status_code == 200 and "text/csv" in response.headers.get("Content-Type", ""):
                        with open(file_path, "wb") as f:
                            f.write(response.content)
                        print(f"[DOWNLOAD] File saved: {file_path}")
                        logging.info(f"Download file with sucess: {file_path}")
                    else:
                        print(f"[ERRO] Error downloding file: {file_name}")
                        logging.error(f"Error downloding file: {file_name}. URL: {url}")

print("\nVerification and download concluded.")
