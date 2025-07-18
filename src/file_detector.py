#!/usr/bin/env python3

import subprocess
import os
import re
from typing import Optional

class FileDetector:
    def __init__(self):
        self.supported_file_managers = ['thunar', 'nautilus', 'dolphin', 'pcmanfm', 'nemo']
    
    def get_selected_file(self) -> Optional[str]:
        """Try multiple methods to detect the currently selected file"""
        
        # Method 1: Try clipboard (works with Ctrl+C in most file managers)
        file_path = self._get_from_clipboard()
        if file_path and os.path.exists(file_path):
            return file_path
        
        # Method 2: Try DBus for specific file managers
        file_path = self._get_from_dbus()
        if file_path and os.path.exists(file_path):
            return file_path
        
        # Method 3: Try to get from window title (fallback)
        file_path = self._get_from_window_title()
        if file_path and os.path.exists(file_path):
            return file_path
        
        return None
    
    def _get_from_clipboard(self) -> Optional[str]:
        """Get file path from clipboard"""
        try:
            # Try wl-paste for Wayland
            result = subprocess.run(['wl-paste'], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                clipboard_content = result.stdout.strip()
                if clipboard_content.startswith('file://'):
                    return clipboard_content[7:]  # Remove file:// prefix
                elif os.path.exists(clipboard_content):
                    return clipboard_content
        except:
            pass
        
        try:
            # Fallback to xclip for X11
            result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                clipboard_content = result.stdout.strip()
                if clipboard_content.startswith('file://'):
                    return clipboard_content[7:]
                elif os.path.exists(clipboard_content):
                    return clipboard_content
        except:
            pass
        
        return None
    
    def _get_from_dbus(self) -> Optional[str]:
        """Try to get selected file via DBus from file managers"""
        
        # Try Nautilus
        try:
            result = subprocess.run([
                'dbus-send', '--session', '--print-reply',
                '--dest=org.gnome.Nautilus',
                '/org/gnome/Nautilus',
                'org.freedesktop.Application.GetWindows'
            ], capture_output=True, text=True, timeout=3)
            
            if result.returncode == 0:
                # Parse response to get selection (simplified)
                # This is a basic implementation - full DBus parsing would be more complex
                pass
        except:
            pass
        
        return None
    
    def _get_from_window_title(self) -> Optional[str]:
        """Try to extract file path from active window title"""
        try:
            # Get active window info using hyprctl (Hyprland specific)
            result = subprocess.run(['hyprctl', 'activewindow'], 
                                  capture_output=True, text=True, timeout=2)
            
            if result.returncode == 0:
                window_info = result.stdout
                
                # Look for file manager windows
                for line in window_info.split('\n'):
                    if 'title:' in line.lower():
                        title = line.split(':', 1)[1].strip()
                        
                        # Try to extract path from common file manager title patterns
                        file_path = self._extract_path_from_title(title)
                        if file_path and os.path.exists(file_path):
                            return file_path
        except:
            pass
        
        return None
    
    def _extract_path_from_title(self, title: str) -> Optional[str]:
        """Extract file path from window title"""
        
        # Common patterns in file manager titles
        patterns = [
            r'(.+) - Thunar',           # Thunar: "filename - Thunar"
            r'(.+) - Files',            # Nautilus: "filename - Files"  
            r'(.+) - Dolphin',          # Dolphin: "filename - Dolphin"
            r'(.+) - PCManFM',          # PCManFM: "filename - PCManFM"
            r'^(.+) \[.*\]$',           # Generic: "filename [path]"
            r'^(.+)$'                   # Fallback: just the filename
        ]
        
        for pattern in patterns:
            match = re.match(pattern, title)
            if match:
                potential_path = match.group(1).strip()
                
                # If it looks like a full path, return it
                if potential_path.startswith('/'):
                    return potential_path
                
                # If it's just a filename, try to find it in common directories
                if not '/' in potential_path:
                    common_dirs = [
                        os.path.expanduser('~/Downloads'),
                        os.path.expanduser('~/Documents'),
                        os.path.expanduser('~/Pictures'),
                        os.path.expanduser('~/Videos'),
                        os.path.expanduser('~/Music'),
                        os.path.expanduser('~/Desktop'),
                        os.getcwd()
                    ]
                    
                    for directory in common_dirs:
                        full_path = os.path.join(directory, potential_path)
                        if os.path.exists(full_path):
                            return full_path
        
        return None
    
    def _get_focused_file_manager_path(self) -> Optional[str]:
        """Get the current directory of the focused file manager"""
        try:
            # This is a more advanced technique that would require
            # specific integration with each file manager's APIs
            # For now, return None as this is complex to implement generally
            pass
        except:
            pass
        
        return None