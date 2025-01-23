#!/usr/bin/env python3
"""
Music Downloader
Version: 1.0.2
Auteur: JPG
Date: Mars 2024

Compatible avec diverses plateformes de streaming vidéo supportées par yt-dlp
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import os
import threading
import queue
import subprocess
from dataclasses import dataclass

@dataclass
class DownloadProgress:
    url: str
    title: str
    progress: float
    status: str
    error: str = ""
    completed: bool = False

class MusicDownloader(Gtk.Window):
    def __init__(self):
        super().__init__(title="Music Downloader")
        self.set_default_size(600, 400)
        
        self.output_dir = os.path.expanduser("~/Musique/Downloads")
        # ... reste du code ...

def main():
    win = MusicDownloader()
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
