"""Punto de entrada de auditoria (solo verificacion, sin estampar).

Lee todas las obras del workbook, recorre `0. Input\\` de forma recursiva para
encontrar carpetas candidatas y reporta un estado por obra:

    BLUE    los 5 PDFs de salida ya existen (trabajo previamente hecho)
    GREEN   carpeta encontrada + 5 PDFs de entrada presentes (lista para estampar)
    YELLOW  carpeta existe pero falta al menos un PDF o hay ambiguedad
    RED     no se encontro carpeta para esa obra

Emite lineas legibles por humanos y tambien lineas de estado parseables por
maquina con este formato:

    STATUS|<nombre>|<color>|<details>

Ademas escribe `<output_dir>\\faltantes.csv` con faltantes y conflictos para
evitar revisar informacion larga en ventanas emergentes.
"""

import csv
import os
import sys

sys.stdout.reconfigure(errors="replace")
sys.stderr.reconfigure(errors="replace")

import config
from excel_reader import read_obras, read_input_path
from folder_walker import find_obra_folders
from file_matcher import discover_files

FALTANTES_FILENAME = "faltantes.csv"
CSV_FIELDS = ["NOMBRE", "CODIGO", "COMPOSITOR", "TIPO", "PROBLEMA"]


def main() -> int:
    if len(sys.argv) < 2:
        print("ERROR: falta la ruta del workbook. Uso: audit.py <workbook.xlsm>")
        return 1
    workbook_path = sys.argv[1]
    if not os.path.isfile(workbook_path):
        print(f"ERROR: no se encontro el workbook: {workbook_path}")
        return 1

    workbook_dir = os.path.dirname(os.path.abspath(workbook_path))
    typed = read_input_path(workbook_path)
    if typed:
        input_root = typed
        input_src = f"{config.INPUT_PATH_SHEET}!{config.INPUT_PATH_CELL}"
    else:
        input_root = os.path.join(workbook_dir, config.INPUT_SUBFOLDER)
        input_src = f"fallback ({config.INPUT_SUBFOLDER}\\)"
    output_dir = os.path.join(workbook_dir, config.OUTPUT_SUBFOLDER)

    print("=== Auditoria ===")
    print(f"Workbook: {workbook_path}")
    print(f"Input:    {input_root}  [{input_src}]")
    print(f"Output:   {output_dir}")
    print()

    try:
        obras = read_obras(workbook_path)
    except Exception as e:
        print(f"ERROR: no se pudo leer el workbook: {e}")
        return 1
    print(f"Cargadas {len(obras)} obras.")

    try:
        pairs = find_obra_folders(input_root, obras)
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

    folder_by_name = {}
    for obra, folder in pairs:
        folder_by_name.setdefault(obra["nombre"], folder)
    print(f"Coinciden {len(folder_by_name)} de {len(obras)} obras con carpetas.")
    print()

    counts = {"BLUE": 0, "GREEN": 0, "YELLOW": 0, "RED": 0}
    all_issues = []
    for obra in obras:
        nombre = obra["nombre"]
        folder = folder_by_name.get(nombre)
        color, details, issues = _classify(obra, folder, output_dir)
        counts[color] += 1
        all_issues.extend(issues)
        print(f"STATUS|{nombre}|{color}|{details}")

    log_path = ""
    if all_issues:
        os.makedirs(output_dir, exist_ok=True)
        log_path = os.path.join(output_dir, FALTANTES_FILENAME)
        _write_log(log_path, all_issues)

    print()
    if log_path:
        print(f"Lista de faltantes: {log_path}  ({len(all_issues)} entradas)")
    print(
        f"Hecho. blue={counts['BLUE']}  "
        f"green={counts['GREEN']}  "
        f"yellow={counts['YELLOW']}  "
        f"red={counts['RED']}"
    )
    return 0


def _classify(obra, folder, output_dir):
    """Calcula color, resumen y lista de incidencias CSV para una obra.

    Solo se generan incidencias para estados YELLOW y RED.
    """
    if _all_outputs_present(obra, output_dir):
        return "BLUE", "all 5 already stamped", []

    if folder is None:
        return "RED", "sin carpeta", [_issue(obra, "", "Carpeta no encontrada")]

    try:
        matches, ambiguous = discover_files(folder, obra["nombre"])
    except Exception as e:
        return "YELLOW", f"error de carpeta: {e}", [_issue(
            obra, "", f"Error al leer carpeta: {e}",
        )]

    missing_codes = [k for k in config.STICKER_TYPES if not obra["doc_codes"].get(k)]
    missing_files = [k for k in config.STICKER_TYPES if matches.get(k) is None]

    if not missing_codes and not missing_files and not ambiguous:
        return "GREEN", "lista para estampar", []

    issues = []
    for k in missing_codes:
        sheet = config.SHEET_PER_TYPE[k]
        issues.append(_issue(obra, k, f"Falta doc code en la hoja '{sheet}'"))
    for k in missing_files:
        if k == "CARATULA":
            problema = f"Falta PDF cuyo nombre empiece con '{obra['nombre']}'"
        else:
            kws = "/".join(config.FILE_KEYWORDS.get(k, [k.lower()]))
            problema = f"Falta PDF con '{kws}' en el nombre"
        issues.append(_issue(obra, k, problema))
    for k, paths in ambiguous.items():
        names = ", ".join(os.path.basename(p) for p in paths)
        issues.append(_issue(obra, k, f"Mas de un archivo coincide: {names}"))

    bits = []
    if missing_codes:
        bits.append("sin doc code " + ",".join(missing_codes))
    if missing_files:
        bits.append("faltan " + ",".join(missing_files))
    if ambiguous:
        bits.append("ambigua " + ",".join(ambiguous.keys()))
    return "YELLOW", "; ".join(bits), issues


def _issue(obra, tipo, problema):
    return {
        "NOMBRE":     obra["nombre"],
        "CODIGO":     obra.get("codigo", ""),
        "COMPOSITOR": obra.get("author", ""),
        "TIPO":       tipo,
        "PROBLEMA":   problema,
    }


def _write_log(path, issues):
    # `utf-8-sig` agrega BOM para que Excel abra correctamente texto extendido.
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(issues)


def _all_outputs_present(obra, output_dir):
    obra_dir = os.path.join(output_dir, obra["nombre"])
    for kind in config.STICKER_TYPES:
        code = obra["doc_codes"].get(kind)
        if not code:
            return False
        if not os.path.exists(os.path.join(obra_dir, code + ".pdf")):
            return False
    return True


if __name__ == "__main__":
    sys.exit(main())
