#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Panel d'administration
Interface pour configurer les codes et le nom du missile
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from config_manager import ConfigManager
import os
import shutil

class AdminPanel:
    def __init__(self, master, login_class):
        self.master = master
        self.login_class = login_class
        self.config = ConfigManager()
        
        self.frame = tk.Frame(master, bg='#2a2a2a')
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Titre
        title = tk.Label(
            self.frame,
            text="[*] PANNEAU D'ADMINISTRATION",
            font=("Arial", 24, "bold"),
            fg='#ffaa00',
            bg='#2a2a2a'
        )
        title.pack(pady=20)
        
        # Créer un canvas avec scrollbar pour tout le contenu
        canvas = tk.Canvas(self.frame, bg='#2a2a2a', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2a2a2a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame principal (dans le scrollable_frame maintenant)
        main_frame = tk.Frame(scrollable_frame, bg='#3a3a3a', relief=tk.RIDGE, bd=5)
        main_frame.pack(padx=50, pady=20, fill=tk.BOTH, expand=True)
        
        # Configuration des codes
        codes_frame = tk.LabelFrame(
            main_frame,
            text="Codes d'accès",
            font=("Arial", 14, "bold"),
            fg='white',
            bg='#3a3a3a',
            relief=tk.GROOVE,
            bd=3
        )
        codes_frame.pack(padx=20, pady=20, fill=tk.X)
        
        # Code Bureau
        tk.Label(
            codes_frame,
            text="Code Bureau (6 chiffres):",
            font=("Arial", 12),
            fg='#ffaa00',
            bg='#3a3a3a'
        ).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        
        self.code_bureau_var = tk.StringVar(value=self.config.get("code_bureau", "111111"))
        tk.Entry(
            codes_frame,
            textvariable=self.code_bureau_var,
            font=("Courier", 14),
            width=15,
            justify='center'
        ).grid(row=0, column=1, padx=10, pady=10)
        
        # Code Dossier
        tk.Label(
            codes_frame,
            text="Code Dossier (6 chiffres):",
            font=("Arial", 12),
            fg='#00ff00',
            bg='#3a3a3a'
        ).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        
        self.code_dossier_var = tk.StringVar(value=self.config.get("code_dossier", "222222"))
        tk.Entry(
            codes_frame,
            textvariable=self.code_dossier_var,
            font=("Courier", 14),
            width=15,
            justify='center'
        ).grid(row=1, column=1, padx=10, pady=10)
        
        # Code Missile
        tk.Label(
            codes_frame,
            text="Code Missile (6 chiffres):",
            font=("Arial", 12),
            fg='#ff0000',
            bg='#3a3a3a'
        ).grid(row=2, column=0, padx=10, pady=10, sticky='e')
        
        self.code_missile_var = tk.StringVar(value=self.config.get("code_missile", "333333"))
        tk.Entry(
            codes_frame,
            textvariable=self.code_missile_var,
            font=("Courier", 14),
            width=15,
            justify='center'
        ).grid(row=2, column=1, padx=10, pady=10)
        
        # Code Annulation
        tk.Label(
            codes_frame,
            text="Code Annulation (6 chiffres):",
            font=("Arial", 12),
            fg='#ff8800',
            bg='#3a3a3a'
        ).grid(row=3, column=0, padx=10, pady=10, sticky='e')
        
        self.code_annulation_var = tk.StringVar(value=self.config.get("code_annulation", "999999"))
        tk.Entry(
            codes_frame,
            textvariable=self.code_annulation_var,
            font=("Courier", 14),
            width=15,
            justify='center'
        ).grid(row=3, column=1, padx=10, pady=10)
        
        # Configuration du missile
        missile_frame = tk.LabelFrame(
            main_frame,
            text="Configuration du missile",
            font=("Arial", 14, "bold"),
            fg='white',
            bg='#3a3a3a',
            relief=tk.GROOVE,
            bd=3
        )
        missile_frame.pack(padx=20, pady=20, fill=tk.X)
        
        tk.Label(
            missile_frame,
            text="Nom du missile:",
            font=("Arial", 12),
            fg='white',
            bg='#3a3a3a'
        ).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        
        self.missile_var = tk.StringVar(value=self.config.get("missile_name"))
        tk.Entry(
            missile_frame,
            textvariable=self.missile_var,
            font=("Arial", 14),
            width=30
        ).grid(row=0, column=1, padx=10, pady=10)
        
        # Minuteur par défaut
        tk.Label(
            missile_frame,
            text="Minuteur par défaut (sec):",
            font=("Arial", 12),
            fg='white',
            bg='#3a3a3a'
        ).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        
        self.timer_var = tk.StringVar(value=str(self.config.get("missile_timer_default", 2400)))
        tk.Spinbox(
            missile_frame,
            textvariable=self.timer_var,
            from_=10,
            to=3600,
            font=("Arial", 12),
            width=10,
            justify='center'
        ).grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        # Case à cocher pour verrouiller le timer
        self.timer_locked_var = tk.BooleanVar(value=self.config.get("missile_timer_locked", False))
        tk.Checkbutton(
            missile_frame,
            text="Verrouiller le timer (empêcher les joueurs de le modifier)",
            variable=self.timer_locked_var,
            font=("Arial", 11),
            fg='#ff8800',
            bg='#3a3a3a',
            selectcolor='#2a2a2a',
            activebackground='#3a3a3a',
            activeforeground='#ff8800'
        ).grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        
        # Suggestions de noms de missiles
        suggestions = [
            "RS-28 Sarmat",
            "RT-2PM2 Topol-M",
            "RS-24 Yars",
            "R-36M2 Voevoda",
            "Iskander-M"
        ]
        
        tk.Label(
            missile_frame,
            text="Suggestions:",
            font=("Arial", 10, "italic"),
            fg='#aaaaaa',
            bg='#3a3a3a'
        ).grid(row=3, column=0, padx=10, pady=5, sticky='ne')
        
        suggestions_text = "\n".join(suggestions)
        tk.Label(
            missile_frame,
            text=suggestions_text,
            font=("Arial", 9),
            fg='#aaaaaa',
            bg='#3a3a3a',
            justify=tk.LEFT
        ).grid(row=3, column=1, padx=10, pady=5, sticky='w')
        
        # Configuration du mot de passe admin
        password_frame = tk.LabelFrame(
            main_frame,
            text="Mot de passe administrateur",
            font=("Arial", 14, "bold"),
            fg='white',
            bg='#3a3a3a',
            relief=tk.GROOVE,
            bd=3
        )
        password_frame.pack(padx=20, pady=20, fill=tk.X)
        
        tk.Label(
            password_frame,
            text="Nouveau mot de passe:",
            font=("Arial", 12),
            fg='white',
            bg='#3a3a3a'
        ).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        
        self.password_var = tk.StringVar()
        tk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=("Arial", 14),
            width=20,
            show='*'
        ).grid(row=0, column=1, padx=10, pady=10)
        
        # Gestion des fichiers du dossier
        files_frame = tk.LabelFrame(
            main_frame,
            text="Gestion des fichiers (Documents secrets)",
            font=("Arial", 14, "bold"),
            fg='white',
            bg='#3a3a3a',
            relief=tk.GROOVE,
            bd=3
        )
        files_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        tk.Label(
            files_frame,
            text="Fichiers actuels:",
            font=("Arial", 12),
            fg='#00ff00',
            bg='#3a3a3a'
        ).pack(pady=10)
        
        # Liste des fichiers
        self.files_listbox = tk.Listbox(
            files_frame,
            font=("Courier", 10),
            bg='#1a1a1a',
            fg='#00ff00',
            height=6
        )
        self.files_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Boutons de gestion
        files_buttons = tk.Frame(files_frame, bg='#3a3a3a')
        files_buttons.pack(pady=10)
        
        add_btn = tk.Button(
            files_buttons,
            text="+ AJOUTER FICHIER",
            font=("Arial", 12, "bold"),
            bg='#0066cc',
            fg='white',
            command=self.add_file,
            width=22,
            height=2,
            relief=tk.RAISED,
            bd=3
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        del_btn = tk.Button(
            files_buttons,
            text="X SUPPRIMER FICHIER",
            font=("Arial", 12, "bold"),
            bg='#cc0000',
            fg='white',
            command=self.delete_file,
            width=22,
            height=2,
            relief=tk.RAISED,
            bd=3
        )
        del_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(
            files_buttons,
            text="@ RAFRAICHIR",
            font=("Arial", 12, "bold"),
            bg='#666666',
            fg='white',
            command=self.refresh_files,
            width=22,
            height=2,
            relief=tk.RAISED,
            bd=3
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Charger les fichiers
        self.refresh_files()
        
        # Boutons (dans scrollable_frame pour être visibles)
        buttons_frame = tk.Frame(scrollable_frame, bg='#2a2a2a')
        buttons_frame.pack(pady=20)
        
        save_button = tk.Button(
            buttons_frame,
            text="V SAUVEGARDER",
            font=("Arial", 16, "bold"),
            bg='#008800',
            fg='white',
            activebackground='#00aa00',
            width=20,
            height=2,
            relief=tk.RAISED,
            bd=4,
            command=self.save_configuration
        )
        save_button.pack(side=tk.LEFT, padx=10)
        
        reset_button = tk.Button(
            buttons_frame,
            text="@ REINITIALISER",
            font=("Arial", 16, "bold"),
            bg='#ff8800',
            fg='white',
            activebackground='#ffaa00',
            width=20,
            height=2,
            relief=tk.RAISED,
            bd=4,
            command=self.reset_configuration
        )
        reset_button.pack(side=tk.LEFT, padx=10)
        
        back_button = tk.Button(
            buttons_frame,
            text="< RETOUR",
            font=("Arial", 16, "bold"),
            bg='#444444',
            fg='white',
            activebackground='#666666',
            width=20,
            height=2,
            relief=tk.RAISED,
            bd=4,
            command=self.go_back
        )
        back_button.pack(side=tk.LEFT, padx=10)
    
    def save_configuration(self):
        """Sauvegarde la configuration"""
        code_bureau = self.code_bureau_var.get().strip()
        code_dossier = self.code_dossier_var.get().strip()
        code_missile = self.code_missile_var.get().strip()
        code_annulation = self.code_annulation_var.get().strip()
        missile_name = self.missile_var.get().strip()
        timer_default = self.timer_var.get().strip()
        timer_locked = self.timer_locked_var.get()
        new_password = self.password_var.get().strip()
        
        # Validation des codes
        codes_to_validate = [
            ("Bureau", code_bureau),
            ("Dossier", code_dossier),
            ("Missile", code_missile),
            ("Annulation", code_annulation)
        ]
        
        for name, code in codes_to_validate:
            if not code.isdigit() or len(code) != 6:
                messagebox.showerror("Erreur", f"Le code {name} doit contenir exactement 6 chiffres")
                return
        
        if not missile_name:
            messagebox.showerror("Erreur", "Le nom du missile ne peut pas être vide")
            return
        
        # Validation du timer
        try:
            timer_val = int(timer_default)
            if timer_val < 10 or timer_val > 3600:
                messagebox.showerror("Erreur", "Le minuteur doit être entre 10 et 3600 secondes (60 min)")
                return
        except:
            messagebox.showerror("Erreur", "Le minuteur doit être un nombre valide")
            return
        
        # Sauvegarde
        self.config.set("code_bureau", code_bureau)
        self.config.set("code_dossier", code_dossier)
        self.config.set("code_missile", code_missile)
        self.config.set("code_annulation", code_annulation)
        self.config.set("missile_name", missile_name)
        self.config.set("missile_timer_default", timer_val)
        self.config.set("missile_timer_locked", timer_locked)
        
        if new_password:
            self.config.set("admin_password", new_password)
            self.password_var.set("")
        
        messagebox.showinfo(
            "Succès",
            "✓ Configuration sauvegardée avec succès!\n\n" +
            f"Code Bureau: {code_bureau}\n" +
            f"Code Dossier: {code_dossier}\n" +
            f"Code Missile: {code_missile}\n" +
            f"Code Annulation: {code_annulation}\n" +
            f"Missile: {missile_name}\n" +
            f"Minuteur: {timer_val}s\n" +
            f"Timer verrouillé: {'Oui' if timer_locked else 'Non'}"
        )
    
    def reset_configuration(self):
        """Réinitialise la configuration par défaut"""
        response = messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment réinitialiser la configuration?\n\n" +
            "Les valeurs par défaut seront restaurées."
        )
        
        if response:
            self.config.set("code_bureau", "111111")
            self.config.set("code_dossier", "222222")
            self.config.set("code_missile", "333333")
            self.config.set("code_annulation", "999999")
            self.config.set("missile_name", "RS-28 Sarmat")
            self.config.set("missile_timer_default", 2400)
            self.config.set("missile_timer_locked", False)
            self.config.set("admin_password", "admin123")
            
            self.code_bureau_var.set("111111")
            self.code_dossier_var.set("222222")
            self.code_missile_var.set("333333")
            self.code_annulation_var.set("999999")
            self.missile_var.set("RS-28 Sarmat")
            self.timer_var.set("2400")
            self.timer_locked_var.set(False)
            self.password_var.set("")
            
            messagebox.showinfo("Succès", "Configuration réinitialisée")
    
    def refresh_files(self):
        """Rafraîchit la liste des fichiers"""
        self.files_listbox.delete(0, tk.END)
        docs_folder = self.config.get_documents_folder()
        
        if os.path.exists(docs_folder):
            files = os.listdir(docs_folder)
            if files:
                for file in sorted(files):
                    filepath = os.path.join(docs_folder, file)
                    if os.path.isfile(filepath):
                        size = os.path.getsize(filepath)
                        size_str = self.format_size(size)
                        self.files_listbox.insert(tk.END, f"{file} ({size_str})")
            else:
                self.files_listbox.insert(tk.END, "Aucun fichier")
    
    def format_size(self, size):
        """Formate la taille du fichier"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def add_file(self):
        """Ajoute un fichier au dossier"""
        filetypes = [
            ("Tous les fichiers supportés", "*.pdf *.jpg *.jpeg *.png *.gif *.bmp *.mp4 *.avi *.mov *.mkv *.txt"),
            ("Images", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("PDF", "*.pdf"),
            ("Vidéos", "*.mp4 *.avi *.mov *.mkv"),
            ("Texte", "*.txt"),
            ("Tous les fichiers", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Sélectionner des fichiers à ajouter",
            filetypes=filetypes
        )
        
        if files:
            docs_folder = self.config.get_documents_folder()
            added_count = 0
            
            for file in files:
                try:
                    filename = os.path.basename(file)
                    dest = os.path.join(docs_folder, filename)
                    
                    # Vérifier si le fichier existe déjà
                    if os.path.exists(dest):
                        response = messagebox.askyesno(
                            "Fichier existant",
                            f"Le fichier '{filename}' existe déjà.\n\nRemplacer?"
                        )
                        if not response:
                            continue
                    
                    shutil.copy2(file, dest)
                    added_count += 1
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur lors de la copie de {filename}:\n{str(e)}")
            
            if added_count > 0:
                messagebox.showinfo("Succès", f"{added_count} fichier(s) ajouté(s)")
                self.refresh_files()
    
    def delete_file(self):
        """Supprime le fichier sélectionné"""
        selection = self.files_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un fichier à supprimer")
            return
        
        index = selection[0]
        file_text = self.files_listbox.get(index)
        
        if file_text == "Aucun fichier":
            return
        
        # Extraire le nom du fichier
        filename = file_text.split(" (")[0]
        
        response = messagebox.askyesno(
            "Confirmation",
            f"Voulez-vous vraiment supprimer le fichier:\n{filename}?"
        )
        
        if response:
            try:
                docs_folder = self.config.get_documents_folder()
                filepath = os.path.join(docs_folder, filename)
                os.remove(filepath)
                messagebox.showinfo("Succès", "Fichier supprimé")
                self.refresh_files()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression:\n{str(e)}")
    
    def go_back(self):
        """Retour à l'écran de connexion"""
        self.frame.destroy()
        self.login_class(self.master)
