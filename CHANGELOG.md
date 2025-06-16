# Changelog

Tutte le modifiche notevoli a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it-IT/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/lang/it/).

## [1.0.0] - 2024-12-16

### ✨ Aggiunto
- **Interfaccia grafica** completa con Tkinter per facilità d'uso
- **Riconoscimento automatico** di file MP3 già conformi (192kbps CBR, 44.1kHz)
- **Conversione intelligente** di file audio in formati multipli (MP3, FLAC, WAV, M4A, AAC, OGG)
- **Preservazione struttura cartelle** dall'input all'output
- **Logging dettagliato** con file `conformer_fixed.log`
- **Gestione robusta degli errori** con recupero automatico
- **Statistiche elaborate** al completamento dell'elaborazione
- **Supporto completo FFmpeg** con percorso automatico su Windows
- **Documentazione completa** con README, requirements, licenza

### 🔧 Tecnico
- Formato target ottimizzato per Liquidsoap/AzuraCast
- Elaborazione sequenziale per massima stabilità
- Validazione input/output completa
- Gestione metadati ID3v2.3 puliti
- Ottimizzazione artwork per streaming

### 🛠️ Risolto
- Problemi di concorrenza con multithreading rimosso
- Errori `[WinError 2]` per file non trovati
- Gestione percorsi file lunghi su Windows
- Compatibilità FFmpeg cross-platform
- Memory management per file di grandi dimensioni

### 📋 Formati Supportati
- **Input**: MP3, FLAC, WAV, M4A, AAC, OGG
- **Output**: MP3 192kbps CBR, 44.1kHz, Stereo

### 🎯 Performance
- Elaborazione sequenziale ottimizzata
- Gestione memoria efficiente
- Progress reporting ogni 50 file
- Log dettagliati per debugging

---

### Note per Sviluppatori

#### Architettura
- **SimpleConformer**: Classe principale per elaborazione
- **launch_gui()**: Interfaccia grafica Tkinter
- **Logging robusto**: File log con timestamp dettagliati

#### Testing
- ✅ Testato su oltre 6.800 file MP3
- ✅ Gestione errori verificata
- ✅ Performance ottimizzate
- ✅ Compatibilità Windows confermata

#### Dipendenze
- Python 3.7+
- mutagen >= 1.47.0
- ffmpeg-python >= 0.2.0
- Pillow >= 10.0.0
- FFmpeg (installazione di sistema)

---

*Per vedere tutte le modifiche: [Confronta versioni](https://github.com/tuonome/LiquidSopaConformer/compare)* 