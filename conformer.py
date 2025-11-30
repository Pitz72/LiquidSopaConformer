#!/usr/bin/env python3
"""
Audio & Metadata Converter - Premium Edition v2.0
Script professionale per ottimizzare librerie musicali per sistemi radio
Developed by Simone Pizzi with LLM assistance
"""

# Informazioni sul software
APP_NAME = "Audio & Metadata Converter"
APP_VERSION = "2.0.0"
VERSION_NAME = "Premium Edition"
AUTHOR = "Simone Pizzi"
FULL_VERSION = f"{APP_NAME} - {VERSION_NAME} v{APP_VERSION}"

import os
import sys
import logging
import argparse
from pathlib import Path
import shutil
import threading
import time
import webbrowser

# Import CustomTkinter and Locales
try:
    import customtkinter as ctk
    from PIL import Image, ImageTk
    import locales
except ImportError as e:
    print(f"Errore: Modulo mancante {e}")
    print("Installa le dipendenze con: pip install customtkinter pillow packaging")
    sys.exit(1)

try:
    import ffmpeg
except ImportError as e:
    print(f"Errore: Modulo mancante {e}")
    print("Installa le dipendenze con: pip install ffmpeg-python")
    sys.exit(1)

# Global Language Variable
CURRENT_LANG = 'IT'  # Default

def get_resource_path(relative_path):
    """Ottiene il percorso assoluto della risorsa, compatibile con PyInstaller"""
    try:
        # PyInstaller crea una cartella temporanea e memorizza il percorso in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def t(key):
    """Helper per le traduzioni"""
    return locales.TRANSLATIONS[CURRENT_LANG].get(key, key)

class SimpleConformer:
    """Versione semplificata e robusta del conformer"""
    
    SUPPORTED_FORMATS = {'.mp3', '.flac', '.wav', '.m4a', '.aac', '.ogg'}
    TARGET_SAMPLE_RATE = 44100
    TARGET_BITRATE = 192
    FFMPEG_PATH = None
    
    def __init__(self, input_dir: str, output_dir: str, progress_callback=None):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.progress_callback = progress_callback
        self.stop_requested = False
        self.stats = {
            'processed': 0,
            'copied': 0,
            'converted': 0,
            'errors': 0,
            'skipped': 0
        }
        self.FFMPEG_PATH = self._find_ffmpeg()
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[
                logging.FileHandler('conformer.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def stop(self):
        self.stop_requested = True

    def _find_ffmpeg(self) -> str:
        import subprocess
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return 'ffmpeg'
        except:
            pass
        
        if os.name == 'nt':
            common_paths = [
                r"C:\Users\Utente\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe",
                r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
                r"C:\ffmpeg\bin\ffmpeg.exe"
            ]
            for path in common_paths:
                if Path(path).exists():
                    return path
        return 'ffmpeg'
    
    def is_conforming_mp3(self, file_path: Path) -> bool:
        if file_path.suffix.lower() != '.mp3':
            return False
        try:
            probe = ffmpeg.probe(str(file_path), cmd=self.FFMPEG_PATH)
            for stream in probe['streams']:
                if stream['codec_type'] == 'audio':
                    bitrate = int(stream.get('bit_rate', 0))
                    sample_rate = int(stream.get('sample_rate', 0))
                    bitrate_ok = abs(bitrate - self.TARGET_BITRATE * 1000) < 10000
                    sample_rate_ok = sample_rate == self.TARGET_SAMPLE_RATE
                    return bitrate_ok and sample_rate_ok
            return False
        except:
            return False
    
    def safe_copy(self, src: Path, dst: Path) -> bool:
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src), str(dst))
            return True
        except Exception as e:
            self.logger.error(f"Errore copia {src.name}: {e}")
            return False
    
    def convert_to_mp3(self, src: Path, dst: Path) -> bool:
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
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
        try:
            rel_path = file_path.relative_to(self.input_dir)
            output_path = self.output_dir / rel_path.with_suffix('.mp3')
            
            if output_path.exists():
                self.stats['skipped'] += 1
                return True
            
            if file_path.suffix.lower() not in self.SUPPORTED_FORMATS:
                self.stats['skipped'] += 1
                return True
            
            if self.is_conforming_mp3(file_path):
                if self.safe_copy(file_path, output_path):
                    self.stats['copied'] += 1
                    self.stats['processed'] += 1
                    return True
                else:
                    self.stats['errors'] += 1
                    return False
            
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
        self.logger.info("=== INIZIO ELABORAZIONE ===")
        all_files = list(self.input_dir.rglob("*"))
        audio_files = [f for f in all_files if f.is_file() and f.suffix.lower() in self.SUPPORTED_FORMATS]
        total_files = len(audio_files)
        
        for i, file_path in enumerate(audio_files, 1):
            if self.stop_requested:
                break
            self.process_single_file(file_path)
            if self.progress_callback:
                self.progress_callback(i, total_files, file_path.name)

