#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Écran de connexion
Interface pour entrer les 2 codes à 6 chiffres
"""

import tkinter as tk
from tkinter import messagebox
from config_manager import ConfigManager
from desktop_screen import DesktopScreen
from admin_panel import AdminPanel

class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.config = ConfigManager()
        self.admin_click_count = 0
        
        self.frame = tk.Frame(master, bg='#1a1a1a')
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Titre avec style russe
        title = tk.Label(
            self.frame,
            text="СИСТЕМА БЕЗОПАСНОСТИ",
            font=("Arial", 32, "bold"),
            fg='#ff0000',
            bg='#1a1a1a'
        )
        title.pack(pady=50)
        
        # Sous-titre
        subtitle = tk.Label(
            self.frame,
            text="Военный Комплекс - Доступ Ограничен",
            font=("Arial", 16),
            fg='#ffff00',
            bg='#1a1a1a'
        )
        subtitle.pack(pady=10)
        
        # Container pour le code
        code_frame = tk.Frame(self.frame, bg='#1a1a1a')
        code_frame.pack(pady=50)
        
        # Code d'accès
        code_label = tk.Label(
            code_frame,
            text="КОД ДОСТУПА:",
            font=("Arial", 14, "bold"),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        code_label.grid(row=0, column=0, padx=20, pady=10, sticky='e')
        
        self.code_entry = tk.Entry(
            code_frame,
            font=("Courier", 18, "bold"),
            width=10,
            justify='center',
            bg='#2a2a2a',
            fg='#00ff00',
            insertbackground='#00ff00',
            relief=tk.RIDGE,
            bd=3
        )
        self.code_entry.grid(row=0, column=1, padx=20, pady=10)
        self.code_entry.bind('<KeyRelease>', self.validate_code_input)
        
        # Bouton de connexion
        self.login_button = tk.Button(
            self.frame,
            text="ВОЙТИ",
            font=("Arial", 16, "bold"),
            bg='#008800',
            fg='white',
            activebackground='#00ff00',
            activeforeground='black',
            width=15,
            height=2,
            command=self.attempt_login,
            relief=tk.RAISED,
            bd=5
        )
        self.login_button.pack(pady=30)
        
        # Message d'avertissement
        warning = tk.Label(
            self.frame,
            text="⚠ НЕСАНКЦИОНИРОВАННЫЙ ДОСТУП ЗАПРЕЩЕН ⚠",
            font=("Arial", 12, "bold"),
            fg='#ff0000',
            bg='#1a1a1a'
        )
        warning.pack(side=tk.BOTTOM, pady=20)
        
        # Zone cliquable pour accès admin (invisible)
        admin_trigger = tk.Label(
            self.frame,
            text="",
            bg='#1a1a1a',
            width=2,
            height=1
        )
        admin_trigger.place(x=0, y=0)
        admin_trigger.bind('<Button-1>', self.admin_access)
        
        # Bind Enter key
        self.code_entry.bind('<Return>', lambda e: self.attempt_login())
        
        # Focus sur le champ
        self.code_entry.focus()
    
    def validate_code_input(self, event):
        """Limite l'entrée à 6 chiffres"""
        entry = event.widget
        value = entry.get()
        
        # Ne garder que les chiffres
        filtered = ''.join(c for c in value if c.isdigit())
        
        # Limiter à 6 caractères
        if len(filtered) > 6:
            filtered = filtered[:6]
        
        if filtered != value:
            entry.delete(0, tk.END)
            entry.insert(0, filtered)
    
    def attempt_login(self):
        """Tente la connexion avec le code fourni"""
        code = self.code_entry.get().strip()
        
        # Vérification de la longueur
        if len(code) != 6:
            messagebox.showerror(
                "ОШИБКА",
                "Код должен содержать 6 цифр"
            )
            return
        
        # Vérification du code
        if self.config.verify_bureau_code(code):
            self.show_desktop()
        else:
            messagebox.showerror(
                "ДОСТУП ЗАПРЕЩЕН",
                "Неверный код доступа!\n\nСистема заблокирована."
            )
            self.code_entry.delete(0, tk.END)
            self.code_entry.focus()
    
    def show_desktop(self):
        """Affiche le bureau virtuel"""
        self.frame.destroy()
        DesktopScreen(self.master)
    
    def admin_access(self, event):
        """Accès secret à l'interface administrateur"""
        self.admin_click_count += 1
        
        if self.admin_click_count >= 5:
            self.admin_click_count = 0
            password = tk.simpledialog.askstring(
                "Admin Access",
                "Enter admin password:",
                show='*'
            )
            if password and self.config.verify_admin_password(password):
                self.frame.destroy()
                AdminPanel(self.master, self.__class__)
            else:
                messagebox.showerror("Error", "Invalid password")

# Import nécessaire pour askstring
import tkinter.simpledialog
