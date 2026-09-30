# Aufbau des Datenbankschemas

Dieses Verzeichnis enthält die SQL-Skripte für die exist_db Datenbank.

## Dateien

* **01_create_tables.sql**: Erstellt die kompletten Tabellen, Fremdschlüssel, den View und die Indizes.
* **02_seed_data.sql**: Enthält Testdaten, damit man das Dashboard mit verschiedenen Benutzern und Anträgen ausprobieren kann.

## Tabellen der Datenbank

### Stammdaten
* `plz_ort`, `forschungseinrichtung`, `ansprechpartner`, `gruendungsteam`, `gruender`, `mentor`, `bearbeiter`
* `benutzer` (wichtig für die Anmeldung und Rollenverteilung)

### Anträge (Kernstück)
* `antrag`: Haupttabelle für alle Förderanträge, in der Status und Programm stehen.
* `gruendungsidee`: Details zur Idee.
* `antrag_status_historie`: Speichert, wann welcher Bearbeiter den Status geändert hat.
* `notiz`: Für Feedback der Bearbeiter.

### Spezifische Programme
* `exist_women`, `exist_gruendungsfoerderung`, `exist_forschungstransfer`
* Diese Tabellen sind mit der antrag Tabelle verknüpft und referenzieren die jeweils benötigten Dokumente.

### Dokumente
* `dokumente`: Speichert die hochgeladenen Dateien.
* `lebenslauf`: Verknüpft die Gründer mit ihren Dokumenten.

## Ergänzende Datenbankobjekte

### View
* **view_antrag_uebersicht**: Verbindet die Tabelle antrag mit forschungseinrichtung. Wird genutzt, um im Dashboard Anträge leichter anzuzeigen.

### Indizes
* **idx_antrag_status** (auf antrag.status) und **idx_gruender_nachname** (auf gruender.nachname). Dienen für schnellere Abfragen, da im Dashboard oft danach gefiltert wird.

## Setup

Zum Initialisieren der Datenbank die Skripte in dieser Reihenfolge im Terminal ausführen:

```bash
mysql -u root -p < 01_create_tables.sql
mysql -u root -p < 02_seed_data.sql

