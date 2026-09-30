# EXIST-Gründungsförderung Datenbanksystem

Dieses Projekt umfasst eine relationale Datenbank und ein interaktives Dashboard für das EXIST-Förderprogramm. Das System dient der Einreichung, Verwaltung und Überprüfung von Förderanträgen im Hochschul- und Forschungskontext.

Autoren: Jasper Liang, Frederik Gräven

## Überblick der Förderprogramme

*   **EXIST-Women**: Für gründungsinteressierte Frauen (Ideenentwicklung, Vernetzung).
*   **EXIST-Gründungsstipendium**: Für Studierende, Absolvierende und Wissenschaftler:innen (Entwicklung einer Geschäftsidee).
*   **EXIST-Forschungstransfer**: Für Forscher:innen (Überführung von Forschungsergebnissen in marktfähige Produkte).

## Benutzerrollen

Das System implementiert ein Rechtemanagement für drei Hauptrollen:

1.  **Ansprechpartner (Forschungseinrichtung)**: Reicht Anträge offiziell ein und hat Einsicht in die Anträge der eigenen Einrichtung.
2.  **Gründer (Gründerteam)**: Das ausführende Team. Stellt persönliche Daten, Qualifikationen und Lebensläufe zur Verfügung.
3.  **Bearbeiter (PTJ)**: Prüft eingereichte Anträge, verfasst Notizen und ändert den Antragsstatus (z. B. auf "bewilligt" oder "abgelehnt").

## Projektstruktur

*   `schema/`: Enthält die SQL-Dateien zum Erstellen der Tabellen und zum Einfügen der Testdaten.
*   `Dashboard/`: Enthält den Python-Code für die Streamlit-App (Frontend).
*   `docs/`: Enthält den vollständigen Projektbericht und das ER-Diagramm.

## Installation und Setup

Um das Projekt lokal auszuführen, müssen die Datenbank und die Python-App eingerichtet werden.

### 1. Datenbank einrichten
Stelle sicher, dass ein MySQL-Server lokal läuft. Führe die beiden SQL-Skripte aus dem `schema`-Ordner in dieser Reihenfolge aus:
1. `schema/01_create_tables.sql` (Erstellt die komplette Tabellenstruktur)
2. `schema/02_seed_data.sql` (Füllt die Datenbank mit Test-Benutzern und Anträgen)

### 2. Datenbank-Verbindung konfigurieren
Wechsle in den Ordner `Dashboard`. Dort befindet sich eine `.env` Datei. Passe die Werte an deine lokale MySQL-Datenbank an:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=dein_passwort
DB_NAME=exist_db


