# Inserts für Anträge und alle dazugehörigen Tabellen

# =====================================================================
# 1. Benutzer & Rollen (Registrierung)
# =====================================================================

# Forschungseinrichtung anlegen
sql = """
    INSERT INTO forschungseinrichtung (name, url) 
    VALUES (%s, %s)
"""
cursor.execute(sql, (name, url))


# Ansprechpartner anlegen
sql = """
    INSERT INTO ansprechpartner (vorname, nachname, strasse, plz, email, telefon, einrichtung_id) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
cursor.execute(sql, (vorname, nachname, strasse, plz, email, telefon, einrichtung_id))


# Bearbeiter anlegen (PtJ)
sql = """
    INSERT INTO bearbeiter (vorname, nachname, email) 
    VALUES (%s, %s, %s)
"""
cursor.execute(sql, (vorname, nachname, email))


# Benutzerkonto anlegen (Je nach Rolle eine der IDs mitgeben, der Rest ist None)
sql = """
    INSERT INTO benutzer (email, passwort, rolle, ansprechpartner_id, gruender_id, bearbeiter_id) 
    VALUES (%s, %s, %s, %s, %s, %s)
"""
cursor.execute(sql, (email, passwort, rolle, ansprechpartner_id, gruender_id, bearbeiter_id))


# =====================================================================
# 2. Teams & Gründer
# =====================================================================

# Neues Gründungsteam erstellen (WICHTIG: team_name darf nicht leer sein)
sql = """
    INSERT INTO gruendungsteam (team_name, einrichtung_id) 
    VALUES (%s, %s)
