# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FileStats is a lightweight popup application for Hyprland that displays file metadata when triggered via hotkey while a file is selected. It's designed as a single-shot application that runs, shows metadata, and exits.

## Development Environment

This project uses UV for Python environment management. All Python dependencies are isolated in a virtual environment.

### Setup Commands
```bash
# Install all dependencies (system packages + Python environment)
./install.sh

# Run the application directly
./launch.sh

# Or run with UV manually
uv run src/file_stats.py

# Install Python dependencies only
uv pip install -r requirements.txt
```

## Architecture

The application follows a modular architecture with clear separation of concerns:

1. **file_stats.py** - Main application coordinator that orchestrates the workflow
2. **file_detector.py** - Multi-method file detection (clipboard, DBus, window title parsing)
3. **metadata_parser.py** - File type-specific metadata extraction using external tools
4. **popup_ui.py** - GTK4 popup interface with auto-close functionality

### Application Flow
1. FileDetector attempts multiple detection methods to find selected file
2. MetadataParser routes to appropriate extraction method based on file extension
3. FileStatsPopup displays formatted metadata in GTK4 window
4. Application exits after user interaction or 10-second timeout

### File Detection Strategy
The application tries detection methods in order:
- Clipboard content (primary method, works with Ctrl+C)
- DBus integration with file managers
- Window title parsing (Hyprland-specific using hyprctl)

### Metadata Extraction Tools
- **Videos**: ffprobe (FFmpeg) for comprehensive video/audio stream analysis
- **Audio**: mutagen library for metadata tags + format info
- **Images**: Pillow for dimensions/format + EXIF data extraction
- **Documents**: PyPDF2 for PDF metadata, extensible for other formats

## System Integration

### Hyprland Configuration
Add to hyprland.conf:
```
bind = CTRL SHIFT, slash, exec, /path/to/FileStats/launch.sh
```

### Required System Dependencies
- GTK4 + PyGObject (UI framework)
- ffmpeg (ffprobe command)
- exiftool (image metadata)
- mediainfo (media file analysis)
- wl-paste or xclip (clipboard access)

## Error Handling

The application is designed to fail gracefully:
- No file selected: exits silently
- File not found: displays error in popup
- Missing tools: shows "N/A" for unavailable metadata
- Parsing errors: displays error message with file basics

## File Type Support

Extensible design based on file extension mapping:
- Video: .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v
- Audio: .mp3, .wav, .flac, .aac, .ogg, .wma, .m4a  
- Image: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .webp, .svg
- Document: .pdf, .doc, .docx, .txt, .odt, .rtf

To add support for new file types, extend the appropriate extension set in MetadataParser and implement the corresponding extraction method.