import streamlit as st
from datetime import date
from database.connection import get_connection
from components.upload import uploade_file

#Formular für die Gründungsförderung
st.title("Antrag exist forschungstransfer")

#Uploader für Files welche benötigt werden um das Formular zu vervollständigen. Z.B. Lebenslauf
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

    team_id = st.number_input("Team ID",min_value=1,step=1)
    bereich = st.text_input("Technischer Bereich")
    unternehmen = st.selectbox("Unternehmen bereits als Kapitalgesellschaft gegründet?",
                               options = ["Nein", "Ja"])
    #Dropdown für die Liste an Einrichtungen
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT einrichtung_id, name FROM forschungseinrichtung")
    einrichtung_liste = cursor.fetchall()
    cursor.close()
    connection.close()
    einrichtung_dict = {
        f"{row[0]} - {row[1]}": row[0]
        for row in einrichtung_liste
    }
    selected_einrichtung_label = st.selectbox(
        "ID & Einrichtung",
        options=["Bitte wählen..."] + list(einrichtung_dict.keys())
    )
    if selected_einrichtung_label != "Bitte wählen...":
        einrichtung_id= einrichtung_dict[selected_einrichtung_label]
    else:
        einrichtung_id = None
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
