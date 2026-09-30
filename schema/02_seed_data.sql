USE exist_db;

-- ---------------------------------------------------------------------
-- 1. Postleitzahlen und Orte
-- ---------------------------------------------------------------------
INSERT IGNORE INTO plz_ort (plz, ort) VALUES
('10115', 'Berlin'),
('10117', 'Berlin'),
('10623', 'Berlin'),
('80333', 'München'),
('52062', 'Aachen'),
('20146', 'Hamburg'),
('50931', 'Köln');

-- ---------------------------------------------------------------------
-- 2. Forschungseinrichtungen (Hochschulen und Institute)
-- ---------------------------------------------------------------------
INSERT INTO forschungseinrichtung (einrichtung_id, name, url) VALUES
(1, 'Humboldt-Universität zu Berlin', 'https://www.hu-berlin.de'),
(2, 'Technische Universität Berlin', 'https://www.tu.berlin'),
(3, 'Technische Universität München', 'https://www.tum.de'),
(4, 'RWTH Aachen', 'https://www.rwth-aachen.de'),
(5, 'Universität Hamburg', 'https://www.uni-hamburg.de')
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- ---------------------------------------------------------------------
-- 3. Ansprechpartner der Forschungseinrichtungen (Gründungsservice)
-- ---------------------------------------------------------------------
INSERT INTO ansprechpartner (ansprechpartner_id, vorname, nachname, strasse, plz, email, telefon, einrichtung_id) VALUES
(1, 'Sabine', 'Neumann', 'Unter den Linden 6', '10117', 'sabine.neumann@hu-berlin.de', '+49 30 2093 1111', 1),
(2, 'Markus', 'Zimmermann', 'Straße des 17. Juni 135', '10623', 'markus.zimmermann@tu-berlin.de', '+49 30 3140 2222', 2),
(3, 'Claudia', 'Bauer', 'Arcisstraße 21', '80333', 'claudia.bauer@tum.de', '+49 89 2890 3333', 3),
(4, 'Jens', 'Schröder', 'Templergraben 55', '52062', 'jens.schroeder@rwth-aachen.de', '+49 241 80 12345', 4),
(5, 'Anna', 'Müller', 'Mittelweg 177', '20146', 'anna.mueller@uni-hamburg.de', '+49 40 42838 0', 5);

-- ---------------------------------------------------------------------
-- 4. Mentoren und Bearbeiter (Wissenschaftliche Begleitung & PtJ)
-- ---------------------------------------------------------------------
INSERT INTO mentor (mentor_id, vorname, nachname, email, telefon) VALUES
(1, 'Prof. Dr. Thomas', 'Lehmann', 'thomas.lehmann@hu-berlin.de', '+49 30 2093 9901'),
(2, 'Dr. Sarah', 'Kaufmann', 'sarah.kaufmann@biotech-innovations.de', '+49 89 5566 7788'),
(3, 'Prof. Dr. Klaus', 'Wagner', 'wagner@rwth-aachen.de', '+49 241 80 55555'),
(4, 'Dr. Julia', 'Schulz', 'julia.schulz@uni-hamburg.de', '+49 40 42838 1111');

INSERT INTO bearbeiter (bearbeiter_id, vorname, nachname, email) VALUES
(1, 'Michael', 'Braun', 'michael.braun@ptj.de'),
(2, 'Katharina', 'Koch', 'katharina.koch@ptj.de'),
(3, 'Stefan', 'Lange', 'stefan.lange@ptj.de');

-- ---------------------------------------------------------------------
-- 5. Gründungsteams
-- ---------------------------------------------------------------------
INSERT INTO gruendungsteam (team_id, team_name, einrichtung_id) VALUES
(1, 'FemTech Diagnostics', 2),
(2, 'GreenCycle Solutions', 1),
(3, 'QuantumBit Technologies', 3),
(4, 'AI Legal Aid', 1),
(5, 'EcoCharge', 4),
(6, 'MedVR', 3),
(7, 'OceanClean', 5),
(8, 'SmartFarm', 2),
(9, 'BioPlastics', 4),
(10, 'EduCode', 1),
(11, 'NextGen Batteries', 3),
(12, 'FinTech Secure', 5);

