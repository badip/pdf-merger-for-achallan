import logging
from pathlib import Path


def setup_logging(log_dir: str = None) -> logging.Logger:
    if log_dir is None:
        log_dir = Path.home() / ".pdf_processor"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"
    logger = logging.getLogger("pdf_processor")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        fh.setFormatter(fmt)
        ch.setFormatter(fmt)
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger


logger = setup_logging()


def find_pdfs(folder: str) -> list[str]:
    folder_path = Path(folder)
    if not folder_path.exists() or not folder_path.is_dir():
        logger.error(f"Folder not found or not a directory: {folder}")
        return []
    pdfs = sorted(folder_path.glob("*.pdf"))
    return [str(p) for p in pdfs]


def make_output_name(input_path: str, suffix: str = "_processed") -> str:
    p = Path(input_path)
    return str(p.with_name(p.stem + suffix + p.suffix))


def validate_output_path(path: str) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return str(p)
