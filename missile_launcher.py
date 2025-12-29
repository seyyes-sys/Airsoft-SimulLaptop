#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programme de lancement de missile
Simulation d'un système de contrôle de missile
"""

import tkinter as tk
from tkinter import messagebox
from config_manager import ConfigManager
import time
import threading
import platform
import os

class MissileLauncher:
    def __init__(self, master, desktop_class):
        self.master = master
        self.desktop_class = desktop_class
        self.config = ConfigManager()
        self.launch_in_progress = False
        
        self.frame = tk.Frame(master, bg='#0a0a0a')
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Barre de titre
        titlebar = tk.Frame(self.frame, bg='#ff0000', height=50)
        titlebar.pack(fill=tk.X)
        
        title = tk.Label(
            titlebar,
            text="⚠ СИСТЕМА УПРАВЛЕНИЯ РАКЕТОЙ ⚠",
            font=("Arial", 18, "bold"),
            fg='white',
            bg='#ff0000'
        )
        title.pack(pady=10)
        
        # Zone principale
        main_area = tk.Frame(self.frame, bg='#0a0a0a')
        main_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Informations sur le missile
        info_frame = tk.Frame(main_area, bg='#1a1a1a', relief=tk.RIDGE, bd=5)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        info_title = tk.Label(
            info_frame,
            text="ИНФОРМАЦИЯ О РАКЕТЕ",
            font=("Arial", 16, "bold"),
            fg='#ffff00',
            bg='#1a1a1a'
        )
        info_title.pack(pady=10)
        
        # Nom du missile
        missile_name = self.config.get("missile_name", "RS-28 Sarmat")
        
        missile_label = tk.Label(
            info_frame,
            text=f"Тип: {missile_name}",
            font=("Courier", 14, "bold"),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        missile_label.pack(pady=5)
        
        status_label = tk.Label(
            info_frame,
            text="Статус: ГОТОВА К ЗАПУСКУ",
            font=("Courier", 14),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        status_label.pack(pady=5)
        
        target_label = tk.Label(
            info_frame,
            text="Координаты: 48.8566° N, 2.3522° E",
            font=("Courier", 14),
            fg='#00ffff',
            bg='#1a1a1a'
        )
        target_label.pack(pady=5)
        
        # Minuteur configurable
        timer_frame = tk.Frame(info_frame, bg='#1a1a1a')
        timer_frame.pack(pady=10)
        
        timer_label = tk.Label(
            timer_frame,
            text="Таймер запуска (сек):",
            font=("Courier", 12),
            fg='#ffaa00',
            bg='#1a1a1a'
        )
        timer_label.pack(side=tk.LEFT, padx=5)
        
        self.timer_var = tk.StringVar(value=str(self.config.get("missile_timer_default", 1200)))
        self.timer_spinbox = tk.Spinbox(
            timer_frame,
            from_=10,
            to=1800,
            textvariable=self.timer_var,
            font=("Courier", 12, "bold"),
            width=8,
            bg='#2a2a2a',
            fg='#ffaa00',
            buttonbackground='#444444',
            relief=tk.RIDGE,
            bd=3
        )
        self.timer_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Zone de statut de lancement
        self.status_text = tk.Text(
            main_area,
            height=8,
            font=("Courier", 10),
            bg='#0a0a0a',
            fg='#00ff00',
            insertbackground='#00ff00',
            relief=tk.RIDGE,
            bd=3
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.status_text.insert(1.0, ">>> Система готова\n>>> Ожидание команды запуска...\n")
        self.status_text.config(state=tk.DISABLED)
        
        # Boutons de contrôle
        controls_frame = tk.Frame(main_area, bg='#0a0a0a')
        controls_frame.pack(pady=20)
        
        # Bouton de lancement
        self.launch_button = tk.Button(
            controls_frame,
            text="🚀 ЗАПУСК РАКЕТЫ",
            font=("Arial", 18, "bold"),
            bg='#ff0000',
            fg='white',
            activebackground='#ff4444',
            activeforeground='white',
            width=20,
            height=3,
            command=self.confirm_launch,
            relief=tk.RAISED,
            bd=8
        )
        self.launch_button.pack(side=tk.LEFT, padx=20)
        
        # Bouton retour
        back_button = tk.Button(
            controls_frame,
            text="← НАЗАД",
            font=("Arial", 14, "bold"),
            bg='#444444',
            fg='white',
            activebackground='#666666',
            width=15,
            height=2,
            command=self.go_back
        )
        back_button.pack(side=tk.LEFT, padx=20)
        
        # Warning clignotant
        self.warning_label = tk.Label(
            main_area,
            text="⚠ ВНИМАНИЕ: НЕОБРАТИМОЕ ДЕЙСТВИЕ ⚠",
            font=("Arial", 14, "bold"),
            fg='#ff0000',
            bg='#0a0a0a'
        )
        self.warning_label.pack(pady=10)
        self.blink_warning()
    
    def blink_warning(self):
        """Fait clignoter le message d'avertissement"""
        try:
            current_color = self.warning_label.cget("fg")
            new_color = '#ff0000' if current_color == '#ffff00' else '#ffff00'
            self.warning_label.config(fg=new_color)
            self.master.after(500, self.blink_warning)
        except:
            # Le widget a été détruit, arrêter le clignotement
            pass
    
    def confirm_launch(self):
        """Demande confirmation avant le lancement"""
        if self.launch_in_progress:
            return
        
        response = messagebox.askyesno(
            "ПОДТВЕРЖДЕНИЕ ЗАПУСКА",
            "⚠️ ВНИМАНИЕ ⚠️\n\n" +
            "Вы уверены, что хотите запустить ракету?\n\n" +
            "Это действие не может быть отменено!\n\n" +
            "Продолжить?",
            icon='warning'
        )
        
        if response:
            self.initiate_launch()
    
    def initiate_launch(self):
        """Lance la séquence de lancement"""
        self.launch_in_progress = True
        self.launch_button.config(state=tk.DISABLED, bg='#666666')
        
        # Lance la séquence dans un thread
        thread = threading.Thread(target=self.launch_sequence)
        thread.daemon = True
        thread.start()
    
    def launch_sequence(self):
        """Séquence de lancement avec décompte configurable"""
        missile_name = self.config.get("missile_name", "RS-28 Sarmat")
        
        # Récupérer le minuteur
        try:
            timer_seconds = int(self.timer_var.get())
            if timer_seconds < 10:
                timer_seconds = 10
            elif timer_seconds > 1800:
                timer_seconds = 1800
        except:
            timer_seconds = 1200
        
        messages = [
            f">>> Инициализация системы запуска {missile_name}...\n",
            ">>> Проверка топливных баков... ОК\n",
            ">>> Проверка навигации... ОК\n",
            ">>> Проверка боеголовки... ОК\n",
            ">>> Координаты цели подтверждены\n",
            f">>> Установлен таймер: {timer_seconds} секунд\n",
            ">>> Начало обратного отсчета...\n",
            "\n"
        ]
        
        for msg in messages:
            self.add_status_message(msg)
            time.sleep(0.8)
        
        # Décompte
        for i in range(timer_seconds, 0, -1):
            # Bip sonore à chaque seconde
            try:
                if platform.system() == 'Windows':
                    import winsound
                    winsound.Beep(800, 100)  # Fréquence 800Hz, durée 100ms
                else:
                    # Linux/Raspberry Pi: utiliser beep via subprocess
                    os.system('(speaker-test -t sine -f 800 >/dev/null 2>&1 &); sleep 0.1; killall speaker-test >/dev/null 2>&1')
            except:
                pass
            
            # Annonce vocale chaque minute
            if i % 60 == 0:
                minutes_remaining = i // 60
                self.add_status_message(f">>> [{minutes_remaining} минут до запуска]\n")
                # Annonce vocale
                try:
                    if platform.system() == 'Windows':
                        import pyttsx3
                        engine = pyttsx3.init()
                        engine.say(f"{minutes_remaining} minutes remaining")
                        engine.runAndWait()
                    else:
                        # Linux/Raspberry Pi: utiliser espeak directement
                        os.system(f'espeak "{minutes_remaining} minutes remaining" 2>/dev/null &')
                except Exception as e:
                    print(f"Erreur voix: {e}")
                    pass
            
            self.add_status_message(f">>> {i}...\n")
            time.sleep(1)
        
        self.add_status_message("\n")
        
        # Sirène d'alerte
        self.add_status_message(">>> ⚠️ ALARME! ALARME! ALARME! ⚠️\n")
        try:
            if platform.system() == 'Windows':
                import winsound
                # Sirène avec sons croissants et décroissants
                for _ in range(3):
                    for freq in range(400, 1200, 100):
                        winsound.Beep(freq, 50)
                    for freq in range(1200, 400, -100):
                        winsound.Beep(freq, 50)
            else:
                # Linux/Raspberry Pi: sirène alternative
                for _ in range(3):
                    os.system('(speaker-test -t sine -f 800 >/dev/null 2>&1 &); sleep 0.5; killall speaker-test >/dev/null 2>&1')
                    os.system('(speaker-test -t sine -f 1200 >/dev/null 2>&1 &); sleep 0.5; killall speaker-test >/dev/null 2>&1')
        except:
            pass
        
        self.add_status_message(">>> ЗАПУСК! 🚀🚀🚀\n")
        
        # Annonce vocale du lancement
        try:
            if platform.system() == 'Windows':
                import pyttsx3
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                engine.setProperty('volume', 1.0)
                engine.say("Missile launched! Launch successful!")
                engine.runAndWait()
            else:
                # Linux/Raspberry Pi: utiliser espeak avec emphase
                os.system('espeak -s 150 -a 200 "Missile launched! Launch successful!" 2>/dev/null &')
        except Exception as e:
            print(f"Erreur voix lancement: {e}")
            pass
        time.sleep(0.5)
        self.add_status_message(">>> Ракета покинула шахту\n")
        time.sleep(0.5)
        self.add_status_message(">>> Первая ступень: АКТИВНА\n")
        time.sleep(1)
        self.add_status_message(">>> Вторая ступень: АКТИВНА\n")
        time.sleep(1)
        self.add_status_message(">>> Траектория стабильна\n")
        time.sleep(1)
        self.add_status_message(">>> Расчетное время до цели: 25 минут\n")
        time.sleep(1)
        self.add_status_message("\n>>> ✓ МИССИЯ ВЫПОЛНЕНА ✓\n")
        
        # Message final
        self.master.after(1000, self.show_mission_complete)
    
    def add_status_message(self, message):
        """Ajoute un message dans la zone de statut"""
        def update():
            self.status_text.config(state=tk.NORMAL)
            self.status_text.insert(tk.END, message)
            self.status_text.see(tk.END)
            self.status_text.config(state=tk.DISABLED)
        
        self.master.after(0, update)
    
    def show_mission_complete(self):
        """Affiche le message de fin de mission"""
        messagebox.showinfo(
            "МИССИЯ ВЫПОЛНЕНА",
            "✓ Ракета успешно запущена!\n\n" +
            "Цель будет поражена через 25 минут.\n\n" +
            "Операция завершена."
        )
        self.launch_button.config(state=tk.NORMAL, bg='#ff0000')
        self.launch_in_progress = False
    
    def go_back(self):
        """Retour au bureau"""
        if not self.launch_in_progress:
            self.frame.destroy()
            self.desktop_class(self.master)
        else:
            messagebox.showwarning(
                "ВНИМАНИЕ",
                "Невозможно выйти во время запуска!"
            )
