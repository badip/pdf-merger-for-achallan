# PDF Processing Tool - Read First

## Project Goal
Build a user-friendly desktop application that automatically processes PDF files by:
1. Detecting and removing blank space from the bottom of each page
2. Merging two pages into a single A4-sized page (vertical stack)
3. Processing all PDFs in a folder in batch mode

## Who This Is For
Non-technical users who need to process multiple PDF files without understanding PDF editing tools.

## How To Use This Project
1. Read `tech.md` to understand the technology stack and architecture
2. Check `update.md` for current progress and what's being worked on
3. The main application will be in `src/` directory
4. Run `python main.py` or use the packaged executable

## Key Features
- **Auto-detect blank space**: Automatically detects where content ends and blank space begins
- **Batch processing**: Select a folder, process all PDFs inside
- **A4 output**: Combined content scaled to fit A4 page
- **GUI interface**: Point-and-click, no command line needed

## Project Structure
```
pdf-processor/
├── README.md          # This file - start here
├── tech.md           # Technology stack and architecture
├── update.md         # Progress tracker and checkpoints
├── src/
│   ├── main.py       # Application entry point
│   ├── gui/          # PyQt6 interface
│   ├── processor/    # PDF processing logic
│   └── utils/        # Helper functions
├── tests/            # Test suite
├── docs/             # Documentation
└── dist/             # Compiled executables (generated)
```

## Getting Started
See `update.md` for current status and next steps.
