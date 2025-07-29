import os
import pandas as pd
import logging
from glob import glob

# Folder path
folder_path = '08_RawDataMonthWithTipo'

# Logging setup
log_file_path = os.path.join(folder_path, "tipo_descricao_update.log")
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Tipo description mapping
tipo_descricao_map = {
    "0": "Todos",
    "1": "Ajuste Direto Regime Geral",
    "2": "Concurso público",
    "3": "Concurso limitado por prévia qualificação",
    "4": "Procedimento de negociação",
    "5": "Diálogo concorrencial",
    "6": "Ao abrigo de acordo-quadro (art.º 258.º)",
    "7": "Ao abrigo de acordo-quadro (art.º 259.º)",
    "8": "Consulta Prévia",
    "9": "Parceria para a inovação",
    "10": "Disponibilização de bens móveis",
    "11": "Serviços sociais e outros serviços específicos",
    "13": "Concurso de conceção simplificado",
    "14": "Concurso de ideias simplificado",
    "15": "Consulta Prévia Simplificada",
    "16": "Concurso público simplificado",
    "17": "Concurso limitado por prévia qualificação simplificado",
    "18": "Ajuste Direto Regime Geral ao abrigo do artigo 7º da Lei n.º 30/2021, de 21.05",
    "19": "Consulta prévia ao abrigo do artigo 7º da Lei n.º 30/2021, de 21.05",
    "20": "Ajuste direto simplificado",
    "21": "Ajuste direto simplificado ao abrigo da Lei n.º 30/2021, de 21.05",
    "22": "Setores especiais – isenção parte II",
    "23": "Contratação excluída II"
}

# Process each CSV in the folder
csv_files = glob(os.path.join(folder_path, '*.csv'))

for file in csv_files:
    file_name = os.path.basename(file)
    try:
        df = pd.read_csv(file, sep=';', encoding='utf-8', on_bad_lines='skip')

        if 'Tipo' not in df.columns:
            logging.warning(f"'Tipo' column not found in {file_name}. Skipping.")
            continue

        # Convert 'Tipo' to string for safe mapping
        df['Tipo'] = df['Tipo'].astype(str)
        df['TipoDescricao'] = df['Tipo'].map(tipo_descricao_map).fillna("Desconhecido")

        # Overwrite original file
        df.to_csv(file, index=False, sep=';', encoding='utf-8')
        logging.info(f"Updated {file_name} with 'TipoDescricao'.")
        print(f"Updated {file_name} with 'TipoDescricao'.")

    except Exception as e:
        logging.error(f"Error processing {file_name}: {e}")
        print(f"Error processing {file_name}: {e}")
