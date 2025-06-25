# 🚀 Come Avviare Audio & Metadata Converter

**Guida completa all'avvio del software su Windows, macOS e Linux**

## 🖥️ Windows

### 🚀 **Metodo 1: Eseguibile Standalone (CONSIGLIATO)**

1. **Apri la cartella** dove hai scaricato il software
2. **Doppio click** su `AudioMetadataConverter.exe`
3. **Il software si avvierà immediatamente** senza necessità di installare nulla

### 📂 **Metodo 2: Script Automatico**

1. **Apri la cartella** dove hai scaricato il software
2. **Doppio click** su `AudioConverter-Windows.bat`
3. **Il software si avvierà automaticamente** verificando tutte le dipendenze

### ⚙️ **Metodo 3: Manuale**

1. **Apri il Prompt dei Comandi** (cmd) o PowerShell
2. **Naviga** nella cartella del software:
   ```cmd
   cd "C:\path\del\tuo\software"
   ```
3. **Avvia** il software:
   ```cmd
   python conformer.py
   ```

### 🔧 **Prerequisiti Windows**

Se il software non si avvia, installa i prerequisiti:

**1. Python:**
- Scarica da: https://python.org/downloads/
- ⚠️ **IMPORTANTE**: Seleziona "Add to PATH" durante l'installazione

**2. FFmpeg:**
```cmd
winget install ffmpeg
```
*Oppure scarica da: https://ffmpeg.org/download.html*

**3. Dipendenze Python:**
```cmd
pip install mutagen ffmpeg-python pillow
```

---

## 🍎 macOS

### 📂 **Metodo 1: Script Automatico (Consigliato)**

1. **Apri Finder** e naviga nella cartella del software
2. **Doppio click** su `AudioConverter-Mac.sh`
3. Se richiesto, autorizza l'esecuzione nelle **Preferenze di Sistema**

### ⚙️ **Metodo 2: Terminale**

1. **Apri Terminale** (Cmd+Spazio, cerca "Terminal")
2. **Naviga** nella cartella del software:
   ```bash
   cd "/path/del/tuo/software"
   ```
3. **Rendi eseguibile** lo script (solo la prima volta):
   ```bash
   chmod +x AudioConverter-Mac.sh
   ```
4. **Avvia** il software:
   ```bash
   ./AudioConverter-Mac.sh
   ```

### 🔧 **Prerequisiti macOS**

**1. Homebrew (consigliato):**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**2. Python:**
```bash
brew install python
```

**3. FFmpeg:**
```bash
brew install ffmpeg
```

**4. Dipendenze Python:**
```bash
pip3 install mutagen ffmpeg-python pillow
```

---

## 🐧 Linux

### 📂 **Metodo 1: Script Automatico (Consigliato)**

1. **Apri il file manager** e naviga nella cartella del software
2. **Doppio click** su `AudioConverter-Linux.sh`
3. Oppure **click destro** → "Esegui nel terminale"

### ⚙️ **Metodo 2: Terminale**

1. **Apri il terminale** (Ctrl+Alt+T)
2. **Naviga** nella cartella del software:
   ```bash
   cd "/path/del/tuo/software"
   ```
3. **Rendi eseguibile** lo script (solo la prima volta):
   ```bash
   chmod +x AudioConverter-Linux.sh
   ```
4. **Avvia** il software:
   ```bash
   ./AudioConverter-Linux.sh
   ```

### 🔧 **Prerequisiti Linux**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk ffmpeg
pip3 install mutagen ffmpeg-python pillow
```

**Fedora/CentOS/RHEL:**
```bash
sudo dnf install python3 python3-pip python3-tkinter ffmpeg
pip3 install mutagen ffmpeg-python pillow
```

**Arch/Manjaro:**
```bash
sudo pacman -S python python-pip tk ffmpeg
pip install mutagen ffmpeg-python pillow
```

---

## 🎯 Utilizzo dell'Interfaccia

### 1. **Schermata di Benvenuto**
Al primo avvio vedrai:
- Nome del software e versione
- Informazioni sull'autore
- Link per donazioni (opzionale)
- Pulsante "AVVIA SOFTWARE"

### 2. **Finestra Principale**
Dopo aver cliccato "AVVIA SOFTWARE":

**📂 Cartella di Input:**
- Clicca "Sfoglia" per selezionare la cartella con la tua musica originale

**💾 Cartella di Output:**
- Clicca "Sfoglia" per selezionare dove salvare i file ottimizzati

**🚀 Avvio Elaborazione:**
- Clicca "AVVIA ELABORAZIONE" per iniziare la conversione

### 3. **Monitoraggio Progresso**
- Vedrai aggiornamenti in tempo reale nel terminale
- Ogni 50 file elaborati riceverai un aggiornamento
- Al termine: statistiche complete dell'elaborazione

---

## ❗ Risoluzione Problemi

### 🚫 **"Python non trovato"**
- **Windows**: Reinstalla Python da python.org, seleziona "Add to PATH"
- **macOS**: Installa con `brew install python`
- **Linux**: Installa con il package manager della tua distribuzione

### 🚫 **"FFmpeg non trovato"**
- **Windows**: `winget install ffmpeg` o riavvia dopo installazione
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg` (Ubuntu) o equivalente

### 🚫 **"Modulo non trovato"**
Installa le dipendenze Python:
```bash
pip install mutagen ffmpeg-python pillow
# oppure su Linux/Mac:
pip3 install mutagen ffmpeg-python pillow
```

### 🚫 **"Permission Denied" (Linux/Mac)**
Rendi eseguibile lo script:
```bash
chmod +x AudioConverter-Linux.sh   # Linux
chmod +x AudioConverter-Mac.sh     # Mac
```

### 🚫 **GUI non si apre (Linux)**
Installa tkinter:
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

---

## 📋 Check List Veloce

Prima di avviare il software, verifica che hai:

### ✅ **Requisiti Minimi:**
- [ ] **Python 3.7+** installato
- [ ] **FFmpeg** installato e funzionante
- [ ] **Dipendenze Python** installate
- [ ] **Tkinter** disponibile (per GUI)

### ✅ **Test Rapido:**
Apri terminale/cmd e testa:
```bash
python --version    # Deve mostrare Python 3.7+
ffmpeg -version     # Deve mostrare informazioni FFmpeg
python -c "import tkinter" # Non deve dare errori
```

### ✅ **Struttura Directory:**
```
AudioConverter/
├── conformer.py              # File principale
├── AMC-Free/                 # Cartella distribuzione
│   ├── AudioConverter-Windows.bat
│   ├── AudioConverter-Mac.sh
│   ├── AudioConverter-Linux.sh
│   └── [documenti di supporto]
└── [altri file del progetto]
```

---

## 💡 Suggerimenti

### 🎯 **Prima Esecuzione:**
1. **Testa** con una cartella piccola (10-20 file)
2. **Verifica** che l'output sia corretto
3. **Procedi** con la libreria completa

### ⚡ **Performance:**
- **Chiudi** altri software pesanti durante la conversione
- **Evita** di usare il computer per altro durante l'elaborazione
- **Libera** spazio disco sufficiente (almeno il doppio della libreria originale)

### 🛡️ **Sicurezza:**
- **SEMPRE** fai backup dei file originali prima di iniziare
- **Testa** su una copia di prova prima dell'elaborazione finale
- **Controlla** i log in caso di errori

---

**🎵 Audio & Metadata Converter - Harmony Edition v1.0**  
*Avvio semplice e veloce su tutte le piattaforme*  
*Developed by Simone Pizzi* 