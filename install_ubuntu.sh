#!/bin/bash
# Script d'installation automatique pour Ubuntu
# Application Airsoft Simulation

set -e  # Arrêter en cas d'erreur

echo "================================================"
echo "   Installation Airsoft Simulation"
echo "   Pour Ubuntu / Linux Desktop"
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

# Vérifier que le script est exécuté sur Linux
log_info "Vérification du système..."
if [ "$(uname)" != "Linux" ]; then
    log_error "Ce script est conçu pour Linux/Ubuntu"
    exit 1
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
    pulseaudio \
    x11-xserver-utils

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

# D'abord tenter l'installation normale
pip install -r requirements.txt || {
    log_warn "Erreur d'installation, tentative module par module..."
    pip install "Pillow>=10.0.0" || log_warn "Pillow non installé"
    pip install "pyttsx3>=2.90" || log_warn "pyttsx3 non installé"
    pip install "PyMuPDF>=1.23.0" || log_warn "PyMuPDF non installé"
    pip install "opencv-python-headless>=4.8.0" || log_warn "OpenCV non installé, les vidéos ne seront pas lues"
}

# Vérifier que les modules critiques fonctionnent (détecte les 'Illegal instruction')
log_info "Vérification des modules installés..."
python3 -c "import PIL; print('  Pillow: OK')" || log_warn "Pillow ne fonctionne pas"
python3 -c "import fitz; print('  PyMuPDF: OK')" || log_warn "PyMuPDF ne fonctionne pas (les PDF ne seront pas affichés)"
python3 -c "import cv2; print('  OpenCV: OK')" || log_warn "OpenCV ne fonctionne pas (les vidéos ne seront pas lues)"

deactivate

# Créer le script de démarrage
log_info "Création du script de démarrage..."
cat > "$HOME/start_airsoft.sh" << 'EOFSCRIPT'
#!/bin/bash
# Script de démarrage de l'application Airsoft

# Attendre que le bureau soit prêt
sleep 3

# Désactiver l'économiseur d'écran
xset s off 2>/dev/null
xset -dpms 2>/dev/null
xset s noblank 2>/dev/null

# Lancer l'application avec l'environnement virtuel
cd ~/airsoft-simullaptop
source venv/bin/activate

# Désactiver les instructions AVX si problème de compatibilité
export OPENCV_LOG_LEVEL=ERROR
export OPENBLAS_CORETYPE=ARMV8

python main.py

# En cas d'erreur, afficher les détails et attendre
if [ $? -ne 0 ]; then
    echo ""
    echo "=== Erreur lors du lancement de l'application ==="
    echo "Diagnostic en cours..."
    echo ""
    python3 -c "import tkinter; print('  tkinter: OK')" 2>&1 || echo "  tkinter: ERREUR"
    python3 -c "import PIL; print('  Pillow: OK')" 2>&1 || echo "  Pillow: ERREUR"
    python3 -c "import fitz; print('  PyMuPDF: OK')" 2>&1 || echo "  PyMuPDF: ERREUR (crash probable)"
    python3 -c "import cv2; print('  OpenCV: OK')" 2>&1 || echo "  OpenCV: ERREUR (crash probable)"
    echo ""
    echo "Si un module affiche ERREUR/crash, reinstallez-le :"
    echo "  cd ~/airsoft-simullaptop && source venv/bin/activate"
    echo "  pip install --force-reinstall opencv-python-headless PyMuPDF"
    echo ""
    sleep 30
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

# Détecter l'environnement de bureau
DESKTOP_ENV="unknown"
if [ "$XDG_CURRENT_DESKTOP" ]; then
    DESKTOP_ENV="$XDG_CURRENT_DESKTOP"
elif [ "$DESKTOP_SESSION" ]; then
    DESKTOP_ENV="$DESKTOP_SESSION"
fi
log_info "Environnement de bureau détecté: $DESKTOP_ENV"

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

# Configuration pour désactiver l'économiseur d'écran selon l'environnement
log_info "Configuration de l'économiseur d'écran..."
case "$DESKTOP_ENV" in
    *GNOME*|*gnome*|*ubuntu*)
        log_info "Configuration pour GNOME/Ubuntu..."
        # Désactiver l'économiseur d'écran GNOME
        gsettings set org.gnome.desktop.session idle-delay 0 2>/dev/null || true
        gsettings set org.gnome.desktop.screensaver lock-enabled false 2>/dev/null || true
        gsettings set org.gnome.desktop.screensaver idle-activation-enabled false 2>/dev/null || true
        ;;
    *XFCE*|*xfce*)
        log_info "Configuration pour XFCE..."
        xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/dpms-enabled -s false 2>/dev/null || true
        xfconf-query -c xfce4-screensaver -p /saver/enabled -s false 2>/dev/null || true
        ;;
    *LXDE*|*lxde*)
        log_info "Configuration pour LXDE..."
        mkdir -p "$HOME/.config/lxsession/LXDE"
        if [ -f "$HOME/.config/lxsession/LXDE/autostart" ]; then
            grep -qxF '@xset s off' "$HOME/.config/lxsession/LXDE/autostart" || echo '@xset s off' >> "$HOME/.config/lxsession/LXDE/autostart"
            grep -qxF '@xset -dpms' "$HOME/.config/lxsession/LXDE/autostart" || echo '@xset -dpms' >> "$HOME/.config/lxsession/LXDE/autostart"
            grep -qxF '@xset s noblank' "$HOME/.config/lxsession/LXDE/autostart" || echo '@xset s noblank' >> "$HOME/.config/lxsession/LXDE/autostart"
        else
            cat > "$HOME/.config/lxsession/LXDE/autostart" << EOF
@lxpanel --profile LXDE
@pcmanfm --desktop --profile LXDE
@xset s off
@xset -dpms
@xset s noblank
EOF
        fi
        ;;
    *)
        log_warn "Environnement de bureau non reconnu, configuration manuelle peut être nécessaire"
        ;;
esac

# Configuration de l'audio
log_info "Configuration de l'audio..."
echo ""
log_info "Vérification de PulseAudio..."
if command -v pulseaudio &> /dev/null; then
    log_info "PulseAudio détecté et configuré"
    # S'assurer que PulseAudio est démarré
    pulseaudio --check || pulseaudio --start &>/dev/null || true
else
    log_warn "PulseAudio non trouvé, audio peut ne pas fonctionner correctement"
fi

# Test de l'audio
log_info "Test de l'audio..."
if command -v speaker-test &> /dev/null; then
    log_info "Lancement du test audio (3 secondes)..."
    timeout 3 speaker-test -t sine -f 1000 2>/dev/null || true
fi

# Test de espeak
log_info "Test de la synthèse vocale..."
if command -v espeak &> /dev/null; then
    echo "Test vocal..." | espeak -v fr 2>/dev/null || espeak -v en 2>/dev/null || true
else
    log_warn "espeak non trouvé, la synthèse vocale peut ne pas fonctionner"
fi

# Résumé de l'installation
echo ""
echo "================================================"
log_info "Installation terminée avec succès !"
echo "================================================"
echo ""
echo "Configuration:"
echo "  - Emplacement: $HOME/airsoft-simullaptop"
echo "  - Environnement: $DESKTOP_ENV"
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
echo "  - Volume audio:           alsamixer  (ou pavucontrol pour PulseAudio)"
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
