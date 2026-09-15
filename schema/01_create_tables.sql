CREATE DATABASE IF NOT EXISTS exist_db
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE exist_db;

CREATE TABLE IF NOT EXISTS gruender (
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    geburtsdatum DATE NOT NULL,
    strasse VARCHAR(100),
    plz VARCHAR(50),
    email VARCHAR(255) NOT NULL UNIQUE,
    telefon VARCHAR(100),
    nationalitaet VARCHAR(100),
    anzahl_kinder VARCHAR(50) NOT NULL,
    hochschulstatus VARCHAR(100) NOT NULL,
    team_id INT NOT NULL,

    PRIMARY KEY (vorname, nachname, geburtsdatum)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS lebenslauf (
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    geburtsdatum DATE NOT NULL,

    PRIMARY KEY (vorname, nachname, geburtsdatum)
    #FOREIGN KEY (vorname) REFERENCES gruender(vorname),
    #FOREIGN KEY (nachname) REFERENCES gruender(nachname),
    #FOREIGN KEY (geburtsdatum) REFERENCES gruender(geburtsdatum)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS ansprechpartner (
    vorname VARCHAR(100) NOT NULL,
    nachname VARCHAR(100) NOT NULL,
    strasse VARCHAR(100),
    plz VARCHAR(50),
    email VARCHAR(255) NOT NULL UNIQUE,
    telefon VARCHAR(100),
    forschungseinrichtung VARCHAR(100),

    PRIMARY KEY (vorname, nachname)
    #FOREIGN KEY (forschungseinrichtung) REFERENCES forschungseinrichtung(name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS forschungseinrichtung (
    name VARCHAR(100) NOT NULL,
    url VARCHAR(100) NOT NULL,

    PRIMARY KEY (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;