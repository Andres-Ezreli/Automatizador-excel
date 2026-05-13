# Ajusta estos valores sin tocar el resto del codigo.

# Tipos de sticker en el orden en que se imprimen los resumentes.
STICKER_TYPES = ["CARATULA", "FORMATO", "CERTIFICADO", "LETRA", "PARTITURA"]

# --- Estructura del workbook -----------------------------------------------

# Hoja maestra: fuente de la lista de obras (NOMBRE + COMPOSITOR + fechas +
# codigo + funcionario). Usa la hoja mas completa.
MASTER_SHEET = "CERTIFICADOS"

# Hoja por tipo: cada una guarda el codigo documental en su columna STICKER.
SHEET_PER_TYPE = {
    "CARATULA":    "CD",
    "FORMATO":     "FORMATOS",
    "CERTIFICADO": "CERTIFICADOS",
    "LETRA":       "LETRA",
    "PARTITURA":   "PARTITURAS",
}

# Encabezados de columna (sin importar mayusculas). La posicion no importa;
# las columnas se ubican por nombre.
HEADER_NOMBRE         = "NOMBRE"                  # clave de union entre hojas
HEADER_CODIGO         = "CODIGO"
HEADER_COMPOSITOR     = "COMPOSITOR"              # nombre del autor; debe aparecer en ancestros de carpeta
HEADER_STICKER        = "STICKER"                 # codigo documental en cada hoja de tipo (primer match)
HEADER_FECHA_RECIBIDO = "RECIBIDO"
HEADER_FECHA_ALTA_SGS = "FECHA ALTA DE LA OBRA"
# La columna de funcionario en MASTER_SHEET se toma por posicion (ultima
# columna) porque hoy su encabezado dice "RECIBIDO" pero la celda contiene un
# nombre. Si corriges el encabezado, configura FUNCIONARIO_HEADER.
FUNCIONARIO_HEADER = None     # None = usar la ultima columna de MASTER_SHEET

# Numero de fila de los encabezados en todas las hojas.
HEADER_ROW = 1

# --- Modo archivo unico (botones Examinar) ---------------------------------
#
# Cuando se elige un PDF con un boton "Examinar", `stamp_one.py` lee el texto
# del sticker, el nombre de salida y el titulo de obra desde `STICKERmaker`.
# La ruta de origen llega como argumento de linea de comandos desde VBA.

STICKERMAKER_SHEET = "STICKERmaker"

# Texto de sticker por tipo (multilinea, calculado por formulas del workbook).
STICKER_CELLS = {
    "CARATULA":    "B12",
    "FORMATO":     "C12",
    "CERTIFICADO": "D12",
    "LETRA":       "E12",
    "PARTITURA":   "F12",
}

# Nombre de salida por tipo (formula del workbook, termina en .pdf).
OUTPUT_NAME_CELLS = {
    "CARATULA":    "B19",
    "FORMATO":     "C19",
    "CERTIFICADO": "D19",
    "LETRA":       "E19",
    "PARTITURA":   "F19",
}

# --- Modo archivo unico (botones Pegar Sticker) ---------------------------
STICKERMAKER_SHEET = "STICKERmaker"

# Mapa de celdas exactas por columna (B=Caratula, C=Formato, etc.).
# Ajusta los numeros de fila para que coincidan con tu hoja real.

