#!/bin/bash

# Créer le répertoire d'installation
install_dir="$HOME/.local/share/music-downloader"
mkdir -p "$install_dir"

# Copier les fichiers
cp music_downloader.py "$install_dir/"
chmod +x "$install_dir/music_downloader.py"

# Créer le répertoire pour le fichier .desktop
mkdir -p "$HOME/.local/share/applications"

# Créer le fichier .desktop
cat > ~/.local/share/applications/music-downloader.desktop << EOL
[Desktop Entry]
Name=Music Downloader
Comment=Télécharge des vidéos en MP3 depuis YouTube, PeerTube et autres
Exec=~/.local/share/music-downloader/music_downloader.py
Icon=audio-x-generic
Terminal=false
Type=Application
Categories=AudioVideo;Audio;
EOL

# Rendre le fichier .desktop exécutable
chmod +x "$HOME/.local/share/applications/music-downloader.desktop"

echo "Installation terminée !" 