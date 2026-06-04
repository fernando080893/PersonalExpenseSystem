Requisiti di Sistema e Componenti Necessari

Per garantire il corretto funzionamento del software, sono richiesti i seguenti componenti:



Interprete Python

Python 3.x: Il codice è sviluppato in Python 3 ed è compatibile con le versioni 3.8 e successive. Trattandosi di un linguaggio interpretato, non è necessario alcun compilatore.



Librerie Standard Utilizzate

Il progetto si basa esclusivamente sulla Standard Library di Python per garantire la massima portabilità e semplificare la revisione del codice. Non occorre installare alcun pacchetto esterno.



sqlite3: Gestisce la creazione, la connessione e il polling del database relazionale spese\_personali.db.



os: Gestisce i percorsi dei file (assoluti e relativi), garantendo la compatibilità multipiattaforma (Windows, macOS, Linux).



datetime: Utilizzata per la gestione e la validazione delle date.



Guida all'Esecuzione del Programma

Fase di Compilazione

Essendo Python un linguaggio interpretato, non è prevista alcuna fase di compilazione: il codice sorgente viene eseguito direttamente dall'interprete.



Istruzioni di Avvio

Per lanciare il programma, segui questi passaggi:



Apri il Terminale: Apri il Prompt dei comandi (Windows), il Terminale (macOS/Linux) o la PowerShell.



Verifica l'ambiente: Assicurati che Python 3 sia installato digitando uno dei seguenti comandi:

python --version oppure python3 --version oppure py --version



Naviga nel progetto: Spostati all'interno della cartella principale del progetto (quella che contiene le directory src e sql) usando il comando cd.



Esempio: cd percorso/della/cartella/PersonalExpenseSystem



Avvia il software: Dalla cartella principale, digita uno dei seguenti comandi e premi Invio:

python src/main.py oppure py src/main.py



Primo Avvio e Interfaccia

Inizializzazione automatica: Al primissimo avvio, il sistema rileverà automaticamente lo script sql/database.sql e genererà il file di database src/spese\_personali.db.



Menu Principale: Subito dopo, a schermo comparirà l'interfaccia testuale con le 5 opzioni disponibili per la gestione del sistema.

