# 🔧 Come Funziona Audio & Metadata Converter

**Guida tecnica completa al funzionamento del convertitore audio professionale**

## 🎯 Panoramica del Processo

Audio & Metadata Converter utilizza un algoritmo di elaborazione intelligente che ottimizza le librerie musicali attraverso un processo in 4 fasi principali:

```
📁 INPUT → 🔍 ANALISI → ⚡ ELABORAZIONE → 📁 OUTPUT
```

## 🔍 Fase 1: Scansione e Analisi

### 📋 **Rilevamento File**
1. **Scansione ricorsiva** di tutte le cartelle nella directory di input
2. **Identificazione formati** supportati tramite estensione file
3. **Catalogazione struttura** cartelle per preservazione layout

### 🎵 **Formati Riconosciuti**
- `.mp3` - MPEG Audio Layer 3
- `.flac` - Free Lossless Audio Codec
- `.wav` - Waveform Audio File Format
- `.m4a` - MPEG-4 Audio
- `.aac` - Advanced Audio Coding
- `.ogg` - Ogg Vorbis

### 📊 **Analisi Tecnica MP3**
Per ogni file MP3 esistente, il software verifica:
- **Bitrate**: Deve essere esattamente 192 kbps
- **Tipo encoding**: Deve essere CBR (Constant Bit Rate)
- **Sample Rate**: Deve essere 44.1 kHz
- **Canali**: Deve essere stereo (2 canali)

## ⚡ Fase 2: Classificazione Intelligente

### ✅ **File Conformi (COPIA)**
File MP3 che **già rispettano** tutti i parametri target:
```
Input:  song.mp3 (192kbps CBR, 44.1kHz, stereo)
Azione: COPIA DIRETTA (velocissima)
Output: song.mp3 (identico)
```

### 🔄 **File Non Conformi (CONVERSIONE)**
Tutti gli altri file audio vengono convertiti:
```
Input:  song.flac (lossless, 48kHz)
Azione: CONVERSIONE FFmpeg
Output: song.mp3 (192kbps CBR, 44.1kHz, stereo)
```

### 🚫 **File Non Audio (IGNORATI)**
File che non sono audio vengono completamente ignorati:
```
Input:  readme.txt, cover.jpg, .DS_Store
Azione: IGNORA
Output: (nessun output)
```

## 🔧 Fase 3: Elaborazione Tecnica

### 🎛️ **Engine di Conversione: FFmpeg**
Il software utilizza **FFmpeg**, lo standard industriale per:
- **Decodifica**: Lettura di tutti i formati input
- **Processamento**: Conversione con parametri precisi
- **Encoding**: Creazione MP3 con qualità professionale

### ⚙️ **Parametri di Conversione**
```bash
# Comando FFmpeg utilizzato internamente:
ffmpeg -i input_file -acodec libmp3lame -ab 192k -ar 44100 -ac 2 output_file.mp3
```

**Spiegazione parametri:**
- `-acodec libmp3lame`: Usa encoder MP3 LAME (massima qualità)
- `-ab 192k`: Bitrate 192 kbps (ottimale radio/streaming)
- `-ar 44100`: Sample rate 44.1 kHz (standard CD)
- `-ac 2`: 2 canali audio (stereo)

### 📁 **Preservazione Struttura**
```
INPUT/
├── Rock/
│   ├── Band A/
│   │   └── song1.flac
│   └── song2.wav
└── Pop/
    └── hit.m4a

OUTPUT/
├── Rock/
│   ├── Band A/
│   │   └── song1.mp3  [convertito]
│   └── song2.mp3      [convertito]
└── Pop/
    └── hit.mp3         [convertito]
```

## 📊 Fase 4: Output e Reportistica

### 📈 **Statistiche Elaborate**
Il software traccia e reporta:
- **File processati**: Totale file audio elaborati
- **File copiati**: MP3 già conformi (nessuna conversione)
- **File convertiti**: File trasformati nel formato target
- **File saltati**: File già esistenti nell'output
- **Errori**: Problemi durante l'elaborazione

