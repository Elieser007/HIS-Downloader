import os
from datetime import datetime
import json


LISTA_ESTABLECIMIENTOS = [
    {
        "codigo_establecimiento": "0004000.00090336",
        "nombre_establecimiento": "USF-ITURBE",
    },
    {
        "codigo_establecimiento": "0004000.00090353",
        "nombre_establecimiento": "USF- COSTA ALEGRE",
    },
    {
        "codigo_establecimiento": "0004000.00170354",
        "nombre_establecimiento": "USF-MANGRULLO",
    },
    {
        "codigo_establecimiento": "0004000.00100330",
        "nombre_establecimiento": "USF-JOSE FASSARDI",
    },
    {
        "codigo_establecimiento": "0004000.00030210",
        "nombre_establecimiento": "MAURICIO JOSE TROCHE",
    },
    {"codigo_establecimiento": "0004000.00090204", "nombre_establecimiento": "ITURBE"},
    {
        "codigo_establecimiento": "0004000.00170202",
        "nombre_establecimiento": "PASO YOBAI",
    },
    {
        "codigo_establecimiento": "0004000.00010338",
        "nombre_establecimiento": "USF- MA. AUXILIADORA",
    },
    {
        "codigo_establecimiento": "0004000.00150334",
        "nombre_establecimiento": "USF-YATAITY",
    },
    {
        "codigo_establecimiento": "0004000.00070345",
        "nombre_establecimiento": "USF- POTRERO DEL CARMEN",
    },
    {
        "codigo_establecimiento": "0004000.00040314",
        "nombre_establecimiento": "USF- CORONEL MARTINEZ (TEBICUARY)",
    },
    {
        "codigo_establecimiento": "0004000.00050313",
        "nombre_establecimiento": "USF- FELIX PEREZ CARDOZO",
    },
    {
        "codigo_establecimiento": "0004000.00010349",
        "nombre_establecimiento": "USF- SAN MIGUEL",
    },
    {
        "codigo_establecimiento": "0004000.00180316",
        "nombre_establecimiento": "USF- LOMA PINDO",
    },
    {
        "codigo_establecimiento": "0004000.00010370",
        "nombre_establecimiento": "USF- HOSPITAL-I SAN MIGUEL",
    },
    {
        "codigo_establecimiento": "0004000.00030320",
        "nombre_establecimiento": "USF- MAURICIO J. TROCHE",
    },
    {"codigo_establecimiento": "0004000.00080211", "nombre_establecimiento": "ITAPE"},
    {
        "codigo_establecimiento": "0004000.00010505",
        "nombre_establecimiento": "CLINICA MUNICIPAL",
    },
    {
        "codigo_establecimiento": "0004000.00060321",
        "nombre_establecimiento": "USF-GRAL. A. GARAY",
    },
    {
        "codigo_establecimiento": "0004000.00080327",
        "nombre_establecimiento": "USF-ITAPE",
    },
    {
        "codigo_establecimiento": "0004000.00010348",
        "nombre_establecimiento": "USF- 14 DE MAYO",
    },
    {
        "codigo_establecimiento": "0004000.00010504",
        "nombre_establecimiento": "POLICLINICO SAN MIGUEL",
    },
    {
        "codigo_establecimiento": "0004000.00100209",
        "nombre_establecimiento": "JOSE FASSARDI",
    },
    {
        "codigo_establecimiento": "0004000.00110331",
        "nombre_establecimiento": "USF-MBOCAYATY",
    },
    {
        "codigo_establecimiento": "0004000.00070207",
        "nombre_establecimiento": "USF- COL. INDEPENDENCIA",
    },
    {
        "codigo_establecimiento": "0004000.00080602",
        "nombre_establecimiento": "USF- COSTA JHU",
    },
    {
        "codigo_establecimiento": "0004000.00170335",
        "nombre_establecimiento": "USF-PASO YOBAI",
    },
    {
        "codigo_establecimiento": "0004000.00010101",
        "nombre_establecimiento": "H.R. - VILLARRICA",
    },
    {
        "codigo_establecimiento": "0004000.00120332",
        "nombre_establecimiento": "USF-NATALICIO TALAVERA",
    },
    {
        "codigo_establecimiento": "0004000.00030319",
        "nombre_establecimiento": "USF- CERRO PUNTA",
    },
    {
        "codigo_establecimiento": "0004000.00030364",
        "nombre_establecimiento": "USF- ITACURUBÍ",
    },
    {
        "codigo_establecimiento": "0004000.00020356",
        "nombre_establecimiento": "USF - VALLE PÉ",
    },
    {
        "codigo_establecimiento": "0004000.00110357",
        "nombre_establecimiento": "USF- JORGE NAVILLE",
    },
    {
        "codigo_establecimiento": "0004000.00060309",
        "nombre_establecimiento": "GENERAL EUGENIO A. GARAY",
    },
    {
        "codigo_establecimiento": "0004000.00120303",
        "nombre_establecimiento": "NATALICIO TALAVERA",
    },
    {
        "codigo_establecimiento": "0004000.00130306",
        "nombre_establecimiento": "USF- ÑUMI",
    },
    {
        "codigo_establecimiento": "0004000.00140205",
        "nombre_establecimiento": "SAN SALVADOR",
    },
    {
        "codigo_establecimiento": "0004000.00010358",
        "nombre_establecimiento": "USF-RINCÓN",
    },
    {
        "codigo_establecimiento": "0004000.00160305",
        "nombre_establecimiento": "USF- DR. BOTRELL",
    },
    {
        "codigo_establecimiento": "0004000.00140333",
        "nombre_establecimiento": "USF-SAN SALVADOR",
    },
    {
        "codigo_establecimiento": "0004000.00010339",
        "nombre_establecimiento": "USF- CAROVENI NUEVO",
    },
    {
        "codigo_establecimiento": "0004000.00010206",
        "nombre_establecimiento": "USF-VILLARRICA",
    },
    {
        "codigo_establecimiento": "0004000.00070203",
        "nombre_establecimiento": "H.D. - COLONIA INDEPENDENCIA",
    },
]

