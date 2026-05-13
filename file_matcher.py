import os
import re

import config
from text_utils import normalize

# Modulo: reconocimiento de archivos PDF por nombre.
# Este modulo usa heuristicas de nombre para clasificar PDFs por tipo de
# sticker sin abrir el contenido del documento.


def discover_files(folder: str, obra_title: str):
    """
    Escanea `folder` en busca de PDFs y asigna cada archivo a un tipo.

    Devuelve una tupla (matches, ambiguous):
      - matches[type]   = ruta completa al PDF elegido (None si no hay match)
      - ambiguous[type] = lista de rutas cuando 2+ PDFs coinciden en un tipo

    Reglas y decisiones:
      - La clasificacion se hace solo por nombre normalizado.
      - Archivos sin coincidencia se ignoran silenciosamente.
      - Si `obra_title` esta vacio, no se intenta detectar CARATULA por prefijo.
      - Si hay multiples candidatos de un tipo, se reportan en `ambiguous` y
        `matches[type]` queda en None para forzar decision explicita.
    """
    if not folder:
        # Validacion temprana para evitar trabajar con rutas vacias.
        raise ValueError("Folder path is empty")
    if not os.path.isdir(folder):
        raise NotADirectoryError(f"Folder not found: {folder}")

    pdfs = sorted(
        name for name in os.listdir(folder)
        if name.lower().endswith(".pdf")
        and os.path.isfile(os.path.join(folder, name))
    )

    # Construye regex de CARATULA a partir del titulo de obra normalizado.
    caratula_re = None
    if obra_title:
        title_norm = normalize(obra_title)
        if title_norm:
            caratula_re = re.compile(r"^" + re.escape(title_norm) + r"\b")

    assignments = {t: [] for t in config.STICKER_TYPES}
    for pdf in pdfs:
        stem_norm = normalize(os.path.splitext(pdf)[0])
        kind = _classify(stem_norm, caratula_re)
        if kind is not None:
            assignments[kind].append(os.path.join(folder, pdf))

    matches = {}
    ambiguous = {}
    for kind in config.STICKER_TYPES:
        hits = assignments[kind]
        if len(hits) == 0:
            matches[kind] = None
        elif len(hits) == 1:
            matches[kind] = hits[0]
        else:
            matches[kind] = None
            ambiguous[kind] = hits

    return matches, ambiguous


def _classify(stem_norm: str, caratula_re):
    """
    Clasifica un nombre normalizado segun prioridad de `config.MATCH_PRIORITY`.

    Orden de decision:
      1. CARATULA: match por prefijo usando `caratula_re`.
      2. Demas tipos: presencia de keywords en `config.FILE_KEYWORDS`.
    """
    for kind in config.MATCH_PRIORITY:
        if kind == "CARATULA":
            if caratula_re and caratula_re.match(stem_norm):
                return kind
        else:
            for kw in config.FILE_KEYWORDS.get(kind, []):
                if kw in stem_norm:
                    return kind
    return None
