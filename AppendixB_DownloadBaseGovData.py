import os
import requests
import logging
from datetime import datetime, timedelta
from urllib.parse import urlencode
import csv

# Create folders that don’t exist
raw_data_folder = "01_RawData"
logs_folder = os.path.join(raw_data_folder, "Logs")
os.makedirs(raw_data_folder, exist_ok=True)
os.makedirs(logs_folder, exist_ok=True)

# Logger configuration
log_file_path = os.path.join(logs_folder, "script_log.log")
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Base URL
BASE_URL = "https://www.base.gov.pt/Base4/pt/resultados/"

# Fixed search parameters
base_params = {
    "type": "csv_contratos",
    "tipo": "",
    "tipocontrato": "",
    "sel_price": "price_c1",
    "sel_date": "date_c1",
    "pais": "187",
    "distrito": "0",
    "concelho": "0",
}

# Value ranges for district and municipality
distritos_concelhos = {
    2: range(3, 22),
    3: range(23, 37),
    4: range(38, 52),
    5: range(53, 65),
    6: range(66, 77),
    7: range(78, 95),
    8: range(96, 110),
    9: range(111, 127),
    10: range(128, 142),
    11: range(143, 159),
    12: range(160, 176),
    13: range(177, 192),
    14: range(193, 211),
    15: range(212, 233),
    16: range(234, 247),
    17: range(248, 258),
    18: range(259, 273),
    19: range(274, 298),
    20: range(299, 318),
    21: range(319, 330),
    22: [0],
    23: [0],
    24: [0],
}

# Types of information from the portal
tipos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

# HTTP headers with User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
}

def fetch_data(params):
    try:
        url = BASE_URL + "?" + urlencode(params)
        print(f"URL: {url}")
        response = requests.get(url, headers=headers)

        if 300 <= response.status_code < 400:
            redirect_url = response.headers.get('Location')
            response = requests.get(redirect_url, headers=headers)

        debug_file_path = os.path.join(raw_data_folder, "debug_file.csv")
        with open(debug_file_path, "wb") as f:
            f.write(response.content)

        return response, url
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao obter dados: {e}")
        print(f"Erro fatal: {e}")
        return None, None

def verify_csv(output_file):
    try:
        with open(output_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            linhas = list(reader)
            num_registros = len(linhas) - 1
            if num_registros == 500:
                logging.info(f"The file {output_file} contains exactly 500 records.")
            else:
                logging.warning(f"The file {output_file} contains {num_registros} records, which is different from expected.")
    except Exception as e:
        logging.error(f"Error verifying CSV {output_file}: {e}")
        print(f"Erro fatal: {e}")

def download_csv(link, output_file):
    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()

        with open(output_file, "wb") as file:
            file.write(response.content)

        print(f"CSV file saved in: {output_file}")
        verify_csv(output_file)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error retrieving the CSV file: {e}")
        print(f"Fatal Error: {e}")

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
    data_fim=datetime(2024, 12, 31)
)

for desdedata, atedata in datas_pesquisa:
    for distrito, concelhos in distritos_concelhos.items():
        for concelho in concelhos:
            for tipo in tipos:
                params = base_params.copy()
                params.update({
                    "distrito": distrito,
                    "concelho": concelho,
                    "tipo": tipo,
                    "desdedatacontrato": desdedata,
                    "atedatacontrato": atedata,
                })

                print(f"Retrieving data: distrito={distrito}, concelho={concelho}, tipo={tipo}, período={desdedata} a {atedata}")

                try:
                    result, url2 = fetch_data(params)

                    if result and result.status_code == 200 and "text/csv" in result.headers.get("Content-Type", ""):
                        output_file = os.path.join(
                            raw_data_folder,
                            f"csv_resultados_{desdedata}_a_{atedata}_distrito_{distrito}_concelho_{concelho}_tipo_{tipo}.csv"
                        )
                        download_csv(url2, output_file)
                    else:
                        logging.warning(f"Invalid response for URL: {url2}. Content type: {result.headers.get('Content-Type')}")
                except Exception as e:
                    logging.error(f"Error processing distrito={distrito}, concelho={concelho}, tipo={tipo}, período={desdedata}-{atedata}: {e}")
                    continue
