# 🎮 Application Airsoft - Simulation Bureau Russe

Application locale pour partie d'Airsoft simulant un ordinateur militaire russe avec système de lancement de missile.

## 📋 Description

Cette application permet de créer une expérience immersive pour vos parties d'Airsoft. Les joueurs doivent trouver trois codes à 6 chiffres sur le terrain pour déverrouiller l'accès à un bureau virtuel russe, accéder aux documents secrets et lancer un missile (simulation). Un quatrième code permet d'annuler le lancement en cours.

## ✨ Fonctionnalités

- 🔐 **Écran de connexion sécurisé** : Nécessite 3 codes à 6 chiffres (bureau, dossier, missile)
- 🖥️ **Bureau virtuel russe** : Interface réaliste avec icônes et dossiers
- 🚀 **Système de lancement de missile** : Simulation complète avec décompte configurable
- 🛑 **Annulation de missile** : Possibilité d'annuler le lancement avec un code secret
- ⚙️ **Panel administrateur** : Configuration des codes, du minuteur et du nom du missile
- 📁 **Gestion de fichiers** : Upload de documents PDF, images et vidéos
- 🌐 **100% local** : Fonctionne sans connexion internet
- 🎯 **Optimisé Raspberry Pi 4** : Interface plein écran avec audio

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
2. **Connexion** : Entrez le code bureau (6 chiffres)
3. **Bureau** : Explorez le bureau virtuel russe
4. **Dossier** : Entrez le code dossier pour accéder aux documents secrets
5. **Missile** : Entrez le code missile pour accéder au système de lancement
6. **Lancement** : Confirmez le lancement et observez le décompte
7. **Annulation (optionnel)** : Entrez le code d'annulation pour arrêter le missile

### Mode Administrateur

1. **Accès secret** : Cliquez 5 fois rapidement dans le coin supérieur gauche de l'écran de connexion
2. **Mot de passe** : Entrez le mot de passe admin (défaut: `admin123`)
3. **Configuration** :
   - Modifier le **Code Bureau** (6 chiffres)
   - Modifier le **Code Dossier** (6 chiffres)
   - Modifier le **Code Missile** (6 chiffres)
   - Modifier le **Code Annulation** (6 chiffres)
   - Personnaliser le **nom du missile**
   - Configurer le **minuteur par défaut** (10-1800 secondes)
   - Gérer les **fichiers uploadés** (PDF, images, vidéos)
   - Changer le **mot de passe admin**
4. **Sauvegarde** : Cliquez sur "SAUVEGARDER"

## ⚙️ Configuration

Le fichier `config.json` contient les paramètres :

```json
{
  "code_bureau": "111111",
  "code_dossier": "222222",
  "code_missile": "333333",
  "code_annulation": "999999",
  "admin_password": "admin123",
  "missile_name": "R-73",
  "missile_timer_default": 1200,
  "missile_timer_max": 1800
}
```

**Paramètres** :
- `code_bureau` : Code d'accès au bureau (défaut: 111111)
- `code_dossier` : Code d'accès aux documents (défaut: 222222)
- `code_missile` : Code d'accès au lancement (défaut: 333333)
- `code_annulation` : Code pour annuler le lancement (défaut: 999999)
- `missile_name` : Nom du missile affiché
- `missile_timer_default` : Durée du décompte en secondes (défaut: 1200 = 20 min)
- `missile_timer_max` : Durée maximale autorisée (1800 = 30 min)

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

## 🎮 Scénarios type

### Scénario 1 : Mission d'attaque
1. **Briefing** : Les joueurs reçoivent la mission de trouver 3 codes cachés sur le terrain
2. **Recherche** : Les codes sont dissimulés dans différents endroits
3. **Accès** : Une fois les codes trouvés, accès au terminal russe
4. **Mission** : Lancement du missile pour compléter l'objectif
5. **Victoire** : L'équipe ayant lancé le missile remporte la partie!

### Scénario 2 : Mission de défense
1. **Briefing** : Une équipe doit lancer le missile, l'autre doit l'empêcher
2. **Codes cachés** : L'équipe attaquante cherche les 3 codes de lancement
3. **Code secret** : L'équipe défensive cherche le code d'annulation
4. **Course contre la montre** : Une fois le missile lancé, l'équipe défensive a le temps du décompte pour entrer le code d'annulation
5. **Victoire** : Missile lancé = attaquants gagnent, missile annulé = défenseurs gagnent

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
