# FileStats

A lightweight, hotkey-triggered popup application for Hyprland that displays comprehensive file metadata when a file is selected. Built with Python and GTK4, FileStats provides instant access to detailed information about videos, images, audio files, and documents without interrupting your workflow.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)

## ✨ Features

### 📹 Video Files
- **Format & Codec**: Container format and video/audio codecs
- **Resolution**: Width x Height dimensions
- **Frame Rate**: FPS (frames per second)
- **Duration**: Runtime in HH:MM:SS format
- **Bitrate**: Video and audio bitrates

### 🖼️ Image Files
- **Resolution**: Pixel dimensions
- **Format**: File format (JPEG, PNG, etc.)
- **Color Mode**: RGB, RGBA, Grayscale
- **EXIF Data**: Camera make, model, date taken, and more

### 🎵 Audio Files
- **Duration**: Track length
- **Quality**: Bitrate and sample rate
- **Metadata**: Title, artist, album from ID3 tags
- **Format**: Audio codec information

### 📄 Document Files
- **Page Count**: Number of pages (PDF)
- **Author & Title**: Document metadata
- **Creation Date**: When the document was created
- **File Size**: Human-readable file size

## 🚀 Quick Start

### Prerequisites

- **Operating System**: Arch Linux with Hyprland window manager
- **System Dependencies**: 
  - Python 3.8+
  - GTK4
  - PyGObject (python-gobject)
  - FFmpeg (for ffprobe)
  - ExifTool
  - MediaInfo

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/VertexVirtuoso/FileStats.git
   cd FileStats
   ```

2. **Run the installation script**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Add hotkey to Hyprland**
   
   Add this line to your `~/.config/hypr/hyprland.conf`:
   ```
   bind = CTRL SHIFT, slash, exec, /path/to/FileStats/launch.sh
   ```
   
   Replace `/path/to/FileStats` with the actual path to your installation.

4. **Reload Hyprland configuration**
   ```bash
   hyprctl reload
   ```

## 🎯 Usage

1. **Select a file** in your file manager (Thunar, Nautilus, Dolphin, etc.)
2. **Press the hotkey** (`Ctrl+Shift+/` by default)
3. **View the metadata** in the popup window
4. **Close** with:
   - `Escape` key
   - Close button
   - Window X button
   - Auto-closes after 30 seconds

### Supported File Managers

- ✅ Thunar (XFCE)
- ✅ Nautilus (GNOME Files)
- ✅ Dolphin (KDE)
- ✅ PCManFM
- ✅ Nemo (Cinnamon)
- ✅ Most other file managers via clipboard detection

### File Type Support

| Category | Extensions |
|----------|------------|
| **Video** | `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm`, `.m4v` |
| **Audio** | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma`, `.m4a` |
| **Images** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.svg` |
| **Documents** | `.pdf`, `.doc`, `.docx`, `.txt`, `.odt`, `.rtf` |

## 🔧 How It Works

FileStats uses a multi-layered approach to detect selected files:

1. **Clipboard Detection** (Primary) - Works when you copy a file (`Ctrl+C`)
2. **Window Title Parsing** - Extracts file paths from file manager window titles
3. **DBus Integration** - Direct communication with supported file managers

The application then routes files to specialized metadata extractors:
- **FFprobe** for video/audio analysis
- **PIL/Pillow** for image processing and EXIF data
- **Mutagen** for audio metadata tags
- **PyPDF2** for PDF document information

## 🛠️ Development

### Project Structure

```
FileStats/
├── src/
│   ├── file_stats.py      # Main application entry point
│   ├── metadata_parser.py # File metadata extraction logic
│   ├── file_detector.py   # File selection detection methods
│   └── popup_ui.py        # GTK4 popup interface
├── launch.sh              # Application launcher script
├── install.sh             # Setup and dependency installer
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

### Running from Source

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run directly
./launch.sh
```

### Adding New File Types

To extend support for new file formats:

1. Add file extensions to the appropriate set in `metadata_parser.py`
2. Implement extraction method (e.g., `_get_newtype_info()`)
3. Add the new type to the routing logic in `get_file_info()`

## 🐛 Troubleshooting

### Popup doesn't appear
- Ensure a file is selected in your file manager
- Try copying the file first (`Ctrl+C`) then trigger the hotkey
- Check that the hotkey is correctly configured in Hyprland
- Verify all dependencies are installed

### Import errors
- Ensure you're using system Python, not conda/anaconda
- The install script automatically handles this by creating a proper virtual environment

### No metadata shown
- Check that required tools are installed (`ffprobe`, `exiftool`, `mediainfo`)
- Some metadata may not be available for all file types
- Corrupted files may not provide complete information

### Performance issues
- Large video files may take a moment to analyze
- Network-mounted files may be slower to process
- Consider the file size and complexity for processing time

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines

- Follow existing code style and structure
- Add appropriate error handling for new features
- Test with various file types and managers
- Update documentation for new functionality

## 🙏 Acknowledgments

- Built with [GTK4](https://gtk.org/) for the user interface
- Uses [FFmpeg](https://ffmpeg.org/) for video/audio analysis
- [ExifTool](https://exiftool.org/) for image metadata extraction
- [Hyprland](https://hyprland.org/) for the window manager integration


---

