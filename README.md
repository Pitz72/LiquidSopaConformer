# 🎵 LiquidSopaConformer

**Ottimizzatore di Librerie Musicali per Liquidsoap/AzuraCast**

Un tool potente e robusto per standardizzare e ottimizzare librerie musicali per l'uso con software di automazione radio come Liquidsoap e AzuraCast.

## 🎯 Caratteristiche Principali

- **🔄 Conversione Intelligente**: Converte automaticamente file audio non conformi al formato ottimale
- **📋 File Conformi**: Riconosce e copia senza modifiche i file MP3 già conformi (192kbps CBR, 44.1kHz)
- **🗂️ Struttura Preservata**: Mantiene l'organizzazione originale delle cartelle
- **🖥️ Interfaccia Grafica**: GUI user-friendly con Tkinter per facilità d'uso
- **📊 Reporting Dettagliato**: Log completi e statistiche di elaborazione
- **⚡ Performance**: Elaborazione sequenziale ottimizzata per stabilità

## 📋 Formati Supportati

**Input**: MP3, FLAC, WAV, M4A, AAC, OGG
**Output**: MP3 (192kbps CBR, 44.1kHz stereo)

## 🚀 Requisiti di Sistema

- **Python 3.7+**
- **FFmpeg** (installato automaticamente su Windows tramite winget)
- **Dipendenze Python**: 
  - `mutagen` - Gestione metadati audio
  - `ffmpeg-python` - Interfaccia Python per FFmpeg
  - `Pillow` - Elaborazione immagini per artwork

## 📦 Installazione

### 1. Clona il Repository
```bash
git clone https://github.com/tuonome/LiquidSopaConformer.git
cd LiquidSopaConformer
```

### 2. Installa le Dipendenze
```bash
pip install mutagen ffmpeg-python pillow
```

### 3. Installa FFmpeg (Windows)
```bash
winget install ffmpeg
```

## 🎮 Utilizzo

### Interfaccia Grafica (Consigliato)
```bash
python conformer.py --gui
```

### Riga di Comando
```bash
python conformer.py "path/to/input" "path/to/output"
```

### Parametri Disponibili
- `--gui`: Avvia l'interfaccia grafica
- `--help`: Mostra l'aiuto completo

## 🔧 Come Funziona

1. **Scansione**: Analizza ricorsivamente la directory di input
2. **Classificazione**: Distingue tra file conformi e non conformi
3. **Elaborazione**:
   - **File conformi**: Copiati direttamente senza modifiche
   - **File non conformi**: Convertiti al formato target
4. **Output**: Salva i risultati mantenendo la struttura delle cartelle

## 📊 Specifiche Tecniche

### Formato Target Ottimale per Liquidsoap/AzuraCast
- **Codec**: MP3 (MPEG-1 Layer 3)
- **Bitrate**: 192 kbps CBR (Constant Bitrate)
- **Sample Rate**: 44.1 kHz
- **Canali**: Stereo (2 canali)
- **Metadati**: ID3v2.3, puliti e ottimizzati

### Vantaggi del Formato Target
- ✅ **Compatibilità universale** con tutti i player
- ✅ **Qualità audio elevata** per lo streaming
- ✅ **Bitrate costante** per calcoli precisi della durata
- ✅ **Overhead minimo** per server di streaming
- ✅ **Latenza ridotta** per live broadcasting

## 📝 File di Log

Il programma genera automaticamente:
- `conformer_fixed.log`: Log dettagliato dell'elaborazione
- Report statistiche al completamento

## 🛠️ Risoluzione Problemi

### FFmpeg non trovato
Se ricevi errori riguardo FFmpeg:
1. Riavvia il terminale dopo l'installazione
2. Verifica l'installazione: `ffmpeg -version`
3. Su Windows, potrebbe essere necessario riavviare completamente

### Errori di permessi
- Assicurati di avere permessi di scrittura nella directory di output
- Esegui come amministratore se necessario

### File non elaborati
- Controlla che i file di input esistano e siano accessibili
- Verifica che non siano protetti da DRM

## 🧪 Test e Qualità

Il progetto include:
- ✅ Gestione robusta degli errori
- ✅ Logging completo per debugging
- ✅ Validazione input/output
- ✅ Testing su diverse tipologie di file

## 🤝 Contributi

I contributi sono benvenuti! Per contribuire:

1. Fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/nuova-feature`)
3. Commit delle modifiche (`git commit -am 'Aggiunge nuova feature'`)
4. Push del branch (`git push origin feature/nuova-feature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.

## 🙏 Riconoscimenti

- **FFmpeg** - Per l'eccellente engine di conversione audio
- **Mutagen** - Per la gestione avanzata dei metadati
- **Community Liquidsoap** - Per l'ispirazione e i feedback

---

**Sviluppato con ❤️ per la community di radio streaming italiana**

### 📞 Supporto

Per problemi, suggerimenti o domande:
- 🐛 [Apri un Issue](https://github.com/tuonome/LiquidSopaConformer/issues)
- 💬 [Discussioni](https://github.com/tuonome/LiquidSopaConformer/discussions)

---

*Ultimo aggiornamento: Dicembre 2024* 