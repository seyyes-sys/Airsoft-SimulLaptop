#!/bin/bash
# Script de test pour résoudre les problèmes sur Raspberry Pi

echo "=========================================="
echo "Test de configuration Raspberry Pi"
echo "=========================================="
echo ""

# Test 1: Polices pour les emojis
echo "1. Installation des polices emoji..."
sudo apt install -y fonts-noto-color-emoji fonts-dejavu fonts-liberation

# Test 2: Configuration de espeak
echo ""
echo "2. Test de la synthèse vocale (espeak)..."
espeak "Test vocal. Ceci est un test." 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ Espeak fonctionne"
else
    echo "✗ Espeak ne fonctionne pas"
    echo "Réinstallation de espeak..."
    sudo apt install --reinstall espeak espeak-data
fi

# Test 3: Volume audio
echo ""
echo "3. Vérification du volume audio..."
VOLUME=$(amixer get Master | grep -o '[0-9]*%' | head -1)
echo "Volume actuel: $VOLUME"
if [ "${VOLUME%\%}" -lt 50 ]; then
    echo "Augmentation du volume à 80%..."
    amixer set Master 80%
fi

# Test 4: Test complet de la voix
echo ""
echo "4. Test vocal complet..."
espeak -s 150 -a 200 "5 minutes remaining" 2>/dev/null &
sleep 2
espeak -s 150 -a 200 "Missile launched! Launch successful!" 2>/dev/null &
sleep 2

# Test 5: Affichage des emojis
echo ""
echo "5. Test d'affichage des emojis..."
python3 << 'PYEOF'
import tkinter as tk
root = tk.Tk()
root.title("Test Emoji")
root.geometry("400x300")

emojis = ["📁", "🏠", "🚀", "⚙️"]
for i, emoji in enumerate(emojis):
    label = tk.Label(root, text=emoji, font=("DejaVu Sans", 48))
    label.pack(pady=10)
    print(f"Emoji {i+1}: {emoji}")

tk.Label(root, text="Si vous voyez 4 emojis ci-dessus, les icônes fonctionneront!", 
         wraplength=350).pack(pady=10)
tk.Button(root, text="Fermer", command=root.quit).pack(pady=10)

root.after(5000, root.quit)  # Fermer après 5 secondes
root.mainloop()
PYEOF

echo ""
echo "=========================================="
echo "Tests terminés!"
echo "=========================================="
echo ""
echo "Si les emojis ne s'affichent pas, essayez:"
echo "  sudo apt install fonts-noto-color-emoji"
echo "  sudo fc-cache -f -v"
echo ""
echo "Si la voix ne fonctionne pas, vérifiez:"
echo "  amixer set Master 80%"
echo "  espeak 'test'"
