#!/bin/bash

# Créer le répertoire d'installation
install_dir="$HOME/.local/share/youtube-music-downloader"
mkdir -p "$install_dir"

# Copier les fichiers
cp extract_youtube.py "$install_dir/"
chmod +x "$install_dir/extract_youtube.py"

# Créer le répertoire pour le fichier .desktop
mkdir -p "$HOME/.local/share/applications"

# Créer le fichier .desktop
cat > ~/.local/share/applications/youtube-music-downloader.desktop << EOL
[Desktop Entry]
Name=Music Downloader
Comment=Télécharge des vidéos en MP3 depuis YouTube, PeerTube et autres
Exec=~/.local/share/youtube-music-downloader/youtube-music-downloader
Icon=audio-x-generic
Terminal=false
Type=Application
Categories=AudioVideo;Audio;
EOL

# Rendre le fichier .desktop exécutable
chmod +x "$HOME/.local/share/applications/youtube-music-downloader.desktop"

echo "Installation terminée !" 