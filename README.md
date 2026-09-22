# EXIST-Gründungsförderung: Datenbanksystem

![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)
![Database Design](https://img.shields.io/badge/Database_Design-Relational-blue?style=for-the-badge)

Dieses Projekt umfasst die Konzeption und Implementierung einer relationalen Datenbank für das **EXIST-Förderprogramm** (Bundesministerium für Wirtschaft und Klimaschutz). Das System dient der effizienten Einreichung, Verwaltung und Überprüfung von Förderanträgen im Hochschul- und Forschungskontext.

> **Autoren:** Jasper Liang, Frederik Gräven (Mai 2026)

## 📌 Inhaltsverzeichnis
- [Systembeschreibung](#systembeschreibung)
- [Unterstützte Förderprogramme](#unterstützte-förderprogramme)
- [Akteure & Benutzerrollen](#akteure--benutzerrollen)
- [Datenbankarchitektur (SQL Schema)](#datenbankarchitektur-sql-schema)
- [Installation & Setup](#installation--setup)

---

## 🎯 Systembeschreibung
Das exist-Datenbanksystem digitalisiert den kompletten Lebenszyklus eines Förderantrags. Es ermöglicht Forschungseinrichtungen, Anträge für ihre Gründerteams einzureichen, relevante Dokumente hochzuladen und den aktuellen Status zu verfolgen. Die Sachbearbeiter:innen (z. B. Projektträger Jülich) können die Anträge prüfen, Notizen hinterlassen und über die Bewilligung entscheiden.

**Kernfunktionen:**
- Rollenbasierte Benutzerverwaltung (RBAC).
- Zentrales Dokumentenmanagement (Speicherung von PDFs als `LONGBLOB`).
- Nachverfolgbarkeit des Antragsstatus (Historisierung).
- Dynamische Formular- und Dokumentenanforderungen je nach Förderprogramm.

---

## 🚀 Unterstützte Förderprogramme
Das System deckt die spezifischen Anforderungen und Dokumente der drei großen EXIST-Programme ab:

| Programm | Zielgruppe | Ziel |
| :--- | :--- | :--- |
| **EXIST-Women** | Gründungsinteressierte Frauen | Ideenentwicklung, Vernetzung und Aufbau eines Gründungsteams. |
| **EXIST-Gründungsstipendium** | Studierende, Absolvierende, Wissenschaftler:innen | Entwicklung einer innovativen Geschäftsidee und Vorbereitung der Unternehmensgründung. |
| **EXIST-Forschungstransfer** | Forscher:innen | Überführung von Forschungsergebnissen in marktfähige High-Tech-Produkte. |

---

## 👥 Akteure & Benutzerrollen

Das System implementiert ein striktes Rechtemanagement über die Tabelle `benutzer`:

1. **Forschungseinrichtung**: Reicht den Antrag offiziell ein, verwaltet Kontaktpersonen (`ansprechpartner`) und hat Einsicht in die Anträge der eigenen Teams.
2. **Gründerteam**: Das ausführende Team, bestehend aus bis zu 3 `gruender` (Gründer:innen). Stellt persönliche Daten, Qualifikationen und Lebensläufe zur Verfügung.
3. **Bearbeiter:in (PTJ)**: Prüft eingereichte Anträge, verfasst Notizen und ändert den Antragsstatus (Genehmigung/Ablehnung/Korrektur).

---

## 🏗️ Datenbankarchitektur (SQL Schema)

Der logische Entwurf der Datenbank wurde für MySQL optimiert. Das Schema nutzt fortgeschrittene relationale Konzepte wie *Subtyping* für die unterschiedlichen Förderprogramme.

### Wichtige Entitäten & Tabellen:

* **Stammdaten & Akteure:**
  * `forschungseinrichtung`, `ansprechpartner`
  * `gruendungsteam`, `gruender`, `mentor`
  * `benutzer` (Authentifizierung & Rollenverwaltung)
  * `plz_ort` (Normalisierung der Adressdaten)

* **Antragsverwaltung (Core):**
  * `antrag`: Die zentrale Tabelle für alle Förderanträge, inklusive Verknüpfung zum Basis-Formular (`antragsformular_id`).
  * `gruendungsidee`: Kerninformationen zur innovativen Geschäftsidee.
  * `antrag_status_historie`: Ein Audit-Log, das jede Änderung des Antragsstatus (`eingereicht`, `in_pruefung`, `in_korrektur`, `bewilligt`, `abgelehnt`) mit Zeitstempel protokolliert.
  * `notiz`: Ermöglicht die Kommunikation und interne Vermerke der Bearbeiter:innen zu einem Antrag.

* **Programmspezifische Tabellen (Inheritance-Pattern):**
  Da jedes Programm unterschiedliche Dokumenten-Anforderungen hat, wurden spezialisierte Tabellen erstellt, die per `antrag_id` mit der Haupttabelle verknüpft sind:
  * `exist_women` (Referenziert: Motivationspapier)
  * `exist_gruendungsfoerderung` (Referenziert: Ideenpapier)
  * `exist_forschungstransfer` (Referenziert: Projektbeschreibung, Businessplan)

* **Dokumentenmanagement:**
  * `dokumente`: Zentrale Ablage für alle Datei-Uploads (Dateiname, Typ, BLOB-Daten). 
  * Alle spezifischen Dokumentanforderungen (wie `lebenslauf` oder `ideenpapier_id`) referenzieren via Foreign Key auf diese Tabelle.

---

## ⚙️ Installation & Setup

1. Stelle sicher, dass ein MySQL-Server (Version 8.0+) lokal oder remote läuft.
2. Klone dieses Repository:
   ```bash
   git clone https://github.com/DeinBenutzername/exist-datenbanksystem.git
   ```
3. Führe das SQL-Skript zur Erstellung der Datenbankstruktur aus:
   ```bash
   mysql -u root -p < sql/01_create_tables.sql
   ```
4. Die Datenbank `exist_db` mitsamt aller Tabellen, Views (z.B. `view_antrag_uebersicht`) und Indizes ist nun einsatzbereit.
