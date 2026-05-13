import os
import sys
import config
from mp3_mover import move_mp3s

def main():
    # VBA envia: workbook_path, input_path, folder_name.
    if len(sys.argv) < 3:
        print("Error: faltan argumentos.")
        return 1

    workbook_path = sys.argv[1]
    source_path = sys.argv[2]
    target_name = sys.argv[3]

    workbook_dir = os.path.dirname(os.path.abspath(workbook_path))
    # Ruta: 1. Output/FONOGRAMAS/<target_name>.
    target_dir = os.path.join(workbook_dir, config.OUTPUT_SUBFOLDER, config.MP3_OUTPUT_SUBFOLDER, target_name)

    print(f"=== Movimiento Manual de Fonogramas ===")
    print(f"Destino: {target_dir}")

    try:
        # move_mp3s internamente llama a os.makedirs(target_dir, exist_ok=True)
        # y omite archivos si ya existen en el destino.
        moved, skipped = move_mp3s(source_path, target_dir)
        
        if moved:
            print(f"Movimiento hecho: {len(moved)} archivos movidos.")
        if skipped:
            print(f"Omitidos: {len(skipped)} (ya existian).")
        if not moved and not skipped:
            print("No se encontraron MP3s para mover.")

    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())