class LanguageSelectionDialog(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Language Selection")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Center window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 300) // 2
        self.geometry(f"400x300+{x}+{y}")
        
        # Icon
        try:
            icon_path = get_resource_path("audioconv.png")
            if Path(icon_path).exists():
                self.iconbitmap(icon_path) # Windows only usually
                img = Image.open(icon_path)
                self.iconphoto(False, ImageTk.PhotoImage(img))
        except:
            pass

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(self, text="Select Language / Seleziona Lingua", 
                     font=("Roboto", 18, "bold")).grid(row=0, column=0, pady=20)

        ctk.CTkButton(self, text="🇮🇹 Italiano", 
                      command=lambda: self.set_lang('IT'),
                      font=("Roboto", 14), height=40).grid(row=1, column=0, pady=10, padx=50, sticky="ew")

        ctk.CTkButton(self, text="🇬🇧 English", 
                      command=lambda: self.set_lang('EN'),
                      font=("Roboto", 14), height=40).grid(row=2, column=0, pady=10, padx=50, sticky="ew")
        
        self.lang_selected = None

    def set_lang(self, lang):
        self.lang_selected = lang
        self.destroy()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration
        self.title(f"{t('app_title')} - {t('version_name')} v{APP_VERSION}")
        self.geometry("800x700")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Icon
        try:
            icon_path = get_resource_path("audioconv.png")
            if Path(icon_path).exists():
                self.iconbitmap(icon_path)
                self.icon_image = ctk.CTkImage(Image.open(icon_path), size=(40, 40))
                self.large_icon = ctk.CTkImage(Image.open(icon_path), size=(100, 100))
            else:
                self.icon_image = None
                self.large_icon = None
        except:
            self.icon_image = None
            self.large_icon = None

        # Variables
        self.input_path = ctk.StringVar()
        self.output_path = ctk.StringVar()
        self.status_text = ctk.StringVar(value=t('status_ready'))
        self.current_conformer = None

        self.setup_ui()

    def setup_ui(self):
        # Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=1) # Content
        self.grid_rowconfigure(2, weight=0) # Footer

        # === Header ===
        header_frame = ctk.CTkFrame(self, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew")
        
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(pady=10)
        
        if self.icon_image:
            ctk.CTkLabel(header_content, image=self.icon_image, text="").pack(side="left", padx=10)
            
        ctk.CTkLabel(header_content, text=t('app_title'), font=("Roboto", 20, "bold")).pack(side="left")
        ctk.CTkLabel(header_content, text=f"v{APP_VERSION}", font=("Roboto", 12), text_color="gray").pack(side="left", padx=5, pady=(5,0))

        # === Main Content ===
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Input Section
        ctk.CTkLabel(main_frame, text=t('input_folder'), font=("Roboto", 14, "bold")).pack(anchor="w", pady=(0, 5))
        input_row = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_row.pack(fill="x", pady=(0, 15))
        
        ctk.CTkEntry(input_row, textvariable=self.input_path, placeholder_text="C:/Music/Input").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(input_row, text=t('browse'), width=100, command=self.browse_input).pack(side="right")

        # Output Section
        ctk.CTkLabel(main_frame, text=t('output_folder'), font=("Roboto", 14, "bold")).pack(anchor="w", pady=(0, 5))
        output_row = ctk.CTkFrame(main_frame, fg_color="transparent")
        output_row.pack(fill="x", pady=(0, 20))
        
        ctk.CTkEntry(output_row, textvariable=self.output_path, placeholder_text="C:/Music/Output").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(output_row, text=t('browse'), width=100, command=self.browse_output).pack(side="right")

        # Info Card
        info_card = ctk.CTkFrame(main_frame)
        info_card.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(info_card, text=f"ℹ️ {t('info_title')}", font=("Roboto", 14, "bold")).pack(anchor="w", padx=15, pady=(10, 5))
        ctk.CTkLabel(info_card, text=t('info_text'), justify="left", font=("Roboto", 12)).pack(anchor="w", padx=15, pady=(0, 15))

        # Progress Section
        self.status_label = ctk.CTkLabel(main_frame, textvariable=self.status_text, anchor="w", text_color="gray")
        self.status_label.pack(fill="x", pady=(0, 5))
        
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.pack(fill="x", pady=(0, 20))
        self.progress_bar.set(0)

        # Action Buttons
        action_row = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_row.pack(pady=10)
        
        self.start_btn = ctk.CTkButton(action_row, text=t('start_process'), 
                                     command=self.start_process,
                                     font=("Roboto", 16, "bold"),
                                     height=50, width=200,
                                     fg_color="#2ecc71", hover_color="#27ae60")
        self.start_btn.pack(side="left", padx=10)
        
        self.stop_btn = ctk.CTkButton(action_row, text=t('stop_process'), 
                                    command=self.stop_process,
                                    font=("Roboto", 16, "bold"),
                                    height=50, width=100,
                                    fg_color="#e74c3c", hover_color="#c0392b",
                                    state="disabled")
        self.stop_btn.pack(side="left", padx=10)

        # === Footer ===
        footer_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a1a")
        footer_frame.grid(row=2, column=0, sticky="ew")
        
        ctk.CTkLabel(footer_frame, text=f"{t('developed_by')} {AUTHOR} | {t('llm_credit')}", 
                     font=("Roboto", 10), text_color="gray").pack(pady=5)
        
        ctk.CTkButton(footer_frame, text=f"💝 {t('donate_btn')}", 
                      command=lambda: webbrowser.open('https://paypal.me/runtimeradio'),
                      fg_color="transparent", border_width=1, border_color="#f39c12",
                      text_color="#f39c12", hover_color="#2c2c2c", height=25).pack(pady=(0, 10))

    def browse_input(self):
        path = ctk.filedialog.askdirectory()
        if path:
            self.input_path.set(path)

    def browse_output(self):
        path = ctk.filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def update_progress_safe(self, current, total, filename):
        progress = current / total
        self.progress_bar.set(progress)
        self.status_text.set(t('status_processing').format(filename=filename, current=current, total=total))

    def start_process(self):
        in_dir = self.input_path.get()
        out_dir = self.output_path.get()
        
        if not in_dir or not out_dir:
            ctk.filedialog.showerror(t('error_title'), t('error_input_output'))
            return
            
        if not Path(in_dir).exists():
            ctk.filedialog.showerror(t('error_title'), t('error_input_not_found').format(path=in_dir))
            return

        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.status_text.set(t('status_ready'))

        def worker():
            try:
                self.current_conformer = SimpleConformer(
                    in_dir, out_dir, 
                    progress_callback=lambda c, t, f: self.after(0, self.update_progress_safe, c, t, f)
                )
                self.current_conformer.run()
                
                if self.current_conformer.stop_requested:
                    self.after(0, lambda: self.status_text.set(t('status_stopped')))
                    self.after(0, lambda: ctk.filedialog.showinfo("Info", t('status_stopped')))
                else:
                    self.after(0, lambda: self.status_text.set(t('status_completed')))
                    stats = self.current_conformer.stats
                    msg = t('success_body').format(
                        processed=stats['processed'],
                        copied=stats['copied'],
                        converted=stats['converted'],
                        skipped=stats['skipped'],
                        errors=stats['errors'],
                        out_dir=out_dir
                    )
                    self.after(0, lambda: ctk.filedialog.showinfo(t('success_title'), msg))
                    
            except Exception as e:
                self.after(0, lambda: ctk.filedialog.showerror(t('error_title'), str(e)))
            finally:
                self.after(0, self.reset_ui)

        threading.Thread(target=worker, daemon=True).start()

    def stop_process(self):
        if self.current_conformer:
            self.current_conformer.stop()
            self.status_text.set(t('status_stopping'))
            self.stop_btn.configure(state="disabled")

    def reset_ui(self):
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.current_conformer = None

def main():
    global CURRENT_LANG
    
    # Parse args for CLI usage
    parser = argparse.ArgumentParser(description='Audio & Metadata Converter')
    parser.add_argument('input_dir', nargs='?', help='Input Directory')
    parser.add_argument('output_dir', nargs='?', help='Output Directory')
    parser.add_argument('--gui', action='store_true', help='Force GUI')
    args = parser.parse_args()

    # If CLI args provided, run headless
    if args.input_dir and args.output_dir and not args.gui:
        if not Path(args.input_dir).exists():
            print(f"Error: {args.input_dir} not found")
            sys.exit(1)
        conformer = SimpleConformer(args.input_dir, args.output_dir)
        conformer.run()
        return

    # GUI Mode
    
    # 1. Language Selection
    lang_dialog = LanguageSelectionDialog()
    lang_dialog.mainloop()
    
    if not lang_dialog.lang_selected:
        sys.exit(0) # User closed dialog
        
    CURRENT_LANG = lang_dialog.lang_selected
    
    # 2. Main App
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()