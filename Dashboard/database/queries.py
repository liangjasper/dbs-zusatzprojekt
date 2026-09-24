# Inserts für Anträge und alle dazugehörigen Tabellen


# Python Beispielscode:

# Dropdown-Menü für Ansprechpartner
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

