from pathlib import Path
from src.utils.helpers import find_pdfs, make_output_name


def test_make_output_name():
    p = Path("/tmp/abc.pdf")
    assert make_output_name(str(p)) == str(Path("/tmp/abc_processed.pdf"))


def test_find_pdfs_empty(tmp_path):
    assert find_pdfs(str(tmp_path)) == []


def test_find_pdfs_nonempty(tmp_path):
    (tmp_path / "a.pdf").write_text("pdf")
    (tmp_path / "b.txt").write_text("txt")
    pdfs = find_pdfs(str(tmp_path))
    assert [Path(p).name for p in pdfs] == ["a.pdf"]
