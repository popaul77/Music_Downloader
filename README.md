# Music Downloader

## Description
Music Downloader est une application graphique simple permettant de télécharger des vidéos en format MP3 depuis différentes plateformes :
- YouTube (vidéos et playlists)
- PeerTube
- Et autres plateformes supportées par yt-dlp

## Fonctionnalités
- Interface graphique GTK3
- Téléchargement de vidéos uniques
- Téléchargement de playlists complètes
- Conversion automatique en MP3
- Choix du dossier de destination
- Affichage de la progression en temps réel

## 📋 Prérequis

**Système cible :**

Distrib : Debian 12 "Bookworm"

## 🛠 Installation

1. Configurer les backports :
```bash
sudo tee /etc/apt/sources.list.d/bookworm-backports.list <<EOF
deb http://deb.debian.org/debian bookworm-backports main
EOF
sudo apt update
```

2. Installer les dépendances :
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 ffmpeg
sudo apt install -t bookworm-backports yt-dlp=2025.01.15-1~bpo12+1
```


## Installation depuis l'archive tar.gz

1. Téléchargez l'archive tar.gz
```bash
wget https://github.com/popaul77/Music_Downloader/releases/download/Music_Downloader/Music_Downloader-1.0.4.tar.gz

```

2. Décompressez l'archive
```bash
tar xzf Music_Downloader-1.0.4.tar.gz
```

3. Entrez dans le dossier
```bash
cd Music_Downloader
```

4. Rendez le script d'installation exécutable
```bash
chmod +x install.sh
```

5. Exécutez le script d'installation
```bash
./install.sh
```

6. Déconnectez-vous puis reconnectez-vous à votre session pour que l'application apparaisse dans le menu

## Guide d'utilisation

### Lancement de l'application
- Depuis le menu des applications / Son Vidéos : cherchez "Music Downloader"
- Depuis le terminal : `Music_Downloader`

### Télécharger des vidéos
1. Copiez l'URL d'une vidéo (YouTube, PeerTube, etc.) ou d'une playlist
2. Collez l'URL dans la zone de texte de l'application
3. (Optionnel) Changez le dossier de destination en cliquant sur "Changer"
4. Cliquez sur "Télécharger"

### Télécharger depuis un fichier texte
1. Créez un fichier texte avec une URL par ligne
2. Cliquez sur "Charger urls.txt"
3. Sélectionnez votre fichier
4. Cliquez sur "Télécharger"

### Suivi des téléchargements
- La zone de texte inférieure affiche la progression
- Les titres des morceaux s'affichent pendant le téléchargement
- Un message confirme la fin du téléchargement

### Dossier de destination
- Par défaut : `~/Musique/YouTube`
- Pour changer : cliquez sur le bouton "Changer" et sélectionnez un nouveau dossier

## Notes
- Les fichiers sont automatiquement convertis en MP3
- La meilleure qualité audio disponible est sélectionnée
- Les noms des fichiers sont basés sur les titres des vidéos

## Support
Pour signaler un bug ou suggérer une amélioration, veuillez créer une issue sur le dépôt GitHub. 

## 📄 Licence

GPL-3.0 - Consultez [LICENSE_DEBIAN](LICENSE_DEBIAN) pour les conditions spécifiques à Debian