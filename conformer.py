#!/usr/bin/env python3
"""
Audio & Metadata Converter - Harmony Edition v1.0
Script professionale per ottimizzare librerie musicali per sistemi radio
Developed by Simone Pizzi with LLM assistance
"""

# Informazioni sul software
APP_NAME = "Audio & Metadata Converter"
APP_VERSION = "1.0"
VERSION_NAME = "Harmony Edition"
AUTHOR = "Simone Pizzi"
FULL_VERSION = f"{APP_NAME} - {VERSION_NAME} v{APP_VERSION}"

import os
import sys
import json
import logging
import argparse
from pathlib import Path
import shutil

try:
    import ffmpeg
    import mutagen
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, APIC
    from mutagen.flac import FLAC
    from PIL import Image
    import io
except ImportError as e:
    print(f"Errore: Modulo mancante {e}")
    print("Installa le dipendenze con: pip install mutagen ffmpeg-python pillow")
    sys.exit(1)

class SimpleConformer:
    """Versione semplificata e robusta del conformer"""
    
    SUPPORTED_FORMATS = {'.mp3', '.flac', '.wav', '.m4a', '.aac', '.ogg'}
    TARGET_SAMPLE_RATE = 44100
    TARGET_BITRATE = 192
    # Percorso FFmpeg - auto-detection
    FFMPEG_PATH = None  # Verrà configurato automaticamente in __init__
    
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.stats = {
            'processed': 0,
            'copied': 0,
            'converted': 0,
            'errors': 0,
            'skipped': 0
        }
        
        # Auto-detection del percorso FFmpeg
        self.FFMPEG_PATH = self._find_ffmpeg()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[
                logging.FileHandler('conformer.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _find_ffmpeg(self) -> str:
        """Auto-detection del percorso FFmpeg"""
        import subprocess
        
        # Prova prima con 'ffmpeg' nel PATH
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return 'ffmpeg'
        except:
            pass
        
        # Su Windows, cerca nelle location comuni di WinGet
        if os.name == 'nt':
            common_paths = [
                r"C:\Users\Utente\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe",
                r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
                r"C:\ffmpeg\bin\ffmpeg.exe"
            ]
            
            for path in common_paths:
                if Path(path).exists():
                    return path
        
        # Fallback
        return 'ffmpeg'
    
    def is_conforming_mp3(self, file_path: Path) -> bool:
        """Verifica se un MP3 è già conforme"""
        if file_path.suffix.lower() != '.mp3':
            return False
        
        try:
            # Usa un approccio più semplice e sicuro
            probe = ffmpeg.probe(str(file_path), cmd=self.FFMPEG_PATH)
            for stream in probe['streams']:
                if stream['codec_type'] == 'audio':
                    bitrate = int(stream.get('bit_rate', 0))
                    sample_rate = int(stream.get('sample_rate', 0))
                    
                    # Verifica parametri
                    bitrate_ok = abs(bitrate - self.TARGET_BITRATE * 1000) < 10000
                    sample_rate_ok = sample_rate == self.TARGET_SAMPLE_RATE
                    
                    return bitrate_ok and sample_rate_ok
            return False
        except:
            return False
    
    def safe_copy(self, src: Path, dst: Path) -> bool:
        """Copia sicura di un file"""
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src), str(dst))
            return True
        except Exception as e:
            self.logger.error(f"Errore copia {src.name}: {e}")
            return False
    
    def convert_to_mp3(self, src: Path, dst: Path) -> bool:
        """Converte un file audio in MP3 conforme"""
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            
            # Conversione con ffmpeg
            stream = ffmpeg.input(str(src))
            stream = ffmpeg.output(
                stream, str(dst),
                acodec='libmp3lame',
                audio_bitrate=f'{self.TARGET_BITRATE}k',
                ar=self.TARGET_SAMPLE_RATE,
                ac=2
            )
            ffmpeg.run(stream, overwrite_output=True, quiet=True, cmd=self.FFMPEG_PATH)
            return True
        except Exception as e:
            self.logger.error(f"Errore conversione {src.name}: {e}")
            return False
    
    def process_single_file(self, file_path: Path) -> bool:
        """Processa un singolo file"""
        try:
            # Calcola percorso output
            rel_path = file_path.relative_to(self.input_dir)
            output_path = self.output_dir / rel_path.with_suffix('.mp3')
            
            # Skip se già esiste
            if output_path.exists():
                self.stats['skipped'] += 1
                return True
            
            # Se non è un formato supportato, salta
            if file_path.suffix.lower() not in self.SUPPORTED_FORMATS:
                self.stats['skipped'] += 1
                return True
            
            # Se è MP3 conforme, copia
            if self.is_conforming_mp3(file_path):
                if self.safe_copy(file_path, output_path):
                    self.stats['copied'] += 1
                    self.stats['processed'] += 1
                    return True
                else:
                    self.stats['errors'] += 1
                    return False
            
            # Altrimenti converti
            if self.convert_to_mp3(file_path, output_path):
                self.stats['converted'] += 1
                self.stats['processed'] += 1
                return True
            else:
                self.stats['errors'] += 1
                return False
                
        except Exception as e:
            self.logger.error(f"Errore generale su {file_path.name}: {e}")
            self.stats['errors'] += 1
            return False
    
    def run(self):
        """Esegue l'elaborazione completa"""
        self.logger.info("=== INIZIO ELABORAZIONE ===")
        self.logger.info(f"Input: {self.input_dir}")
        self.logger.info(f"Output: {self.output_dir}")
        
        # Trova tutti i file
        all_files = list(self.input_dir.rglob("*"))
        audio_files = [f for f in all_files if f.is_file() and f.suffix.lower() in self.SUPPORTED_FORMATS]
        
        self.logger.info(f"File audio trovati: {len(audio_files)}")
        
        # Processa file uno alla volta
        for i, file_path in enumerate(audio_files, 1):
            self.logger.info(f"[{i}/{len(audio_files)}] {file_path.name}")
            self.process_single_file(file_path)
            
            # Progress ogni 50 file
            if i % 50 == 0:
                self.logger.info(f"Progresso: {i}/{len(audio_files)} - Errori: {self.stats['errors']}")
        
        # Report finale
        self.logger.info("=== ELABORAZIONE COMPLETATA ===")
        self.logger.info(f"File processati: {self.stats['processed']}")
        self.logger.info(f"File copiati (conformi): {self.stats['copied']}")
        self.logger.info(f"File convertiti: {self.stats['converted']}")
        self.logger.info(f"File saltati: {self.stats['skipped']}")
        self.logger.info(f"Errori: {self.stats['errors']}")

