#!/bin/bash
# Script d'installation automatique pour Raspberry Pi 4
# Application Airsoft Simulation

set -e  # Arrêter en cas d'erreur

echo "================================================"
echo "   Installation Airsoft Simulation"
echo "   Pour Raspberry Pi 4"
echo "================================================"
echo ""

# Couleurs pour l'affichage
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[ATTENTION]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERREUR]${NC} $1"
}

# Vérifier que le script est exécuté sur Raspberry Pi
log_info "Vérification du système..."
if [ ! -f /proc/cpuinfo ] || ! grep -q "Raspberry Pi" /proc/cpuinfo; then
    log_warn "Ce script est conçu pour Raspberry Pi"
    read -p "Continuer quand même ? (o/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Oo]$ ]]; then
        exit 1
    fi
fi

# Obtenir le répertoire du script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
log_info "Répertoire d'installation: $SCRIPT_DIR"

# Mise à jour du système
log_info "Mise à jour du système..."
sudo apt update
sudo apt upgrade -y

# Installation de Python et dépendances système
log_info "Installation de Python 3 et dépendances..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-tk \
    python3-pil \
    python3-pil.imagetk \
    portaudio19-dev \
    python3-pyaudio \
    espeak \
    pulseaudio

# Installation des dépendances Python
log_info "Installation des packages Python..."
cd "$SCRIPT_DIR"

# Créer un environnement virtuel pour éviter l'erreur externally-managed-environment
log_info "Création d'un environnement virtuel Python..."
python3 -m venv venv

# Activer l'environnement virtuel et installer les dépendances
log_info "Installation des packages dans l'environnement virtuel..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# Créer le script de démarrage
log_info "Création du script de démarrage..."
cat > "$HOME/start_airsoft.sh" << 'EOFSCRIPT'
#!/bin/bash
# Script de démarrage de l'application Airsoft

# Attendre que le bureau soit prêt
sleep 5

# Désactiver l'économiseur d'écran
xset s off
xset -dpms
xset s noblank

# Lancer l'application avec l'environnement virtuel
cd ~/airsoft-simullaptop
source venv/bin/activate
python main.py

# En cas d'erreur, attendre avant de fermer
if [ $? -ne 0 ]; then
    echo "Erreur lors du lancement de l'application"
    sleep 10
fi
EOFSCRIPT

chmod +x "$HOME/start_airsoft.sh"

# Copier les fichiers dans le home si nécessaire
if [ "$SCRIPT_DIR" != "$HOME/airsoft-simullaptop" ]; then
    log_info "Copie des fichiers vers $HOME/airsoft-simullaptop..."
    mkdir -p "$HOME/airsoft-simullaptop"
    cp -r "$SCRIPT_DIR"/* "$HOME/airsoft-simullaptop/"
    cd "$HOME/airsoft-simullaptop"
fi

# Configuration de l'autostart (optionnel)
echo ""
log_info "Configuration du démarrage automatique..."
read -p "Voulez-vous que l'application démarre automatiquement au démarrage ? (o/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    log_info "Activation du démarrage automatique..."
    mkdir -p "$HOME/.config/autostart"
    cat > "$HOME/.config/autostart/airsoft.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Airsoft Simulation
Comment=Application de simulation russe pour Airsoft
Exec=$HOME/start_airsoft.sh
Terminal=false
Hidden=false
X-GNOME-Autostart-enabled=true
EOF
    log_info "Démarrage automatique activé"
else
    log_info "Démarrage automatique désactivé"
    log_info "Pour lancer l'application manuellement: $HOME/start_airsoft.sh"
    # Supprimer l'autostart s'il existe
    rm -f "$HOME/.config/autostart/airsoft.desktop"
fi

# Configuration LXDE pour désactiver l'économiseur d'écran
log_info "Configuration de l'économiseur d'écran..."
mkdir -p "$HOME/.config/lxsession/LXDE-pi"
if [ -f "$HOME/.config/lxsession/LXDE-pi/autostart" ]; then
    # Ajouter les lignes si elles n'existent pas déjà
    grep -qxF '@xset s off' "$HOME/.config/lxsession/LXDE-pi/autostart" || echo '@xset s off' >> "$HOME/.config/lxsession/LXDE-pi/autostart"
    grep -qxF '@xset -dpms' "$HOME/.config/lxsession/LXDE-pi/autostart" || echo '@xset -dpms' >> "$HOME/.config/lxsession/LXDE-pi/autostart"
    grep -qxF '@xset s noblank' "$HOME/.config/lxsession/LXDE-pi/autostart" || echo '@xset s noblank' >> "$HOME/.config/lxsession/LXDE-pi/autostart"
else
    cat > "$HOME/.config/lxsession/LXDE-pi/autostart" << EOF
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@xset s off
@xset -dpms
@xset s noblank
EOF
fi

# Configuration de l'audio
log_info "Configuration de l'audio..."
echo ""
echo "Sélectionnez la sortie audio :"
echo "1) HDMI (écran avec son)"
echo "2) Jack 3.5mm (haut-parleurs externes)"
read -p "Votre choix (1 ou 2): " audio_choice

case $audio_choice in
    1)
        log_info "Configuration de la sortie HDMI..."
        amixer cset numid=3 2
        ;;
    2)
        log_info "Configuration de la sortie Jack..."
        amixer cset numid=3 1
        ;;
    *)
        log_warn "Choix invalide, audio par défaut conservé"
        ;;
esac

# Test de l'audio
log_info "Test de l'audio..."
if command -v speaker-test &> /dev/null; then
    log_info "Lancement du test audio (Ctrl+C pour arrêter)..."
    timeout 3 speaker-test -t sine -f 1000 || true
fi

# Configuration du clavier (optionnel)
log_info "Configuration du clavier..."
read -p "Configurer le clavier en français ? (o/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    sudo raspi-config nonint do_configure_keyboard fr
fi

# Résumé de l'installation
echo ""
echo "================================================"
log_info "Installation terminée avec succès !"
echo "================================================"
echo ""
echo "Configuration:"
echo "  - Emplacement: $HOME/airsoft-simullaptop"
if [ -f "$HOME/.config/autostart/airsoft.desktop" ]; then
    echo "  - Démarrage automatique: Activé"
else
    echo "  - Démarrage automatique: Désactivé"
fi
echo "  - Économiseur d'écran: Désactivé"
echo ""
echo "Codes par défaut:"
echo "  - Code bureau:    111111"
echo "  - Code dossier:   222222"
echo "  - Code missile:   333333"
echo "  - Admin:          admin123 (5 clics coin supérieur gauche)"
echo ""
echo "Commandes utiles:"
echo "  - Lancer manuellement:    $HOME/start_airsoft.sh"
echo "  - Tester:                 cd $HOME/airsoft-simullaptop && source venv/bin/activate && python main.py"
echo "  - Configurer raspi:       sudo raspi-config"
echo ""

# Proposer de redémarrer seulement si autostart est activé
if [ -f "$HOME/.config/autostart/airsoft.desktop" ]; then
    read -p "Redémarrer maintenant pour activer l'autostart ? (o/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        log_info "Redémarrage dans 5 secondes..."
        sleep 5
        sudo reboot
    else
        log_info "Redémarrez manuellement avec: sudo reboot"
    fi
else
    log_info "Installation terminée. Lancez l'application avec: $HOME/start_airsoft.sh"
    read -p "Voulez-vous lancer l'application maintenant ? (o/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        log_info "Lancement de l'application..."
        $HOME/start_airsoft.sh
    fi
fi
