import streamlit as st
from database.connection import get_connection
from components.upload import uploade_file
import pandas as pd
from components.build_join_team import build_team
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
st.write("Hier stehen bald weitere Perönlichen Daten")

if st.session_state["rolle"] == "gruender":
    st.title("Team")

    connection = get_connection()
    df = pd.read_sql("SELECT * FROM forschungseinrichtung", connection)
    st.title("Forschungseinrichtungen")
    st.dataframe(df, use_container_width=True)
    connection.close()
    with st.form("team_form"):

        einrichtung_id = st.number_input(
            "Forschungseinrichtungs ID",
            min_value=1,
            step=1
        )
        submitted = st.form_submit_button("Team gründen")
        print("submitted =", submitted)
        if submitted:
            team_id = build_team(einrichtung_id)
            st.success(f"Team gegründet! Team-ID: {team_id}")

if st.button("Team beitreten"):
    st.warning("Funktion in bearbeitung")

    # Uploader für Files welche benötigt werden um das Formular zu vervollständigen. Z.B. Lebenslauf
    uploaded_file = st.file_uploader(
        "Lebenslauf hochladen",
        type=["pdf", "docx", "png", "jpg"]
    )
    if uploaded_file is not None:
        st.success(f"{uploaded_file.name} wurde hochgeladen!")

        # Funktion aus der neuen Datei aufrufen
        success = uploade_file(uploaded_file)

        if success:
            st.success("Dokument wurde erfolgreich in der Datenbank gespeichert!")

if st.session_state["rolle"] == "Bearbeiter":
    if st.button(""):
        st.warning("Funktion in bearbeitung")
    st.title("Zusammenfassungen")
    st.title("Notiz erstellen")
    st.title("")

if st.session_state["rolle"] == "ansprechpartner":
    st.title("Mentor anlegen")
