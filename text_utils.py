import re
import unicodedata


def normalize(s: str) -> str:
    """Pasa a minusculas, quita diacriticos y compacta espacios.

    Se usa como clave para comparar titulos de obra, nombres de carpeta y de
    archivo, y encabezados de columna con constantes de config.
    """
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s


def tokenize(s: str) -> frozenset:
    """Normaliza, quita puntuacion y divide en palabras.

    Es util para matches difusos donde el orden no importa, por ejemplo
    RESTREPO AGUIRRE MARIANA (workbook) vs MARIANA RESTREPO AGUIRRE (carpeta).
    """
    n = normalize(s)
    n = re.sub(r"[^\w\s]", " ", n)
    return frozenset(n.split())
