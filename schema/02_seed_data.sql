-- =====================================================================
-- 02_seed_data.sql
-- EXIST-Datenbank: Initialer Datenbestand (Seed Data / Testdaten)
-- =====================================================================

USE exist_db;

-- ---------------------------------------------------------------------
-- 1. Postleitzahlen und Orte
-- ---------------------------------------------------------------------
INSERT IGNORE INTO plz_ort (plz, ort) VALUES
('10115', 'Berlin'),
('10117', 'Berlin'),
('10623', 'Berlin'),
('80333', 'München'),
('52062', 'Aachen');

-- ---------------------------------------------------------------------
-- 2. Forschungseinrichtungen (Hochschulen und Institute)
-- ---------------------------------------------------------------------
INSERT INTO forschungseinrichtung (einrichtung_id, name, url) VALUES
(1, 'Humboldt-Universität zu Berlin', 'https://www.hu-berlin.de'),
(2, 'Technische Universität Berlin', 'https://www.tu.berlin'),
(3, 'Technische Universität München', 'https://www.tum.de')
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- ---------------------------------------------------------------------
-- 3. Ansprechpartner der Forschungseinrichtungen (Gründungsservice)
-- ---------------------------------------------------------------------
INSERT INTO ansprechpartner (ansprechpartner_id, vorname, nachname, strasse, plz, email, telefon, einrichtung_id) VALUES
(1, 'Sabine', 'Neumann', 'Unter den Linden 6', '10117', 'sabine.neumann@hu-berlin.de', '+49 30 2093 1111', 1),
(2, 'Markus', 'Zimmermann', 'Straße des 17. Juni 135', '10623', 'markus.zimmermann@tu-berlin.de', '+49 30 3140 2222', 2),
(3, 'Claudia', 'Bauer', 'Arcisstraße 21', '80333', 'claudia.bauer@tum.de', '+49 89 2890 3333', 3);

-- ---------------------------------------------------------------------
-- 4. Mentoren und Bearbeiter (Wissenschaftliche Begleitung & PtJ)
-- ---------------------------------------------------------------------
INSERT INTO mentor (mentor_id, vorname, nachname, email, telefon) VALUES
(1, 'Prof. Dr. Thomas', 'Lehmann', 'thomas.lehmann@hu-berlin.de', '+49 30 2093 9901'),
(2, 'Dr. Sarah', 'Kaufmann', 'sarah.kaufmann@biotech-innovations.de', '+49 89 5566 7788');

INSERT INTO bearbeiter (bearbeiter_id, vorname, nachname, email) VALUES
(1, 'Michael', 'Braun', 'michael.braun@ptj.de'),
(2, 'Katharina', 'Koch', 'katharina.koch@ptj.de');

-- ---------------------------------------------------------------------
-- 5. Gründungsteams
-- ---------------------------------------------------------------------
INSERT INTO gruendungsteam (team_id, team_name, einrichtung_id) VALUES
(1, 'FemTech Diagnostics', 2), -- Team 1 (TU Berlin) -> EXIST-Women[cite: 5]
(2, 'GreenCycle Solutions', 1), -- Team 2 (HU Berlin) -> EXIST-Gründungsstipendium[cite: 5]
(3, 'QuantumBit Technologies', 3); -- Team 3 (TU München) -> EXIST-Forschungstransfer[cite: 5]

-- ---------------------------------------------------------------------
-- 6. Gründer:innen (Teammitglieder und Qualifikationsstatus)
-- ---------------------------------------------------------------------
INSERT INTO gruender (gruender_id, vorname, nachname, geburtsdatum, strasse, plz, email, telefon, nationalitaet, anzahl_kinder, hochschulstatus, team_id) VALUES
-- Team 1: EXIST-Women (Einzelgründerin)
(1, 'Clara', 'Richter', '1999-05-14', 'Kantstraße 42', '10623', 'clara.richter@gmail.com', '+49 170 1122334', 'Deutsch', 0, 'Wissenschaftliche Mitarbeiterin', 1),

-- Team 2: EXIST-Gründungsstipendium (2-Personen-Team)
(2, 'Lukas', 'Weber', '1997-11-20', 'Invalidenstraße 110', '10115', 'lukas.weber@outlook.com', '+49 171 2233445', 'Deutsch', 0, 'Absolvent', 2),
(3, 'Maximilian', 'Becker', '1998-03-08', 'Chausseestraße 25', '10115', 'max.becker@posteo.de', '+49 172 3344556', 'Österreichisch', 1, 'Student', 2),