SINGLE_STAMP_CELLS = {
    "CARATULA": {
        "sticker":   "B13",
        "input_pdf": "B19",
        "out_name":  "B27",
        "out_dir":   "B23",
        "eje_y":     "C42",  # antes margin_top
        "eje_x":     "D42"    # antes margin_right
    },
    "FORMATO": {
        "sticker":   "C13",
        "input_pdf": "C19",
        "out_name":  "C27",
        "out_dir":   "C23",
        "eje_y":     "C43",  # antes margin_top
        "eje_x":     "D43"    # antes margin_right
    },
    "CERTIFICADO": {
        "sticker":   "D13",
        "input_pdf": "D19",
        "out_name":  "D27",
        "out_dir":   "D23",
        "eje_y":     "C44",  # antes margin_top
        "eje_x":     "D44"    # antes margin_right
    },
    "LETRA": {
        "sticker":   "E13",
        "input_pdf": "E19",
        "out_name":  "E27",
        "out_dir":   "E23",
        "eje_y":     "C45",  # antes margin_top
        "eje_x":     "D45"    # antes margin_right
    },
    "PARTITURA": {
        "sticker":   "F13",
        "input_pdf": "F19",
        "out_name":  "F27",
        "out_dir":   "F23",
        "eje_y":     "C46",  # antes margin_top
        "eje_x":     "D46"    # antes margin_right
    }
}   

# Titulo de obra: se usa para elegir la subcarpeta de salida.
OBRA_TITLE_CELL = "H3"

# --- Estructura de carpetas -----------------------------------------------

# El script busca carpetas de obra en este orden:
#   1. Ruta absoluta escrita en INPUT_PATH_CELL de INPUT_PATH_SHEET.
#   2. Si esta vacia, <workbook folder>\<INPUT_SUBFOLDER>\ como respaldo.
INPUT_PATH_SHEET = "STICKERmaker"
INPUT_PATH_CELL  = "B15"
INPUT_SUBFOLDER  = "Input"

# La salida va en <workbook folder>\<OUTPUT_SUBFOLDER>\.
#   PDFs : <OUTPUT_SUBFOLDER>\<obra NOMBRE>\<doc_code>.pdf
#   MP3s : <OUTPUT_SUBFOLDER>\<MP3_OUTPUT_SUBFOLDER>\<obra CODIGO>\<mp3 filename>
OUTPUT_SUBFOLDER     = "Output"
MP3_OUTPUT_SUBFOLDER = "FONOGRAMAS"

# --- Deteccion de tipos de archivo dentro de una carpeta -------------------

# El nombre (sin extension y normalizado) debe contener alguna keyword del tipo.
# CARATULA se evalua aparte: el nombre debe empezar con el NOMBRE de la obra.
FILE_KEYWORDS = {
    "LETRA":       ["letra"],
    "FORMATO":     ["formato"],
    "CERTIFICADO": ["certificado"],
    "PARTITURA":   ["partitura"],
}
# La primera coincidencia gana. CARATULA va al final para no capturar archivos
# LETRA/FORMATO/etc. que tambien contengan el titulo de la obra.
MATCH_PRIORITY = ["LETRA", "FORMATO", "CERTIFICADO", "PARTITURA", "CARATULA"]

# --- Plantilla de texto del sticker ----------------------------------------

# Campos: codigo, doc_code, fecha_recibido, fecha_alta_sgs, funcionario.
STICKER_TEMPLATE = (
    "{codigo}\n"
    "{doc_code}\n"
    "COORD. DOCUMENTACION\n"
    "RECIBIDO: {fecha_recibido}\n"
    "DOC SGS:{fecha_alta_sgs}\n"
    "{funcionario}"
)
DATE_FORMAT = "%d/%m/%Y"

# --- Posicion del sello (PDF points; 1 inch = 72 points; origen arriba-izq) ---

MARGIN_TOP    = 40
MARGIN_RIGHT  = 40
STAMP_WIDTH   = 130
STAMP_HEIGHT  = 90

# Estilo.
FONT_NAME  = "hebo"        # Fuente interna PyMuPDF: helv / hebo (bold) / heit / hebi
FONT_SIZE  = 10
FONT_COLOR = (1, 0, 0)     # RGB 0-1 - rojo
TEXT_ALIGN = 2             # 0=izq 1=centro 2=der 3=justificado

# (El destino MP3 se configura arriba con MP3_OUTPUT_SUBFOLDER + CODIGO.)