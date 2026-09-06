# Technology Stack

## Core Technologies
- **Language**: Python 3.10+
- **GUI Framework**: PyQt6
- **PDF Processing**: PyMuPDF (fitz)
- **Image Processing**: Pillow (PIL)
- **Packaging**: PyInstaller

## Key Libraries

### PyQt6
- Purpose: Desktop GUI framework
- Used for: Main window, file dialogs, progress bars, user interface
- Why: Native look and feel, excellent PDF integration, professional appearance

### PyMuPDF (fitz)
- Purpose: PDF manipulation and rendering
- Used for: Reading PDF pages, detecting content boundaries, cropping, merging
- Why: Fast, accurate, supports Python directly, good content detection

### Pillow (PIL)
- Purpose: Image processing
- Used for: Rendering PDF pages to images for preview, image manipulation
- Why: Industry standard, well-maintained, PyMuPDF integrates with it

### PyInstaller
- Purpose: Create standalone executables
- Used for: Packaging the app into .exe for non-technical users
- Why: Creates single-folder or single-file executables, handles dependencies

## Architecture

### Main Components
1. **GUI Layer** (`src/gui/`)
   - MainWindow: Main application window
   - FileSelector: Folder selection and file list
   - PreviewWidget: Shows PDF preview with crop line
   - ProgressDialog: Batch processing progress

2. **Processing Layer** (`src/processor/`)
   - BlankDetector: Auto-detects blank space at bottom of pages
   - Cropper: Crops PDF pages based on detection
   - Merger: Combines two cropped pages into A4
   - BatchProcessor: Processes multiple PDFs in folder

3. **Utility Layer** (`src/utils/`)
   - FileManager: Handles file operations
   - Logger: Application logging
   - ConfigManager: User preferences

### Data Flow
```
User selects folder → App lists PDFs → User configures settings
    → BatchProcessor processes each PDF:
        → Read PDF → Detect blank space → Crop pages → Merge to A4 → Save output
    → Progress updates → Complete
```

## Dependencies
```
PyQt6>=6.4.0
PyMuPDF>=1.22.0
Pillow>=9.5.0
pyinstaller>=5.10.0
```

## Development Environment
- Python 3.10 or higher
- pip for package management
- Virtual environment recommended
- Windows/macOS/Linux compatible