-- ---------------------------------------------------------------------
-- 6. Gründer:innen
-- ---------------------------------------------------------------------
INSERT INTO gruender (gruender_id, vorname, nachname, geburtsdatum, strasse, plz, email, telefon, nationalitaet, anzahl_kinder, hochschulstatus, team_id) VALUES
-- Team 1
(1, 'Clara', 'Richter', '1999-05-14', 'Kantstraße 42', '10623', 'clara.richter@gmail.com', '+49 170 1122334', 'Deutsch', 0, 'Wissenschaftliche Mitarbeiterin', 1),
-- Team 2
(2, 'Lukas', 'Weber', '1997-11-20', 'Invalidenstraße 110', '10115', 'lukas.weber@outlook.com', '+49 171 2233445', 'Deutsch', 0, 'Absolvent', 2),
(3, 'Maximilian', 'Becker', '1998-03-08', 'Chausseestraße 25', '10115', 'max.becker@posteo.de', '+49 172 3344556', 'Österreichisch', 1, 'Student', 2),
-- Team 3
(4, 'Dr. Elena', 'Hoffmann', '1990-09-02', 'Barer Straße 15', '80333', 'elena.hoffmann@tum-lab.de', '+49 173 4455667', 'Deutsch', 2, 'Postdoc / Gruppenleiterin', 3),
(5, 'Jan', 'Vogel', '1994-01-19', 'Türkenstraße 80', '80333', 'jan.vogel@tum.de', '+49 174 5566778', 'Deutsch', 0, 'Promovierender', 3),
-- Team 4
(6, 'Sophie', 'Klein', '1999-12-01', 'Alexanderplatz 1', '10117', 'sophie.klein@hu-berlin.de', '+49 151 1234567', 'Deutsch', 0, 'StudentIn', 4),
-- Team 5
(7, 'Felix', 'Mayer', '1996-08-15', 'Pontstraße 10', '52062', 'felix.mayer@rwth-aachen.de', '+49 160 9876543', 'Deutsch', 0, 'Absolvent', 5),
-- Team 6
(8, 'Maria', 'Garcia', '1995-04-22', 'Leopoldstraße 50', '80333', 'maria.garcia@tum.de', '+49 176 11223344', 'Spanisch', 0, 'Wissenschaftliche Mitarbeiterin', 6),
-- Team 7
(9, 'Tom', 'Peters', '1998-02-10', 'Reeperbahn 1', '20146', 'tom.peters@uni-hamburg.de', '+49 172 9988776', 'Deutsch', 0, 'Student', 7),
-- Team 8
(10, 'Lea', 'Fischer', '1997-07-30', 'Hardenbergstraße 30', '10623', 'lea.fischer@tu-berlin.de', '+49 152 33445566', 'Deutsch', 0, 'Absolvent', 8),
-- Team 9
(11, 'Ali', 'Yilmaz', '1993-11-05', 'Jülicher Straße 100', '52062', 'ali.yilmaz@rwth-aachen.de', '+49 173 55667788', 'Türkisch', 1, 'Promovierender', 9),
-- Team 10
(12, 'Sara', 'Kovac', '1999-01-20', 'Friedrichstraße 200', '10117', 'sara.kovac@hu-berlin.de', '+49 174 22334455', 'Kroatisch', 0, 'Student', 10),
-- Team 11
(13, 'Dr. Hans', 'Schmidt', '1988-06-12', 'Maxvorstadt 12', '80333', 'hans.schmidt@tum.de', '+49 175 66778899', 'Deutsch', 2, 'Postdoc / GruppenleiterIn', 11),
-- Team 12
(14, 'Emma', 'Brown', '1995-09-09', 'Altona 5', '20146', 'emma.brown@uni-hamburg.de', '+49 176 77889900', 'Britisch', 0, 'Absolvent', 12);

