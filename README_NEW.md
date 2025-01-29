# Music Downloader (Debian 12 Edition)

Outil de téléchargement audio optimisé pour Debian 12 avec interface GTK3

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
sudo apt install -t bookworm-backports \
    yt-dlp=2025.01.15-1~bpo12+1 \
    python3-gi \
    gir1.2-gtk-3.0
```

3. Télécharger l'application :
```bash
git clone https://github.com/popaul77/Music_Downloader.git
cd Music_Downloader
```

## ▶ Utilisation

Démarrer l'interface graphique :
```bash
python3 main.py --debian-mode
```

Options spécifiques Debian :
```
--repo-check   : Vérifie la configuration des dépôts
--gtk3-fallback: Force le mode GTK3
```

## 🔧 Compatibilité

Environnements supportés :
| Desktop | Version | Statut |
|---------|---------|--------|
| GNOME   | ≥ 42.5  | ✅     |
| XFCE    | ≥ 4.18  | ✅     |
| KDE     | ≥ 5.24  | ⚠ Nécessite Qt5 |

## 🚨 Support technique

Pour rapporter un problème :
1. Vérifier la configuration :
```bash
apt policy yt-dlp
gnome-shell --version
```

2. Capturer les logs :
```bash
journalctl -u music-downloader.service --since "5 min ago"
```

## 📄 Licence

GPL-3.0 - Consultez [LICENSE_DEBIAN](LICENSE_DEBIAN) pour les conditions spécifiques à Debian