-- Team 3: EXIST-Forschungstransfer (DeepTech-Team, 3 Personen)
(4, 'Dr. Elena', 'Hoffmann', '1990-09-02', 'Barer Straße 15', '80333', 'elena.hoffmann@tum-lab.de', '+49 173 4455667', 'Deutsch', 2, 'Postdoc / Gruppenleiterin', 3),
(5, 'Jan', 'Vogel', '1994-01-19', 'Türkenstraße 80', '80333', 'jan.vogel@tum.de', '+49 174 5566778', 'Deutsch', 0, 'Promovierender', 3),
(6, 'Florian', 'Schneider', '1992-07-30', 'Schellingstraße 3', '80333', 'florian.schneider@tum.de', '+49 175 6677889', 'Schweizerisch', 0, 'Absolvent', 3);

-- ---------------------------------------------------------------------
-- 7. Dokumente (Simulation von Dateiuploads als Binärdaten)
-- ---------------------------------------------------------------------
INSERT INTO dokumente (dokument_id, dateiname, dateityp, datei) VALUES
-- Übergreifende Antragsformulare
(1, 'antragsformular_femtech.pdf', 'application/pdf', CAST('DUMMY_PDF_FEMTECH_FORMULAR' AS BINARY)),
(2, 'antragsformular_greentech.pdf', 'application/pdf', CAST('DUMMY_PDF_GREENTECH_FORMULAR' AS BINARY)),
(3, 'antragsformular_quantumbit.pdf', 'application/pdf', CAST('DUMMY_PDF_QUANTUM_FORMULAR' AS BINARY)),

-- Programmspezifische Pflichtdokumente
(4, 'motivationspapier_richter.pdf', 'application/pdf', CAST('DUMMY_PDF_MOTIVATION_RICHTER' AS BINARY)),
(5, 'ideenpapier_greentech.pdf', 'application/pdf', CAST('DUMMY_PDF_IDEENPAPIER_GREENTECH' AS BINARY)),
(6, 'projektbeschreibung_quantumbit.pdf', 'application/pdf', CAST('DUMMY_PDF_PROJEKTBESCHREIBUNG_QUANTUM' AS BINARY)),
(7, 'businessplan_quantumbit.pdf', 'application/pdf', CAST('DUMMY_PDF_BUSINESSPLAN_QUANTUM' AS BINARY)),

-- Lebensläufe der Gründer:innen
(8, 'cv_clara_richter.pdf', 'application/pdf', CAST('DUMMY_PDF_CV_RICHTER' AS BINARY)),
(9, 'cv_lukas_weber.pdf', 'application/pdf', CAST('DUMMY_PDF_CV_WEBER' AS BINARY)),
(10, 'cv_maximilian_becker.pdf', 'application/pdf', CAST('DUMMY_PDF_CV_BECKER' AS BINARY)),
(11, 'cv_elena_hoffmann.pdf', 'application/pdf', CAST('DUMMY_PDF_CV_HOFFMANN' AS BINARY)),
(12, 'cv_jan_vogel.pdf', 'application/pdf', CAST('DUMMY_PDF_CV_VOGEL' AS BINARY)),
(13, 'cv_florian_schneider.pdf', 'application/pdf', CAST('DUMMY_PDF_CV_SCHNEIDER' AS BINARY)),

-- Dateianhang zu Gutachternotizen
(14, 'nachforderung_finanzierung_anmerkungen.pdf', 'application/pdf', CAST('DUMMY_PDF_AUDIT_NOTES' AS BINARY));

-- ---------------------------------------------------------------------
-- 8. Zuordnung der Lebensläufe zu den Gründer:innen
-- ---------------------------------------------------------------------
INSERT INTO lebenslauf (gruender_id, dokument_id) VALUES
(1, 8),
(2, 9),
(3, 10),
(4, 11),
(5, 12),
(6, 13);

-- ---------------------------------------------------------------------
-- 9. Förderanträge (Haupttabelle)
-- ---------------------------------------------------------------------
INSERT INTO antrag (antrag_id, gruendungstitel, status, programm, einreichungsdatum, antragsformular_id, mentor_id, team_id, bearbeiter_id, einrichtung_id) VALUES
-- Antrag 1: EXIST-Women (neu eingereicht, noch kein Bearbeiter zugewiesen)
(1, 'FemTech Diagnostics', 'eingereicht', 'exist_women', '2026-05-10', 1, NULL, 1, NULL, 2),

-- Antrag 2: EXIST-Gründungsstipendium (in Prüfung, Nachbesserung erforderlich)
(2, 'GreenCycle Analytics', 'in_pruefung', 'exist_gruendungsfoerderung', '2026-04-18', 2, 1, 2, 1, 1),

