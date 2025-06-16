#!/usr/bin/env python3
"""
Liquidsoap Library Optimizer - Versione Fixed
Script semplificato e robusto per ottimizzare librerie musicali
"""

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
    """Lancia una semplice GUI Tkinter per selezionare cartelle e avviare l'ottimizzazione"""
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
        import threading
    except ImportError:
        print("Errore: tkinter non disponibile. Usa la modalità command line.")
        return

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
    root.title('🎵 Liquidsoap Library Optimizer - Fixed')
    root.geometry('700x300')
    root.configure(bg='#f0f0f0')

    input_var = tk.StringVar()
    output_var = tk.StringVar()

    # Header
    header = tk.Label(root, text='🎵 Liquidsoap Library Optimizer', 
                      font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#333')
    header.grid(row=0, column=0, columnspan=3, pady=15)

    # Input directory
    tk.Label(root, text='📂 Cartella di input:', font=('Arial', 10, 'bold'), 
             bg='#f0f0f0').grid(row=1, column=0, sticky='w', padx=15, pady=5)
    tk.Entry(root, textvariable=input_var, width=50, font=('Arial', 9)).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text='Sfoglia', command=browse_input, bg='#2196F3', fg='white', 
              font=('Arial', 9)).grid(row=1, column=2, padx=5, pady=5)

    # Output directory
    tk.Label(root, text='💾 Cartella di output:', font=('Arial', 10, 'bold'), 
             bg='#f0f0f0').grid(row=2, column=0, sticky='w', padx=15, pady=5)
    tk.Entry(root, textvariable=output_var, width=50, font=('Arial', 9)).grid(row=2, column=1, padx=5, pady=5)
    tk.Button(root, text='Sfoglia', command=browse_output, bg='#2196F3', fg='white', 
              font=('Arial', 9)).grid(row=2, column=2, padx=5, pady=5)

    # Informazioni
    info_frame = tk.Frame(root, bg='#e8f4f8', relief='solid', bd=1)
    info_frame.grid(row=3, column=0, columnspan=3, padx=15, pady=15, sticky='ew')
    
    info_text = """ℹ️  Cosa fa questo script:
• Trova tutti i file audio nella cartella di input (MP3, FLAC, WAV, M4A, AAC, OGG)
• Copia i file MP3 già conformi (192kbps CBR, 44.1kHz) senza modifiche
• Converte tutti gli altri file al formato ottimale per Liquidsoap
• Mantiene la struttura delle cartelle nell'output"""
    
    tk.Label(info_frame, text=info_text, justify='left', bg='#e8f4f8', 
             font=('Arial', 9), fg='#555').pack(padx=10, pady=10)

    # Pulsante avvia
    start_btn = tk.Button(root, text='🚀 AVVIA ELABORAZIONE', command=start_process, 
                          bg='#4CAF50', fg='white', font=('Arial', 14, 'bold'), 
                          width=25, height=2)
    start_btn.grid(row=4, column=0, columnspan=3, pady=20)

    # Configura colonne per il resize
    root.grid_columnconfigure(1, weight=1)

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