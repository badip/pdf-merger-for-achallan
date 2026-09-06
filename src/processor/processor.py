from io import BytesIO

import fitz
from PIL import Image
import numpy as np


def _render_page_to_array(page, dpi: int = 150) -> np.ndarray:
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return np.array(img)


def detect_blank_bottom(page, threshold: float = 240.0, min_white_ratio: float = 0.98) -> float:
    arr = _render_page_to_array(page)
    h, w, _ = arr.shape
    gray = arr.mean(axis=2)
    blank_counts = (gray > threshold).sum(axis=1)
    white_ratios = blank_counts / w

    cut_y = h
    for i in range(h - 1, -1, -1):
        if white_ratios[i] < min_white_ratio:
            cut_y = i + 1
            break
    page_height_pts = page.rect.height
    crop_y = cut_y / h * page_height_pts
    return max(crop_y, 0)


def _render_page_to_cropped_png(page, crop_bottom_pts: float, dpi: int = 150) -> bytes:
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    crop_px = int(crop_bottom_pts / 72 * dpi)
    if crop_px < img.height:
        img = img.crop((0, 0, img.width, crop_px))
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def merge_two_to_a4(page1, page2, page1_crop: float, page2_crop: float, margin: int = 30, dpi: int = 150):
    out_doc = fitz.open()
    page = out_doc.new_page(width=595, height=842)
    available = 842 - 2 * margin
    half = available / 2
    r1 = fitz.Rect(margin, margin, 595 - margin, margin + half)
    r2 = fitz.Rect(margin, margin + half, 595 - margin, margin + half + half)

    img1 = _render_page_to_cropped_png(page1, page1_crop, dpi=dpi)
    img2 = _render_page_to_cropped_png(page2, page2_crop, dpi=dpi)

    page.insert_image(r1, stream=img1, keep_proportion=True)
    page.insert_image(r2, stream=img2, keep_proportion=True)
    return out_doc


def process_pdf(input_path: str, output_path: str) -> bool:
    src = None
    out = None
    try:
        src = fitz.open(input_path)
        if src.page_count == 0:
            return False

        out = fitz.open()
        pages = list(src)
        i = 0
        while i < len(pages):
            a = pages[i]
            crop_a = detect_blank_bottom(a)

            if i + 1 < len(pages):
                b = pages[i + 1]
                crop_b = detect_blank_bottom(b)
                merged = merge_two_to_a4(a, b, crop_a, crop_b)
                out.insert_pdf(merged)
                merged.close()
                i += 2
            else:
                page = out.new_page(width=595, height=842)
                img = _render_page_to_cropped_png(a, crop_a)
                page.insert_image(fitz.Rect(30, 30, 595 - 30, 842 - 30), stream=img, keep_proportion=True)
                i += 1

        out.save(output_path)
        return True
    finally:
        if out:
            out.close()
        if src:
            src.close()
