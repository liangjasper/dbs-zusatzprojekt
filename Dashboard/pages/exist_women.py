import streamlit as st
from datetime import datetime, date
from database.connection import get_connection
from components.upload import uploade_file

#Formular für die Gründungsförderung
st.title("Antrag exist women")
with st.form("antrag_form"):

    gruendungstitel = st.text_input("Gründungstitel")

    antragsformular_id = st.number_input(
        "Antragsformular ID",
        min_value=1,
        step=1
    )

    mentor_id = st.number_input(
        "Mentor ID",
        min_value=1,
        step=1
    )

    team_id = st.number_input(
        "Team ID",
        min_value=1,
        step=1
    )

    einrichtung_id = st.number_input(
        "Einrichtung ID",
        min_value=1,
        step=1
    )

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
               antragsformular_id,
               mentor_id,
               team_id,
               einrichtung_id)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
              """

        werte = (
            gruendungstitel,
            "eingereicht",
            "exist_women",
            date.today().strftime("%Y-%m-%d"),
            antragsformular_id,
            mentor_id,
            team_id,
            einrichtung_id
        )

        cursor.execute(sql, werte)
        connection.commit()

        st.success("Antrag wurde erfolgreich eingereicht.")

        cursor.close()
        connection.close()
#Uploader für Files welche benötigt werden um das Formular zu vervollständigen. Z.B. Lebenslauf
uploaded_file = st.file_uploader(
        "Dokumente hochladen",
        type=["pdf", "docx", "png", "jpg"]
    )

if uploaded_file is not None:
    st.success(f"{uploaded_file.name} wurde hochgeladen!")

    # Funktion aus der neuen Datei aufrufen
    success = uploade_file(uploaded_file, get_connection)

    if success:
        st.success("Dokument wurde erfolgreich in der Datenbank gespeichert!")

st.write("Informationen zu EXIST Women.")
