#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualiseur de fichiers
Affiche PDF, images et vidéos dans le bureau virtuel
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import io
from PIL import Image, ImageTk
import platform
import threading
import time

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

class FileViewer:
    def __init__(self, master, desktop_class, documents_folder):
        self.master = master
        self.desktop_class = desktop_class
        self.documents_folder = documents_folder
        self.current_file_index = 0
        
        self.frame = tk.Frame(master, bg='#1a1a1a')
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.load_files()
        self.create_widgets()
    
    def load_files(self):
        """Charge la liste des fichiers du dossier"""
        self.files = []
        if os.path.exists(self.documents_folder):
            for file in os.listdir(self.documents_folder):
                filepath = os.path.join(self.documents_folder, file)
                if os.path.isfile(filepath):
                    ext = os.path.splitext(file)[1].lower()
                    if ext in ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp4', '.avi', '.mov', '.mkv', '.txt']:
                        self.files.append(filepath)
        
        self.files.sort()
    
    def create_widgets(self):
        # Barre de titre
        titlebar = tk.Frame(self.frame, bg='#ff0000', height=50)
        titlebar.pack(fill=tk.X)
        
        title = tk.Label(
            titlebar,
            text="📂 СЕКРЕТНЫЕ ДОКУМЕНТЫ",
            font=("Arial", 18, "bold"),
            fg='white',
            bg='#ff0000'
        )
        title.pack(pady=10)
        
        # Zone de contenu
        content_frame = tk.Frame(self.frame, bg='#2a2a2a')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        if not self.files:
            # Aucun fichier
            no_files_label = tk.Label(
                content_frame,
                text="📭 Дossier vide\n\nAucun document trouvé",
                font=("Arial", 16),
                fg='#ffaa00',
                bg='#2a2a2a',
                justify=tk.CENTER
            )
            no_files_label.pack(expand=True)
        else:
            # Liste des fichiers
            list_frame = tk.Frame(content_frame, bg='#2a2a2a')
            list_frame.pack(fill=tk.BOTH, expand=True)
            
            # Titre de la liste
            list_title = tk.Label(
                list_frame,
                text=f"📋 Documents trouvés: {len(self.files)}",
                font=("Arial", 14, "bold"),
                fg='#00ff00',
                bg='#2a2a2a'
            )
            list_title.pack(pady=10)
            
            # Scrollbar et Listbox
            scroll_frame = tk.Frame(list_frame, bg='#2a2a2a')
            scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            scrollbar = tk.Scrollbar(scroll_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            self.files_listbox = tk.Listbox(
                scroll_frame,
                font=("Courier", 12),
                bg='#1a1a1a',
                fg='#00ff00',
                selectbackground='#00ff00',
                selectforeground='#000000',
                yscrollcommand=scrollbar.set,
                height=15
            )
            self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=self.files_listbox.yview)
            
            # Remplir la liste
            for filepath in self.files:
                filename = os.path.basename(filepath)
                size = os.path.getsize(filepath)
                size_str = self.format_size(size)
                self.files_listbox.insert(tk.END, f"{filename} ({size_str})")
            
            # Double-clic pour ouvrir
            self.files_listbox.bind('<Double-Button-1>', self.open_selected_file)
            
            # Bouton ouvrir
            open_button = tk.Button(
                list_frame,
                text=">> ОТКРЫТЬ ФАЙЛ",
                font=("Arial", 14, "bold"),
                bg='#0066cc',
                fg='white',
                activebackground='#0088ff',
                width=25,
                height=2,
                command=self.open_selected_file
            )
            open_button.pack(pady=10)
        
        # Bouton retour
        back_button = tk.Button(
            content_frame,
            text="← НАЗАД",
            font=("Arial", 14, "bold"),
            bg='#444444',
            fg='white',
            activebackground='#666666',
            width=25,
            height=2,
            command=self.go_back
        )
        back_button.pack(pady=20)
    
    def format_size(self, size):
        """Formate la taille du fichier"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def open_selected_file(self, event=None):
        """Ouvre le fichier sélectionné dans le bureau virtuel"""
        selection = self.files_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        filepath = self.files[index]
        ext = os.path.splitext(filepath)[1].lower()
        
        try:
            # Images
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                self.open_image(filepath)
            # PDF
            elif ext == '.pdf':
                self.open_pdf(filepath)
            # Vidéos
            elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
                self.open_video(filepath)
            # Texte
            elif ext == '.txt':
                self.open_text(filepath)
        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Невозможно открыть файл:\n{str(e)}"
            )
    
    def open_image(self, filepath):
        """Ouvre une image dans une fenêtre"""
        viewer_window = tk.Toplevel(self.master)
        viewer_window.title("🖼️ Просмотр изображения")
        viewer_window.configure(bg='#1a1a1a')
        viewer_window.attributes('-fullscreen', True)
        
        # Barre de titre
        titlebar = tk.Frame(viewer_window, bg='#ff0000', height=50)
        titlebar.pack(fill=tk.X)
        
        title = tk.Label(
            titlebar,
            text=f"🖼️ {os.path.basename(filepath)}",
            font=("Arial", 16, "bold"),
            fg='white',
            bg='#ff0000'
        )
        title.pack(pady=10)
        
        # Zone d'affichage avec scrollbars
        canvas_frame = tk.Frame(viewer_window, bg='#1a1a1a')
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg='#1a1a1a', highlightthickness=0)
        scrollbar_y = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar_x = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
        
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Charger et afficher l'image
        img = Image.open(filepath)
        # Redimensionner si trop grande
        max_width = viewer_window.winfo_screenwidth() - 100
        max_height = viewer_window.winfo_screenheight() - 200
        
        if img.width > max_width or img.height > max_height:
            ratio = min(max_width/img.width, max_height/img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo  # Garder une référence
        canvas.config(scrollregion=canvas.bbox(tk.ALL))
        
        # Bouton fermer
        close_button = tk.Button(
            viewer_window,
            text="X ЗАКРЫТЬ",
            font=("Arial", 14, "bold"),
            bg='#ff0000',
            fg='white',
            activebackground='#cc0000',
            command=viewer_window.destroy
        )
        close_button.pack(pady=10)
    
    def open_pdf(self, filepath):
        """Ouvre un PDF dans une fenêtre"""
        if not PYMUPDF_AVAILABLE:
            messagebox.showwarning(
                "Предупреждение",
                "PyMuPDF не установлен.\nУстановите: pip install PyMuPDF"
            )
            return
        
        viewer_window = tk.Toplevel(self.master)
        viewer_window.title("📄 Просмотр PDF")
        viewer_window.configure(bg='#1a1a1a')
        viewer_window.attributes('-fullscreen', True)
        
        # Barre de titre
        titlebar = tk.Frame(viewer_window, bg='#ff0000', height=50)
        titlebar.pack(fill=tk.X)
        
        title = tk.Label(
            titlebar,
            text=f"📄 {os.path.basename(filepath)}",
            font=("Arial", 16, "bold"),
            fg='white',
            bg='#ff0000'
        )
        title.pack(pady=10)
        
        # Ouvrir le PDF
        doc = fitz.open(filepath)
        current_page = [0]  # Liste pour modification dans les fonctions imbriquées
        
        # Zone d'affichage
        canvas_frame = tk.Frame(viewer_window, bg='#1a1a1a')
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg='#1a1a1a', highlightthickness=0)
        scrollbar_y = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar_x = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
        
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        def show_page(page_num):
            """Affiche une page du PDF"""
            page = doc[page_num]
            # Convertir en image
            zoom = 2  # Facteur de zoom pour meilleure qualité
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Convertir en format PIL
            img_data = pix.tobytes("ppm")
            img = Image.open(io.BytesIO(img_data))
            
            # Redimensionner si nécessaire
            max_width = viewer_window.winfo_screenwidth() - 100
            max_height = viewer_window.winfo_screenheight() - 300
            
            if img.width > max_width or img.height > max_height:
                ratio = min(max_width/img.width, max_height/img.height)
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img)
            canvas.delete("all")
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            canvas.image = photo
            canvas.config(scrollregion=canvas.bbox(tk.ALL))
            page_label.config(text=f"Страница {page_num + 1} / {len(doc)}")
        
        # Contrôles de navigation
        controls_frame = tk.Frame(viewer_window, bg='#2a2a2a')
        controls_frame.pack(fill=tk.X, pady=5)
        
        def prev_page():
            if current_page[0] > 0:
                current_page[0] -= 1
                show_page(current_page[0])
        
        def next_page():
            if current_page[0] < len(doc) - 1:
                current_page[0] += 1
                show_page(current_page[0])
        
        prev_button = tk.Button(
            controls_frame,
            text="< Предыдущая",
            font=("Arial", 12, "bold"),
            bg='#0066cc',
            fg='white',
            command=prev_page
        )
        prev_button.pack(side=tk.LEFT, padx=10)
        
        page_label = tk.Label(
            controls_frame,
            text=f"Страница 1 / {len(doc)}",
            font=("Arial", 12, "bold"),
            fg='#00ff00',
            bg='#2a2a2a'
        )
        page_label.pack(side=tk.LEFT, padx=20)
        
        next_button = tk.Button(
            controls_frame,
            text="Следующая >",
            font=("Arial", 12, "bold"),
            bg='#0066cc',
            fg='white',
            command=next_page
        )
        next_button.pack(side=tk.LEFT, padx=10)
        
        close_button = tk.Button(
            controls_frame,
            text="X ЗАКРЫТЬ",
            font=("Arial", 12, "bold"),
            bg='#ff0000',
            fg='white',
            command=lambda: [doc.close(), viewer_window.destroy()]
        )
        close_button.pack(side=tk.RIGHT, padx=10)
        
        # Afficher la première page
        show_page(0)
    
    def open_video(self, filepath):
        """Ouvre une vidéo dans une fenêtre"""
        if not OPENCV_AVAILABLE:
            messagebox.showwarning(
                "Предупреждение",
                "OpenCV не установлен.\nУстановите: pip install opencv-python"
            )
            return
        
        viewer_window = tk.Toplevel(self.master)
        viewer_window.title("🎬 Просмотр видео")
        viewer_window.configure(bg='#1a1a1a')
        viewer_window.attributes('-fullscreen', True)
        
        # Barre de titre
        titlebar = tk.Frame(viewer_window, bg='#ff0000', height=50)
        titlebar.pack(fill=tk.X)
        
        title = tk.Label(
            titlebar,
            text=f"🎬 {os.path.basename(filepath)}",
            font=("Arial", 16, "bold"),
            fg='white',
            bg='#ff0000'
        )
        title.pack(pady=10)
        
        # Zone d'affichage
        video_label = tk.Label(viewer_window, bg='#000000')
        video_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Contrôles
        controls_frame = tk.Frame(viewer_window, bg='#2a2a2a')
        controls_frame.pack(fill=tk.X, pady=5)
        
        is_playing = [True]
        video_thread = [None]
        
        def play_video():
            """Lit la vidéo"""
            cap = cv2.VideoCapture(filepath)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            delay = int(1000 / fps)
            
            while cap.isOpened() and is_playing[0]:
                ret, frame = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reboucler
                    continue
                
                # Convertir BGR vers RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                
                # Redimensionner pour l'écran
                max_width = viewer_window.winfo_screenwidth() - 100
                max_height = viewer_window.winfo_screenheight() - 250
                
                if img.width > max_width or img.height > max_height:
                    ratio = min(max_width/img.width, max_height/img.height)
                    new_size = (int(img.width * ratio), int(img.height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(img)
                
                try:
                    video_label.config(image=photo)
                    video_label.image = photo
                except:
                    break
                
                time.sleep(delay / 1000)
            
            cap.release()
        
        def toggle_play():
            """Pause/Lecture"""
            is_playing[0] = not is_playing[0]
            play_button.config(text="> Воспроизвести" if not is_playing[0] else "|| Пауза")
            
            if is_playing[0] and (video_thread[0] is None or not video_thread[0].is_alive()):
                video_thread[0] = threading.Thread(target=play_video, daemon=True)
                video_thread[0].start()
        
        play_button = tk.Button(
            controls_frame,
            text="|| Пауза",
            font=("Arial", 12, "bold"),
            bg='#0066cc',
            fg='white',
            command=toggle_play
        )
        play_button.pack(side=tk.LEFT, padx=10)
        
        close_button = tk.Button(
            controls_frame,
            text="X ЗАКРЫТЬ",
            font=("Arial", 12, "bold"),
            bg='#ff0000',
            fg='white',
            command=lambda: [is_playing.__setitem__(0, False), viewer_window.destroy()]
        )
        close_button.pack(side=tk.RIGHT, padx=10)
        
        # Démarrer la lecture
        video_thread[0] = threading.Thread(target=play_video, daemon=True)
        video_thread[0].start()
    
    def open_text(self, filepath):
        """Ouvre un fichier texte"""
        viewer_window = tk.Toplevel(self.master)
        viewer_window.title("📝 Просмотр текста")
        viewer_window.configure(bg='#1a1a1a')
        viewer_window.attributes('-fullscreen', True)
        
        # Barre de titre
        titlebar = tk.Frame(viewer_window, bg='#ff0000', height=50)
        titlebar.pack(fill=tk.X)
        
        title = tk.Label(
            titlebar,
            text=f"📝 {os.path.basename(filepath)}",
            font=("Arial", 16, "bold"),
            fg='white',
            bg='#ff0000'
        )
        title.pack(pady=10)
        
        # Zone de texte
        text_frame = tk.Frame(viewer_window, bg='#1a1a1a')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(
            text_frame,
            font=("Courier", 12),
            bg='#1a1a1a',
            fg='#00ff00',
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)
        
        # Charger le contenu
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        text_widget.insert('1.0', content)
        text_widget.config(state=tk.DISABLED)
        
        # Bouton fermer
        close_button = tk.Button(
            viewer_window,
            text="X ЗАКРЫТЬ",
            font=("Arial", 14, "bold"),
            bg='#ff0000',
            fg='white',
            command=viewer_window.destroy
        )
        close_button.pack(pady=10)
    
    def go_back(self):
        """Retour au bureau"""
        self.frame.destroy()
        self.desktop_class(self.master)
