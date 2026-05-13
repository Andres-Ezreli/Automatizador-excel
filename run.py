import os
import sys

# Los nombres de archivo aqui pueden contener caracteres no ASCII.
# La consola heredada por WScript.Shell.Exec suele usar cp1252 y puede fallar
# al imprimir algunos de ellos; con esto evitamos cortes durante el resumen.
sys.stdout.reconfigure(errors="replace")
sys.stderr.reconfigure(errors="replace")

import config
from excel_reader import read_obras, read_input_path
from folder_walker import find_obra_folders
from file_matcher import discover_files
from sticker_builder import build_sticker
from stamper import stamp_pdf


def main() -> int:
    if len(sys.argv) < 2:
        print("ERROR: falta la ruta del workbook. Uso: run.py <workbook.xlsm>")
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

    print("=== Estampar carpeta ===")
    print(f"Workbook: {workbook_path}")
    print(f"Input:    {input_root}  [{input_src}]")
    print(f"Output:   {output_dir}")
    print()

    try:
        obras = read_obras(workbook_path)
    except Exception as e:
        print(f"ERROR: no se pudo leer el workbook: {e}")
        return 1
    print(f"Cargadas {len(obras)} obras desde el workbook.")

    try:
        pairs = find_obra_folders(input_root, obras)
    except Exception as e:
        print(f"ERROR: {e}")
        return 1
    print(f"Encontradas {len(pairs)} carpetas de obra que coinciden en {config.INPUT_SUBFOLDER}\\.")
    if not pairs:
        print("(nada para hacer)")
        return 0
    print()

    os.makedirs(output_dir, exist_ok=True)

    totals = {"stamped": 0, "skipped": 0, "failed": 0, "already_done": 0}
    output_seen = {}

    for obra, folder in pairs:
        rel_folder = os.path.relpath(folder, workbook_dir)
        print(f"--- {obra['nombre']}  ({obra['codigo']})  [{rel_folder}] ---")

        try:
            files, ambiguous = discover_files(folder, obra["nombre"])
        except Exception as e:
            print(f"  X discovery failed: {e}")
            totals["failed"] += 1
            print()
            continue

        for kind in config.STICKER_TYPES:
            src = files.get(kind)
            doc_code = obra["doc_codes"].get(kind)
            sticker = build_sticker(obra, kind)

            if kind in ambiguous:
                names = "  ".join(os.path.basename(p) for p in ambiguous[kind])
                print(f"  {kind:12s} X ambigua: {names}")
                totals["failed"] += 1
                continue

            if src is None:
                print(f"  {kind:12s} O (sin archivo)")
                totals["skipped"] += 1
                continue

            if not doc_code:
                print(f"  {kind:12s} X sin doc code en la hoja '{config.SHEET_PER_TYPE[kind]}' "
                      f"para '{obra['nombre']}'")
                totals["failed"] += 1
                continue

            if not sticker:
                print(f"  {kind:12s} X no se pudo construir el texto del sticker (faltan campos)")
                totals["failed"] += 1
                continue

            out_name = doc_code + ".pdf"
            obra_out_dir = os.path.join(output_dir, obra["nombre"])
            dst = os.path.join(obra_out_dir, out_name)
            rel_dst = os.path.join(obra["nombre"], out_name)

            # Idempotencia: si este archivo de salida ya existe, se omite para no rehacer
            # trabajo ni sobreescribir resultados previos.
            if os.path.exists(dst):
                print(f"  {kind:12s} RE ya hecho ({rel_dst})")
                totals["already_done"] += 1
                continue

            # Deteccion de colisiones: si dos obras apuntan al mismo archivo de
            # salida, se rechaza para evitar sobreescritura silenciosa.
            prior = output_seen.get(dst)
            if prior and prior != (obra["nombre"], kind):
                print(f"  {kind:12s} X colision de salida: {rel_dst} tambien lo reclama "
                      f"{prior[0]} ({prior[1]})")
                totals["failed"] += 1
                continue
            output_seen[dst] = (obra["nombre"], kind)

            try:
                stamp_pdf(src, dst, sticker)
                print(f"  {kind:12s} OK {os.path.basename(src)}  ->  {rel_dst}")
                totals["stamped"] += 1
            except Exception as e:
                print(f"  {kind:12s} X fallo el estampado: {e}")
                totals["failed"] += 1

        print()

    print(
        f"Hecho. obras={len(pairs)}  "
        f"stamped={totals['stamped']}  "
        f"already_done={totals['already_done']}  "
        f"skipped={totals['skipped']}  "
        f"failed={totals['failed']}"
    )
    return 0 if totals["failed"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