"""
cursor.execute(sql, (team_name, einrichtung_id))


# Gründer anlegen
sql = """
    INSERT INTO gruender (
        vorname, nachname, geburtsdatum, strasse, plz, 
        email, telefon, nationalitaet, anzahl_kinder, hochschulstatus, team_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
cursor.execute(sql, (
    vorname, nachname, geburtsdatum, strasse, plz,
    email, telefon, nationalitaet, anzahl_kinder, hochschulstatus, team_id
))


# =====================================================================
# 3. Dokumente (Datei-Upload)
# =====================================================================

# Dokument speichern (Binärdaten aus Streamlit)
sql = """
    INSERT INTO dokumente (dateiname, dateityp, datei) 
    VALUES (%s, %s, %s)
"""
cursor.execute(sql, (dateiname, dateityp, datei_als_bytes))


# Lebenslauf zu Gründer zuordnen (überschreibt alten Lebenslauf automatisch)
sql = """
    INSERT INTO lebenslauf (gruender_id, dokument_id) 
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE dokument_id = VALUES(dokument_id)
"""
cursor.execute(sql, (gruender_id, dokument_id))


# =====================================================================
# 4. Die EXIST-Anträge (Das Kernstück)
# =====================================================================

# 1. Haupt-Antrag erstellen (Muss immer als Erstes gemacht werden)
sql = """
    INSERT INTO antrag (
        gruendungstitel, status, programm, einreichungsdatum, 
        antragsformular_id, mentor_id, team_id, bearbeiter_id, einrichtung_id
    ) VALUES (%s, 'eingereicht', %s, CURDATE(), %s, %s, %s, %s, %s)
"""
cursor.execute(sql, (
    gruendungstitel, programm, antragsformular_id, mentor_id,
    team_id, bearbeiter_id, einrichtung_id
))
# Danach antrag_id holen: antrag_id = cursor.lastrowid


# 2a. Spezifische Tabelle: EXIST-Women
sql = """
    INSERT INTO exist_women (antrag_id, motivationspapier_id) 
    VALUES (%s, %s)
"""
cursor.execute(sql, (antrag_id, motivationspapier_id))


# 2b. Spezifische Tabelle: EXIST-Gründungsstipendium
sql = """
    INSERT INTO exist_gruendungsfoerderung (antrag_id, ideenpapier_id) 
    VALUES (%s, %s)
"""
cursor.execute(sql, (antrag_id, ideenpapier_id))


# 2c. Spezifische Tabelle: EXIST-Forschungstransfer
sql = """
    INSERT INTO exist_forschungstransfer (antrag_id, projektbeschreibung_id, businessplan_id) 
    VALUES (%s, %s, %s)
"""
cursor.execute(sql, (antrag_id, projektbeschreibung_id, businessplan_id))


# Gründungsidee-Details hinzufügen
sql = """
    INSERT INTO gruendungsidee (antrag_id, titel, bereich, unternehmen) 
    VALUES (%s, %s, %s, %s)
"""
cursor.execute(sql, (antrag_id, titel, bereich, unternehmen))


# =====================================================================
# 5. Bearbeiter-Funktionen (Audit & Notizen)
# =====================================================================

# Status-Historie speichern (Audit-Trail)
sql = """
    INSERT INTO antrag_status_historie (antrag_id, bearbeiter_id, alter_status, neuer_status) 
    VALUES (%s, %s, %s, %s)
"""
cursor.execute(sql, (antrag_id, bearbeiter_id, alter_status, neuer_status))


# Notiz zum Antrag hinzufügen
sql = """
    INSERT INTO notiz (antrag_id, inhalt, dokument_id) 
    VALUES (%s, %s, %s)
"""
cursor.execute(sql, (antrag_id, inhalt, dokument_id))



# Python Beispielscode:

# Dropdown-Menü für Einrichtungen
# -------------------------------------------------------------------------
# 1. Datenbankabfrage ausführen
cursor.execute("SELECT einrichtung_id, name FROM forschungseinrichtung")
einrichtungen = cursor.fetchall()

# 2. Dictionary erstellen: Zuordnung von Name zu ID
einrichtung_dict = {row[1]: row[0] for row in einrichtungen}

# 3. Dropdown-Menü in Streamlit anzeigen
selected_einrichtung_name = st.selectbox(
    "Forschungseinrichtung auswählen",
    options=list(einrichtung_dict.keys())
)

# 4. Zugehörige ID für den INSERT-Befehl abrufen
einrichtung_id_to_save = einrichtung_dict[selected_einrichtung_name]
# -------------------------------------------------------------------------


# Dropdown-Menü für Gründer
# -------------------------------------------------------------------------
# 1. Datenbankabfrage mit JOIN ausführen
sql_team = """
    SELECT t.team_id, t.team_name, f.name 
    FROM gruendungsteam t
    LEFT JOIN forschungseinrichtung f ON t.einrichtung_id = f.einrichtung_id
"""
cursor.execute(sql_team)
teams = cursor.fetchall()

# 2. Dictionary erstellen
team_dict = {f"{row[1]} ({row[2]})" if row[2] else row[1]: row[0] for row in teams}

# 3. Dropdown-Menü in Streamlit anzeigen
selected_team_label = st.selectbox(
    "Gründungsteam auswählen",
    options=list(team_dict.keys())
)

# 4. Zugehörige ID für den INSERT-Befehl abrufen
team_id_to_save = team_dict[selected_team_label]
# -------------------------------------------------------------------------


# -------------------------------------------------------------------------
# Dropdown-Menü für Postleitzahl (PLZ) und Ort
# -------------------------------------------------------------------------
# 1. Datenbankabfrage ausführen (PLZ und zugehörigen Ort abrufen)
cursor = connection.cursor()
cursor.execute("SELECT plz, ort FROM plz_ort")
plz_liste = cursor.fetchall()

# 2. Dictionary erstellen: Zuordnung von Anzeige-Text (z.B. "10115 - Berlin") zur reinen PLZ ("10115")
plz_dict = {f"{row[0]} - {row[1]}": row[0] for row in plz_liste}

# 3. Dropdown-Menü in Streamlit anzeigen
selected_plz_label = st.selectbox(
    "Postleitzahl & Ort",
    options=["Bitte wählen..."] + list(plz_dict.keys())
)

# 4. Zugehörige PLZ für den INSERT-Befehl abrufen
if selected_plz_label != "Bitte wählen...":
    form_value["Plz"] = plz_dict[selected_plz_label]
else:
    form_value["Plz"] = None  # Oder wie du leere Eingaben abfangen möchtest
# -------------------------------------------------------------------------


# -------------------------------------------------------------------
    # Dynamisches Dropdown für Gründungsteams (gefiltert nach Einrichtung)
    # -------------------------------------------------------------------
    connection = get_connection()
    cursor = connection.cursor()

    # SQL-Abfrage: Holt nur die Teams, die zur selben Einrichtung gehören
    # wie der aktuell eingeloggte Ansprechpartner.
    sql_teams = """
        SELECT t.team_id, t.team_name 
        FROM gruendungsteam t
        JOIN ansprechpartner a ON t.einrichtung_id = a.einrichtung_id
        WHERE a.ansprechpartner_id = %s
    """
    cursor.execute(sql_teams, (st.session_state["ansprechpartner_id"],))
    team_liste = cursor.fetchall()
    cursor.close()
    connection.close()

    # Dictionary für das Dropdown-Menü erstellen
    team_dict = {
        f"ID: {row[0]} - {row[1]}": row[0]
        for row in team_liste
    }

    selected_team_label = st.selectbox(
        "Gründungsteam auswählen",
        options=["Bitte wählen..."] + list(team_dict.keys())
    )

    # team_id für den späteren INSERT-Befehl speichern
    if selected_team_label != "Bitte wählen...":
        team_id = team_dict[selected_team_label]
    else:
        team_id = None
    # -------------------------------------------------------------------


# -------------------------------------------------------------------
    # Dynamisches Dropdown für Mentoren (Alle registrierten Mentoren)
    # -------------------------------------------------------------------
    connection = get_connection()
    cursor = connection.cursor()

    # SQL-Abfrage: Holt alle Mentoren aus der Datenbank
    cursor.execute("SELECT mentor_id, vorname, nachname FROM mentor")
    mentor_liste = cursor.fetchall()

    cursor.close()
    connection.close()

    # Dictionary für das Dropdown-Menü erstellen
    mentor_dict = {
        f"ID: {row[0]} - {row[1]} {row[2]}": row[0]
        for row in mentor_liste
    }

    selected_mentor_label = st.selectbox(
        "Mentor auswählen",
        options=["Bitte wählen..."] + list(mentor_dict.keys())
    )

    # mentor_id für den späteren Datenbank-Befehl speichern
    if selected_mentor_label != "Bitte wählen...":
        mentor_id = mentor_dict[selected_mentor_label]
    else:
        mentor_id = None
    # -------------------------------------------------------------------


# -------------------------------------------------------------------
    # Übersicht der eingereichten Anträge für den Ansprechpartner
    # -------------------------------------------------------------------
    st.subheader("Übersicht: Eingereichte Anträge (Meine Einrichtung)")

    connection_antrag = get_connection()
    cursor_antrag = connection_antrag.cursor()

    # SQL-Abfrage: Holt alle Anträge, die zur Einrichtung des eingeloggten Ansprechpartners gehören
    sql_uebersicht = """
        SELECT a.antrag_id, a.gruendungstitel, a.programm, a.status, a.einreichungsdatum
        FROM antrag a
        JOIN ansprechpartner ap ON a.einrichtung_id = ap.einrichtung_id
        WHERE ap.ansprechpartner_id = %s
        ORDER BY a.einreichungsdatum DESC
    """
    cursor_antrag.execute(sql_uebersicht, (st.session_state["ansprechpartner_id"],))
    antraege = cursor_antrag.fetchall()

    cursor_antrag.close()
    connection_antrag.close()

    if antraege:
        # Daten in ein Pandas DataFrame umwandeln für eine schöne Tabellenansicht
        df_antraege = pd.DataFrame(
            antraege,
            columns=["Antrag ID", "Gründungstitel", "Programm", "Status", "Einreichungsdatum"]
        )
        # Tabelle in Streamlit anzeigen
        st.dataframe(df_antraege, use_container_width=True)
    else:
        st.info("Bisher wurden noch keine Anträge für deine Einrichtung eingereicht.")
    # -------------------------------------------------------------------


# -------------------------------------------------------------------
    # Übersicht der eingereichten Anträge für das eigene Gründungsteam
    # -------------------------------------------------------------------
    st.subheader("Übersicht: Anträge meines Teams")

    connection_antrag = get_connection()
    cursor_antrag = connection_antrag.cursor()

    # SQL-Abfrage: Holt alle Anträge, bei denen die team_id mit der team_id des Gründers übereinstimmt
    sql_uebersicht = """
        SELECT a.antrag_id, a.gruendungstitel, a.programm, a.status, a.einreichungsdatum
        FROM antrag a
        JOIN gruender g ON a.team_id = g.team_id
        WHERE g.gruender_id = %s
        ORDER BY a.einreichungsdatum DESC
    """
    cursor_antrag.execute(sql_uebersicht, (st.session_state["gruender_id"],))
    antraege = cursor_antrag.fetchall()

    cursor_antrag.close()
    connection_antrag.close()

    if antraege:
        # Daten in ein Pandas DataFrame umwandeln
        df_antraege = pd.DataFrame(
            antraege,
            columns=["Antrag ID", "Gründungstitel", "Programm", "Status", "Einreichungsdatum"]
        )
        # Tabelle anzeigen
        st.dataframe(df_antraege, use_container_width=True)
    else:
        st.info("Dein Team hat bisher noch keine Anträge eingereicht, oder du bist noch keinem Team beigetreten.")
    # -------------------------------------------------------------------



# team dropdown liste
# mentor dropdown liste
# einrichtungen vom ansprechpartner ziehen
# anträge für alle leute ziehen
# anfangen mit bearbeiter

# ansprechpartner muss noch Anträge ändern können

