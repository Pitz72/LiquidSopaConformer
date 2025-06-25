# 🎵 Audio & Metadata Converter - Harmony Edition v1.0

**Convertitore professionale per ottimizzare librerie musicali per sistemi radio**

Sviluppato da **Simone Pizzi** con assistenza LLM

## 📋 Panoramica

Audio & Metadata Converter è uno strumento professionale progettato per ottimizzare librerie musicali per l'uso con software di automazione radiofonica come Liquidsoap, AzuraCast e altri sistemi broadcasting. Il software converte automaticamente i file audio nel formato ottimale garantendo qualità uniforme e compatibilità massima.

## ✨ Caratteristiche Principali

### 🎯 Conversione Intelligente
- **Rilevamento automatico**: Identifica i file già conformi agli standard radio
- **Copia diretta**: I file MP3 già ottimali vengono copiati senza riprocessamento
- **Conversione selettiva**: Solo i file non conformi vengono convertiti
- **Preservazione struttura**: Mantiene l'organizzazione delle cartelle originali

### 🔧 Formati Supportati
- **Input**: MP3, FLAC, WAV, M4A, AAC, OGG
- **Output**: MP3 192kbps CBR, 44.1kHz Stereo (standard radio professionale)

### 🖥️ Interfacce Multiple
- **GUI Elegante**: Interfaccia grafica moderna con tema dark
- **Splash Screen**: Schermata di introduzione con informazioni complete
- **Command Line**: Supporto completo per automazione e scripting

### ⚡ Prestazioni Ottimizzate
- **Auto-detection FFmpeg**: Trova automaticamente FFmpeg nel sistema
- **Elaborazione sequenziale**: Processamento stabile e robusto
- **Gestione errori avanzata**: Logging completo e recovery automatico

## 🔧 Installazione e Utilizzo

### 💻 **Windows - Versione Eseguibile (CONSIGLIATO)**

La versione più semplice per utenti Windows:

1. **Scarica** l'archivio `AudioMetadataConverter-v1.0-Free.zip`
2. **Estrai** la cartella `AMC-Free`
3. **Doppio click** su `AudioMetadataConverter.exe`
4. **Il software si avvia immediatamente!**

✅ **Vantaggi dell'eseguibile:**
- Nessuna installazione Python richiesta
- Nessuna configurazione dipendenze
- Avvio istantaneo
- Include tutte le librerie necessarie

### 📁 **Distribuzione Completa AMC-Free**

La cartella `AMC-Free` contiene:
- **`AudioMetadataConverter.exe`** - Eseguibile Windows standalone
- **Script multi-platform** per Mac e Linux
- **Documentazione completa** (guide, disclaimer, licenza)
- **Tutto il necessario** per uso immediato

### 🔧 **Installazione da Codice Sorgente**

Per sviluppatori o sistemi non-Windows:

#### Prerequisiti
- Python 3.7+
- FFmpeg (installato automaticamente o manualmente)

#### Installazione Dipendenze
```bash
pip install -r requirements.txt
```

#### Verifica FFmpeg
Il software rileva automaticamente FFmpeg. Su Windows con WinGet:
```bash
winget install ffmpeg
```

## 🚀 Utilizzo

### 💻 **Windows (Eseguibile)**
```
Doppio click su AudioMetadataConverter.exe
```

### 🖥️ **Interfaccia Grafica (Da Codice)**
```bash
python conformer.py
```
o
```bash
python conformer.py --gui
```

### Command Line
```bash
python conformer.py /percorso/input /percorso/output
```

### Esempi Pratici

#### Conversione Libreria Completa
```bash
# Windows
python conformer.py "C:\Musica\Originale" "C:\Musica\Radio"

# Linux/Mac
python conformer.py "/home/user/musica" "/home/user/radio"
```

## 📊 Output e Statistiche

Il software fornisce report dettagliati:
- **File processati**: Totale file elaborati
- **File copiati**: MP3 già conformi (nessuna conversione)
- **File convertiti**: File trasformati nel formato target
- **File saltati**: File non audio o già esistenti
- **Errori**: Problemi riscontrati durante l'elaborazione

## 🎵 Standard di Conversione

### Target Format
- **Codec**: MP3 (MPEG-1 Audio Layer III)
- **Bitrate**: 192 kbps CBR (Constant Bit Rate)
- **Frequenza**: 44.1 kHz
- **Canali**: Stereo (2 canali)
- **Qualità**: Ottimale per broadcasting radio

