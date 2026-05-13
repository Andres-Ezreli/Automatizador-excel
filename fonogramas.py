import os
import sys

sys.stdout.reconfigure(errors="replace")
sys.stderr.reconfigure(errors="replace")

import config
from excel_reader import read_obras, read_input_path
from folder_walker import find_obra_folders
from mp3_mover import move_mp3s

def main() -> int:
    if len(sys.argv) < 2:
        print("ERROR: workbook path missing.")
        return 1
    workbook_path = sys.argv[1]

    workbook_dir = os.path.dirname(os.path.abspath(workbook_path))
    typed = read_input_path(workbook_path)
    input_root = typed if typed else os.path.join(workbook_dir, config.INPUT_SUBFOLDER)
    output_dir = os.path.join(workbook_dir, config.OUTPUT_SUBFOLDER)

    print("=== Mover Fonogramas ===")
    
    obras = read_obras(workbook_path)
    pairs = find_obra_folders(input_root, obras)
    
    if not pairs:
        print("(No folders found to process)")
        return 0

    totals = {"moved": 0, "skipped": 0}

    for obra, folder in pairs:
        # Segun la estructura definida en `config.py`: 1. Output/FONOGRAMAS/<codigo>/
        codigo = obra.get("codigo", "SIN_CODIGO")
        target_dir = os.path.join(output_dir, config.MP3_OUTPUT_SUBFOLDER, codigo)
        
        moved, skipped = move_mp3s(folder, target_dir)
        if moved:
            print(f"✓ {obra['nombre']} -> Moved {len(moved)} MP3s to {codigo}/")
        
        totals["moved"] += len(moved)
        totals["skipped"] += len(skipped)

    print(f"\nDone. mp3_moved={totals['moved']}  skipped={totals['skipped']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())