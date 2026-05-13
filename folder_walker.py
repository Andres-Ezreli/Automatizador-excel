import os

from text_utils import normalize, tokenize


def find_obra_folders(input_root: str, obras: list) -> list:
    """Recorre `input_root` de forma recursiva para hallar carpetas de obra.

    Una carpeta coincide con una obra cuando:
      * su nombre final == NOMBRE de la obra (normalizado), y
      * alguno de sus ancestros tiene el mismo conjunto de palabras que COMPOSITOR.

    Esta comparacion por conjunto de palabras maneja cambios de orden como
    RESTREPO AGUIRRE MARIANA (workbook) vs MARIANA RESTREPO AGUIRRE (carpeta).
    Si una obra no tiene COMPOSITOR, se omite esa validacion (fallback por NOMBRE).

    Devuelve lista de pares (obra_dict, ruta_carpeta).
    """
    if not os.path.isdir(input_root):
        raise NotADirectoryError(f"Input folder not found: {input_root}")

    by_nombre = {}
    for o in obras:
        nombre = o.get("nombre", "").strip()
        if not nombre:
            continue
        key = normalize(nombre)
        if key:
            by_nombre.setdefault(key, []).append(o)

    matches = []
    for dirpath, dirnames, _ in os.walk(input_root):
        ancestor_token_sets = _ancestor_token_sets(dirpath)
        for d in dirnames:
            key = normalize(d)
            if key not in by_nombre:
                continue
            full = os.path.join(dirpath, d)
            for o in by_nombre[key]:
                author = o.get("author", "")
                if not author.strip():
                    matches.append((o, full))
                    continue
                author_tokens = tokenize(author)
                if author_tokens in ancestor_token_sets:
                    matches.append((o, full))
    return matches


def _ancestor_token_sets(dirpath: str) -> set:
    """Conjunto de token-sets, uno por cada nombre ancestro de `dirpath`."""
    out = set()
    p = dirpath
    while True:
        head, tail = os.path.split(p)
        if not tail or head == p:
            break
        out.add(tokenize(tail))
        p = head
    return out
