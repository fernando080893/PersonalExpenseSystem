-- Creazione della tabella Categorie
CREATE TABLE IF NOT EXISTS Categorie (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,                     -- PRIMARY KEY
    nome TEXT UNIQUE NOT NULL                                           -- UNIQUE e NOT NULL
);

-- Creazione della tabella Spese
CREATE TABLE IF NOT EXISTS Spese (
    id_spesa INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,                                                 -- NOT NULL
    importo REAL NOT NULL CHECK(importo > 0),                           -- CHECK
    descrizione TEXT,
    id_categoria INTEGER NOT NULL,
    -- FOREIGN KEY: lega la spesa a una categoria esistente
    FOREIGN KEY (id_categoria) REFERENCES Categorie(id_categoria)
);

-- Creazione della tabella Budget
CREATE TABLE IF NOT EXISTS Budget (
    id_budget INTEGER PRIMARY KEY AUTOINCREMENT,
    mese TEXT NOT NULL,
    importo REAL NOT NULL CHECK(importo > 0),                           -- CHECK
    id_categoria INTEGER NOT NULL,
    -- UNIQUE composto: impedisce di definire due volte il budget per lo stesso mese/categoria
    UNIQUE(mese, id_categoria),
    FOREIGN KEY (id_categoria) REFERENCES Categorie(id_categoria)
);