-- ---------------------------------------------------------------------
-- 7. Dokumente
-- ---------------------------------------------------------------------
-- Wir erstellen 12 Dummy-Dokumente für die 12 Anträge
INSERT INTO dokumente (dokument_id, dateiname, dateityp, datei) VALUES
(1, 'dokument_team1.pdf', 'application/pdf', CAST('DUMMY' AS BINARY)),
(2, 'dokument_team2.pdf', 'application/pdf', CAST('DUMMY' AS BINARY)),
(3, 'dokument_team3.pdf', 'application/pdf', CAST('DUMMY' AS BINARY)),
(4, 'dokument_team4.pdf', 'application/pdf', CAST('DUMMY' AS BINARY)),
(5, 'dokument_team5.pdf', 'application/pdf', CAST('DUMMY' AS BINARY)),
(6, 'dokument_team6.pdf', 'application/pdf', CAST('DUMMY' AS BINARY)),
(7, 'dokument_team7.pdf', 'application/pdf', CAST('DUMMY' AS BINARY)),
(8, 'dokument_team8.pdf', 'application/pdf', CAST('DUMMY' AS BINARY)),
(9, 'dokument_team9.pdf', 'application/pdf', CAST('DUMMY' AS BINARY)),
(10, 'dokument_team10.pdf', 'application/pdf', CAST('DUMMY' AS BINARY)),
(11, 'dokument_team11.pdf', 'application/pdf', CAST('DUMMY' AS BINARY)),
(12, 'dokument_team12.pdf', 'application/pdf', CAST('DUMMY' AS BINARY));

-- ---------------------------------------------------------------------
-- 9. Förderanträge (Haupttabelle) mit verteilten Statuswerten
-- ---------------------------------------------------------------------
INSERT INTO antrag (antrag_id, gruendungstitel, status, programm, einreichungsdatum, mentor_id, team_id, bearbeiter_id, einrichtung_id) VALUES
(1, 'FemTech Diagnostics', 'eingereicht', 'exist_women', '2026-05-10', NULL, 1, NULL, 2),
(2, 'GreenCycle Analytics', 'in_korrektur', 'exist_gruendungsfoerderung', '2026-04-18', 1, 2, 1, 1),
(3, 'QuantumBit Computing Systems', 'bewilligt', 'exist_forschungstransfer', '2026-02-01', 2, 3, 2, 3),
(4, 'AI Legal Aid', 'in_pruefung', 'exist_gruendungsfoerderung', '2026-05-12', 1, 4, 3, 1),
(5, 'EcoCharge', 'bewilligt', 'exist_gruendungsfoerderung', '2026-01-20', 3, 5, 1, 4),
(6, 'MedVR Training', 'abgelehnt', 'exist_forschungstransfer', '2025-11-15', 2, 6, 2, 3),
(7, 'OceanClean Drones', 'eingereicht', 'exist_women', '2026-05-20', NULL, 7, NULL, 5),
(8, 'SmartFarm Sensors', 'in_pruefung', 'exist_gruendungsfoerderung', '2026-04-30', 2, 8, 1, 2),
(9, 'BioPlastics Packaging', 'bewilligt', 'exist_forschungstransfer', '2026-02-15', 3, 9, 3, 4),
(10, 'EduCode Platform', 'in_korrektur', 'exist_women', '2026-03-10', NULL, 10, 2, 1),
(11, 'NextGen Solid State Batteries', 'in_pruefung', 'exist_forschungstransfer', '2026-05-01', 2, 11, 1, 3),
(12, 'FinTech Secure Transactions', 'abgelehnt', 'exist_gruendungsfoerderung', '2025-10-05', 4, 12, 3, 5);

-- ---------------------------------------------------------------------
-- 10. Programmspezifische Tabellen (Zuordnung der 12 Anträge)
-- ---------------------------------------------------------------------
-- EXIST-Women (Antrag 1, 7, 10)
INSERT INTO exist_women (antrag_id, motivationspapier_id) VALUES
(1, 1), (7, 7), (10, 10);

