import os
from datetime import datetime
import json

LISTA_ESTABLECIMIENTOS_AVANZADO = [
    {
        "departamento": "GUAIRA",
        "distritos": [
            {
                "distrito": "BORJA",
                "establecimientos": [
                    {"value": "0004000.00020374", "text": "20 DE JUNIO"},
                    {"value": "0004000.00020310", "text": "PS- BORJA"},
                    {"value": "0004000.00020365", "text": "ROJAS SILVERA"},
                    {"value": "0004000.00020325", "text": "USF - BOQUERÓN"},
                    {"value": "0004000.00020356", "text": "USF - VALLE PÉ"},
                    {"value": "0004000.00020326", "text": "USF- AGUSTIN MOLAS"},
                ],
            },
            {
                "distrito": "CAPITÁN MAURICIO JOSÉ TROCHE",
                "establecimientos": [
                    {"value": "0004000.00030601", "text": "CHACORE"},
                    {"value": "0004000.00030363", "text": "CORA GUAZÚ"},
                    {
                        "value": "0004000.00030702",
                        "text": "IPS- PS USUFRUCTO M.J. TROCHE",
                    },
                    {"value": "0004000.00030210", "text": "MAURICIO JOSE TROCHE"},
                    {"value": "0004000.00030501", "text": "NUEVA ESPERANZA"},
                    {"value": "0004000.00030319", "text": "USF- CERRO PUNTA"},
                    {"value": "0004000.00030364", "text": "USF- ITACURUBÍ"},
                    {"value": "0004000.00030320", "text": "USF- MAURICIO J. TROCHE"},
                ],
            },
            {
                "distrito": "CORONEL MARTÍNEZ",
                "establecimientos": [
                    {"value": "0004000.00040330", "text": "COSTA BARRIOS"},
                    {"value": "0004000.00040503", "text": "FERREIRA"},
                    {"value": "0004000.00040502", "text": "MONGES PASO"},
                    {"value": "0004000.00040320", "text": "POTRERO VILLAR"},
                    {
                        "value": "0004000.00040314",
                        "text": "USF- CORONEL MARTINEZ (TEBICUARY)",
                    },
                ],
            },
            {
                "distrito": "DOCTOR BOTTRELL",
                "establecimientos": [
                    {"value": "0004000.00160305", "text": "USF- DR. BOTRELL"},
                ],
            },
            {
                "distrito": "FÉLIX PÉREZ CARDOZO",
                "establecimientos": [
                    {"value": "0004000.00050367", "text": "AQUINO COSTA"},
                    {"value": "0004000.00050313", "text": "USF- FELIX PEREZ CARDOZO"},
                ],
            },
            {
                "distrito": "GRAL. EUGENIO A. GARAY",
                "establecimientos": [
                    {"value": "0004000.00060324", "text": "AMAMBAY"},
                    {"value": "0004000.00060309", "text": "GENERAL EUGENIO A. GARAY"},
                    {
                        "value": "0004000.00060318",
                        "text": "USF- COL. GUARANI (EX AMAMBAY)",
                    },
                    {"value": "0004000.00060323", "text": "USF- SAN ROQUE GONZÁLEZ"},
                    {"value": "0004000.00060321", "text": "USF-GRAL. A. GARAY"},
                ],
            },
            {
                "distrito": "INDEPENDENCIA",
                "establecimientos": [
                    {
                        "value": "0004000.00070203",
                        "text": "H.D. - COLONIA INDEPENDENCIA",
                    },
                    {
                        "value": "0004000.00070703",
                        "text": "IPS- US COLONIA INDEPENDENCIA",
                    },
                    {"value": "0004000.00070368", "text": "USF- 13 LÍNEA SAN PEDRO"},
                    {"value": "0004000.00070207", "text": "USF- COL. INDEPENDENCIA"},
                    {"value": "0004000.00070346", "text": "USF- PIRECA"},
                    {"value": "0004000.00070345", "text": "USF- POTRERO DEL CARMEN"},
                    {"value": "0004000.00070343", "text": "USF- SAN GERVACIO"},
                    {
                        "value": "0004000.00070317",
                        "text": "USF- SAN PEDRO 13 LINEA - YROYSA",
                    },
                    {"value": "0004000.00070315", "text": "USF- SANTA CECILIA"},
                    {"value": "0004000.00070369", "text": "USF- SANTO DOMINGO"},
                    {"value": "0004000.00070304", "text": "USF- YBYTURUZU"},
                    {"value": "0004000.00070308", "text": "USF- YROYSA - 7MA. LINEA"},
                    {"value": "0004000.00070351", "text": "USF- YROYSÁ"},
                ],
            },
            {
                "distrito": "ITAPÉ",
                "establecimientos": [
                    {"value": "0004000.00080211", "text": "ITAPE"},
                    {"value": "0004000.00080603", "text": "LOMA JHOVY"},
                    {"value": "0004000.00080602", "text": "USF- COSTA JHU"},
                    {"value": "0004000.00080327", "text": "USF-ITAPE"},
                ],
            },
            {
                "distrito": "ITURBE",
                "establecimientos": [
                    {"value": "0004000.00090372", "text": "CAP. BRIZUELA"},
                    {"value": "0004000.00090604", "text": "CONCEPCION-MI"},
                    {"value": "0004000.00090704", "text": "IPS- US ITURBE"},
                    {"value": "0004000.00090204", "text": "ITURBE"},
                    {"value": "0004000.00090360", "text": "USF- CANDE´A GUAZÚ"},
                    {"value": "0004000.00090353", "text": "USF- COSTA ALEGRE"},
                    {"value": "0004000.00090336", "text": "USF-ITURBE"},
                ],
            },
            {
                "distrito": "JOSÉ FASSARDI",
                "establecimientos": [
                    {
                        "value": "0004000.00100705",
                        "text": "IPS- PS CONVENIO JOSE FASSARDI",
                    },
                    {"value": "0004000.00100209", "text": "JOSE FASSARDI"},
                    {"value": "0004000.00100340", "text": "SAN AGUSTÍN"},
                    {"value": "0004000.00100366", "text": "USF-CAGUARE I"},
                    {"value": "0004000.00100330", "text": "USF-JOSE FASSARDI"},
                ],
            },
            {
                "distrito": "MBOCAYATY",
                "establecimientos": [
                    {"value": "0004000.00110302", "text": "MBOCAYATY"},
                    {"value": "0004000.00110342", "text": "SANTA BARBARA"},
                    {"value": "0004000.00110357", "text": "USF- JORGE NAVILLE"},
                    {"value": "0004000.00110605", "text": "USF- TACUARITA"},
                    {"value": "0004000.00110331", "text": "USF-MBOCAYATY"},
                ],
            },
            {
                "distrito": "NATALICIO TALAVERA",
                "establecimientos": [
                    {"value": "0004000.00120371", "text": "APERA-ATY"},
                    {"value": "0004000.00120303", "text": "NATALICIO TALAVERA"},
                    {"value": "0004000.00120332", "text": "USF-NATALICIO TALAVERA"},
                ],
            },
            {
                "distrito": "PASO YOBAI",
                "establecimientos": [
                    {
                        "value": "0004000.00170401",
                        "text": "HOSPITAL UNIVERSITARIO ESPÍRITU SANTO",
                    },
                    {"value": "0004000.00170706", "text": "IPS- PS PASO YOBAI"},
                    {"value": "0004000.00170362", "text": "MANGRULLO"},
                    {"value": "0004000.00170202", "text": "PASO YOBAI"},
                    {"value": "0004000.00170311", "text": "USF- KURUZU"},
                    {
                        "value": "0004000.00170341",
                        "text": "USF- PLANCHADA (EX ARROYO MOROTÍ)",
                    },
                    {"value": "0004000.00170340", "text": "USF- SAN AGUSTIN"},
                    {
                        "value": "0004000.00170329",
                        "text": "USF-3 DE NOVIEMBRE - KURUSU",
                    },
                    {"value": "0004000.00170354", "text": "USF-MANGRULLO"},
                    {"value": "0004000.00170335", "text": "USF-PASO YOBAI"},
                    {"value": "0004000.00170361", "text": "USF-SAN FRANCISCO"},
                    {"value": "0004000.00170347", "text": "USF-TORRES CUÉ"},
                    {"value": "0004000.00170370", "text": "ÑU VERA"},
                ],
            },
            {
                "distrito": "SAN SALVADOR",
                "establecimientos": [
                    {"value": "0004000.00140205", "text": "SAN SALVADOR"},
                    {"value": "0004000.00140333", "text": "USF-SAN SALVADOR"},
                ],
            },
            {
                "distrito": "TEBICUARY",
                "establecimientos": [
                    {"value": "0004000.00180707", "text": "IPS TEBICUARY"},
                    {"value": "0004000.00180316", "text": "USF- LOMA PINDO"},
                ],
            },
            {
                "distrito": "VILLARRICA",
                "establecimientos": [
                    {
                        "value": "0004000.00010601",
                        "text": "CENTRO EDUCATIVO SEMBRADOR VILLARRICA",
                    },
                    {"value": "0004000.00010505", "text": "CLINICA MUNICIPAL"},
                    {
                        "value": "0004000.00010369",
                        "text": "CLINICA PERIFERICA SAN MIGUEL",
                    },
                    {"value": "0004000.00010450", "text": "CSS- P. R. - VILLARRICA"},
                    {"value": "0004000.00010101", "text": "H.R. - VILLARRICA"},
                    {
                        "value": "0004000.00010A02",
                        "text": "HOSPITAL UNIVERSITARIO ESPÍRITU SANTO",
                    },
                    {"value": "0004000.00010701", "text": "IPS- HR VILLARRICA"},
                    {"value": "0004000.00010312", "text": "PERULEROMÍ"},
                    {"value": "0004000.00010504", "text": "POLICLINICO SAN MIGUEL"},
                    {"value": "0004000.00010506", "text": "PP POLICLINICO POLICIAL"},
                    {"value": "0004000.00010352", "text": "ROSADO"},
                    {
                        "value": "0004000.00010600",
                        "text": "UNIDAD DE SALUD PENITENCIARIO ADULTO",
                    },
                    {"value": "0004000.00010344", "text": "USF - ITA YBÚ"},
                    {"value": "0004000.00010348", "text": "USF- 14 DE MAYO"},
                    {"value": "0004000.00010339", "text": "USF- CAROVENI NUEVO"},
                    {"value": "0004000.00010370", "text": "USF- HOSPITAL-I SAN MIGUEL"},
                    {"value": "0004000.00010338", "text": "USF- MA. AUXILIADORA"},
                    {"value": "0004000.00010322", "text": "USF- POTRERO BÁEZ"},
                    {"value": "0004000.00010349", "text": "USF- SAN MIGUEL"},
                    {"value": "0004000.00010328", "text": "USF- TORORO"},
                    {"value": "0004000.00010358", "text": "USF-RINCÓN"},
                    {"value": "0004000.00010337", "text": "USF. CENTRO"},
                    {"value": "0004000.00010206", "text": "USF. LOMAS VALENTINA"},
                ],
            },
            {
                "distrito": "YATAITY",
                "establecimientos": [
                    {"value": "0004000.00150359", "text": "POTRERO BENEGAS"},
                    {"value": "0004000.00150334", "text": "USF-YATAITY"},
                    {"value": "0004000.00150307", "text": "YATAITY"},
                ],
            },
            {
                "distrito": "ÑUMÍ",
                "establecimientos": [
                    {"value": "0004000.00130606", "text": "CERRO CORA"},
                    {"value": "0004000.00130350", "text": "SANTA ELENA"},
                    {"value": "0004000.00130306", "text": "USF- ÑUMI"},
                ],
            },
        ],
    },
]

