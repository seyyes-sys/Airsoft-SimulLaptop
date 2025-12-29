# Installation sur Ubuntu / Linux Desktop

Ce guide explique comment installer l'application Airsoft Simulation sur Ubuntu ou toute autre distribution Linux avec environnement de bureau.

## Prérequis

- Ubuntu 20.04 ou supérieur (ou distribution basée sur Debian)
- Accès sudo
- Connexion internet pour l'installation des paquets

## Installation Automatique

### 1. Transférer les fichiers

Copiez tout le dossier `airsoft-simullaptop` sur votre machine Ubuntu (via clé USB, réseau, etc.)

### 2. Rendre le script exécutable

```bash
cd airsoft-simullaptop
chmod +x install_ubuntu.sh
```

### 3. Lancer l'installation

```bash
./install_ubuntu.sh
```

Le script va :
- Mettre à jour le système
- Installer Python 3 et toutes les dépendances
- Créer un environnement virtuel Python
- Installer les packages Python requis
- Configurer l'audio (PulseAudio)
- Désactiver l'économiseur d'écran
- Optionnellement configurer le démarrage automatique

### 4. Configuration

Pendant l'installation, vous serez invité à :
- **Activer le démarrage automatique** : Si vous choisissez "oui", l'application se lancera automatiquement au démarrage de la session
- **Lancer l'application** : Tester immédiatement après l'installation

## Environnements de Bureau Supportés

Le script détecte automatiquement votre environnement et s'adapte :

- **GNOME** (Ubuntu par défaut)
- **Unity** (anciennes versions Ubuntu)
- **XFCE** (Xubuntu)
- **LXDE** (Lubuntu)
- **KDE** (Kubuntu)

## Lancement Manuel

Si vous n'avez pas activé le démarrage automatique :

```bash
~/start_airsoft.sh
```

Ou directement depuis le dossier :

```bash
cd ~/airsoft-simullaptop
source venv/bin/activate
python main.py
```

## Configuration Audio

### Vérifier l'audio

```bash
# Tester les haut-parleurs
speaker-test -t sine -f 1000

# Tester la synthèse vocale
espeak -v fr "Bonjour"
```

### Ajuster le volume

```bash
# Interface ALSA (console)
alsamixer

# Interface PulseAudio (graphique, si installé)
pavucontrol
```

### Si l'audio ne fonctionne pas

1. Vérifier que PulseAudio est actif :
```bash
pulseaudio --check
pulseaudio --start
```

2. Vérifier les sorties audio disponibles :
```bash
pactl list short sinks
```

3. Augmenter le volume système dans les paramètres Ubuntu

## Désactivation de l'Économiseur d'Écran

Le script désactive automatiquement l'économiseur selon votre environnement.

### Vérification manuelle (GNOME/Ubuntu)

```bash
gsettings get org.gnome.desktop.session idle-delay
# Doit retourner : uint32 0

gsettings get org.gnome.desktop.screensaver lock-enabled
# Doit retourner : false
```

### Si l'écran s'éteint encore

Ajoutez cette commande au script de démarrage :

```bash
# Éditer le script
nano ~/start_airsoft.sh

# Ajouter après "sleep 5" :
xset s off
xset -dpms
xset s noblank
```

## Résolution des Problèmes

### L'application ne démarre pas

1. Vérifier les erreurs :
```bash
cd ~/airsoft-simullaptop
source venv/bin/activate
python main.py
```

2. Vérifier que Tkinter est installé :
```bash
python3 -m tkinter
```

### Erreur "externally-managed-environment"

Le script utilise un environnement virtuel pour éviter cette erreur. Si elle persiste :

```bash
cd ~/airsoft-simullaptop
python3 -m venv --system-site-packages venv
source venv/bin/activate
pip install -r requirements.txt
```

### Les icônes ne s'affichent pas

Régénérer les icônes :

```bash
cd ~/airsoft-simullaptop
source venv/bin/activate
python create_icons.py
```

### La voix ne fonctionne pas

Vérifier espeak :

```bash
# Installer ou réinstaller
sudo apt install espeak espeak-data

# Tester
espeak -v fr "Test"

# Lister les voix disponibles
espeak --voices
```

### Le plein écran ne fonctionne pas

Éditer `main.py` et ajuster la méthode de mise en plein écran selon votre gestionnaire de fenêtres.

## Désinstallation

```bash
# Supprimer l'application
rm -rf ~/airsoft-simullaptop

# Supprimer le script de démarrage
rm ~/start_airsoft.sh

# Supprimer l'autostart
rm ~/.config/autostart/airsoft.desktop

# Réactiver l'économiseur d'écran (GNOME)
gsettings reset org.gnome.desktop.session idle-delay
gsettings reset org.gnome.desktop.screensaver lock-enabled
gsettings reset org.gnome.desktop.screensaver idle-activation-enabled
```

## Codes par Défaut

- **Code bureau** : `111111`
- **Code dossier** : `222222`
- **Code missile** : `333333`
- **Panel admin** : Cliquer 5 fois dans le coin supérieur gauche, mot de passe : `admin123`

Ces codes peuvent être modifiés depuis le panel administrateur ou dans le fichier `config.json`.

## Support

En cas de problème, vérifiez :
1. Les logs dans le terminal
2. Les permissions des fichiers
3. Que toutes les dépendances sont installées
4. Que l'environnement virtuel est activé

Pour tester l'installation :
```bash
cd ~/airsoft-simullaptop
source venv/bin/activate
python -c "import tkinter; import PIL; import fitz; import cv2; print('OK')"
```
