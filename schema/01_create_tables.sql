DROP DATABASE IF EXISTS exist_db;

CREATE DATABASE IF NOT EXISTS exist_db
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE exist_db;

CREATE TABLE IF NOT EXISTS plz_ort (
    plz VARCHAR(10) PRIMARY KEY,
    ort VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS forschungseinrichtung (
    name VARCHAR(100) NOT NULL,
    url VARCHAR(100) NOT NULL,
    PRIMARY KEY (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS gruendungsteam (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    forschungseinrichtung VARCHAR(100),
    FOREIGN KEY (forschungseinrichtung)
        REFERENCES forschungseinrichtung(name) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS gruender (
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    geburtsdatum DATE NOT NULL,
    strasse VARCHAR(100),
    plz VARCHAR(10),
    email VARCHAR(255) NOT NULL UNIQUE,
    telefon VARCHAR(100),
    nationalitaet VARCHAR(100),
    anzahl_kinder INT NOT NULL DEFAULT 0,
    hochschulstatus VARCHAR(100) NOT NULL,
    team_id INT,

    PRIMARY KEY (vorname, nachname, geburtsdatum),
    FOREIGN KEY (plz) REFERENCES plz_ort(plz) ON UPDATE CASCADE,
    FOREIGN KEY (team_id) REFERENCES gruendungsteam(team_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS lebenslauf (
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    geburtsdatum DATE NOT NULL,
    dateipfad VARCHAR(255) NOT NULL,

    PRIMARY KEY (vorname, nachname, geburtsdatum),
    FOREIGN KEY (vorname, nachname, geburtsdatum)
        REFERENCES gruender(vorname, nachname, geburtsdatum) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS ansprechpartner (
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    strasse VARCHAR(100),
    plz VARCHAR(10),
    email VARCHAR(255) NOT NULL UNIQUE,
    telefon VARCHAR(100),
    forschungseinrichtung VARCHAR(100),

    PRIMARY KEY (vorname, nachname),
    FOREIGN KEY (forschungseinrichtung)
        REFERENCES forschungseinrichtung(name) ON UPDATE CASCADE,
    FOREIGN KEY (plz) REFERENCES plz_ort(plz) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS mentor (
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefon VARCHAR(100),

    PRIMARY KEY (vorname, nachname)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS bearbeiter (
    bearbeiter_id INT AUTO_INCREMENT PRIMARY KEY,
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS antrag (
    antrag_id INT AUTO_INCREMENT PRIMARY KEY,
    gruendungstitel VARCHAR(150),
    status ENUM('eingereicht', 'in_pruefung', 'bewilligt', 'abgelehnt') NOT NULL DEFAULT 'eingereicht',
    einreichungsdatum DATE NOT NULL,
    mentor_vorname VARCHAR(100),
    mentor_nachname VARCHAR(100),
    team_id INT,
    bearbeiter_id INT,
    forschungseinrichtung VARCHAR(100),

    FOREIGN KEY (forschungseinrichtung)
        REFERENCES forschungseinrichtung(name) ON UPDATE CASCADE,
    FOREIGN KEY (mentor_vorname, mentor_nachname)
        REFERENCES mentor(vorname, nachname) ON DELETE SET NULL,
    FOREIGN KEY (team_id)
        REFERENCES gruendungsteam(team_id) ON DELETE CASCADE,
    FOREIGN KEY (bearbeiter_id)
        REFERENCES bearbeiter(bearbeiter_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


