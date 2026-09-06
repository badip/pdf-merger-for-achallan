from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QProgressBar, QLabel,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal
from src.utils.helpers import find_pdfs, make_output_name
from src.processor.processor import process_pdf


class Worker(QThread):
    progress = pyqtSignal(int, int)  # current, total
    finished_file = pyqtSignal(str, bool, str)
    done = pyqtSignal()

    def __init__(self, files: list[str], out_folder: str):
        super().__init__()
        self.files = files
        self.out_folder = out_folder
        self._stopped = False

    def run(self):
        total = len(self.files)
        for idx, path in enumerate(self.files, 1):
            if self._stopped:
                break
            out_name = make_output_name(path)
            out_path = str(Path(self.out_folder) / Path(out_name).name)
            try:
                ok = process_pdf(path, out_path)
                self.finished_file.emit(path, ok, out_path)
            except Exception as e:
                self.finished_file.emit(path, False, str(e))
            self.progress.emit(idx, total)
        self.done.emit()

    def stop(self):
        self._stopped = True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Challan PDF Processor")
        self.setMinimumSize(780, 520)
        self.worker: Worker | None = None
        self.files: list[str] = []
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        top = QHBoxLayout()
        self.lbl_folder = QLabel("Select input folder...")
        self.btn_pick = QPushButton("Pick Folder")
        self.btn_pick.clicked.connect(self.pick_folder)
        top.addWidget(self.lbl_folder, 1)
        top.addWidget(self.btn_pick)
        root.addLayout(top)

        self.list = QListWidget()
        root.addWidget(self.list, 1)

        self.progress = QProgressBar()
        self.progress.setRange(0, 1)
        root.addWidget(self.progress)

        self.status = QLabel("Ready")
        root.addWidget(self.status)

        row = QHBoxLayout()
        self.btn_out = QPushButton("Choose Output Folder")
        self.btn_out.clicked.connect(self.pick_output)
        self.lbl_out = QLabel("Output: same as input")
        row.addWidget(self.btn_out)
        row.addWidget(self.lbl_out, 1)
        root.addLayout(row)

        self.btn_run = QPushButton("Run")
        self.btn_run.clicked.connect(self.run)
        root.addWidget(self.btn_run)

        self.output_dir: str | None = None

    def pick_folder(self):
        d = QFileDialog.getExistingDirectory(self, "Select PDF Folder")
        if not d:
            return
        self.files = find_pdfs(d)
        self.input_dir = d
        self.lbl_folder.setText(d)
        self.list.clear()
        for f in self.files:
            self.list.addItem(Path(f).name)
        self.status.setText(f"{len(self.files)} PDFs found")

    def pick_output(self):
        d = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if not d:
            return
        self.output_dir = d
        self.lbl_out.setText(d)

    def run(self):
        if not self.files:
            QMessageBox.warning(self, "No files", "Please select a folder with PDFs first.")
            return
        out = self.output_dir or getattr(self, "input_dir", None)
        if not out:
            QMessageBox.warning(self, "No output", "Choose an output folder.")
            return
        self.btn_run.setEnabled(False)
        self.progress.setRange(0, len(self.files))
        self.progress.setValue(0)
        self.worker = Worker(self.files, out)
        self.worker.progress.connect(lambda cur, total: self.progress.setValue(cur))
        self.worker.finished_file.connect(lambda path, ok, msg: self.status.setText(f"{Path(path).name}: {'OK' if ok else 'FAIL'} -> {msg}"))
        self.worker.done.connect(lambda: self.status.setText("Done") or self.btn_run.setEnabled(True))
        self.worker.start()
