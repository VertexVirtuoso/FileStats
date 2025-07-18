#!/usr/bin/env python3

import sys
import os
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from metadata_parser import MetadataParser
from file_detector import FileDetector
from popup_ui import FileStatsPopup

class FileStatsApp:
    def __init__(self):
        self.parser = MetadataParser()
        self.detector = FileDetector()
        self.app = None
        self.popup = None
        
    def run(self):
        """Main application entry point"""
        # Detect the selected file
        file_path = self.detector.get_selected_file()
        
        if not file_path:
            # No file selected, exit silently
            return
        
        # Get file metadata
        file_info = self.parser.get_file_info(file_path)
        
        # Create GTK application
        self.app = Gtk.Application(application_id='com.filestats.popup')
        self.popup = FileStatsPopup(self.app)
        self.app.connect('activate', lambda app: self._on_activate(file_info))
        
        # Run the application
        self.app.run([])
    
    def _on_activate(self, file_info):
        """Handle application activation"""
        self.popup.show_file_info(file_info)

def main():
    """Entry point for the application"""
    try:
        app = FileStatsApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()