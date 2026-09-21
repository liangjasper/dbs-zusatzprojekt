-- DROP DATABASE IF EXISTS exist_db;

CREATE DATABASE IF NOT EXISTS exist_db
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE exist_db;

CREATE TABLE IF NOT EXISTS plz_ort (
    plz VARCHAR(10) PRIMARY KEY,
    ort VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS forschungseinrichtung (
    einrichtung_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    url VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS gruendungsteam (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    einrichtung_id INT,
    FOREIGN KEY (einrichtung_id) REFERENCES forschungseinrichtung(einrichtung_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS gruender (
    gruender_id INT AUTO_INCREMENT PRIMARY KEY,
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

    FOREIGN KEY (plz) REFERENCES plz_ort(plz) ON UPDATE CASCADE,
    FOREIGN KEY (team_id) REFERENCES gruendungsteam(team_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS dokumente (
    dokument_id INT AUTO_INCREMENT PRIMARY KEY,
    dateiname VARCHAR(255) NOT NULL,
    dateityp VARCHAR(100),
    datei LONGBLOB NOT NULL,
    hochgeladen_am DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS lebenslauf (
    gruender_id INT PRIMARY KEY,
    -- dateipfad VARCHAR(255) NOT NULL,
    dokument_id INT NOT NULL,

    FOREIGN KEY (gruender_id) REFERENCES gruender(gruender_id) ON DELETE CASCADE,
    FOREIGN KEY (dokument_id) REFERENCES dokumente(dokument_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS ansprechpartner (
    ansprechpartner_id INT AUTO_INCREMENT PRIMARY KEY,
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    strasse VARCHAR(100),
    plz VARCHAR(10),
    email VARCHAR(255) NOT NULL UNIQUE,
    telefon VARCHAR(100),
    einrichtung_id INT,

    FOREIGN KEY (einrichtung_id) REFERENCES forschungseinrichtung(einrichtung_id),
    FOREIGN KEY (plz) REFERENCES plz_ort(plz) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS mentor (
    mentor_id INT AUTO_INCREMENT PRIMARY KEY,
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefon VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS bearbeiter (
    bearbeiter_id INT AUTO_INCREMENT PRIMARY KEY,
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS benutzer (
    benutzer_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    passwort VARCHAR(255) NOT NULL,
    rolle ENUM('forschungseinrichtung', 'gruenderteam', 'bearbeiter') NOT NULL,

    einrichtung_id INT,
    team_id INT,
    bearbeiter_id INT,

    erstellt_am DATETIME DEFAULT CURRENT_TIMESTAMP,
    letzter_login DATETIME,
    ist_aktiv BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (einrichtung_id) REFERENCES forschungseinrichtung(einrichtung_id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES gruendungsteam(team_id) ON DELETE CASCADE,
    FOREIGN KEY (bearbeiter_id) REFERENCES bearbeiter(bearbeiter_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS antrag (
    antrag_id INT AUTO_INCREMENT PRIMARY KEY,
    gruendungstitel VARCHAR(150),
    status ENUM('eingereicht', 'in_pruefung', 'in_korrektur', 'bewilligt', 'abgelehnt') NOT NULL DEFAULT 'eingereicht',
    programm ENUM('exist_women', 'exist_gruendungsfoerderung', 'exist_forschungstransfer') NOT NULL,
    einreichungsdatum DATE NOT NULL,

    zuletzt_aktualisiert DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    antragsformular_id INT,

    mentor_id INT,
    team_id INT,
    bearbeiter_id INT,
    einrichtung_id INT,

    FOREIGN KEY (einrichtung_id) REFERENCES forschungseinrichtung(einrichtung_id),
    FOREIGN KEY (mentor_id) REFERENCES mentor(mentor_id) ON DELETE SET NULL,
    FOREIGN KEY (team_id) REFERENCES gruendungsteam(team_id) ON DELETE CASCADE,
    FOREIGN KEY (bearbeiter_id) REFERENCES bearbeiter(bearbeiter_id) ON DELETE SET NULL,
    FOREIGN KEY (antragsformular_id) REFERENCES dokumente(dokument_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS gruendungsidee (
    antrag_id INT PRIMARY KEY,
    titel VARCHAR(100) NOT NULL,
    bereich VARCHAR(100) NOT NULL,
    unternehmen VARCHAR(100) NOT NULL,

    FOREIGN KEY (antrag_id) REFERENCES antrag (antrag_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS notiz (
    antrag_id INT,
    zeitstempel TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    inhalt TEXT NOT NULL,
    -- dateipfad VARCHAR(255),
    dokument_id INT,

    PRIMARY KEY (antrag_id, zeitstempel),
    FOREIGN KEY (antrag_id) REFERENCES antrag (antrag_id) ON DELETE CASCADE,
    FOREIGN KEY (dokument_id) REFERENCES dokumente(dokument_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS antrag_status_historie (
    historie_id INT AUTO_INCREMENT PRIMARY KEY,
    antrag_id INT NOT NULL,
    bearbeiter_id INT,
    alter_status ENUM('eingereicht', 'in_pruefung', 'in_korrektur', 'bewilligt', 'abgelehnt'),
    neuer_status ENUM('eingereicht', 'in_pruefung', 'in_korrektur', 'bewilligt', 'abgelehnt') NOT NULL,
    aenderungsdatum DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (antrag_id) REFERENCES antrag(antrag_id) ON DELETE CASCADE,
    FOREIGN KEY (bearbeiter_id) REFERENCES bearbeiter(bearbeiter_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS exist_women (
    antrag_id INT PRIMARY KEY,
    motivationspapier_id INT,

    FOREIGN KEY (antrag_id) REFERENCES antrag (antrag_id) ON DELETE CASCADE,
    FOREIGN KEY (motivationspapier_id) REFERENCES dokumente(dokument_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS exist_gruendungsfoerderung (
    antrag_id INT PRIMARY KEY,
    ideenpapier_id INT,

    FOREIGN KEY (antrag_id) REFERENCES antrag (antrag_id) ON DELETE CASCADE,
    FOREIGN KEY (ideenpapier_id) REFERENCES dokumente(dokument_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS exist_forschungstransfer (
    antrag_id INT PRIMARY KEY,
    projektbeschreibung_id INT,
    businessplan_id INT,

    FOREIGN KEY (antrag_id) REFERENCES antrag (antrag_id) ON DELETE CASCADE,
    FOREIGN KEY (projektbeschreibung_id) REFERENCES dokumente(dokument_id) ON DELETE SET NULL,
    FOREIGN KEY (businessplan_id) REFERENCES dokumente(dokument_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*
CREATE TABLE IF NOT EXISTS businessplan (
    antrag_id INT PRIMARY KEY,
    -- dateipfad VARCHAR(255) NOT NULL,
    dokument_id INT NOT NULL,
    FOREIGN KEY (antrag_id) REFERENCES antrag (antrag_id) ON DELETE CASCADE,
    FOREIGN KEY (dokument_id) REFERENCES dokumente(dokument_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS projektbeschreibung (
    antrag_id INT PRIMARY KEY,
    -- dateipfad VARCHAR(255) NOT NULL,
    dokument_id INT NOT NULL,
    FOREIGN KEY (antrag_id) REFERENCES antrag (antrag_id) ON DELETE CASCADE,
    FOREIGN KEY (dokument_id) REFERENCES dokumente(dokument_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
*/

CREATE VIEW view_antrag_uebersicht AS
SELECT
    a.antrag_id,
    a.gruendungstitel AS titel,
    a.programm,
    a.status,
    a.einreichungsdatum,
    f.name AS forschungseinrichtung_name
FROM antrag a
LEFT JOIN forschungseinrichtung f ON a.einrichtung_id = f.einrichtung_id;

CREATE INDEX idx_antrag_status ON antrag(status);

CREATE INDEX idx_gruender_nachname ON gruender(nachname);



