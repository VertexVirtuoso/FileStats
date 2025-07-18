#!/usr/bin/env python3

import subprocess
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image
from PIL.ExifTags import TAGS
import mutagen
from PyPDF2 import PdfReader

class MetadataParser:
    def __init__(self):
        self.video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'}
        self.audio_extensions = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'}
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'}
        self.document_extensions = {'.pdf', '.doc', '.docx', '.txt', '.odt', '.rtf'}

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            return {"error": "File not found"}
        
        path_obj = Path(file_path)
        extension = path_obj.suffix.lower()
        file_size = os.path.getsize(file_path)
        
        base_info = {
            "filename": path_obj.name,
            "extension": extension,
            "size": self._format_size(file_size),
            "path": file_path
        }

        try:
            if extension in self.video_extensions:
                return {**base_info, **self._get_video_info(file_path)}
            elif extension in self.audio_extensions:
                return {**base_info, **self._get_audio_info(file_path)}
            elif extension in self.image_extensions:
                return {**base_info, **self._get_image_info(file_path)}
            elif extension in self.document_extensions:
                return {**base_info, **self._get_document_info(file_path)}
            else:
                return {**base_info, "type": "Unknown", "info": "Unsupported file type"}
        except Exception as e:
            return {**base_info, "error": f"Error parsing metadata: {str(e)}"}

    def _get_video_info(self, file_path: str) -> Dict[str, Any]:
        try:
            cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                return {"type": "Video", "error": "Could not analyze video"}
            
            data = json.loads(result.stdout)
            video_stream = next((s for s in data['streams'] if s['codec_type'] == 'video'), None)
            audio_stream = next((s for s in data['streams'] if s['codec_type'] == 'audio'), None)
            
            info = {"type": "Video"}
            
            if video_stream:
                info.update({
                    "resolution": f"{video_stream.get('width', 'N/A')}x{video_stream.get('height', 'N/A')}",
                    "codec": video_stream.get('codec_name', 'N/A'),
                    "fps": self._get_fps(video_stream),
                    "bitrate": self._format_bitrate(video_stream.get('bit_rate')),
                })
            
            if audio_stream:
                info["audio_codec"] = audio_stream.get('codec_name', 'N/A')
            
            if 'format' in data:
                duration = float(data['format'].get('duration', 0))
                info["duration"] = self._format_duration(duration)
                
            return info
            
        except Exception as e:
            return {"type": "Video", "error": str(e)}

    def _get_audio_info(self, file_path: str) -> Dict[str, Any]:
        try:
            info = {"type": "Audio"}
            
            # Use mutagen for audio metadata
            audio_file = mutagen.File(file_path)
            if audio_file:
                info.update({
                    "duration": self._format_duration(audio_file.info.length if audio_file.info else 0),
                    "bitrate": f"{getattr(audio_file.info, 'bitrate', 'N/A')} kbps" if audio_file.info else 'N/A',
                    "sample_rate": f"{getattr(audio_file.info, 'sample_rate', 'N/A')} Hz" if audio_file.info else 'N/A',
                })
                
                # Extract common tags
                if audio_file.tags:
                    title = audio_file.tags.get('TIT2') or audio_file.tags.get('TITLE')
                    artist = audio_file.tags.get('TPE1') or audio_file.tags.get('ARTIST')
                    album = audio_file.tags.get('TALB') or audio_file.tags.get('ALBUM')
                    
                    if title: info["title"] = str(title[0]) if isinstance(title, list) else str(title)
                    if artist: info["artist"] = str(artist[0]) if isinstance(artist, list) else str(artist)
                    if album: info["album"] = str(album[0]) if isinstance(album, list) else str(album)
            
            return info
            
        except Exception as e:
            return {"type": "Audio", "error": str(e)}

    def _get_image_info(self, file_path: str) -> Dict[str, Any]:
        try:
            info = {"type": "Image"}
            
            with Image.open(file_path) as img:
                info.update({
                    "resolution": f"{img.width}x{img.height}",
                    "mode": img.mode,
                    "format": img.format,
                })
                
                # Extract EXIF data
                exifdata = img.getexif()
                if exifdata:
                    exif_info = {}
                    for tag_id, value in exifdata.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag in ['Make', 'Model', 'DateTime', 'Software']:
                            exif_info[tag] = str(value)
                    
                    if exif_info:
                        info["exif"] = exif_info
            
            return info
            
        except Exception as e:
            return {"type": "Image", "error": str(e)}

    def _get_document_info(self, file_path: str) -> Dict[str, Any]:
        try:
            extension = Path(file_path).suffix.lower()
            info = {"type": "Document"}
            
            if extension == '.pdf':
                with open(file_path, 'rb') as f:
                    pdf = PdfReader(f)
                    info.update({
                        "pages": len(pdf.pages),
                        "format": "PDF"
                    })
                    
                    if pdf.metadata:
                        if pdf.metadata.get('/Title'):
                            info["title"] = pdf.metadata['/Title']
                        if pdf.metadata.get('/Author'):
                            info["author"] = pdf.metadata['/Author']
                        if pdf.metadata.get('/CreationDate'):
                            info["created"] = str(pdf.metadata['/CreationDate'])
            else:
                info["format"] = extension.upper().lstrip('.')
            
            return info
            
        except Exception as e:
            return {"type": "Document", "error": str(e)}

    def _get_fps(self, stream: Dict) -> str:
        fps = stream.get('r_frame_rate', '0/1')
        try:
            if '/' in fps:
                num, den = fps.split('/')
                return f"{float(num) / float(den):.2f} fps"
            return f"{float(fps):.2f} fps"
        except:
            return "N/A fps"

    def _format_duration(self, seconds: float) -> str:
        if seconds == 0:
            return "N/A"
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"

    def _format_size(self, size_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def _format_bitrate(self, bitrate: Optional[str]) -> str:
        if not bitrate:
            return "N/A"
        try:
            br = int(bitrate) // 1000
            return f"{br} kbps"
        except:
            return "N/A"