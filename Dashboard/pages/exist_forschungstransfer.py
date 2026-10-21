import streamlit as st
from datetime import date
from database.connection import get_connection
from components.upload import uploade_file

#-------------------------------------------------------------------
# Diese Seite wird nur für einen benutzer mit der Rolle Ansprechpartner freigeschaltet, wenn die Person eingeloggt ist.
# Es kann ein Antrag für exist_forschungstransfer gestellt werden und alle damit verbundenen Dokumente in die Datenbank hochgeladen werden
#-------------------------------------------------------------------


# Formular für die Gründungsförderung
st.title("Antrag exist forschungstransfer")

# Uploader für Files welche benötigt werden um das Formular zu vervollständigen.
st.write("Bitte zuerst Projektbeschreibung und Businessplan hochladen")

projektbeschreibung = st.file_uploader(
    "Projektbeschreibung hochladen",
    type=["pdf", "docx", "png", "jpg"],
    key="projektbeschreibung"
)

businessplan = st.file_uploader(
    "Businessplan hochladen",
    type=["pdf", "docx", "png", "jpg"],
    key="businessplan"
)

projektbeschreibung_id = None
businessplan_id = None
if projektbeschreibung is not None:
    st.success(f"{projektbeschreibung.name} wurde hochgeladen!")

    # Funktion aus der neuen Datei aufrufen
    projektbeschreibung_id = uploade_file(projektbeschreibung)

    if projektbeschreibung_id is not None:
        st.success("Dokument wurde erfolgreich in der Datenbank gespeichert!")

if businessplan is not None:
    st.success(f"{businessplan.name} wurde hochgeladen!")

    # Funktion aus der neuen Datei aufrufen
    businessplan_id = uploade_file(businessplan)

    if businessplan_id is not None:
        st.success("Dokument wurde erfolgreich in der Datenbank gespeichert!")


connection_team = get_connection()
cursor_team = connection_team.cursor(dictionary=True)
current_user_id = st.session_state["ansprechpartner_id"]
sql_teams = f"""
    SELECT t.team_id, t.team_name, f.name AS einrichtung_name 
    FROM gruendungsteam t 
    JOIN forschungseinrichtung f ON t.einrichtung_id = f.einrichtung_id
    JOIN ansprechpartner a ON f.einrichtung_id = a.einrichtung_id
    WHERE a.ansprechpartner_id = {current_user_id}
"""
cursor_team.execute(sql_teams)
alle_teams = cursor_team.fetchall()
cursor_team.close()
connection_team.close()

team_options = {
    row["team_id"]: f"{row['team_id']} - {row['team_name']} ({row['einrichtung_name']})"
    for row in alle_teams
}

with st.form("antrag_form_forschungstransfer"):

    gruendungstitel = st.text_input("Gründungstitel")

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT mentor_id, vorname, nachname FROM mentor")
    mentor_liste = cursor.fetchall()
    cursor.close()
    connection.close()
    mentor_dict = {
        f"{row[0]} - {row[1]} - {row[2]}": row[0]
        for row in mentor_liste
    }
    selected_mentor_label = st.selectbox(
        "Mentor",
        options=["Bitte wählen..."] + list(mentor_dict.keys())
    )
    if selected_mentor_label != "Bitte wählen...":
        mentor_id = mentor_dict[selected_mentor_label]
    else:
        mentor_id = None

    # team_id = st.number_input("Team ID",min_value=1,step=1)
    team_id = st.selectbox(
        "Gründungsteam auswählen:",
        options=list(team_options.keys()),
        format_func=lambda x: team_options[x]
    )
    bereich = st.text_input("Technischer Bereich")
    unternehmen = st.selectbox("Unternehmen bereits als Kapitalgesellschaft gegründet?",
                               options = ["Nein", "Ja"])
    #Dropdown für die Liste an Einrichtungen
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    current_user_id = st.session_state["ansprechpartner_id"]
    sql_einrichtung = f"""
        SELECT f.einrichtung_id, f.name 
        FROM forschungseinrichtung f
        JOIN ansprechpartner a ON f.einrichtung_id = a.einrichtung_id
        WHERE a.ansprechpartner_id = {current_user_id}
    """
    cursor.execute(sql_einrichtung)
    einrichtung_data = cursor.fetchone()
    cursor.close()
    connection.close()

    if einrichtung_data:
        einrichtung_id = einrichtung_data["einrichtung_id"]
        st.text_input("Zugehörige Einrichtung", value=einrichtung_data["name"], disabled=True)
    else:
        einrichtung_id = None
        st.error("Keine Einrichtung für diesen Ansprechpartner gefunden.")
    speichern = st.form_submit_button("Antrag einreichen")


if speichern:

    if not gruendungstitel:
        st.warning("Bitte einen Gründungstitel eingeben.")

    else:
        connection = None
        cursor = None

        connection = get_connection()
        cursor = connection.cursor()

        sql = """
            INSERT INTO antrag
            (gruendungstitel,
            status,
            programm,
            einreichungsdatum,
            mentor_id,
            team_id,
            einrichtung_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s) \
        """

        werte = (
            gruendungstitel,
            "eingereicht",
            "exist_forschungstransfer",
            date.today().strftime("%Y-%m-%d"),
            mentor_id,
            team_id,
            einrichtung_id
        )
        cursor.execute(sql, werte)
        antrag_id=cursor.lastrowid
        sql = """
            INSERT INTO exist_forschungstransfer
            (antrag_id, projektbeschreibung_id, businessplan_id)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (antrag_id,projektbeschreibung_id,businessplan_id))

        sql = """
            INSERT INTO gruendungsidee
            (antrag_id, titel, bereich, unternehmen)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (antrag_id, gruendungstitel, bereich, unternehmen))
        connection.commit()

        st.success("Antrag wurde erfolgreich eingereicht.")
        cursor.close()
        connection.close()


st.write("Informationen zum Forschungstransfer.")
