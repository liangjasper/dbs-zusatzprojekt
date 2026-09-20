import streamlit as st
from database.benutzer import benutzer_anmelden
from database.benutzer import benutzer_anlegen

st.title("Anmeldung")
email = st.text_input("E-Mail")
passwort = st.text_input(
    "Passwort",
    type="password"
)

if st.button("Anmelden"):
    benutzer = benutzer_anmelden(
        email,
        passwort
    )
    if benutzer is not None:
        st.session_state["eingeloggt"] = True
        st.session_state["benutzer_id"] = benutzer["id"]
        st.session_state["email"] = benutzer["email"]

        st.success("Erfolgreich angemeldet!")
        st.rerun()
    else:
        st.error(
            "E-Mail oder Passwort ist falsch."
        )

st.title("Registrieren")
email_registrierung = st.text_input("E-Mail1")
passwort_registrierung = st.text_input(
    "Passwort1",
    type="password"
)
if st.button("Registrieren"):
    benutzer_anlegen(
        email_registrierung,
        passwort_registrierung
    )