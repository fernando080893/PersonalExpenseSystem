import sqlite3
import os
import datetime

# --- CONFIGURAZIONE DATABASE ---
def get_db_connection():
    """Ottiene il percorso della cartella del file corrente e connette al DB."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'spese_personali.db')
    return sqlite3.connect(db_path)

def inizializza_db():
    """Crea le tabelle leggendo lo script SQL esterno."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Costruisce il percorso verso sql/database.sql
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sql_path = os.path.join(base_dir, '..', 'sql', 'database.sql')
    
    try:
        with open(sql_path, 'r') as f:
            cursor.executescript(f.read())
        conn.commit()
    except Exception as e:
        print(f"Errore inizializzazione DB: {e}")
    return conn

# --- MODULI DEL PROGRAMMA ---

def gestione_categorie(conn):
    cursor = conn.cursor()
    print("\n--- GESTIONE CATEGORIE ---")
    nome = input("Inserisci il nome della nuova categoria: ").strip()
    
    if not nome:
        print("Errore: Il nome non può essere vuoto.")
        return
    
    cursor.execute("SELECT id_categoria FROM Categorie WHERE nome = ?", (nome,))
    if cursor.fetchone():
        print("Errore: La categoria esiste già.")
    else:
        cursor.execute("INSERT INTO Categorie (nome) VALUES (?)", (nome,))
        conn.commit()
        print("Categoria inserita correttamente.")

def inserisci_spesa(conn):
    cursor = conn.cursor()
    print("\n--- INSERIMENTO SPESA ---")
    
    # Validazione Data con datetime
    data_input = input("Data (YYYY-MM-DD): ")
    try:
        # Controlla formato e validità dei giorni del mese (es. no 30 febbraio)
        datetime.datetime.strptime(data_input, '%Y-%m-%d')
    except ValueError:
        print("Errore: Data non valida (formato errato o giorno/mese inesistente).")
        return

    try:
        importo = float(input("Importo: "))
        if importo <= 0:
            print("Errore: L'importo deve essere maggiore di zero.")
            return
    except ValueError:
        print("Errore: Importo non valido.")
        return

    cat_nome = input("Nome categoria: ")
    cursor.execute("SELECT id_categoria FROM Categorie WHERE nome = ?", (cat_nome,))
    res = cursor.fetchone()
    
    if not res:
        print("Errore: La categoria non esiste.")
        return
    
    desc = input("Descrizione facoltativa: ")
    cursor.execute("INSERT INTO Spese (data, importo, id_categoria, descrizione) VALUES (?, ?, ?, ?)", 
                   (data_input, importo, res[0], desc))
    conn.commit()
    print("Spesa inserita correttamente.")

def definisci_budget(conn):
    cursor = conn.cursor()
    print("\n--- DEFINIZIONE BUDGET ---")
    mese = input("Mese (YYYY-MM): ")
    cat_nome = input("Nome categoria: ")
    try:
        importo = float(input("Importo budget: "))
        if importo <= 0:
            print("Errore: Budget deve essere > 0.")
            return
    except ValueError:
        print("Errore: Importo non valido.")
        return
        
    cursor.execute("SELECT id_categoria FROM Categorie WHERE nome = ?", (cat_nome,))
    res = cursor.fetchone()
    if not res:
        print("Errore: Categoria inesistente.")
        return
        
    try:
        cursor.execute("INSERT INTO Budget (mese, importo, id_categoria) VALUES (?, ?, ?)", 
                       (mese, importo, res[0]))
        conn.commit()
        print("Budget salvato correttamente.")
    except sqlite3.IntegrityError:
        print("Errore: Budget per questa categoria/mese già esistente.")

def visualizza_report(conn):
    while True:
        print("\n--- MENU REPORT ---")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo spese")
        print("4. Ritorna al menu principale")
        scelta = input("Scelta: ")
        
        cursor = conn.cursor()
        if scelta == '1':
            cursor.execute("SELECT C.nome, SUM(S.importo) FROM Spese S JOIN Categorie C ON S.id_categoria = C.id_categoria GROUP BY C.nome")
            for row in cursor.fetchall(): print(f"{row[0]}: {row[1]:.2f}€")
        elif scelta == '2':
            cursor.execute("""
                SELECT B.mese, C.nome, B.importo as budget, SUM(S.importo) as speso 
                FROM Budget B 
                JOIN Categorie C ON B.id_categoria = C.id_categoria 
                LEFT JOIN Spese S ON S.id_categoria = C.id_categoria AND strftime('%Y-%m', S.data) = B.mese
                GROUP BY B.mese, C.nome
            """)
            for row in cursor.fetchall(): 
                stato = "SUPERAMENTO" if row[3] > row[2] else "OK"
                print(f"Mese: {row[0]} | Cat: {row[1]} | Budget: {row[2]}€ | Speso: {row[3]:.2f}€ | Stato: {stato}")
        elif scelta == '3':
            cursor.execute("SELECT data, C.nome, importo, descrizione FROM Spese S JOIN Categorie C ON S.id_categoria = C.id_categoria ORDER BY data DESC")
            for row in cursor.fetchall(): print(f"{row[0]} | {row[1]} | {row[2]:.2f}€ | {row[3]}")
        elif scelta == '4':
            break
        else:
            print("Scelta non valida.")

def menu_principale():
    conn = inizializza_db()
    while True:
        print("\n--- SISTEMA SPESE PERSONALI ---")
        print("1. Gestione Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")
        
        scelta = input("Inserisci la tua scelta: ")
        
        if scelta == '1': gestione_categorie(conn)
        elif scelta == '2': inserisci_spesa(conn)
        elif scelta == '3': definisci_budget(conn)
        elif scelta == '4': visualizza_report(conn)
        elif scelta == '5': 
            conn.close()
            print("Uscita dal programma. Arrivederci!")
            break
        else: print("Scelta non valida. Riprovare.")

if __name__ == "__main__":
    print("========================================")
    print("   BENVENUTO NEL GESTORE SPESE PERSONALI")
    print("========================================")
    menu_principale()