-- Antrag 3: EXIST-Forschungstransfer (erfolgreich bewilligt)
(3, 'QuantumBit Computing Systems', 'bewilligt', 'exist_forschungstransfer', '2026-02-01', 3, 2, 3, 2, 3);

-- ---------------------------------------------------------------------
-- 10. Programmspezifische Tabellen
-- ---------------------------------------------------------------------
-- EXIST-Women
INSERT INTO exist_women (antrag_id, motivationspapier_id) VALUES
(1, 4);

-- EXIST-Gründungsförderung
INSERT INTO exist_gruendungsfoerderung (antrag_id, ideenpapier_id) VALUES
(2, 5);

-- EXIST-Forschungstransfer
INSERT INTO exist_forschungstransfer (antrag_id, projektbeschreibung_id, businessplan_id) VALUES
(3, 6, 7);

-- ---------------------------------------------------------------------
-- 11. Details zur Gründungsidee
-- ---------------------------------------------------------------------
INSERT INTO gruendungsidee (antrag_id, titel, bereich, unternehmen) VALUES
(1, 'KI-gestützte Hormondiagnostik für Frauen', 'MedTech / Digital Health', 'FemTech Diagnostics UG (haftungsbeschränkt) i.G.'),
(2, 'Automatisierte CO2-Bilanzierung für den Mittelstand', 'CleanTech / Software', 'GreenCycle Solutions GmbH i.G.'),
(3, 'Fehlertolerante Quantenprozessor-Architektur', 'DeepTech / Hardware', 'QuantumBit Technologies GmbH');

-- ---------------------------------------------------------------------
-- 12. Notizen und Gutachterkommentare
-- ---------------------------------------------------------------------
INSERT INTO notiz (antrag_id, zeitstempel, inhalt, dokument_id) VALUES
(2, '2026-04-25 10:15:00', 'Die Marktanalyse im Ideenpapier ist sehr gut gelungen. Bitte jedoch die Kostentabelle auf Seite 12 präzisieren.', 14),
(3, '2026-02-28 14:30:00', 'Gutachten der externen Fachjury liegt vor: Herausragende technologische Basis, Antrag wird zur Bewilligung empfohlen.', NULL);

-- ---------------------------------------------------------------------
-- 13. Status-Historie der Anträge (Audit-Trail)
-- ---------------------------------------------------------------------
INSERT INTO antrag_status_historie (antrag_id, bearbeiter_id, alter_status, neuer_status, aenderungsdatum) VALUES
-- Statusänderungen für Antrag 2
(2, 1, 'eingereicht', 'in_pruefung', '2026-04-20 09:00:00'),

-- Statusänderungen für Antrag 3 (von Einreichung bis Bewilligung)
(3, 2, 'eingereicht', 'in_pruefung', '2026-02-05 11:00:00'),
(3, 2, 'in_pruefung', 'bewilligt', '2026-03-01 16:45:00');

-- ---------------------------------------------------------------------
-- 14. Benutzerkonten und Rollenverwaltung (RBAC)
-- ---------------------------------------------------------------------
INSERT INTO benutzer (benutzer_id, email, passwort, rolle, ansprechpartner_id, gruender_id, bearbeiter_id, ist_aktiv) VALUES
-- Zugänge für Ansprechpartner (ehemals Forschungseinrichtungen)
(1, 'sabine.neumann@hu-berlin.de', 'PasswordHash#HU2026!', 'ansprechpartner', 1, NULL, NULL, TRUE),
(2, 'markus.zimmermann@tu-berlin.de', 'PasswordHash#TU2026!', 'ansprechpartner', 2, NULL, NULL, TRUE),

-- Zugänge für Gründer:innen (ehemals Gründerteams)
(3, 'clara.richter@gmail.com', 'TeamHash#Women2026', 'gruender', NULL, 1, NULL, TRUE),
(4, 'lukas.weber@outlook.com', 'TeamHash#Green2026', 'gruender', NULL, 2, NULL, TRUE),
-- 注意：Dr. Elena Hoffmann 在第 6 節的設定中是 gruender_id = 4
(5, 'elena.hoffmann@tum-lab.de', 'TeamHash#Quantum2026', 'gruender', NULL, 4, NULL, TRUE),

-- Zugänge für PtJ-Bearbeiter:innen (bleibt unverändert)
(6, 'michael.braun@ptj.de', 'AdminSecure#PtJ2026', 'bearbeiter', NULL, NULL, 1, TRUE),
(7, 'katharina.koch@ptj.de', 'AdminSecure#PtJ2026b', 'bearbeiter', NULL, NULL, 2, TRUE);


