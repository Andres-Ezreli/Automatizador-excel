import os
import fitz  # PyMuPDF
import config


def stamp_pdf(src_path: str, dst_path: str, image_path: str, eje_y: float, eje_x: float) -> None:
    """Lee src_path, superpone un sello de imagen en (X, Y) y guarda en dst_path."""
    
    if not os.path.isfile(src_path):
        raise FileNotFoundError(f"PDF not found: {src_path}")
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Stamp image not found: {image_path}")

    same = os.path.abspath(src_path) == os.path.abspath(dst_path)
    write_path = dst_path + ".stamper.tmp" if same else dst_path

    doc = fitz.open(src_path)
    try:
        if doc.page_count == 0:
            raise ValueError(f"PDF has no pages: {src_path}")

        page = doc[0]

        # Coordenadas PyMuPDF: (0,0) es arriba-izq.
        # Rect = (left, top, right, bottom)
        rect = fitz.Rect(
            eje_x,
            eje_y,
            eje_x + config.STAMP_WIDTH,
            eje_y + config.STAMP_HEIGHT,
        )

        page.insert_image(rect, filename=image_path)

        os.makedirs(os.path.dirname(write_path) or ".", exist_ok=True)
        doc.save(write_path, garbage=4, deflate=True)

    finally:
        doc.close()

    if same:
        os.replace(write_path, dst_path)