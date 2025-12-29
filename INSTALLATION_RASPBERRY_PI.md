# Installation sur Raspberry Pi 4

## Méthode simple : Script automatique

### 1. Transférer les fichiers

Sur votre **PC Windows**, compressez le dossier :
```powershell
Compress-Archive -Path "c:\airsoft-simullaptop\*" -DestinationPath "$HOME\Desktop\airsoft-simullaptop.zip"
```

Transférez `airsoft-simullaptop.zip` vers le Raspberry Pi (clé USB, réseau, etc.)

### 2. Sur le Raspberry Pi

Décompressez et lancez l'installation :
```bash
# Décompresser
cd ~
unzip airsoft-simullaptop.zip -d airsoft-simullaptop
cd airsoft-simullaptop

# Rendre le script exécutable
chmod +x install_raspberry.sh

# Lancer l'installation
./install_raspberry.sh
```

Le script va :
- ✅ Installer Python 3 et toutes les dépendances
- ✅ Configurer le démarrage automatique
- ✅ Désactiver l'économiseur d'écran
- ✅ Configurer l'audio (HDMI ou Jack)
- ✅ Tester le système

### 3. Redémarrer

Après l'installation, redémarrez le Raspberry Pi :
```bash
sudo reboot
```

L'application se lancera automatiquement au démarrage !

---

## Codes par défaut

- **Code bureau** : `111111`
- **Code dossier** : `222222`
- **Code missile** : `333333`
- **Admin** : `admin123` (5 clics sur le coin supérieur gauche)

---

## Commandes utiles

### Lancer manuellement
```bash
~/start_airsoft.sh
```

### Arrêter l'application
```bash
pkill -f main.py
```

### Désactiver le démarrage automatique
```bash
rm ~/.config/autostart/airsoft.desktop
```

### Réactiver le démarrage automatique
```bash
~/airsoft-simullaptop/install_raspberry.sh
# Choisir uniquement la partie autostart
```

### Logs en cas de problème
```bash
cd ~/airsoft-simullaptop
python3 main.py
```

---

## Configuration audio

Si l'audio ne fonctionne pas :

```bash
# Tester les haut-parleurs
speaker-test -t wav -c 2

# Configurer via raspi-config
sudo raspi-config
# System Options > Audio > Choisir HDMI ou Headphones

# Augmenter le volume
amixer set Master 100%
```

---

## Optimisations

### Plein écran sans barre de tâches

Modifiez `/etc/xdg/lxsession/LXDE-pi/autostart` :
```bash
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```

Commentez ou supprimez la ligne `@lxpanel`.

### Performance

Pour de meilleures performances, overclocker le Raspberry Pi :
```bash
sudo raspi-config
# Performance Options > Overclock > Choisir "High" ou "Turbo"
```

---

## Résolution de problèmes

### Problème : L'application ne démarre pas
```bash
# Vérifier les erreurs
cd ~/airsoft-simullaptop
python3 main.py
```

### Problème : Pas de son
```bash
# Réinstaller pulseaudio
sudo apt install --reinstall pulseaudio
pulseaudio --start

# Vérifier la sortie audio
amixer cset numid=3 2  # HDMI
# ou
amixer cset numid=3 1  # Jack 3.5mm
```

### Problème : Écran noir
```bash
# Désactiver l'économiseur d'écran
xset s off
xset -dpms
xset s noblank
```

### Problème : Clavier non reconnu
```bash
sudo raspi-config
# Localisation Options > Keyboard Layout > Choisir "French"
```

---

## Mise à jour de l'application

Pour mettre à jour :
```bash
cd ~/airsoft-simullaptop
# Sauvegardez votre config.json
cp config.json config.json.backup

# Copiez les nouveaux fichiers (depuis USB/réseau)
# puis restaurez la config
cp config.json.backup config.json
```
