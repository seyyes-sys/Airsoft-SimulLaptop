# 🎮 Application Airsoft - Simulation Bureau Russe

Application locale pour partie d'Airsoft simulant un ordinateur militaire russe avec système de lancement de missile.

## 📋 Description

Cette application permet de créer une expérience immersive pour vos parties d'Airsoft. Les joueurs doivent trouver deux codes à 6 chiffres sur le terrain pour déverrouiller l'accès à un bureau virtuel russe et lancer un missile (simulation).

## ✨ Fonctionnalités

- 🔐 **Écran de connexion sécurisé** : Nécessite 2 codes à 6 chiffres
- 🖥️ **Bureau virtuel russe** : Interface réaliste avec icônes et dossiers
- 🚀 **Système de lancement de missile** : Simulation complète avec décompte
- ⚙️ **Panel administrateur** : Configuration des codes et du nom du missile
- 🌐 **100% local** : Fonctionne sans connexion internet
- 🎯 **Optimisé Raspberry Pi 4** : Interface plein écran

## 🛠️ Installation

### Prérequis

- Raspberry Pi 4 (ou ordinateur Windows/Linux/Mac)
- Python 3.7 ou supérieur
- Tkinter (inclus par défaut avec Python)

### Installation sur Raspberry Pi

```bash
# Cloner le projet
cd ~
git clone https://github.com/<votre-username>/airsoft-simullaptop.git
cd airsoft-simullaptop

# Copier le fichier de configuration
cp config.example.json config.json

# Installation automatique
chmod +x install_raspberry.sh
./install_raspberry.sh
```

Documentation complète : [INSTALLATION_RASPBERRY_PI.md](INSTALLATION_RASPBERRY_PI.md)

### Installation sur Ubuntu/Linux

```bash
# Cloner le projet
git clone https://github.com/<votre-username>/airsoft-simullaptop.git
cd airsoft-simullaptop

# Copier le fichier de configuration
cp config.example.json config.json

# Installation automatique
chmod +x install_ubuntu.sh
./install_ubuntu.sh
```

Documentation complète : [INSTALLATION_UBUNTU.md](INSTALLATION_UBUNTU.md)

### Installation sur Windows

```powershell
# Cloner le projet
git clone https://github.com/<votre-username>/airsoft-simullaptop.git
cd airsoft-simullaptop

# Copier le fichier de configuration
copy config.example.json config.json

# Installer les dépendances
pip install -r requirements.txt

# Créer les icônes
python create_icons.py

# Lancer l'application
python main.py
```

## 🎯 Utilisation

### Mode Joueur

1. **Lancement** : Exécutez `python3 main.py`
2. **Connexion** : Entrez les 2 codes à 6 chiffres
3. **Bureau** : Explorez le bureau virtuel
4. **Lancement** : Cliquez sur "Система Запуска" (Système de lancement)
5. **Mission** : Confirmez et regardez le missile se lancer!

### Mode Administrateur

1. **Accès secret** : Cliquez 5 fois rapidement dans le coin supérieur gauche de l'écran de connexion
2. **Mot de passe** : Entrez le mot de passe admin (défaut: `admin123`)
3. **Configuration** :
   - Modifier le **Code 1** (6 chiffres)
   - Modifier le **Code 2** (6 chiffres)
   - Personnaliser le **nom du missile**
   - Changer le **mot de passe admin**
4. **Sauvegarde** : Cliquez sur "SAUVEGARDER"

## ⚙️ Configuration

Le fichier `config.json` contient les paramètres :

```json
{
  "admin_password": "admin123",
  "code1": "123456",
  "code2": "654321",
  "missile_name": "RS-28 Sarmat",
  "language": "ru"
}
```

### Suggestions de noms de missiles russes

- RS-28 Sarmat
- RT-2PM2 Topol-M
- RS-24 Yars
- R-36M2 Voevoda
- Iskander-M

## 📁 Structure du projet

```
airsoft-simullaptop/
├── main.py                 # Point d'entrée de l'application
├── login_screen.py         # Écran de connexion
├── desktop_screen.py       # Bureau virtuel russe
├── missile_launcher.py     # Programme de lancement de missile
├── admin_panel.py          # Panel d'administration
├── config_manager.py       # Gestionnaire de configuration
├── config.json            # Fichier de configuration
├── requirements.txt       # Dépendances Python
└── README.md             # Ce fichier
```

## 🚀 Lancement automatique au démarrage (Raspberry Pi)

Pour lancer l'application automatiquement au démarrage du Raspberry Pi :

```bash
# Éditer le fichier autostart
nano ~/.config/lxsession/LXDE-pi/autostart

# Ajouter cette ligne à la fin :
@python3 /home/pi/airsoft-simullaptop/main.py
```

Ou créer un service systemd :

```bash
sudo nano /etc/systemd/system/airsoft.service
```

Contenu du fichier :

```ini
[Unit]
Description=Airsoft Simulator
After=graphical.target

[Service]
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
ExecStart=/usr/bin/python3 /home/pi/airsoft-simullaptop/main.py
Restart=always
User=pi

[Install]
WantedBy=graphical.target
```

Activer le service :

```bash
sudo systemctl enable airsoft.service
sudo systemctl start airsoft.service
```

## 🎮 Scénario type

1. **Briefing** : Les joueurs reçoivent la mission de trouver 2 codes cachés sur le terrain
2. **Recherche** : Les codes sont dissimulés dans différents endroits
3. **Accès** : Une fois les codes trouvés, accès au terminal russe
4. **Mission** : Lancement du missile pour compléter l'objectif
5. **Victoire** : L'équipe ayant lancé le missile remporte la partie!

## 🔧 Personnalisation

### Modifier les textes en russe

Éditez les fichiers `.py` pour personnaliser les textes affichés.

### Ajouter des sons

Installez `pygame` et ajoutez des effets sonores :

```bash
pip3 install pygame
```

### Changer le thème

Modifiez les couleurs dans les fichiers pour personnaliser l'apparence.

## 🐛 Dépannage

### L'application ne se lance pas en plein écran

Modifiez `main.py` :

```python
root.attributes('-fullscreen', False)  # Mode fenêtré
```

### Les caractères russes ne s'affichent pas

Installez les polices cyrilliques :

```bash
sudo apt-get install fonts-liberation fonts-dejavu
```

### Problème de permissions

```bash
chmod +x main.py
```

## 📝 Licence

Projet libre pour usage personnel et parties d'Airsoft.

## 🤝 Contribution

N'hésitez pas à améliorer cette application et à partager vos modifications!

## 📞 Support

Pour toute question ou problème, consultez la documentation ou ouvrez une issue.

---

**Bon jeu! 🎯🔫**
