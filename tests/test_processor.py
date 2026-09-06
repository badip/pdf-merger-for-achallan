import fitz
import tempfile
from pathlib import Path
from src.processor.processor import detect_blank_bottom, merge_two_to_a4, process_pdf


def _write_sample_pdf(path: Path, pages: int = 2):
    doc = fitz.open()
    for _ in range(pages):
        page = doc.new_page(width=595, height=842)
        page.insert_text((72, 72), "Sample body text", fontsize=14)
    doc.save(str(path))
    doc.close()


def test_detect_blank_bottom_trims_white():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "a.pdf"
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)
        page.insert_text((72, 72), "Sample body text", fontsize=14)
        doc.save(str(p))
        doc.close()
        src = fitz.open(str(p))
        crop = detect_blank_bottom(src[0])
        src.close()
        assert 72 < crop < 842


def test_merge_two_produces_a4():
    with tempfile.TemporaryDirectory() as td:
        p1 = Path(td) / "a.pdf"
        p2 = Path(td) / "b.pdf"
        _write_sample_pdf(p1, 1)
        _write_sample_pdf(p2, 1)
        d1 = fitz.open(str(p1))
        d2 = fitz.open(str(p2))
        merged = merge_two_to_a4(d1[0], d2[0], 100, 100)
        d1.close()
        d2.close()
        assert merged.page_count == 1
        page = merged[0]
        assert abs(page.rect.width - 595) < 1e-3
        assert abs(page.rect.height - 842) < 1e-3
        merged.close()


def test_process_pdf_creates_output():
    with tempfile.TemporaryDirectory() as td_in, tempfile.TemporaryDirectory() as td_out:
        inp = Path(td_in) / "in.pdf"
        out = Path(td_out) / "out.pdf"
        _write_sample_pdf(inp, 2)
        ok = process_pdf(str(inp), str(out))
        assert ok is True
        assert out.exists()