LISTA_ESTABLECIMIENTOS = [
    {
        "codigo_establecimiento": "0004000.00160305",
        "nombre_establecimiento": "USF- DR. BOTRELL",
    },
    {
        "codigo_establecimiento": "0004000.00150334",
        "nombre_establecimiento": "USF-YATAITY",
    },
    {
        "codigo_establecimiento": "0004000.00010337",
        "nombre_establecimiento": "USF. CENTRO",
    },
    {
        "codigo_establecimiento": "0004000.00010344",
        "nombre_establecimiento": "USF - ITA YBÚ",
    },
    {
        "codigo_establecimiento": "0004000.00090336",
        "nombre_establecimiento": "USF-ITURBE",
    },
    {
        "codigo_establecimiento": "0004000.00090353",
        "nombre_establecimiento": "USF- COSTA ALEGRE",
    },
    {
        "codigo_establecimiento": "0004000.00010339",
        "nombre_establecimiento": "USF- CAROVENI NUEVO",
    },
    {
        "codigo_establecimiento": "0004000.00010328",
        "nombre_establecimiento": "USF- TORORO",
    },
    {
        "codigo_establecimiento": "0004000.00030363",
        "nombre_establecimiento": "CORA GUAZÚ",
    },
    {
        "codigo_establecimiento": "0004000.00040330",
        "nombre_establecimiento": "COSTA BARRIOS",
    },
    {
        "codigo_establecimiento": "0004000.00010322",
        "nombre_establecimiento": "USF- POTRERO BÁEZ",
    },
    {
        "codigo_establecimiento": "0004000.00060309",
        "nombre_establecimiento": "GENERAL EUGENIO A. GARAY",
    },
    {"codigo_establecimiento": "0004000.00010352", "nombre_establecimiento": "ROSADO"},
    {
        "codigo_establecimiento": "0004000.00030501",
        "nombre_establecimiento": "NUEVA ESPERANZA",
    },
    {
        "codigo_establecimiento": "0004000.00110357",
        "nombre_establecimiento": "USF- JORGE NAVILLE",
    },
    {
        "codigo_establecimiento": "0004000.00140205",
        "nombre_establecimiento": "SAN SALVADOR",
    },
    {
        "codigo_establecimiento": "0004000.00050313",
        "nombre_establecimiento": "USF- FELIX PEREZ CARDOZO",
    },
    {
        "codigo_establecimiento": "0004000.00150359",
        "nombre_establecimiento": "POTRERO BENEGAS",
    },
    {
        "codigo_establecimiento": "0004000.00040503",
        "nombre_establecimiento": "FERREIRA",
    },
    {
        "codigo_establecimiento": "0004000.00040502",
        "nombre_establecimiento": "MONGES PASO",
    },
    {
        "codigo_establecimiento": "0004000.00040320",
        "nombre_establecimiento": "POTRERO VILLAR",
    },
    {
        "codigo_establecimiento": "0004000.00020356",
        "nombre_establecimiento": "USF - VALLE PÉ",
    },
    {
        "codigo_establecimiento": "0004000.00070346",
        "nombre_establecimiento": "USF- PIRECA",
    },
    {
        "codigo_establecimiento": "0004000.00090360",
        "nombre_establecimiento": "USF- CANDE´A GUAZÚ",
    },
    {
        "codigo_establecimiento": "0004000.00060321",
        "nombre_establecimiento": "USF-GRAL. A. GARAY",
    },
    {
        "codigo_establecimiento": "0004000.00020325",
        "nombre_establecimiento": "USF - BOQUERÓN",
    },
    {
        "codigo_establecimiento": "0004000.00170202",
        "nombre_establecimiento": "PASO YOBAI",
    },
    {
        "codigo_establecimiento": "0004000.00020310",
        "nombre_establecimiento": "PS- BORJA",
    },
    {
        "codigo_establecimiento": "0004000.00060323",
        "nombre_establecimiento": "USF- SAN ROQUE GONZÁLEZ",
    },
    {
        "codigo_establecimiento": "0004000.00010358",
        "nombre_establecimiento": "USF-RINCÓN",
    },
    {
        "codigo_establecimiento": "0004000.00010206",
        "nombre_establecimiento": "USF. LOMAS VALENTINA",
    },
    {
        "codigo_establecimiento": "0004000.00020326",
        "nombre_establecimiento": "USF- AGUSTIN MOLAS",
    },
    {
        "codigo_establecimiento": "0004000.00060318",
        "nombre_establecimiento": "USF- COL. GUARANI (EX AMAMBAY)",
    },
    {
        "codigo_establecimiento": "0004000.00170335",
        "nombre_establecimiento": "USF-PASO YOBAI",
    },
    {
        "codigo_establecimiento": "0004000.00050367",
        "nombre_establecimiento": "AQUINO COSTA",
    },
    {"codigo_establecimiento": "0004000.00030601", "nombre_establecimiento": "CHACORE"},
    {
        "codigo_establecimiento": "0004000.00090604",
        "nombre_establecimiento": "CONCEPCION-MI",
    },
    {
        "codigo_establecimiento": "0004000.00170354",
        "nombre_establecimiento": "USF-MANGRULLO",
    },
    {
        "codigo_establecimiento": "0004000.00010101",
        "nombre_establecimiento": "H.R. - VILLARRICA",
    },
    {
        "codigo_establecimiento": "0004000.00090372",
        "nombre_establecimiento": "CAP. BRIZUELA",
    },
    {
        "codigo_establecimiento": "0004000.00120371",
        "nombre_establecimiento": "APERA-ATY",
    },
    {
        "codigo_establecimiento": "0004000.00070203",
        "nombre_establecimiento": "H.D. - COLONIA INDEPENDENCIA",
    },
    {
        "codigo_establecimiento": "0004000.00110342",
        "nombre_establecimiento": "SANTA BARBARA",
    },
    {
        "codigo_establecimiento": "0004000.00130606",
        "nombre_establecimiento": "CERRO CORA",
    },
    {"codigo_establecimiento": "0004000.00080211", "nombre_establecimiento": "ITAPE"},
    {
        "codigo_establecimiento": "0004000.00100209",
        "nombre_establecimiento": "JOSE FASSARDI",
    },
    {
        "codigo_establecimiento": "0004000.00070207",
        "nombre_establecimiento": "USF- COL. INDEPENDENCIA",
    },
    {
        "codigo_establecimiento": "0004000.00180316",
        "nombre_establecimiento": "USF- LOMA PINDO",
    },
    {
        "codigo_establecimiento": "0004000.00070345",
        "nombre_establecimiento": "USF- POTRERO DEL CARMEN",
    },
    {
        "codigo_establecimiento": "0004000.00030320",
        "nombre_establecimiento": "USF- MAURICIO J. TROCHE",
    },
    {
        "codigo_establecimiento": "0004000.00130350",
        "nombre_establecimiento": "SANTA ELENA",
    },
    {
        "codigo_establecimiento": "0004000.00170340",
        "nombre_establecimiento": "USF- SAN AGUSTIN",
    },
    {
        "codigo_establecimiento": "0004000.00170361",
        "nombre_establecimiento": "USF-SAN FRANCISCO",
    },
    {"codigo_establecimiento": "0004000.00170370", "nombre_establecimiento": "ÑU VERA"},
    {
        "codigo_establecimiento": "0004000.00040314",
        "nombre_establecimiento": "USF- CORONEL MARTINEZ (TEBICUARY)",
    },
    {
        "codigo_establecimiento": "0004000.00170347",
        "nombre_establecimiento": "USF-TORRES CUÉ",
    },
    {
        "codigo_establecimiento": "0004000.00070343",
        "nombre_establecimiento": "USF- SAN GERVACIO",
    },
    {
        "codigo_establecimiento": "0004000.00070315",
        "nombre_establecimiento": "USF- SANTA CECILIA",
    },
    {
        "codigo_establecimiento": "0004000.00070369",
        "nombre_establecimiento": "USF- SANTO DOMINGO",
    },
    {
        "codigo_establecimiento": "0004000.00170329",
        "nombre_establecimiento": "USF-3 DE NOVIEMBRE - KURUSU",
    },
    {
        "codigo_establecimiento": "0004000.00010338",
        "nombre_establecimiento": "USF- MA. AUXILIADORA",
    },
    {
        "codigo_establecimiento": "0004000.00100330",
        "nombre_establecimiento": "USF-JOSE FASSARDI",
    },
    {
        "codigo_establecimiento": "0004000.00070308",
        "nombre_establecimiento": "USF- YROYSA - 7MA. LINEA",
    },
    {
        "codigo_establecimiento": "0004000.00080327",
        "nombre_establecimiento": "USF-ITAPE",
    },
    {
        "codigo_establecimiento": "0004000.00080602",
        "nombre_establecimiento": "USF- COSTA JHU",
    },
    {
        "codigo_establecimiento": "0004000.00030364",
        "nombre_establecimiento": "USF- ITACURUBÍ",
    },
    {
        "codigo_establecimiento": "0004000.00080603",
        "nombre_establecimiento": "LOMA JHOVY",
    },
    {
        "codigo_establecimiento": "0004000.00030319",
        "nombre_establecimiento": "USF- CERRO PUNTA",
    },
    {
        "codigo_establecimiento": "0004000.00030210",
        "nombre_establecimiento": "MAURICIO JOSE TROCHE",
    },
    {
        "codigo_establecimiento": "0004000.00010348",
        "nombre_establecimiento": "USF- 14 DE MAYO",
    },
    {"codigo_establecimiento": "0004000.00090204", "nombre_establecimiento": "ITURBE"},
    {
        "codigo_establecimiento": "0004000.00010349",
        "nombre_establecimiento": "USF- SAN MIGUEL",
    },
    {
        "codigo_establecimiento": "0004000.00170341",
        "nombre_establecimiento": "USF- PLANCHADA (EX ARROYO MOROTÍ)",
    },
    {
        "codigo_establecimiento": "0004000.00100366",
        "nombre_establecimiento": "USF-CAGUARE I",
    },
    {
        "codigo_establecimiento": "0004000.00070368",
        "nombre_establecimiento": "USF- 13 LÍNEA SAN PEDRO ",
    },
    {
        "codigo_establecimiento": "0004000.00110331",
        "nombre_establecimiento": "USF-MBOCAYATY",
    },
    {
        "codigo_establecimiento": "0004000.00070304",
        "nombre_establecimiento": "USF- YBYTURUZU",
    },
    {
        "codigo_establecimiento": "0004000.00110605",
        "nombre_establecimiento": "USF- TACUARITA",
    },
    {
        "codigo_establecimiento": "0004000.00120303",
        "nombre_establecimiento": "NATALICIO TALAVERA",
    },
    {
        "codigo_establecimiento": "0004000.00120332",
        "nombre_establecimiento": "USF-NATALICIO TALAVERA",
    },
    {
        "codigo_establecimiento": "0004000.00010370",
        "nombre_establecimiento": "USF- HOSPITAL-I SAN MIGUEL",
    },
    {
        "codigo_establecimiento": "0004000.00130306",
        "nombre_establecimiento": "USF- ÑUMI",
    },
    {
        "codigo_establecimiento": "0004000.00010505",
        "nombre_establecimiento": "CLINICA MUNICIPAL",
    },
    {
        "codigo_establecimiento": "0004000.00140333",
        "nombre_establecimiento": "USF-SAN SALVADOR",
    },
    {
        "codigo_establecimiento": "0004000.00010504",
        "nombre_establecimiento": "POLICLINICO SAN MIGUEL",
    },
    {
        "codigo_establecimiento": "0004000.00010600",
        "nombre_establecimiento": "UNIDAD DE SALUD PENITENCIARIO ADULTO",
    },
    {
        "codigo_establecimiento": "0004000.00010506",
        "nombre_establecimiento": "PP POLICLINICO POLICIAL",
    },
    {
        "codigo_establecimiento": "0004000.00010601",
        "nombre_establecimiento": "CENTRO EDUCATIVO SEMBRADOR VILLARRICA",
    },
    {
        "codigo_establecimiento": "0004000.00020365",
        "nombre_establecimiento": "ROJAS SILVERA",
    },
    {
        "codigo_establecimiento": "0004000.00020374",
        "nombre_establecimiento": "20 DE JUNIO",
    },
]

