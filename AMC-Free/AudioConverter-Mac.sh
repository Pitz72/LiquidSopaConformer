#!/bin/bash

# Audio & Metadata Converter - Harmony Edition v1.0
# Script di avvio per macOS
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

# Verifica Python
print_info "Verifica installazione Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 non è installato!"
    echo
    echo "Installa Python 3 con Homebrew:"
    echo "  brew install python"
    echo
    echo "Oppure scarica da: https://python.org/downloads/"
    echo
    read -p "Premi ENTER per uscire..."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
print_success "Python trovato: $PYTHON_VERSION"

# Verifica Homebrew per FFmpeg
print_info "Verifica Homebrew..."
if ! command -v brew &> /dev/null; then
    print_warning "Homebrew non installato. Installazione consigliata per FFmpeg"
    echo "Installa Homebrew da: https://brew.sh/"
else
    print_success "Homebrew trovato"
    
    # Verifica FFmpeg
    print_info "Verifica FFmpeg..."
    if ! command -v ffmpeg &> /dev/null; then
        print_warning "FFmpeg non trovato. Installazione automatica..."
        brew install ffmpeg
    else
        print_success "FFmpeg trovato"
    fi
fi

# Verifica dipendenze Python
print_info "Verifica dipendenze Python..."
python3 -c "import mutagen, ffmpeg, PIL, tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    print_warning "Alcune dipendenze mancano. Installazione automatica..."
    pip3 install mutagen ffmpeg-python pillow
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