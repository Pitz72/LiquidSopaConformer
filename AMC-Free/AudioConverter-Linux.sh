#!/bin/bash

# Audio & Metadata Converter - Harmony Edition v1.0
# Script di avvio per Linux
# Sviluppato da Simone Pizzi

echo "==============================================="
echo " Audio & Metadata Converter - Harmony Edition"
echo " Versione 1.0 - Convertitore Audio Professionale"
echo " Sviluppato da Simone Pizzi"
echo "==============================================="
echo

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funzione per stampa colorata
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERRORE]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

# Rilevamento distribuzione Linux
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
    print_info "Distribuzione rilevata: $NAME"
else
    DISTRO="unknown"
    print_warning "Distribuzione Linux non riconosciuta"
fi

# Verifica Python
print_info "Verifica installazione Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 non è installato!"
    echo
    case $DISTRO in
        ubuntu|debian)
            echo "Installa Python 3 con:"
            echo "  sudo apt update && sudo apt install python3 python3-pip python3-tk"
            ;;
        fedora|centos|rhel)
            echo "Installa Python 3 con:"
            echo "  sudo dnf install python3 python3-pip python3-tkinter"
            ;;
        arch|manjaro)
            echo "Installa Python 3 con:"
            echo "  sudo pacman -S python python-pip tk"
            ;;
        *)
            echo "Consulta la documentazione della tua distribuzione per installare Python 3"
            ;;
    esac
    echo
    read -p "Premi ENTER per uscire..."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
print_success "Python trovato: $PYTHON_VERSION"

# Verifica display X11 per GUI
print_info "Verifica ambiente grafico..."
if [ -z "$DISPLAY" ]; then
    print_warning "DISPLAY non impostato. Potrebbe essere necessario abilitare X11 forwarding"
    if command -v xhost &> /dev/null; then
        print_info "Tentativo di configurazione automatica display..."
        export DISPLAY=:0.0
    fi
fi

# Verifica tkinter
print_info "Verifica supporto GUI (tkinter)..."
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    print_error "Tkinter non è installato!"
    echo
    case $DISTRO in
        ubuntu|debian)
            echo "Installa tkinter con:"
            echo "  sudo apt install python3-tk"
            ;;
        fedora|centos|rhel)
            echo "Installa tkinter con:"
            echo "  sudo dnf install python3-tkinter"
            ;;
        arch|manjaro)
            echo "Installa tkinter con:"
            echo "  sudo pacman -S tk"
            ;;
    esac
    echo
    read -p "Premi ENTER per uscire..."
    exit 1
fi

print_success "Supporto GUI verificato"

# Verifica e installa FFmpeg
print_info "Verifica FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    print_warning "FFmpeg non trovato"
    case $DISTRO in
        ubuntu|debian)
            print_info "Installazione FFmpeg automatica..."
            sudo apt update && sudo apt install -y ffmpeg
            ;;
        fedora|centos|rhel)
            print_info "Installazione FFmpeg automatica..."
            sudo dnf install -y ffmpeg
            ;;
        arch|manjaro)
            print_info "Installazione FFmpeg automatica..."
            sudo pacman -S --noconfirm ffmpeg
            ;;
        *)
            print_warning "Installa FFmpeg manualmente per la tua distribuzione"
            ;;
    esac
else
    print_success "FFmpeg trovato"
fi

# Verifica dipendenze Python
print_info "Verifica dipendenze Python..."
python3 -c "import mutagen, ffmpeg, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    print_warning "Alcune dipendenze mancano. Installazione automatica..."
    pip3 install --user mutagen ffmpeg-python pillow
else
    print_success "Dipendenze Python verificate"
fi

# Vai alla directory del software
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

print_info "Avvio Audio & Metadata Converter..."
echo

# Avvia il software
python3 conformer.py --gui

# Controllo exit code
if [ $? -ne 0 ]; then
    print_error "Il software ha riscontrato un problema"
    echo "Controlla il file conformer.log per dettagli"
    echo
    read -p "Premi ENTER per uscire..."
else
    print_success "Audio & Metadata Converter terminato correttamente"
fi 