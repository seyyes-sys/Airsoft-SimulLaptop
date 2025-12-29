#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de configuration
Gère le chargement et la sauvegarde des paramètres
"""

import json
import os

CONFIG_FILE = "config.json"

class ConfigManager:
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self):
        """Charge la configuration depuis le fichier JSON"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Configuration par défaut
            default_config = {
                "admin_password": "admin123",
                "code1": "123456",
                "code2": "654321",
                "missile_name": "RS-28 Sarmat",
                "language": "ru"
            }
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config=None):
        """Sauvegarde la configuration dans le fichier JSON"""
        if config is None:
            config = self.config
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def get(self, key, default=None):
        """Récupère une valeur de configuration"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Définit une valeur de configuration"""
        self.config[key] = value
        self.save_config()
    
    def verify_bureau_code(self, code):
        """Vérifie le code d'accès au bureau"""
        return self.config.get("code_bureau") == code
    
    def verify_dossier_code(self, code):
        """Vérifie le code d'accès au dossier"""
        return self.config.get("code_dossier") == code
    
    def verify_missile_code(self, code):
        """Vérifie le code d'accès au missile"""
        return self.config.get("code_missile") == code
    
    def verify_admin_password(self, password):
        """Vérifie le mot de passe administrateur"""
        return self.config.get("admin_password") == password
    
    def get_documents_folder(self):
        """Retourne le chemin du dossier documents"""
        folder = self.config.get("documents_folder", "documents")
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder
