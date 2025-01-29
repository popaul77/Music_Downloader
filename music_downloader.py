#!/usr/bin/env python3
"""
Music Downloader
Version: 1.0.2
Auteur: JPG
Date: Mars 2024

Compatible avec :
- YouTube
- PeerTube
- Et autres plateformes supportées par yt-dlp
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

class YouTubeDownloader(Gtk.Window):
    def __init__(self):
        super().__init__(title="Music Downloader")
        self.set_default_size(600, 400)
        
        self.output_dir = os.path.expanduser("~/Musique/YouTube")
        self.progress_queue = queue.Queue()
        self.downloader = None
        
        # Créer le répertoire de sortie s'il n'existe pas
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Box principale verticale
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(10)
        main_box.set_margin_bottom(10)
        main_box.set_margin_start(10)
        main_box.set_margin_end(10)
        self.add(main_box)

        # Box pour le dossier de destination
        dest_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        
        # Label pour le dossier de destination
        dest_label = Gtk.Label(label="Dossier de destination : ")
        dest_box.pack_start(dest_label, False, True, 0)
        
        # Entry pour afficher le chemin
        self.dest_entry = Gtk.Entry()
        self.dest_entry.set_text(self.output_dir)
        self.dest_entry.set_editable(False)
        dest_box.pack_start(self.dest_entry, True, True, 0)
        
        # Bouton pour changer le dossier
        change_dir_button = Gtk.Button(label="Changer")
        change_dir_button.connect("clicked", self.change_output_dir)
        dest_box.pack_start(change_dir_button, False, True, 0)
        
        main_box.pack_start(dest_box, False, True, 0)

        # Zone de texte pour les URLs
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        self.url_text = Gtk.TextView()
        self.url_text.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled.add(self.url_text)
        main_box.pack_start(scrolled, True, True, 0)

        # Boutons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        button_box.set_halign(Gtk.Align.CENTER)

        # Bouton pour charger urls.txt
        load_button = Gtk.Button(label="Charger urls.txt")
        load_button.connect("clicked", self.load_urls)
        button_box.pack_start(load_button, True, True, 0)

        # Bouton de téléchargement
        self.download_button = Gtk.Button(label="Télécharger")
        self.download_button.connect("clicked", self.start_download)
        button_box.pack_start(self.download_button, True, True, 0)

        # Bouton Quitter
        quit_button = Gtk.Button(label="Quitter")
        quit_button.connect("clicked", self.quit_app)
        button_box.pack_start(quit_button, True, True, 0)

        main_box.pack_start(button_box, False, True, 0)

        # Zone de progression
        scrolled_progress = Gtk.ScrolledWindow()
        scrolled_progress.set_vexpand(True)
        self.progress_text = Gtk.TextView()
        self.progress_text.set_editable(False)
        self.progress_text.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled_progress.add(self.progress_text)
        main_box.pack_start(scrolled_progress, True, True, 0)

        self.connect("destroy", Gtk.main_quit)
        GLib.timeout_add(100, self.check_progress)

    def load_urls(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Choisir le fichier urls.txt",
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            "Annuler", Gtk.ResponseType.CANCEL,
            "Ouvrir", Gtk.ResponseType.OK
        )

        filter_txt = Gtk.FileFilter()
        filter_txt.set_name("Fichiers texte")
        filter_txt.add_pattern("*.txt")
        dialog.add_filter(filter_txt)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    buffer = self.url_text.get_buffer()
                    buffer.set_text(content)
            except Exception as e:
                self.show_error(f"Erreur lors de la lecture du fichier : {str(e)}")
        dialog.destroy()

    def show_error(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()

    def show_info(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()

    def quit_app(self, button):
        if self.downloader and self.downloader.is_alive():
            dialog = Gtk.MessageDialog(
                transient_for=self,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text="Des téléchargements sont en cours. Voulez-vous vraiment quitter ?"
            )
            response = dialog.run()
            dialog.destroy()
            if response == Gtk.ResponseType.YES:
                # Tuer tous les processus yt-dlp
                try:
                    subprocess.run(['pkill', '-f', 'yt-dlp'])
                except:
                    pass
                # Attendre la fin du thread
                self.downloader.join(timeout=1)
                Gtk.main_quit()
        else:
            Gtk.main_quit()

    def append_progress_text(self, text):
        buffer = self.progress_text.get_buffer()
        end_iter = buffer.get_end_iter()
        buffer.insert(end_iter, text + "\n")
        
        # Nouvelle façon de faire défiler jusqu'en bas
        vadj = self.progress_text.get_parent().get_vadjustment()
        vadj.set_value(vadj.get_upper() - vadj.get_page_size())

    def start_download(self, button):
        buffer = self.url_text.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        text = buffer.get_text(start_iter, end_iter, False)
        
        urls = [url.strip() for url in text.split('\n') if url.strip()]
        
        if not urls:
            self.show_error("Veuillez entrer au moins une URL YouTube.")
            return
            
        self.download_button.set_sensitive(False)
        self.progress_text.get_buffer().set_text("")
        
        def download_thread():
            for url in urls:
                self.download_url(url)
            GLib.idle_add(self.download_completed)
            
        self.downloader = threading.Thread(target=download_thread)
        self.downloader.start()

    def download_completed(self):
        self.download_button.set_sensitive(True)
        self.show_info("Tous les téléchargements sont terminés !")

    def download_url(self, url: str):
        """Télécharge une URL YouTube"""
        try:
            # Vérifier si c'est une playlist
            is_playlist = 'list=' in url
            
            if is_playlist:
                # Obtenir les informations de la playlist
                GLib.idle_add(self.append_progress_text, f"Analyse de la playlist...")
                
                # Commande pour obtenir les infos de la playlist
                cmd_info = [
                    'yt-dlp',
                    '--flat-playlist',
                    '--print', 'title',
                    url
                ]
                
                # Récupérer les titres
                process_info = subprocess.run(cmd_info, capture_output=True, text=True)
                if process_info.returncode != 0:
                    raise Exception("Impossible d'obtenir les informations de la playlist")
                
                # Liste des titres
                titles = [line for line in process_info.stdout.split('\n') if line.strip()]
                GLib.idle_add(self.append_progress_text, f"Playlist trouvée : {len(titles)} morceaux")
                
                # Télécharger la playlist
                cmd = [
                    'yt-dlp',
                    '-x',                    # Extraire l'audio
                    '--audio-format', 'mp3', # Format MP3
                    '--audio-quality', '0',  # Meilleure qualité
                    '--yes-playlist',        # Télécharger la playlist
                    '--newline',             # Pour une meilleure lecture de la sortie
                    '--progress',            # Afficher la progression
                    '-o', f'{self.output_dir}/%(title)s.%(ext)s',
                    url
                ]
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    bufsize=1
                )
                
                current_title = None
                # Lire la sortie en temps réel
                for line in process.stdout:
                    if '[download]' in line and 'Destination:' in line:
                        try:
                            current_title = line.split('Destination:')[1].strip().replace('.webm', '').replace('.mp3', '')
                            GLib.idle_add(self.append_progress_text, f"Téléchargement de : {current_title}")
                        except:
                            pass
                    elif '[ExtractAudio]' in line and current_title:
                        GLib.idle_add(self.append_progress_text, f"Conversion en MP3 : {current_title}")
                    elif current_title and 'has already been downloaded' in line:
                        GLib.idle_add(self.append_progress_text, f"Déjà téléchargé : {current_title}")
                
                process.wait()
                
                if process.returncode == 0:
                    GLib.idle_add(self.append_progress_text, f"✓ Playlist téléchargée avec succès")
                else:
                    error = process.stderr.read()
                    raise Exception(f"Erreur lors du téléchargement de la playlist: {error}")
                
            else:
                # Code existant pour une vidéo unique
                cmd_title = ['yt-dlp', '--get-title', url]
                process_title = subprocess.run(cmd_title, capture_output=True, text=True)
                
                if process_title.returncode != 0:
                    raise Exception("Impossible d'obtenir le titre de la vidéo")
                    
                title = process_title.stdout.strip()
                GLib.idle_add(self.append_progress_text, f"Démarrage du téléchargement de : {title}")
                
                cmd = [
                    'yt-dlp',
                    '-x',                    # Extraire l'audio
                    '--audio-format', 'mp3', # Format MP3
                    '--audio-quality', '0',  # Meilleure qualité
                    '--no-playlist',         # Ne pas télécharger la playlist si c'est une vidéo unique
                    '-o', f'{self.output_dir}/%(title)s.%(ext)s',
                    url
                ]
                
                process = subprocess.run(cmd, capture_output=True, text=True)
                
                if process.returncode == 0:
                    GLib.idle_add(self.append_progress_text, f"✓ Téléchargement terminé : {title}")
                else:
                    raise Exception(f"Erreur lors du téléchargement: {process.stderr}")

        except Exception as e:
            GLib.idle_add(self.append_progress_text, f"❌ Erreur : {str(e)}")

    def check_progress(self):
        return True

    def change_output_dir(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Choisir le dossier de destination",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        dialog.add_buttons(
            "Annuler", Gtk.ResponseType.CANCEL,
            "Sélectionner", Gtk.ResponseType.OK
        )
        
        # Définir le dossier actuel comme point de départ
        dialog.set_current_folder(self.output_dir)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            new_dir = dialog.get_filename()
            try:
                os.makedirs(new_dir, exist_ok=True)
                self.output_dir = new_dir
                self.dest_entry.set_text(new_dir)
            except Exception as e:
                self.show_error(f"Erreur lors de la création du dossier : {str(e)}")
        
        dialog.destroy()

def main():
    win = YouTubeDownloader()
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