def launch_gui():
    """Lancia una GUI elegante con schermata di introduzione"""
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
        import threading
        import webbrowser
    except ImportError:
        print("Errore: tkinter non disponibile. Usa la modalità command line.")
        return

    def show_splash_screen():
        """Mostra la schermata di introduzione"""
        splash = tk.Toplevel()
        splash.title(f"{APP_NAME} - {VERSION_NAME}")
        splash.geometry('500x700')
        splash.configure(bg='#1e1e1e')
        splash.resizable(False, False)
        
        # Centra la finestra
        splash.update_idletasks()
        x = (splash.winfo_screenwidth() // 2) - (500 // 2)
        y = (splash.winfo_screenheight() // 2) - (700 // 2)
        splash.geometry(f'500x700+{x}+{y}')
        
        # Frame principale con gradiente simulato
        main_frame = tk.Frame(splash, bg='#1e1e1e')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Icona del software
        try:
            icon_path = r"C:\Users\Utente\Documents\GitHub\LiquidSopaConformer\audioconv.png"
            if Path(icon_path).exists():
                from PIL import Image, ImageTk
                img = Image.open(icon_path)
                img = img.resize((80, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                icon_label = tk.Label(main_frame, image=photo, bg='#1e1e1e')
                icon_label.image = photo  # Mantieni riferimento
                icon_label.pack(pady=(10, 20))
            else:
                raise FileNotFoundError("File icona non trovato")
        except Exception as e:
            # Fallback se l'icona non è disponibile
            print(f"Icona non caricata: {e}")
            icon_label = tk.Label(main_frame, text='🎵', font=('Arial', 48), 
                                bg='#1e1e1e', fg='#6a9cff')
            icon_label.pack(pady=(10, 20))
        
        # Nome del software
        title_label = tk.Label(main_frame, text=APP_NAME, 
                              font=('Segoe UI', 24, 'bold'), 
                              bg='#1e1e1e', fg='#ffffff')
        title_label.pack(pady=(0, 5))
        
        # Versione
        version_label = tk.Label(main_frame, text=f"{VERSION_NAME} v{APP_VERSION}", 
                                font=('Segoe UI', 12), 
                                bg='#1e1e1e', fg='#6a9cff')
        version_label.pack(pady=(0, 20))
        
        # Separatore elegante
        separator = tk.Frame(main_frame, height=2, bg='#6a9cff')
        separator.pack(fill='x', pady=(0, 20))
        
        # Autore
        author_label = tk.Label(main_frame, text=f"Sviluppato da {AUTHOR}", 
                               font=('Segoe UI', 11, 'bold'), 
                               bg='#1e1e1e', fg='#ffffff')
        author_label.pack(pady=(0, 5))
        
        # LLM assistance
        llm_label = tk.Label(main_frame, text="Sviluppatore tramite LLM", 
                            font=('Segoe UI', 10, 'italic'), 
                            bg='#1e1e1e', fg='#cccccc')
        llm_label.pack(pady=(0, 20))
        
        # Info software gratuito
        free_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='solid', bd=1)
        free_frame.pack(fill='x', pady=(0, 15), padx=10)
        
        free_label = tk.Label(free_frame, 
                             text="✨ Software gratuito e liberamente scaricabile ✨", 
                             font=('Segoe UI', 11, 'bold'), 
                             bg='#2d2d2d', fg='#4caf50')
        free_label.pack(pady=10)
        
        # Info donazioni
        donation_frame = tk.Frame(main_frame, bg='#2d2d2d', relief='solid', bd=1)
        donation_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        donation_text = ("Anche se sviluppato con LLM, questo software\n"
                        "richiede impegno mentale e ore di lavoro.\n\n"
                        "Considera una piccola donazione per\n"
                        "sostenere Runtime Radio:")
        
        donation_label = tk.Label(donation_frame, text=donation_text, 
                                 font=('Segoe UI', 10), 
                                 bg='#2d2d2d', fg='#ffffff', justify='center')
        donation_label.pack(pady=(10, 5))
        
        def open_donation():
            webbrowser.open('https://paypal.me/runtimeradio')
        
        donation_btn = tk.Button(donation_frame, text='💝 Dona a Runtime Radio', 
                               command=open_donation,
                               bg='#ff9800', fg='white', 
                               font=('Segoe UI', 10, 'bold'),
                               cursor='hand2', relief='flat',
                               padx=20, pady=5)
        donation_btn.pack(pady=(0, 10))
        
        # Pulsante per avviare il software
        def start_main_app():
            splash.destroy()
            show_main_window()
        
        start_button = tk.Button(main_frame, text='🚀 AVVIA SOFTWARE', 
                               command=start_main_app,
                               bg='#6a9cff', fg='white', 
                               font=('Segoe UI', 14, 'bold'),
                               cursor='hand2', relief='flat',
                               width=25, height=2)
        start_button.pack(pady=20)
        
        # Footer
        footer_label = tk.Label(main_frame, text=f"{FULL_VERSION}", 
                               font=('Segoe UI', 8), 
                               bg='#1e1e1e', fg='#666666')
        footer_label.pack(side='bottom', pady=(20, 0))
        
        splash.transient()
        splash.grab_set()
        splash.focus_set()
    
    def show_main_window():
        """Mostra la finestra principale"""
        def browse_input():
            path = filedialog.askdirectory(title='Seleziona cartella di input')
            if path:
                input_var.set(path)

        def browse_output():
            path = filedialog.askdirectory(title='Seleziona cartella di output')
            if path:
                output_var.set(path)

        def start_process():
            in_dir = input_var.get()
            out_dir = output_var.get()
            if not in_dir or not out_dir:
                messagebox.showerror('Errore', 'Seleziona sia la cartella di input sia quella di output')
                return

            if not Path(in_dir).exists():
                messagebox.showerror('Errore', f'Directory input non esiste: {in_dir}')
                return

            def worker():
                try:
                    conformer = SimpleConformer(in_dir, out_dir)
                    conformer.run()
                    
                    report = f"""✅ Elaborazione completata!

📊 STATISTICHE:
• File processati: {conformer.stats['processed']}
• File copiati (già conformi): {conformer.stats['copied']}
• File convertiti: {conformer.stats['converted']}
• File saltati: {conformer.stats['skipped']}
• Errori: {conformer.stats['errors']}

📁 Output salvato in: {out_dir}"""
                    
                    messagebox.showinfo('🎉 Completato!', report)
                except Exception as exc:
                    messagebox.showerror('❌ Errore', f'Errore durante elaborazione:\n\n{str(exc)}')

            # Avvia elaborazione in thread separato
            threading.Thread(target=worker, daemon=True).start()
            messagebox.showinfo('🚀 Avviato', 'Elaborazione avviata!\n\nVerrà mostrato un messaggio al completamento.\nPuoi controllare il progresso nel terminale.')

        root = tk.Tk()
        root.title(f'{APP_NAME} - {VERSION_NAME} v{APP_VERSION}')
        root.geometry('750x550')
        root.configure(bg='#1e1e1e')

        input_var = tk.StringVar()
        output_var = tk.StringVar()

        # Stile moderno
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dark.TEntry', 
                       fieldbackground='#2d2d2d', 
                       foreground='#ffffff',
                       bordercolor='#6a9cff',
                       insertcolor='#ffffff')

        # Header compatto ed elegante
        header_frame = tk.Frame(root, bg='#2d2d2d', height=50)
        header_frame.pack(fill='x', padx=20, pady=(15, 10))
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text=f'🎵 {APP_NAME}', 
                               font=('Segoe UI', 14, 'bold'), 
                               bg='#2d2d2d', fg='#6a9cff')
        header_label.pack(expand=True)

        # Contenuto principale
        content_frame = tk.Frame(root, bg='#1e1e1e')
        content_frame.pack(fill='both', expand=True, padx=20, pady=5)

        # Input directory
        input_frame = tk.Frame(content_frame, bg='#1e1e1e')
        input_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(input_frame, text='📂 Cartella di input:', 
                font=('Segoe UI', 11, 'bold'), 
                bg='#1e1e1e', fg='#ffffff').pack(anchor='w', pady=(0, 5))
        
        input_row = tk.Frame(input_frame, bg='#1e1e1e')
        input_row.pack(fill='x')
        
        input_entry = tk.Entry(input_row, textvariable=input_var, 
                              font=('Segoe UI', 10), bg='#2d2d2d', 
                              fg='#ffffff', insertbackground='#ffffff',
                              relief='flat', bd=5)
        input_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        input_btn = tk.Button(input_row, text='Sfoglia', command=browse_input, 
                             bg='#6a9cff', fg='white', font=('Segoe UI', 10, 'bold'),
                             relief='flat', cursor='hand2', padx=20)
        input_btn.pack(side='right')

        # Output directory
        output_frame = tk.Frame(content_frame, bg='#1e1e1e')
        output_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(output_frame, text='💾 Cartella di output:', 
                font=('Segoe UI', 11, 'bold'), 
                bg='#1e1e1e', fg='#ffffff').pack(anchor='w', pady=(0, 5))
        
        output_row = tk.Frame(output_frame, bg='#1e1e1e')
        output_row.pack(fill='x')
        
        output_entry = tk.Entry(output_row, textvariable=output_var, 
                               font=('Segoe UI', 10), bg='#2d2d2d', 
                               fg='#ffffff', insertbackground='#ffffff',
                               relief='flat', bd=5)
        output_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        output_btn = tk.Button(output_row, text='Sfoglia', command=browse_output, 
                              bg='#6a9cff', fg='white', font=('Segoe UI', 10, 'bold'),
                              relief='flat', cursor='hand2', padx=20)
        output_btn.pack(side='right')

        # Informazioni
        info_frame = tk.Frame(content_frame, bg='#2d2d2d', relief='solid', bd=1)
        info_frame.pack(fill='x', pady=(0, 15))
        
        info_text = """ℹ️  Funzionalità del convertitore:
• Trova tutti i file audio nella cartella di input (MP3, FLAC, WAV, M4A, AAC, OGG)
• Copia i file MP3 già conformi (192kbps CBR, 44.1kHz) senza modifiche
• Converte tutti gli altri file al formato ottimale per sistemi radio
• Mantiene la struttura delle cartelle nell'output"""
        
        tk.Label(info_frame, text=info_text, justify='left', 
                bg='#2d2d2d', fg='#cccccc',
                font=('Segoe UI', 9)).pack(padx=12, pady=12)

        # Pulsante avvia
        start_btn = tk.Button(content_frame, text='🚀 AVVIA ELABORAZIONE', 
                             command=start_process, 
                             bg='#4caf50', fg='white', 
                             font=('Segoe UI', 13, 'bold'), 
                             relief='flat', cursor='hand2',
                             width=30, height=2)
        start_btn.pack(pady=(15, 25))

        root.mainloop()

    # Avvia con schermata di introduzione
    root = tk.Tk()
    root.withdraw()  # Nascondi finestra principale
    show_splash_screen()
    root.mainloop()

def main():
    parser = argparse.ArgumentParser(description='Conformer semplificato per Liquidsoap')
    parser.add_argument('input_dir', nargs='?', help='Directory di input')
    parser.add_argument('output_dir', nargs='?', help='Directory di output')
    parser.add_argument('--gui', action='store_true', help='Avvia interfaccia grafica')
    
    args = parser.parse_args()
    
    # Se richiesto GUI o mancano argomenti, avvia GUI
    if args.gui or not args.input_dir or not args.output_dir:
        launch_gui()
        return
    
    if not Path(args.input_dir).exists():
        print(f"Errore: Directory input {args.input_dir} non esiste")
        sys.exit(1)
    
    conformer = SimpleConformer(args.input_dir, args.output_dir)
    conformer.run()

if __name__ == '__main__':
    main() 