# PDF Merger for AChallan

A user-friendly Windows desktop app that automatically processes challan PDFs by removing trailing blank space and merging two pages onto a single A4 page.

## Features

- **Auto-detect blank space**: Detects where content ends and blank space begins at the bottom of each page
- **Two-page merge**: Combines two cropped pages into one A4-sized page
- **Single-page support**: Odd-page PDFs are placed on an A4 page top-aligned
- **Batch processing**: Select a folder, process all PDFs inside
- **Simple GUI**: Point-and-click interface, no command line needed

## Requirements

- Windows 10 or 11
- No Python or dependencies needed if using the EXE

## How to Use

1. Download `ChallanPDFProcessor.exe` from the [Releases](../../releases) page.
2. Double-click to run.
3. Click **Pick Folder** and select the folder containing your challan PDFs.
4. Optionally choose an output folder; by default outputs are saved alongside originals.
5. Click **Run** and wait for processing to complete.
6. Processed files are saved with a `_processed` suffix (e.g. `file.pdf` -> `file_processed.pdf`).

## Output

- Two-page PDFs become one A4 page with the content stacked vertically
- Single-page PDFs are placed on an A4 page top-aligned
- Blank trailing space is removed automatically

## Screenshot

![App UI](docs/ui-screenshot.png)

## Building from Source

```bash
git clone https://github.com/badip/pdf-merger-for-achallan.git
cd pdf-merger-for-achallan
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python -m src.main
```

To package the EXE:

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name ChallanPDFProcessor --paths src src/main.py
```

## Project Structure

```
pdf-merger-for-achallan/
├── src/
│   ├── main.py
│   ├── gui/
│   ├── processor/
│   └── utils/
├── tests/
├── docs/
├── dist/
└── README.md
```

## License

MIT
