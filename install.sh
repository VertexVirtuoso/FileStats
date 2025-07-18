#!/bin/bash

echo "Installing FileStats dependencies..."

# Check if running on Arch Linux
if command -v pacman >/dev/null 2>&1; then
    echo "Installing system dependencies via pacman..."
    sudo pacman -S --needed python python-gobject gtk4 ffmpeg exiftool mediainfo
else
    echo "Please install the following packages manually:"
    echo "- Python 3.8+"
    echo "- python-gobject (PyGObject)"
    echo "- GTK4"
    echo "- ffmpeg (for ffprobe)"
    echo "- exiftool"
    echo "- mediainfo"
fi

# Create virtual environment and install Python dependencies
echo "Creating virtual environment..."
if [ ! -d ".venv" ]; then
    /usr/bin/python3 -m venv .venv
fi
echo "Installing Python dependencies..."
.venv/bin/pip install -r requirements.txt

echo "Making launch script executable..."
chmod +x launch.sh

echo "Installation complete!"
echo ""
echo "To add the hotkey to Hyprland, add this line to your hyprland.conf:"
echo "bind = CTRL SHIFT, slash, exec, $(pwd)/launch.sh"