# Nombre del archivo donde se guardan las preferencias y los credenciales
CREDENTIALS_FILE_NAME = "credentials.json"
# Imprime el total de establecimientos disponibles para elegir
print(f"Número de Establecimientos totales: {len(LISTA_ESTABLECIMIENTOS)}")
# Indica el directorio donde se descargan los archivos
DOWNLOADED_DIR = os.path.join(os.getcwd(), "downloaded_data")

# Indica el directorio donde se descargan los archivos de Registro Diario
DIR_REGISTRO_DIARIO_AVANZADO = os.path.join(DOWNLOADED_DIR, "Registro_Diario")
# Indica el directorio donde se descargan los archivos de Registro Diario Avanzado
DIR_REGISTRO_DIARIO_AVANZADO = os.path.join(DOWNLOADED_DIR, "Registro_Diario_Avanzado")
# Indica el nombre que tendrá el archivo de Registro Diario ya procesado
DOWNLOADED_DIR_REGISTRO_DIARIO = os.path.join(
    DIR_REGISTRO_DIARIO_AVANZADO,
    f"Registro_Diario_{str(datetime.now().strftime('%Y-%m-%d_%H.%M.%S.hs'))}/",
)
# Indica el nombre que tendrá el archivo de Registro Diario Avanzado ya procesado
DOWNLOADED_DIR_REGISTRO_DIARIO_AVANZADO = os.path.join(
    DIR_REGISTRO_DIARIO_AVANZADO,
    f"Registro_Diario_Avanzado_{str(datetime.now().strftime('%Y-%m-%d_%H.%M.%S.hs'))}/",
)