### 📝 **Sistema di Logging**
Ogni operazione viene registrata in `conformer.log`:
```
2024-12-20 15:30:01 - [INFO] Inizio elaborazione
2024-12-20 15:30:02 - [INFO] File conformi trovati: 150
2024-12-20 15:30:02 - [INFO] File da convertire: 45
2024-12-20 15:30:15 - [INFO] Conversione completata: song.flac → song.mp3
2024-12-20 15:32:01 - [INFO] Elaborazione terminata - 0 errori
```

## 🧠 Logica di Decisione Avanzata

### 🔀 **Algoritmo di Routing**

```python
for ogni_file_audio:
    if file.estensione == ".mp3":
        if è_conforme(file):
            → COPIA_DIRETTA(file)
        else:
            → CONVERTI(file)
    else:
        → CONVERTI(file)
```

### ⚡ **Ottimizzazioni Performance**

1. **Skip Files Esistenti**: Non riprocessa file già nell'output
2. **Copia Zero-Copy**: File conformi copiati a livello filesystem
3. **Validazione Preventiva**: Verifica spazio disco prima di iniziare
4. **Processing Sequenziale**: Evita race condition e conflitti

## 🛡️ Sicurezza e Robustezza

### 🔒 **Protezioni Implementate**

- **Non-Modifica Originali**: Input directory mai toccata
- **Validazione Path**: Controllo caratteri speciali e lunghezza
- **Error Recovery**: Continua elaborazione anche con singoli errori
- **Atomic Operations**: Ogni file completato prima di passare al successivo

### 🚨 **Gestione Errori**

```
File corrotto/inaccessibile:
├── Log dell'errore specifico
├── Incremento contatore errori
├── Continua con file successivo
└── Report finale con dettagli
```

## ⚙️ Auto-Detection FFmpeg

### 🔍 **Ricerca Automatica**
Il software cerca FFmpeg in:

**Windows:**
1. `ffmpeg` nel PATH di sistema
2. Installazione WinGet: `C:\Users\...\WinGet\Packages\Gyan.FFmpeg\...`
3. Installazioni manuali comuni

**macOS:**
1. `ffmpeg` nel PATH
2. Homebrew: `/usr/local/bin/ffmpeg`
3. `/opt/homebrew/bin/ffmpeg` (Apple Silicon)

**Linux:**
1. `ffmpeg` nel PATH
2. `/usr/bin/ffmpeg` (package manager)
3. `/usr/local/bin/ffmpeg` (compilazione manuale)

## 📱 Interfaccia Utente

### 🖥️ **GUI Flow**

```
Splash Screen
├── Verifica dipendenze
├── Mostra crediti/info
└── [Avvia Software] → Main Window
                         ├── Seleziona Input
                         ├── Seleziona Output
                         └── [Avvia Elaborazione]
                             ├── Progress in tempo reale
                             └── Report finale
```

### 📊 **Feedback Real-time**
- **Progress Counter**: File X di Y elaborati
- **Status Updates**: Ogni 50 file processati
- **Error Notifications**: Alert immediati per problemi
- **Final Report**: Statistiche complete al termine

## 🔄 Flusso Completo Esempio

### 📂 **Scenario Tipico:**
```
INPUT: Libreria 1000 file (800 MP3 + 200 FLAC)
│
├── Scansione: 2 secondi
├── Analisi MP3: 15 secondi
│   ├── 600 MP3 già conformi → COPIA (30 secondi)
│   └── 200 MP3 non conformi → CONVERTI (10 minuti)
├── Conversione FLAC: 200 file → CONVERTI (15 minuti)
│
TOTALE: ~25 minuti
OUTPUT: 1000 file MP3 ottimali
```

### 📈 **Performance Medie:**
- **Copia file conformi**: ~50 file/minuto
- **Conversione audio**: ~20-30 file/minuto (dipende da formato/durata)
- **Memoria utilizzata**: <100MB costanti
- **CPU usage**: 30-60% durante conversione

---

**🎵 Audio & Metadata Converter - Harmony Edition v1.0**  
*Tecnologia avanzata per l'ottimizzazione audio professionale*  
*Developed by Simone Pizzi - Powered by FFmpeg* 