-- EXIST-Gründungsförderung (Antrag 2, 4, 5, 8, 12)
INSERT INTO exist_gruendungsfoerderung (antrag_id, ideenpapier_id) VALUES
(2, 2), (4, 4), (5, 5), (8, 8), (12, 12);

-- EXIST-Forschungstransfer (Antrag 3, 6, 9, 11)
INSERT INTO exist_forschungstransfer (antrag_id, projektbeschreibung_id, businessplan_id) VALUES
(3, 3, 3), (6, 6, 6), (9, 9, 9), (11, 11, 11);

-- ---------------------------------------------------------------------
-- 11. Details zur Gründungsidee
-- ---------------------------------------------------------------------
INSERT INTO gruendungsidee (antrag_id, titel, bereich, unternehmen) VALUES
(1, 'KI Hormondiagnostik', 'MedTech', 'FemTech Diagnostics UG'),
(2, 'CO2-Bilanzierung', 'CleanTech', 'GreenCycle GmbH'),
(3, 'Quantenprozessor', 'DeepTech', 'QuantumBit GmbH'),
(4, 'KI Rechtsberatung', 'LegalTech', 'Nein'),
(5, 'E-Ladesäulen', 'Hardware', 'EcoCharge GmbH'),
(6, 'VR OP-Training', 'MedTech', 'Nein'),
(7, 'Müllsammel-Drohnen', 'CleanTech', 'Nein'),
(8, 'Agrar-Sensoren', 'AgriTech', 'SmartFarm UG'),
(9, 'Abbaubares Plastik', 'MaterialTech', 'BioPlastics GmbH'),
(10, 'Coding für Kinder', 'EdTech', 'Nein'),
(11, 'Feststoffbatterien', 'DeepTech', 'Nein'),
(12, 'Blockchain Security', 'FinTech', 'FinTech Secure UG');

-- ---------------------------------------------------------------------
-- 14. Benutzerkonten und Rollenverwaltung (Einheitliche Passwörter zum Testen)
-- ---------------------------------------------------------------------
-- INFO: Passwort ist für alle Ansprechpartner 'admin', für alle Bearbeiter 'admin', für alle Gründer '123'
INSERT INTO benutzer (email, passwort, rolle, ansprechpartner_id, gruender_id, bearbeiter_id, ist_aktiv) VALUES
-- Ansprechpartner (Passwort: admin)
('sabine.neumann@hu-berlin.de', 'admin', 'ansprechpartner', 1, NULL, NULL, TRUE),
('markus.zimmermann@tu-berlin.de', 'admin', 'ansprechpartner', 2, NULL, NULL, TRUE),
('claudia.bauer@tum.de', 'admin', 'ansprechpartner', 3, NULL, NULL, TRUE),
('jens.schroeder@rwth-aachen.de', 'admin', 'ansprechpartner', 4, NULL, NULL, TRUE),

-- Bearbeiter PtJ (Passwort: admin)
('michael.braun@ptj.de', 'admin', 'bearbeiter', NULL, NULL, 1, TRUE),
('katharina.koch@ptj.de', 'admin', 'bearbeiter', NULL, NULL, 2, TRUE),
('stefan.lange@ptj.de', 'admin', 'bearbeiter', NULL, NULL, 3, TRUE),

-- Gründer:innen (Passwort: 123) - Wir geben hier den Team-Leads Accounts
('clara.richter@gmail.com', '123', 'gruender', NULL, 1, NULL, TRUE),
('lukas.weber@outlook.com', '123', 'gruender', NULL, 2, NULL, TRUE),
('elena.hoffmann@tum-lab.de', '123', 'gruender', NULL, 4, NULL, TRUE),
('sophie.klein@hu-berlin.de', '123', 'gruender', NULL, 6, NULL, TRUE),
('felix.mayer@rwth-aachen.de', '123', 'gruender', NULL, 7, NULL, TRUE);


