#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gdk
from typing import Dict, Any

class FileStatsPopup:
    def __init__(self, app):
        self.window = None
        self.app = app
        
    def show_file_info(self, file_info: Dict[str, Any]):
        """Display file information in a popup window"""
        
        # Create the main window
        self.window = Gtk.ApplicationWindow(application=self.app)
        self.window.set_title("File Information")
        self.window.set_default_size(400, 300)
        self.window.set_resizable(False)
        self.window.set_decorated(True)
        
        # Set window properties for popup behavior
        self.window.set_modal(True)
        # Note: set_type_hint is deprecated in GTK4
        
        # Create main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(15)
        main_box.set_margin_bottom(15)
        main_box.set_margin_start(15)
        main_box.set_margin_end(15)
        
        # Add title
        title_label = Gtk.Label()
        title_label.set_markup(f"<span size='large' weight='bold'>{file_info.get('filename', 'Unknown File')}</span>")
        title_label.set_halign(Gtk.Align.START)
        main_box.append(title_label)
        
        # Add separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.append(separator)
        
        # Create scrolled window for content
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(200)
        
        # Create content box
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
        # Add file information
        self._add_file_details(content_box, file_info)
        
        scrolled.set_child(content_box)
        main_box.append(scrolled)
        
        # Add close button
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        button_box.set_halign(Gtk.Align.END)
        
        close_button = Gtk.Button(label="Close")
        close_button.connect("clicked", self._on_close_clicked)
        close_button.add_css_class("suggested-action")
        button_box.append(close_button)
        
        main_box.append(button_box)
        
        # Set up window
        self.window.set_child(main_box)
        
        # Connect window close events
        self.window.connect("close-request", self._on_window_close)
        
        # Connect keyboard shortcuts
        key_controller = Gtk.EventControllerKey()
        key_controller.connect("key-pressed", self._on_key_pressed)
        self.window.add_controller(key_controller)
        
        # Center window on screen
        self._center_window()
        
        # Show window
        self.window.present()
        
        # Auto-close after 30 seconds
        GLib.timeout_add_seconds(30, self._auto_close)
        
    def _add_file_details(self, container: Gtk.Box, file_info: Dict[str, Any]):
        """Add file details to the container"""
        
        # Handle error case
        if "error" in file_info:
            error_label = Gtk.Label()
            error_label.set_markup(f"<span color='red'>Error: {file_info['error']}</span>")
            error_label.set_halign(Gtk.Align.START)
            container.append(error_label)
            return
        
        # Basic file information
        basic_info = [
            ("Type", file_info.get("type", "Unknown")),
            ("Size", file_info.get("size", "Unknown")),
            ("Extension", file_info.get("extension", "Unknown")),
        ]
        
        for label, value in basic_info:
            self._add_info_row(container, label, value)
        
        # Type-specific information
        file_type = file_info.get("type", "").lower()
        
        if file_type == "video":
            self._add_video_info(container, file_info)
        elif file_type == "audio":
            self._add_audio_info(container, file_info)
        elif file_type == "image":
            self._add_image_info(container, file_info)
        elif file_type == "document":
            self._add_document_info(container, file_info)
        
        # Add path at the end
        if "path" in file_info:
            self._add_info_row(container, "Path", file_info["path"], monospace=True)
    
    def _add_video_info(self, container: Gtk.Box, file_info: Dict[str, Any]):
        """Add video-specific information"""
        video_info = [
            ("Resolution", file_info.get("resolution", "Unknown")),
            ("Codec", file_info.get("codec", "Unknown")),
            ("FPS", file_info.get("fps", "Unknown")),
            ("Duration", file_info.get("duration", "Unknown")),
            ("Bitrate", file_info.get("bitrate", "Unknown")),
        ]
        
        if "audio_codec" in file_info:
            video_info.append(("Audio Codec", file_info["audio_codec"]))
        
        for label, value in video_info:
            if value != "Unknown" and value != "N/A":
                self._add_info_row(container, label, value)
    
    def _add_audio_info(self, container: Gtk.Box, file_info: Dict[str, Any]):
        """Add audio-specific information"""
        audio_info = [
            ("Duration", file_info.get("duration", "Unknown")),
            ("Bitrate", file_info.get("bitrate", "Unknown")),
            ("Sample Rate", file_info.get("sample_rate", "Unknown")),
        ]
        
        # Add metadata if available
        for key in ["title", "artist", "album"]:
            if key in file_info:
                audio_info.append((key.title(), file_info[key]))
        
        for label, value in audio_info:
            if value != "Unknown" and value != "N/A":
                self._add_info_row(container, label, value)
    
    def _add_image_info(self, container: Gtk.Box, file_info: Dict[str, Any]):
        """Add image-specific information"""
        image_info = [
            ("Resolution", file_info.get("resolution", "Unknown")),
            ("Format", file_info.get("format", "Unknown")),
            ("Mode", file_info.get("mode", "Unknown")),
        ]
        
        for label, value in image_info:
            if value != "Unknown" and value != "N/A":
                self._add_info_row(container, label, value)
        
        # Add EXIF data if available
        if "exif" in file_info:
            exif_data = file_info["exif"]
            if exif_data:
                # Add separator for EXIF data
                separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                container.append(separator)
                
                exif_label = Gtk.Label()
                exif_label.set_markup("<span weight='bold'>EXIF Data</span>")
                exif_label.set_halign(Gtk.Align.START)
                container.append(exif_label)
                
                for key, value in exif_data.items():
                    self._add_info_row(container, key, str(value))
    
    def _add_document_info(self, container: Gtk.Box, file_info: Dict[str, Any]):
        """Add document-specific information"""
        doc_info = [
            ("Format", file_info.get("format", "Unknown")),
        ]
        
        if "pages" in file_info:
            doc_info.append(("Pages", str(file_info["pages"])))
        
        for key in ["title", "author", "created"]:
            if key in file_info:
                doc_info.append((key.title(), file_info[key]))
        
        for label, value in doc_info:
            if value != "Unknown" and value != "N/A":
                self._add_info_row(container, label, value)
    
    def _add_info_row(self, container: Gtk.Box, label: str, value: str, monospace: bool = False):
        """Add a label-value row to the container"""
        row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        # Label
        label_widget = Gtk.Label(label=f"{label}:")
        label_widget.set_halign(Gtk.Align.START)
        label_widget.set_size_request(120, -1)  # Fixed width for alignment
        label_widget.add_css_class("caption")
        row_box.append(label_widget)
        
        # Value
        value_widget = Gtk.Label(label=str(value))
        value_widget.set_halign(Gtk.Align.START)
        value_widget.set_selectable(True)  # Allow text selection
        value_widget.set_wrap(True)
        value_widget.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        
        if monospace:
            value_widget.add_css_class("monospace")
        
        row_box.append(value_widget)
        container.append(row_box)
    
    def _center_window(self):
        """Center the window on the screen"""
        # Get display and monitor info
        display = Gdk.Display.get_default()
        if display:
            # This is a simplified centering - GTK4 handles most of this automatically
            pass
    
    def _on_close_clicked(self, button):
        """Handle close button click"""
        self._quit_app()
    
    def _on_window_close(self, window):
        """Handle window close request"""
        self._quit_app()
        return False
    
    def _on_key_pressed(self, controller, keyval, keycode, state):
        """Handle keyboard shortcuts"""
        if keyval == Gdk.KEY_Escape:
            self._quit_app()
            return True
        return False
    
    def _auto_close(self):
        """Auto-close the window after timeout"""
        self._quit_app()
        return False  # Don't repeat the timeout
    
    def _quit_app(self):
        """Quit the application"""
        if self.window:
            self.window.close()
        if self.app:
            self.app.quit()