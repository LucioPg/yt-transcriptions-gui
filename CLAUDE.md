# YouTube Transcriptor Project

## Project Requirements (Italian)

1. **Download Direct Transcriptions**: Il progetto prevede di scaricare DIRETTAMENTE le trascrizioni dal youtube.com
   - Non scaricare i video, ma solo le trascrizioni disponibili
   - Utilizzare le API o metodi disponibili per estrarre le trascrizioni

2. **Python Language**: Linguaggio interamente python
   - Utilizzare Python 3.13+ come specificato nel pyproject.toml
   - Mantenere il codice pulito e leggibile

3. **Non-Production Level**: Non deve essere di livello di produzione
   - Semplice e funzionale
   - Focus su funzionalità base senza complessità eccessive
   - Adatto per uso personale o educativo

4. **Interface Options**: Deve funzionare da linea di comando o sarebbe bello da pagina web in locale
   - **CLI Interface**: Interfaccia a riga di comando per uso base
   - **Optional Web Interface**: Pagina web locale per migliore user experience
   - Priorità alla CLI, web interface come bonus

5. **File Storage**: deve conservare le trascrizioni su file, il cui nome deve essere il titolo del video
   - Salvare le trascrizioni in file di testo
   - Nome del file basato sul titolo del video YouTube
   - Gestire caratteri speciali nei titoli per nomi file validi

## Technical Considerations

- Libraries suggerite: `yt-dlp` o `youtube-transcript-api` per estrarre trascrizioni
- Gestione errori per video senza trascrizioni disponibili
- Supporto per lingue diverse (se disponibile)
- Formato output: testo semplice o formati strutturati (SRT, VTT)