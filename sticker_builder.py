import config


def build_sticker(obra: dict, sticker_type: str):
    """Construye el texto del sticker para una obra y un tipo.

    Devuelve None cuando la obra no tiene doc code para ese tipo; el script
    principal trata ese caso como omision.
    """
    doc_code = obra["doc_codes"].get(sticker_type)
    if not doc_code:
        return None
    return config.STICKER_TEMPLATE.format(
        codigo=obra.get("codigo", ""),
        doc_code=doc_code,
        fecha_recibido=obra.get("fecha_recibido", ""),
        fecha_alta_sgs=obra.get("fecha_alta_sgs", ""),
        funcionario=obra.get("funcionario", ""),
    )
