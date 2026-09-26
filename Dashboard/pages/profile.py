import streamlit as st
from components.upload import uploade_file, lebenslauf_eintrag
from components.build_join_team import build_team,join_team
from database.connection import get_connection

st.title("Profil")
if st.button("Abmelden"):
    st.session_state["eingeloggt"] = None
    st.session_state["benutzer_id"] = None
    st.session_state["email"] = None
    st.session_state["rolle"] = None
    st.rerun()

st.title("Persönliche Daten")

st.write("Benutzer: ", st.session_state["benutzer_id"])
st.write("Email: ", st.session_state["email"])
st.write("Rolle: ",st.session_state["rolle"])
if st.session_state["rolle"] == "bearbeiter":
    st.write("Bearbeiter ID: ",st.session_state["bearbeiter_id"])
elif st.session_state["rolle"] == "gruender":
    st.write("Gründer ID:" ,st.session_state["gruender_id"])
elif st.session_state["rolle"] == "ansprechpartner":
    st.write("Ansprechpartner ID" ,st.session_state["ansprechpartner_id"])
st.write("Hier stehen bald weitere Perönlichen Daten")

#--------------Funktionen im Profil des Gründers--------------------------------
if st.session_state["rolle"] == "gruender":
    st.title("Team")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT einrichtung_id, name FROM forschungseinrichtung"
    )

    einrichtung_liste = cursor.fetchall()

    cursor.close()
    connection.close()

    einrichtung_dict = {
        f"{row[0]} - {row[1]}": row[0]
        for row in einrichtung_liste
    }
    st.write("Hier kannst du ein neues Team gründen")
    with st.form("team_form"):

        selected_einrichtung_label = st.selectbox(
            "Forschungseinrichtung",
            options=["Bitte wählen..."] + list(einrichtung_dict.keys())
        )
        team_name=st.text_input("Team Name")
        submitted = st.form_submit_button("Team gründen")

        if submitted:

            if selected_einrichtung_label == "Bitte wählen...":
                st.error("Bitte wähle eine Forschungseinrichtung aus.")

            else:
                einrichtung_id = einrichtung_dict[selected_einrichtung_label]

                team_id = build_team(einrichtung_id,team_name)

                st.success(
                    f"Team gegründet! Team-ID: {team_id, team_name}"
                )
    st.write("Hier kannst du einem Team beitreten")
    with st.form("join_team_form"):
        team_id = st.number_input(
            "Team-ID",
            min_value=1,
            step=1
        )

        submitted = st.form_submit_button("Team beitreten")

        if submitted:
            join_team(team_id)

            st.success(
                f"Du bist Team {team_id} beigetreten!"
            )

    #Uploader für den Lebenslauf
    uploaded_file = st.file_uploader(
        "Lebenslauf hochladen",
        type=["pdf", "docx", "png", "jpg"]
    )
    if uploaded_file is not None:
        st.success(f"{uploaded_file.name} wurde hochgeladen!")

        # Funktion aus der neuen Datei aufrufen

        success = uploade_file(uploaded_file)
        lebenslauf_eintrag(cursor.lastrowid)
        if success:
            st.success("Dokument wurde erfolgreich in der Datenbank gespeichert!")

#-------------- Funktionen im Profil des Bearbeiters--------------------
if st.session_state["rolle"] == "Bearbeiter":
    if st.button(""):
        st.warning("Funktion in bearbeitung")
    st.title("Zusammenfassungen")
    st.title("Notiz erstellen")
    st.title("")
#------------- Funktionen im Profil des Ansprechpartners-----------------------------
if st.session_state["rolle"] == "ansprechpartner":
    st.title("Mentor anlegen")
    with st.form("mentor_form"):
        vorname = st.text_input("Vorname")
        nachname = st.text_input("Nachname")
        email = st.text_input("E-Mail")
        telefon = st.text_input("Telefon")

        speichern = st.form_submit_button("Mentor speichern")

        if speichern:
            if not vorname or not nachname or not email or not telefon:
                st.warning("Bitte alle Felder ausfüllen.")
            else:
                try:
                    connection = get_connection()
                    cursor = connection.cursor()

                    sql = """
                          INSERT INTO mentor
                              (vorname, nachname, email, telefon)
                          VALUES (%s, %s, %s, %s) \
                          """

                    cursor.execute(sql,( vorname, nachname, email, telefon))
                    connection.commit()

                    st.success("Mentor wurde erfolgreich angelegt.")

                except Exception as e:
                    st.error(f"Fehler beim Speichern: {e}")

                finally:
                    cursor.close()
                    connection.close()

