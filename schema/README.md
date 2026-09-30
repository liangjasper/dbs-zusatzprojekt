# EXIST-Datenbanksystem: Datenbankschema & DDL

Dieses Verzeichnis enthält die vollständigen SQL-Skripte zur Initialisierung, Strukturierung und Befüllung der relationalen Datenbank **`exist_db`** für das Antrags- und Verwaltungssystem der EXIST-Gründungsförderung[cite: 7].

---

## 📁 Dateistruktur

* **`01_create_tables.sql`**: Enthält alle DDL-Befehle (Data Definition Language) zur Erstellung der Datenbank, Relationen, Primär- und Fremdschlüssel, Integritätsbedingungen (Constraints), Views sowie Performance-Indizes[cite: 8].
* **`02_seed_data.sql`**: Enthält umfangreiche Beispieldaten (Seed Data) zum Testen aller Kernfunktionen, Workflows und Visualisierungen im Dashboard[cite: 8].

---

## 🏛️ Architektur & Logischer Entwurf

Das Schema modelliert den Lebenszyklus von Förderanträgen der drei großen Förderlinien (**EXIST-Women**, **EXIST-Gründungsstipendium** und **EXIST-Forschungstransfer**) im Hochschulkontext[cite: 7].

### 1. Normalisierung (3. Normalform)
Das relationale Schema wurde konsistent in die **3. Normalform (3NF)** überführt:
* **1NF**: Alle Attribute sind atomar (z. B. Trennung von Anschriften in `strasse` und `plz`)[cite: 8].
* **2NF**: Durch den konsequenten Einsatz künstlicher Primärschlüssel (Surrogate Keys wie `antrag_id`, `gruender_id`) sind alle Nicht-Schlüssel-Attribute voll funktional vom Primärschlüssel abhängig[cite: 8].
* **3NF**: Transitive Abhängigkeiten wurden eliminiert. So wird der Ortsname nicht redundant in `gruender` oder `ansprechpartner` gespeichert, sondern separat über die Relation `plz_ort` referenziert[cite: 8].

### 2. Tabellenübersicht nach Funktionsbereichen

#### Stammdaten & Akteure
* **`plz_ort`**: Normalisierung von Postleitzahl und Ort[cite: 8].
* **`forschungseinrichtung`**: Hochschulen und Institute mit Name und Webpräsenz[cite: 8].
* **`ansprechpartner`**: Gründungsbeauftragte der jeweiligen Forschungseinrichtung (`einrichtung_id`)[cite: 8].
* **`gruendungsteam`**: Teams, die einer Einrichtung zugeordnet sind (`einrichtung_id`)[cite: 8].
* **`gruender`**: Persönliche und akademische Stammdaten von Gründungsmitgliedern, zugeordnet zu einem Team (`team_id`)[cite: 8].
* **`mentor`**: Fachliche und wissenschaftliche Betreuungspersonen[cite: 8].
* **`bearbeiter`**: Sachbearbeiter:innen des Projektträgers (z. B. PtJ)[cite: 8].
* **`benutzer`**: Zentrales Authentifizierungsmodell mit rollenbasierter Zugriffskontrolle (`ansprechpartner`, `gruender`, `bearbeiter`)[cite: 8].

#### Antragsverwaltung & Audit-Log (Core)
* **`antrag`**: Zentrale Relation für alle Förderanträge inkl. Fremdschlüssel zu Team, Einrichtung, Mentor und Bearbeiter sowie dem Antragsstatus (`eingereicht`, `in_pruefung`, `in_korrektur`, `bewilligt`, `abgelehnt`)[cite: 8].
* **`gruendungsidee`**: Fachbereich und Details zur Geschäftsidee eines Antrags[cite: 8].
* **`antrag_status_historie`**: Revisionssicherer Audit-Trail zur Protokollierung von Statusänderungen inklusive Bearbeiter-Referenz und Zeitstempel[cite: 8].
* **`notiz`**: Interne Vermerke und Feedback der Bearbeiter zu Anträgen[cite: 8].

#### Programmspezifische Tabellen (Subtyping / Inheritance)
Je nach Förderprogramm werden unterschiedliche Dokumente gefordert. Zur Vermeidung von Nullwerten in der Haupttabelle `antrag` wurden relationale Spezialisierungstabellen implementiert:
* **`exist_women`**: Referenziert das Motivationspapier (`motivationspapier_id`)[cite: 8].
* **`exist_gruendungsfoerderung`**: Referenziert das Ideenpapier (`ideenpapier_id`)[cite: 8].
* **`exist_forschungstransfer`**: Referenziert Projektbeschreibung und Businessplan (`projektbeschreibung_id`, `businessplan_id`)[cite: 8].

#### Dokumentenmanagement
* **`dokumente`**: Binäre Speicherung von Uploads (PDF/Dateien) als `LONGBLOB` samt MIME-Typ und Zeitstempel[cite: 8].
* **`lebenslauf`**: m:1- bzw. 1:1-Zuordnung zwischen Gründer und Dokument via `ON DUPLICATE KEY UPDATE`[cite: 8].

---

## 🔍 Sichten (Views)

* **`view_antrag_uebersicht`**: 
  Führt die Relation `antrag` mit `forschungseinrichtung` per `LEFT JOIN` zusammen[cite: 8]. Sie dient der performanten und vereinfachten Darstellung aggregierter Antragslisten im Dashboard, ohne wiederholt komplexe Joins im Frontend-Code formulieren zu müssen[cite: 8].

---

## ⚡ Physischer Entwurf (Indizes)

Zur Optimierung häufiger Filter- und Sortieroperationen wurden Sekundärindizes definiert[cite: 8]:
1. **`idx_antrag_status` (`antrag(status)`)**: Beschleunigt Filterungen nach dem Bearbeitungsstatus und die Aggregation von Antragsstatistiken im Bearbeiter-Dashboard[cite: 8].
2. **`idx_gruender_nachname` (`gruender(nachname)`)**: Optimiert Suchabfragen nach Nachnamen im System[cite: 8].

---

## 🚀 Setup & Ausführung

Zur Initialisierung der Datenbankstruktur und Testdatenbank in MySQL:

```bash
# 1. Tabellenstruktur, Views und Indizes erstellen
mysql -u root -p < schema/01_create_tables.sql

# 2. Testdatenbestand einspielen
mysql -u root -p < schema/02_seed_data.sql

