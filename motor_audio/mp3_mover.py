import os
import shutil


def move_mp3s(source_folder: str, target_dir: str):
    """Mueve todos los archivos .mp3 desde source_folder hacia target_dir.

    Devuelve (moved, skipped):
        moved   = lista de nombres movidos
        skipped = lista de tuplas (nombre, motivo)
    """
    if not os.path.isdir(source_folder):
        raise NotADirectoryError(f"Source folder not found: {source_folder}")

    moved = []
    skipped = []

    mp3s = [
        name for name in os.listdir(source_folder)
        if name.lower().endswith(".mp3")
        and os.path.isfile(os.path.join(source_folder, name))
    ]

    if not mp3s:
        return moved, skipped

    os.makedirs(target_dir, exist_ok=True)

    for name in mp3s:
        src = os.path.join(source_folder, name)
        dst = os.path.join(target_dir, name)
        if os.path.exists(dst):
            skipped.append((name, "ya existe en destino"))
            continue
        shutil.move(src, dst)
        moved.append(name)

    return moved, skipped
