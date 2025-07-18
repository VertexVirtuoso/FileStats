#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to script directory
cd "$SCRIPT_DIR"

# Create virtual environment with system Python if it doesn't exist
if [ ! -d ".venv" ]; then
    /usr/bin/python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
fi

# Run the application using the virtual environment
.venv/bin/python src/file_stats.py