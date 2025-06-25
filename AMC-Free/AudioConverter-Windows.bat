@echo off
title Audio & Metadata Converter - Harmony Edition v1.0

echo ===============================================
echo  Audio & Metadata Converter - Harmony Edition
echo  Versione 1.0 - Convertitore Audio Professionale
echo  Sviluppato da Simone Pizzi
echo ===============================================
echo.

REM Verifica che Python sia installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non e' installato o non e' nel PATH
    echo.
    echo Installa Python da: https://python.org/downloads/
    echo Assicurati di selezionare "Add to PATH" durante l'installazione
    echo.
    pause
    exit /b 1
)

echo [INFO] Python trovato - OK
echo [INFO] Verifica dipendenze...

REM Verifica dipendenze Python
python -c "import mutagen, ffmpeg, PIL, tkinter" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Alcune dipendenze mancano. Installazione automatica...
    pip install mutagen ffmpeg-python pillow
)

echo [INFO] Dipendenze verificate - OK
echo [INFO] Avvio Audio & Metadata Converter...
echo.

REM Vai alla directory dello script
cd /d "%~dp0\.."

REM Avvia il software in modalità GUI
python conformer.py --gui

if errorlevel 1 (
    echo.
    echo [ERRORE] Il software ha riscontrato un problema.
    echo Controlla il file conformer.log per dettagli.
    echo.
    pause
)

REM Fine
echo.
echo [INFO] Audio & Metadata Converter terminato.
pause 