# Indica el directorio donde se encuentra el archivo de Plantilla para Registro Diario
DIR_PLANTILLA_REGISTRO_DIARIO_AVANZADO = os.path.join(
    os.getcwd(), "Plantilla_Registro_Diario.xlsx"
)
# Indica el directorio donde se encuentra el archivo de Plantilla para Registro Diario Avanzado
DIR_PLANTILLA_REGISTRO_DIARIO_AVANZADO = os.path.join(
    os.getcwd(), "Plantilla_Registro_Diario_Avanzado.xlsx"
)
# Indica el nombre de la hoja de la Plantilla para Registro Diario
REGISTRO_DIARIO_AVANZADO_BASE_SHEET_NAME = "BASE"
# Indica el nombre de la hoja de la Plantilla para Registro Diario Avanzado
REGISTRO_DIARIO_AVANZADO_BASE_SHEET_NAME = "BASE"


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
def downloaded_dir_registro_diario_avanzado_with_start_end(start, end):
    return os.path.join(
        DIR_REGISTRO_DIARIO_AVANZADO,
        f"Registro_Diario_{start}_{end}_{str(datetime.now().strftime('%Y-%m-%d_%H.%M.%S.hs'))}/",
    )


# le da nombre a los archivos de Registro Diario Avanzado descargados y guardados en el directorio de Registro Diario
def downloaded_dir_registro_diario_avanzado_with_start_end(start, end):
    return os.path.join(
        DIR_REGISTRO_DIARIO_AVANZADO,
        f"Registro_Diario_Avanzado_{start}_{end}_{str(datetime.now().strftime('%Y-%m-%d_%H.%M.%S.hs'))}/",
    )
