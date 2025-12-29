#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bureau virtuel russe
Simule un bureau d'ordinateur avec dossiers et programmes
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from missile_launcher import MissileLauncher
from file_viewer import FileViewer
from config_manager import ConfigManager
import os

class DesktopScreen:
    def __init__(self, master):
        self.master = master
        self.config = ConfigManager()
        
        self.frame = tk.Frame(master, bg='#2b5876')
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Barre de titre style Windows russe
        titlebar = tk.Frame(self.frame, bg='#1e3c5a', height=40)
        titlebar.pack(fill=tk.X, side=tk.TOP)
        
        title_label = tk.Label(
            titlebar,
            text="Рабочий стол - Военный Компьютер",
            font=("Arial", 12, "bold"),
            fg='white',
            bg='#1e3c5a'
        )
        title_label.pack(side=tk.LEFT, padx=10)
        
        # Heure (simulation)
        time_label = tk.Label(
            titlebar,
            text="13:37",
            font=("Arial", 12),
            fg='white',
            bg='#1e3c5a'
        )
        time_label.pack(side=tk.RIGHT, padx=10)
        
        # Zone du bureau
        desktop_area = tk.Frame(self.frame, bg='#2b5876')
        desktop_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Création des icônes sur le bureau
        icons_data = [
            ("folder", "Секретные\nДокументы", self.open_documents),
            ("computer", "Мой\nКомпьютер", self.open_computer),
            ("rocket", "Система\nЗапуска", self.open_missile_launcher),
            ("settings", "Настройки", self.open_settings),
        ]
        
        row, col = 0, 0
        for emoji, text, command in icons_data:
            self.create_desktop_icon(desktop_area, emoji, text, command, row, col)
            row += 1
            if row > 3:
                row = 0
                col += 1
        
        # Barre des tâches
        taskbar = tk.Frame(self.frame, bg='#1e3c5a', height=50)
        taskbar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Bouton démarrer
        start_button = tk.Button(
            taskbar,
            text="ПУСК",
            font=("Arial", 12, "bold"),
            bg='#ff0000',
            fg='white',
            width=10,
            command=self.show_start_menu
        )
        start_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_desktop_icon(self, parent, icon_name, text, command, row, col):
        """Crée une icône sur le bureau"""
        icon_frame = tk.Frame(parent, bg='#2b5876')
        icon_frame.grid(row=row, column=col, padx=30, pady=30, sticky='n')
        
        # Charger l'image de l'icône
        from PIL import Image, ImageTk
        import os
        
        try:
            # Chemin vers l'image de l'icône (nom simple sans emoji)
            icon_path = os.path.join(os.path.dirname(__file__), 'icons', f'{icon_name}.png')
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                img = img.resize((64, 64), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                icon_button = tk.Button(
                    icon_frame,
                    image=photo,
                    bg='#2b5876',
                    fg='white',
                    relief=tk.FLAT,
                    activebackground='#3d6a8f',
                    command=command,
                    bd=0,
                )
                icon_button.image = photo  # Garder une référence
            else:
                # Fallback sur texte si l'image n'existe pas
                icon_button = tk.Button(
                    icon_frame,
                    text="[?]",
                    font=("Arial", 48),
                    bg='#2b5876',
                    fg='white',
                    relief=tk.FLAT,
                    activebackground='#3d6a8f',
                    command=command,
                    bd=0,
                )
                print(f"Icône non trouvée: {icon_path}")
        except Exception as e:
            # En cas d'erreur, utiliser un placeholder
            print(f"Erreur chargement icône {icon_name}: {e}")
            icon_button = tk.Button(
                icon_frame,
                text="[?]",
                font=("Arial", 48),
                bg='#2b5876',
                fg='white',
                relief=tk.FLAT,
                activebackground='#3d6a8f',
                command=command,
                bd=0,
            cursor='hand2'
        )
        icon_button.pack(anchor='center')
        
        # Label de texte
        text_label = tk.Label(
            icon_frame,
            text=text,
            font=("Arial", 10, "bold"),
            fg='white',
            bg='#2b5876',
            justify=tk.CENTER
        )
        text_label.pack(anchor='center')
        
        # Bind double-click
        icon_button.bind('<Double-Button-1>', lambda e: command())
    
    def open_documents(self):
        """Ouvre le dossier de documents secrets après vérification du code"""
        # Créer une fenêtre de dialogue pour le code
        dialog = tk.Toplevel(self.master)
        dialog.title("Доступ к документам")
        dialog.geometry("400x200")
        dialog.configure(bg='#1a1a1a')
        dialog.transient(self.master)
        dialog.grab_set()
        
        # Centrer la fenêtre
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        tk.Label(
            dialog,
            text="🔐 ТРЕБУЕТСЯ АВТОРИЗАЦИЯ",
            font=("Arial", 14, "bold"),
            fg='#ff0000',
            bg='#1a1a1a'
        ).pack(pady=20)
        
        # Code d'accès
        tk.Label(
            dialog,
            text="Код доступа:",
            font=("Arial", 10),
            fg='#00ff00',
            bg='#1a1a1a'
        ).pack(pady=5)
        
        code_entry = tk.Entry(
            dialog,
            font=("Courier", 12),
            width=15,
            justify='center',
            bg='#2a2a2a',
            fg='#00ff00'
        )
        code_entry.pack(pady=5)
        
        def verify_code():
            code = code_entry.get().strip()
            
            if len(code) != 6:
                messagebox.showerror("Ошибка", "Код должен содержать 6 цифр")
                return
            
            if self.config.verify_dossier_code(code):
                dialog.destroy()
                self.show_documents()
            else:
                messagebox.showerror("Доступ запрещен", "Неверный код доступа!")
                code_entry.delete(0, tk.END)
                code_entry.focus()
        
        tk.Button(
            dialog,
            text="ВОЙТИ",
            font=("Arial", 12, "bold"),
            bg='#008800',
            fg='white',
            command=verify_code,
            width=15
        ).pack(pady=15)
        
        code_entry.focus()
        code_entry.bind('<Return>', lambda e: verify_code())
    
    def show_documents(self):
        """Affiche le visualiseur de documents"""
        self.frame.destroy()
        FileViewer(self.master, self.__class__, self.config.get_documents_folder())
    
    def open_computer(self):
        """Ouvre Poste de travail"""
        messagebox.showinfo(
            "Мой Компьютер",
            "💾 Диск C: (Система)\n" +
            "💿 Диск D: (Данные)\n" +
            "🌐 Сеть: Отключена\n\n" +
            "ℹ Все системы работают"
        )
    
    def open_missile_launcher(self):
        """Ouvre le programme de lancement de missile après vérification du code"""
        # Créer une fenêtre de dialogue pour le code
        dialog = tk.Toplevel(self.master)
        dialog.title("Доступ к ракете")
        dialog.geometry("400x200")
        dialog.configure(bg='#1a1a1a')
        dialog.transient(self.master)
        dialog.grab_set()
        
        # Centrer la fenêtre
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        tk.Label(
            dialog,
            text="⚠ СИСТЕМА ЗАПУСКА ⚠",
            font=("Arial", 14, "bold"),
            fg='#ff0000',
            bg='#1a1a1a'
        ).pack(pady=20)
        
        # Code d'autorisation
        tk.Label(
            dialog,
            text="Код авторизации:",
            font=("Arial", 10),
            fg='#00ff00',
            bg='#1a1a1a'
        ).pack(pady=5)
        
        code_entry = tk.Entry(
            dialog,
            font=("Courier", 12),
            width=15,
            justify='center',
            bg='#2a2a2a',
            fg='#00ff00'
        )
        code_entry.pack(pady=5)
        
        def verify_code():
            code = code_entry.get().strip()
            
            if len(code) != 6:
                messagebox.showerror("Ошибка", "Код должен содержать 6 цифр")
                return
            
            if self.config.verify_missile_code(code):
                dialog.destroy()
                self.show_missile_launcher()
            else:
                messagebox.showerror("Доступ запрещен", "Неверный код авторизации!")
                code_entry.delete(0, tk.END)
                code_entry.focus()
        
        tk.Button(
            dialog,
            text="ПРОДОЛЖИТЬ",
            font=("Arial", 12, "bold"),
            bg='#ff0000',
            fg='white',
            command=verify_code,
            width=15
        ).pack(pady=15)
        
        code_entry.focus()
        code_entry.bind('<Return>', lambda e: verify_code())
    
    def show_missile_launcher(self):
        """Affiche le programme de lancement de missile"""
        self.frame.destroy()
        MissileLauncher(self.master, self.__class__)
    
    def open_settings(self):
        """Ouvre les paramètres"""
        messagebox.showinfo(
            "Настройки",
            "⚙️ Настройки системы\n\n" +
            "Язык: Русский\n" +
            "Часовой пояс: MSK (UTC+3)\n" +
            "Сеть: Локальная\n\n" +
            "❌ Доступ ограничен"
        )
    
    def show_start_menu(self):
        """Affiche le menu démarrer"""
        messagebox.showinfo(
            "Меню Пуск",
            "📋 Программы\n" +
            "⚙️ Параметры\n" +
            "🔌 Выключение\n\n" +
            "ℹ Функция недоступна"
        )
