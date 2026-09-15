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