# Nombre del archivo donde se guardan las preferencias y los credenciales
CREDENTIALS_FILE_NAME = "credentials.json"
# Imprime el total de establecimientos disponibles para elegir
print(f"Número de Establecimientos totales: {len(LISTA_ESTABLECIMIENTOS)}")
# Indica el directorio donde se descargan los archivos
DOWNLOADED_DIR = os.path.join(os.getcwd(), "downloaded_data")

# Indica el directorio donde se descargan los archivos de Registro Diario
DIR_REGISTRO_DIARIO = os.path.join(DOWNLOADED_DIR, "Registro_Diario")
# Indica el nombre que tendrá el archivo de Registro Diario ya procesado
DOWNLOADED_DIR_REGISTRO_DIARIO = os.path.join(
    DIR_REGISTRO_DIARIO,
    f"Registro_Diario_{str(datetime.now().strftime('%Y-%m-%d_%H.%M.%S.hs'))}/",
)

# Indica el directorio donde se encuentra el archivo de Plantilla para Registro Diario
DIR_PLANTILLA_REGISTRO_DIARIO = os.path.join(
    os.getcwd(), "Plantilla_Registro_Diario.xlsx"
)
# Indica el nombre de la hoja de la Plantilla para Registro Diario
REGISTRO_DIARIO_BASE_SHEET_NAME = "BASE"


# Credenciales

try:
    # intentar abrir el archivo de credenciales y extraer las credenciales del archivo
    data = json.loads(open(CREDENTIALS_FILE_NAME).read())
    USERNAME = data["username"]
    PASSWORD = data["password"]
    ESTABLECIMIENTOS = data["establecimientos"]
    ESTABLECIMIENTO_LOGIN = data["establecimiento_login"]
    print(f"Número de Establecimientos en la lista: {len(ESTABLECIMIENTOS)}")
except FileNotFoundError:
    # si no se encuentra el archivo de credenciales, crear uno nuevo
    with open(CREDENTIALS_FILE_NAME, "x+t") as f:
        json.dump(
            {
                "username": "",
                "password": "",
                "establecimiento_login": "",
                "establecimientos": [],
            },
            f,
        )
    # cargar las credenciales del archivo
    data = json.loads(open(CREDENTIALS_FILE_NAME).read())
    USERNAME = data["username"]
    PASSWORD = data["password"]
    ESTABLECIMIENTOS = data["establecimientos"]
    ESTABLECIMIENTO_LOGIN = data["establecimiento_login"]
    print(f"Número de Establecimientos en la lista: {len(ESTABLECIMIENTOS)}")


# le da nombre a los archivos de Registro Diario descargados y guardados en el directorio de Registro Diario
def downloaded_dir_registro_diario_with_start_end(start, end):
    return os.path.join(
        DIR_REGISTRO_DIARIO,
        f"Registro_Diario_{start}_{end}_{str(datetime.now().strftime('%Y-%m-%d_%H.%M.%S.hs'))}/",
    )
