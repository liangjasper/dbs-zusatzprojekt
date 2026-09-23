import streamlit as st
from database.benutzer import benutzer_anmelden, forschungseinrichtung_anlegen, bearbeiter_anlegen, gruender_anlegen
from database.benutzer import benutzer_anlegen
from database.connection import get_connection
from datetime import datetime, date

#Seite die für die Anmeldung und Registrierung zuständig ist.
st.title("Anmeldung")

#gibt das Anmeldeformular aus, wenn noch niemand eingeloggt ist und Speichert die Anmeldung als session_state und updatet in der Datenbank Tabelle: "benutzer" die Spalte: "letzer_login"
if not st.session_state.get("eingeloggt", False):
    email = st.text_input("E-Mail")
    passwort = st.text_input(
    "Passwort",
    type = "password"
    )
    if st.button("Anmelden"):
        benutzer = benutzer_anmelden(
            email,
            passwort
        )
        st.write("Benutzer gefunden:", benutzer)
        if benutzer is not None:
            st.session_state["eingeloggt"] = True
            st.session_state["benutzer_id"] = benutzer["benutzer_id"]
            st.session_state["email"] = benutzer["email"]
            st.session_state["rolle"] = benutzer["rolle"]

            connection = get_connection()
            cursor = connection.cursor()
            sql = """
                UPDATE benutzer
                SET letzter_login = now()
                WHERE benutzer_id = %s
            """
            cursor.execute(sql, (benutzer["benutzer_id"],))
            connection.commit()
            cursor.close()
            connection.close()

            st.rerun()
        else:
            st.error(
                "E-Mail oder Passwort ist falsch."
            )
else:
    st.success(f"Erfolgreich angemeldet mit {st.session_state['email']}")

#Registriert einen neuen Benutzer je nach eingetragener Rolle. Ein Eintrag in einer der Tabellen von "forschungseinrichtung", "gruenderteam", "bearbeiter" wird erstellt und die ID wird mit in die benutzer Tabelle übernommen und ein Eintrag angelegt
st.title("Registrieren")
email_registrierung = st.text_input("E-Mail1")
passwort_registrierung = st.text_input(
    "Passwort1",
    type="password"
)
rolle_registrierung = st.selectbox("Rolle", ["forschungseinrichtung", "Gründer", "bearbeiter"])
if rolle_registrierung == "forschungseinrichtung":
    url_registrierung = st.text_input("Url")
    name_registrierung = st.text_input("Name")

if rolle_registrierung == "bearbeiter":
    vorname_registrierung = st.text_input("Vorname")
    nachname_registrierung = st.text_input("Nachname")


form_value = {
    "Vorname": None
    ,"Nachname": None
    ,"Geburtsdatum": None
    ,"Strasse": None
    ,"Plz": None
    ,"Email": None
    ,"Telefon": None
    ,"Nationalitaet": None
    ,"Anzahl_kinder": None
    ,"Hochschulstatus": None
    ,"Team_id": None
}

if rolle_registrierung == "Gründer":
    form_value["Vorname"] = st.text_input("Vorname")
    form_value["Nachname"] = st.text_input("Nachname")
    form_value["Geburtsdatum"] = st.date_input("Geburtsdatum", None, min_value=date(1900, 1, 1),
                                               max_value=datetime.now(), format="YYYY-MM-DD")
    form_value["Strasse"] = st.text_input("Strasse")
    form_value["Plz"] = st.text_input("Plz")
    form_value["Email"] = st.text_input("Email")
    form_value["Telefon"] = st.text_input("Telefon")
    form_value["Nationalitaet"] = st.text_input("Nationalität")
    form_value["Anzahl_kinder"] = st.selectbox("Anzahl der kinder", [None, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    form_value["Hochschulstatus"] = st.selectbox("Hochschulstatus", ["", "StudentIn", "AbsolventIn"])

if st.button("Registrieren"):
    if rolle_registrierung == "forschungseinrichtung":
        forschungseinrichtung_anlegen(
            name_registrierung,
            url_registrierung,
            email_registrierung,
            passwort_registrierung,
            rolle_registrierung,
        )
        st.success("Registrierung der Forschungseinrichtung erfolgreich")

    if rolle_registrierung == "bearbeiter":
        bearbeiter_anlegen(
            vorname_registrierung,
            nachname_registrierung,
            email_registrierung,
            passwort_registrierung,
            rolle_registrierung,
        )
        st.success("Registrierung als Bearbeiter/in erfolgreich")

    if rolle_registrierung == "Gründer":
        gruender_anlegen(
            form_value,
            email_registrierung,
            passwort_registrierung,
            rolle_registrierung
        )
        st.warning("Noch nicht implementiert")