import os
import pandas as pd
from glob import glob
import logging
from collections import defaultdict

# Path settings
input_folder = '08_RawDataMonthWithTipo'
output_folder = '09_RawDataMonthWithCounty'

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Logging
log_file_path = os.path.join(output_folder, "processing_log.log")
logging.basicConfig(filename=log_file_path, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Concelho descriptions
concelho_descriptions = {
    "3": "Águeda", "4": "Albergaria-a-Velha", "5": "Anadia", "6": "Arouca", "7": "Aveiro",
    "8": "Castelo de Paiva", "9": "Espinho", "10": "Estarreja", "11": "Santa Maria da Feira",
    "12": "Ílhavo", "13": "Mealhada", "14": "Murtosa", "15": "Oliveira de Azemeis",
    "16": "Oliveira do Bairro", "17": "Ovar", "18": "São João da Madeira", "19": "Sever do Vouga",
    "20": "Vagos", "21": "Vale de Cambra", "23": "Aljustrel", "24": "Almodovar", "25": "Alvito",
    "26": "Barrancos", "27": "Beja", "28": "Castro Verde", "29": "Cuba", "30": "Ferreira do Alentejo",
    "31": "Mértola", "32": "Moura", "33": "Odemira", "34": "Ourique", "35": "Serpa", "36": "Vidigueira",
    "38": "Amares", "39": "Barcelos", "40": "Braga", "41": "Cabeceiras de Basto",
    "42": "Celorico de Basto", "43": "Esposende", "44": "Fafe", "45": "Guimarães",
    "46": "Póvoa de Lanhoso", "47": "Terras de Bouro", "48": "Vieira do Minho",
    "49": "Vila Nova de Famalicão", "50": "Vila Verde", "51": "Vizela", "53": "Alfandega da Fé",
    "54": "Bragança", "55": "Carrazeda de Ansiães", "56": "Freixo Espada a Cinta",
    "57": "Macedo de Cavaleiros", "58": "Miranda do Douro", "59": "Mirandela", "60": "Mogadouro",
    "61": "Torre de Moncorvo", "62": "Vila Flor", "63": "Vimioso", "64": "Vinhais", "66": "Belmonte",
    "67": "Castelo Branco", "68": "Covilhã", "69": "Fundão", "70": "Idanha-a-Nova", "71": "Oleiros",
    "72": "Penamacor", "73": "Proença-a-Nova", "74": "Sertã", "75": "Vila de Rei",
    "76": "Vila Velha de Ródão", "78": "Arganil", "79": "Cantanhede", "80": "Coimbra",
    "81": "Condeixa-a-Nova", "82": "Figueira da Foz", "83": "Góis", "84": "Lousã", "85": "Mira",
    "86": "Miranda do Corvo", "87": "Montemor-o-Velho", "88": "Oliveira do Hospital",
    "89": "Pampilhosa da Serra", "90": "Penacova", "91": "Penela", "92": "Soure", "93": "Tábua",
    "94": "Vila Nova de Poiares", "96": "Alandroal", "97": "Arraiolos", "98": "Borba", "99": "Estremoz",
    "100": "Évora", "101": "Montemor-o-Novo", "102": "Mora", "103": "Mourão", "104": "Portel",
    "105": "Redondo", "106": "Reguengos de Monsaraz", "107": "Vendas Novas",
    "108": "Viana do Alentejo", "109": "Vila Viçosa", "111": "Albufeira", "112": "Alcoutim",
    "113": "Aljezur", "114": "Castro Marim", "115": "Faro", "116": "Lagoa", "117": "Lagos",
    "118": "Loulé", "119": "Monchique", "120": "Olhão", "121": "Portimão",
    "122": "São Brás de Alportel", "123": "Silves", "124": "Tavira", "125": "Vila do Bispo",
    "126": "Vila Real Sto Antonio", "128": "Aguiar da Beira", "129": "Almeida",
    "130": "Celorico da Beira", "131": "Fig. Castelo Rodrigo", "132": "Fornos de Algodres",
    "133": "Gouveia", "134": "Guarda", "135": "Manteigas", "136": "Meda", "137": "Pinhel",
    "138": "Sabugal", "139": "Seia", "140": "Trancoso", "141": "Vila Nova de Foz Coa",
    "143": "Alcobaça", "144": "Alvaiázere", "145": "Ansião", "146": "Batalha",
    "147": "Bombarral", "148": "Caldas da Rainha", "149": "Castanheira de Pera",
    "150": "Figueiró dos Vinhos", "151": "Leiria", "152": "Marinha Grande", "153": "Nazaré",
    "154": "Óbidos", "155": "Pedrogão Grande", "156": "Peniche", "157": "Pombal",
    "158": "Porto de Mós", "160": "Alenquer", "161": "Arruda dos Vinhos", "162": "Azambuja",
    "163": "Cadaval", "164": "Cascais", "165": "Lisboa", "166": "Loures", "167": "Lourinhã",
    "168": "Mafra", "169": "Oeiras", "170": "Sintra", "171": "Sobral de Monte Agraço",
    "172": "Torres Vedras", "173": "Vila Franca de Xira", "174": "Amadora", "175": "Odivelas",
    "177": "Alter do Chão", "178": "Arronches", "179": "Avis", "180": "Campo Maior",
    "181": "Castelo de Vide", "182": "Crato", "183": "Elvas", "184": "Fronteira", "185": "Gavião",
    "186": "Marvão", "187": "Monforte", "188": "Nisa", "189": "Ponte de Sor",
    "190": "Portalegre", "191": "Sousel", "193": "Amarante", "194": "Baião", "195": "Felgueiras",
    "196": "Gondomar", "197": "Lousada", "198": "Maia", "199": "Marco de Canaveses",
    "200": "Matosinhos", "201": "Paços de Ferreira", "202": "Paredes", "203": "Penafiel",
    "204": "Porto", "205": "Póvoa de Varzim", "206": "Santo Tirso", "207": "Valongo",
    "208": "Vila do Conde", "209": "Vila Nova de Gaia", "210": "Trofa", "212": "Abrantes",
    "213": "Alcanena", "214": "Almeirim", "215": "Alpiarça", "216": "Benavente",
    "217": "Cartaxo", "218": "Chamusca", "219": "Constancia", "220": "Coruche",
    "221": "Entroncamento", "222": "Ferreira do Zezere", "223": "Golegã", "224": "Mação",
    "225": "Rio Maior", "226": "Salvaterra de Magos", "227": "Santarém", "228": "Sardoal",
    "229": "Tomar", "230": "Torres Novas", "231": "Vila Nova da Barquinha", "232": "Ourém",
    "234": "Alcácer do Sal", "235": "Alcochete", "236": "Almada", "237": "Barreiro",
    "238": "Grandola", "239": "Moita", "240": "Montijo", "241": "Palmela",
    "242": "Santiago do Cacém", "243": "Seixal", "244": "Sesimbra", "245": "Setúbal",
    "246": "Sines", "248": "Arcos de Valdevez", "249": "Caminha", "250": "Melgaço",
    "251": "Monção", "252": "Paredes de Coura", "253": "Ponte da Barca",
    "254": "Ponte de Lima", "255": "Valença", "256": "Viana do Castelo",
    "257": "Vila Nova de Cerveira", "259": "Alijó", "260": "Boticas", "261": "Chaves",
    "262": "Mesão Frio", "263": "Mondim de Basto", "264": "Montalegre", "265": "Murça",
    "266": "Peso da Régua", "267": "Ribeira de Pena", "268": "Sabrosa",
    "269": "Sta Marta de Penaguião", "270": "Valpaços", "271": "Vila Pouca de Aguiar",
    "272": "Vila Real", "274": "Armamar", "275": "Carregal do Sal", "276": "Castro Daire",
    "277": "Cinfães", "278": "Lamego", "279": "Mangualde", "280": "Moimenta da Beira",
    "281": "Mortágua", "282": "Nelas", "283": "Oliveira de Frades",
    "284": "Penalva do Castelo", "285": "Penedono", "286": "Resende", "287": "Santa Comba Dão",
    "288": "São João da Pesqueira", "289": "São Pedro do Sul", "290": "Sátão",
    "291": "Sernancelhe", "292": "Tabuaço", "293": "Tarouca", "294": "Tondela",
    "295": "Vila Nova de Paiva", "296": "Viseu", "297": "Vouzela", "299": "Angra do Heroismo",
    "300": "Calheta", "301": "Santa Cruz da Graciosa", "302": "Velas", "303": "Praia da Vitória",
    "304": "Corvo", "305": "Horta", "306": "Lajes das Flores", "307": "Lajes do Pico",
    "308": "Madalena", "309": "Santa Cruz das Flores", "310": "São Roque do Pico",
    "311": "Lagoa", "312": "Nordeste", "313": "Ponta Delgada", "314": "Povoação",
    "315": "Ribeira Grande", "316": "Vila Franca do Campo", "317": "Vila do Porto",
    "319": "Calheta", "320": "Câmara de Lobos", "321": "Funchal", "322": "Machico",
    "323": "Ponta do Sol", "324": "Porto Moniz", "325": "Porto Santo", "326": "Ribeira Brava",
    "327": "Santa Cruz", "328": "Santana", "329": "São Vicente"
}

# Group files by (start_date, end_date, distrito)
file_groups = defaultdict(list)

for file in glob(os.path.join(input_folder, '*.csv')):
    file_name = os.path.basename(file)
    parts = file_name.split('_')

    if len(parts) < 9:
        logging.warning(f"Skipping file with unexpected format: {file_name}")
        continue

    desdedata = parts[2]
    atedata = parts[4]
    distrito = parts[6]
    concelho = parts[8].split('.')[0]

    key = (desdedata, atedata, distrito)
    file_groups[key].append((file, concelho))

# Merge per group (no aggregation)
for (desdedata, atedata, distrito), file_concelhos in file_groups.items():
    combined_df = pd.DataFrame()

    for file, concelho in file_concelhos:
        file_name = os.path.basename(file)
        try:
            df = pd.read_csv(file, sep=';', encoding='utf-8', on_bad_lines='skip')
            df['ConcelhoId'] = concelho
            df['ConcelhoNome'] = concelho_descriptions.get(concelho, f"Unknown ({concelho})")
            df['DistritoId'] = distrito
            combined_df = pd.concat([combined_df, df], ignore_index=True)

            logging.info(f"Loaded {file_name} with {len(df)} rows.")
            print(f"Loaded {file_name} with {len(df)} rows.")
        except Exception as e:
            logging.error(f"Failed to process {file_name}: {e}")
            print(f"Failed to process {file_name}: {e}")

    # Output file
    output_filename = f"csv_resultados_{desdedata}_a_{atedata}_distrito_{distrito}.csv"
    output_path = os.path.join(output_folder, output_filename)

    try:
        combined_df.to_csv(output_path, index=False, sep=';', encoding='utf-8')
        logging.info(f"Saved merged file: {output_filename} with {len(combined_df)} rows.")
        print(f"Saved merged file: {output_filename} with {len(combined_df)} rows.")
    except Exception as e:
        logging.error(f"Failed to save {output_filename}: {e}")
        print(f"Failed to save {output_filename}: {e}")
