#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application Airsoft - Simulation Bureau Russe
Point d'entrée principal de l'application
"""

import tkinter as tk
from login_screen import LoginScreen
import platform

def main():
    root = tk.Tk()
    root.title("Système Sécurisé")
    
    # Forcer le plein écran sur tous les systèmes
    root.attributes('-fullscreen', True)
    
    # Sur Linux/Raspberry Pi, s'assurer que la fenêtre est au premier plan
    if platform.system() == 'Linux':
        root.attributes('-zoomed', True)  # Maximiser d'abord
        root.update_idletasks()  # Forcer la mise à jour
        root.attributes('-fullscreen', True)  # Puis plein écran
        root.focus_force()  # Forcer le focus
    
    root.configure(bg='black')
    
    # Empêcher la fermeture avec Alt+F4 ou autres (optionnel)
    # root.protocol("WM_DELETE_WINDOW", lambda: None)
    
    app = LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
