# Aufbau des Datenbankschemas

Dieses Verzeichnis enthält die SQL-Skripte für die exist_db Datenbank.

## Dateien

* **01_create_tables.sql**: Erstellt die kompletten Tabellen, Fremdschlüssel, den View und die Indizes[cite: 8].
* **02_seed_data.sql**: Enthält Testdaten, damit man das Dashboard mit verschiedenen Benutzern und Anträgen ausprobieren kann[cite: 8].

## Tabellen der Datenbank

### Stammdaten
* `plz_ort`, `forschungseinrichtung`, `ansprechpartner`, `gruendungsteam`, `gruender`, `mentor`, `bearbeiter`[cite: 8]
* `benutzer` (wichtig für die Anmeldung und Rollenverteilung)[cite: 8]

### Anträge (Kernstück)
* `antrag`: Haupttabelle für alle Förderanträge, in der Status und Programm stehen[cite: 8].
* `gruendungsidee`: Details zur Idee[cite: 8].
* `antrag_status_historie`: Speichert, wann welcher Bearbeiter den Status geändert hat[cite: 8].
* `notiz`: Für Feedback der Bearbeiter[cite: 8].

### Spezifische Programme
* `exist_women`, `exist_gruendungsfoerderung`, `exist_forschungstransfer`[cite: 8]
* Diese Tabellen sind mit der antrag Tabelle verknüpft und referenzieren die jeweils benötigten Dokumente[cite: 8].

### Dokumente
* `dokumente`: Speichert die hochgeladenen Dateien[cite: 8].
* `lebenslauf`: Verknüpft die Gründer mit ihren Dokumenten[cite: 8].

## Ergänzende Datenbankobjekte

### View
* **view_antrag_uebersicht**: Verbindet die Tabelle antrag mit forschungseinrichtung[cite: 8]. Wird genutzt, um im Dashboard Anträge leichter anzuzeigen[cite: 8].

### Indizes
* **idx_antrag_status** (auf antrag.status) und **idx_gruender_nachname** (auf gruender.nachname)[cite: 8]. Dienen für schnellere Abfragen, da im Dashboard oft danach gefiltert wird[cite: 8].

## Setup

Zum Initialisieren der Datenbank die Skripte in dieser Reihenfolge im Terminal ausführen:

```bash
mysql -u root -p < 01_create_tables.sql
mysql -u root -p < 02_seed_data.sql

