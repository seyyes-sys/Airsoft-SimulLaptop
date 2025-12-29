#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur d'icônes pour le bureau virtuel
Crée des images PNG avec des dessins géométriques
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_folder_icon(filename):
    """Icône de dossier"""
    size = 128
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Dossier jaune/orange
    # Onglet du dossier
    draw.polygon([(30, 35), (55, 35), (60, 45), (30, 45)], fill='#f39c12', outline='#e67e22', width=2)
    # Corps du dossier
    draw.rounded_rectangle([(25, 45), (105, 95)], radius=5, fill='#f4a542', outline='#e67e22', width=3)
    
    img.save(os.path.join(os.path.dirname(__file__), 'icons', filename), 'PNG')
    print(f"Icône créée: {filename}")

def create_computer_icon(filename):
    """Icône d'ordinateur/maison"""
    size = 128
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Maison bleue
    # Toit
    draw.polygon([(64, 25), (25, 55), (103, 55)], fill='#3498db', outline='#2980b9', width=3)
    # Murs
    draw.rectangle([(35, 55), (93, 100)], fill='#4a90e2', outline='#2980b9', width=3)
    # Porte
    draw.rectangle([(50, 70), (70, 100)], fill='#2c3e50', outline='#34495e', width=2)
    # Fenêtre
    draw.rectangle([(75, 65), (88, 78)], fill='#f1c40f', outline='#f39c12', width=2)
    
    img.save(os.path.join(os.path.dirname(__file__), 'icons', filename), 'PNG')
    print(f"Icône créée: {filename}")

def create_rocket_icon(filename):
    """Icône de fusée"""
    size = 128
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fusée rouge
    # Corps
    draw.rounded_rectangle([(50, 40), (78, 90)], radius=10, fill='#e74c3c', outline='#c0392b', width=3)
    # Pointe
    draw.polygon([(64, 20), (50, 40), (78, 40)], fill='#c0392b', outline='#922b21', width=2)
    # Aileron gauche
    draw.polygon([(50, 70), (35, 90), (50, 90)], fill='#95a5a6', outline='#7f8c8d', width=2)
    # Aileron droit
    draw.polygon([(78, 70), (93, 90), (78, 90)], fill='#95a5a6', outline='#7f8c8d', width=2)
    # Hublot
    draw.ellipse([(56, 50), (72, 66)], fill='#3498db', outline='#2980b9', width=2)
    # Flammes
    draw.ellipse([(54, 88), (64, 105)], fill='#f39c12', outline='#e67e22', width=1)
    draw.ellipse([(64, 88), (74, 105)], fill='#f39c12', outline='#e67e22', width=1)
    
    img.save(os.path.join(os.path.dirname(__file__), 'icons', filename), 'PNG')
    print(f"Icône créée: {filename}")

def create_settings_icon(filename):
    """Icône d'engrenage"""
    size = 128
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Engrenage gris
    center = 64
    outer_r = 40
    inner_r = 25
    teeth = 8
    
    import math
    
    # Dessiner les dents de l'engrenage
    for i in range(teeth):
        angle1 = 2 * math.pi * i / teeth
        angle2 = 2 * math.pi * (i + 0.4) / teeth
        angle3 = 2 * math.pi * (i + 0.6) / teeth
        angle4 = 2 * math.pi * (i + 1) / teeth
        
        points = [
            (center + inner_r * math.cos(angle1), center + inner_r * math.sin(angle1)),
            (center + outer_r * math.cos(angle2), center + outer_r * math.sin(angle2)),
            (center + outer_r * math.cos(angle3), center + outer_r * math.sin(angle3)),
            (center + inner_r * math.cos(angle4), center + inner_r * math.sin(angle4)),
        ]
        draw.polygon(points, fill='#95a5a6', outline='#7f8c8d')
    
    # Cercle central
    draw.ellipse([(center-inner_r, center-inner_r), (center+inner_r, center+inner_r)], 
                 fill='#7f8c8d', outline='#5d6d7e', width=3)
    # Trou central
    draw.ellipse([(center-12, center-12), (center+12, center+12)], 
                 fill='#34495e', outline='#2c3e50', width=2)
    
    img.save(os.path.join(os.path.dirname(__file__), 'icons', filename), 'PNG')
    print(f"Icône créée: {filename}")

# Créer les icônes
print("Génération des icônes...")

create_folder_icon('folder.png')
create_computer_icon('computer.png')
create_rocket_icon('rocket.png')
create_settings_icon('settings.png')

print("Toutes les icônes ont été créées dans le dossier 'icons'")