### Logica di Elaborazione
1. **Scansione**: Trova tutti i file audio nella directory input
2. **Analisi**: Verifica se i file MP3 sono già conformi
3. **Routing**:
   - File conformi → Copia diretta
   - File non conformi → Conversione + copia
   - File non audio → Ignorati
4. **Output**: Struttura identica con file ottimizzati

## 🔍 Risoluzione Problemi

### Errore FFmpeg Non Trovato
```bash
# Windows (WinGet)
winget install ffmpeg

# Windows (Chocolatey)
choco install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt install ffmpeg

# macOS (Homebrew)
brew install ffmpeg
```

### Problemi di Permessi
- Assicurati di avere permessi di lettura sulla cartella input
- Assicurati di avere permessi di scrittura sulla cartella output
- Su Linux/Mac potrebbe essere necessario `chmod +x conformer.py`

### File Non Processati
- Verifica che i file siano in formati supportati
- Controlla il log `conformer.log` per dettagli specifici
- Assicurati che FFmpeg sia accessibile nel PATH

## 📁 Struttura Progetto

```
LiquidSopaConformer/
├── conformer.py                          # Script principale
├── requirements.txt                      # Dipendenze Python
├── README.md                            # Documentazione
├── LICENSE                              # Licenza
├── CHANGELOG.md                         # Cronologia versioni
├── test_conformer.py                    # Test di regressione
├── SOFTWARE_STATUS.md                   # Stato e anti-regressione
├── .gitignore                           # Esclusioni Git
├── audioconv.png                        # Icona applicazione
├── AMC-Free/                            # 📦 DISTRIBUZIONE COMPLETA
│   ├── AudioMetadataConverter.exe       # 🚀 Eseguibile Windows
│   ├── AudioConverter-Windows.bat       # Script Windows alternativo
│   ├── AudioConverter-Mac.sh            # Script macOS
│   ├── AudioConverter-Linux.sh          # Script Linux
│   ├── README.md                        # Guida distribuzione
│   ├── CHE_COS_E.md                     # Cosa è il software
│   ├── COME_FUNZIONA.md                 # Come funziona
│   ├── COME_AVVIARE.md                  # Istruzioni avvio
│   ├── DISCLAIMER.md                    # Responsabilità e backup
│   ├── LICENSE.txt                      # Licenza MIT
│   ├── DISTRIBUZIONE.md                 # Summary distribuzione
│   └── audioconv.png                    # Icona software
└── AudioMetadataConverter-v1.0-Free.zip # 📦 Archivio distribuzione
```

## 🧪 Testing

### Test Base
```bash
python test_conformer.py
```

### Test su Directory Piccola
Prima di processare librerie enormi, testa su una sottocartella:
```bash
python conformer.py "C:\Test\Input" "C:\Test\Output"
```

## 📝 Logging

Il software genera log dettagliati in `conformer.log`:
- Timestamp di ogni operazione
- File processati con successo
- Errori e warning dettagliati
- Statistiche finali

## 🤝 Contributi

Questo software è stato sviluppato da **Simone Pizzi** utilizzando assistenza LLM. 

### Supporto Progetto
Se questo software ti è utile, considera una donazione per sostenere **Runtime Radio**:
💝 [Dona su PayPal](https://paypal.me/runtimeradio)

Anche se sviluppato con LLM, questo progetto richiede impegno mentale significativo e ore di lavoro per perfezionamento e testing.

## 📜 Licenza

Questo software è distribuito sotto licenza MIT. Vedi il file `LICENSE` per dettagli completi.

## 🔄 Cronologia Versioni

### v1.0 "Harmony Edition" (Corrente)
- Interfaccia grafica completamente ridisegnata
- Tema dark mode elegante
- Splash screen con informazioni complete
- Auto-detection FFmpeg migliorata
- Elaborazione sequenziale stabile
- Documentazione completa
- Testing anti-regressione

## 📞 Supporto

Per problemi, bug report o richieste di funzionalità:
1. Controlla la sezione "Risoluzione Problemi"
2. Verifica il file `conformer.log`
3. Assicurati di avere l'ultima versione
4. Crea un issue dettagliato con:
   - Sistema operativo
   - Versione Python
   - Output di errore completo
   - Passi per riprodurre il problema

---

**Audio & Metadata Converter - Harmony Edition v1.0**  
*Software professionale per l'ottimizzazione di librerie musicali radio*  
*Sviluppato con ❤️ da Simone Pizzi* 