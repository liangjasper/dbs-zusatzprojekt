import streamlit as st
from database.benutzer import benutzer_anmelden, ansprechpartner_anlegen, bearbeiter_anlegen, gruender_anlegen
from database.connection import get_connection
from datetime import datetime, date
from components.form_values import form_value_ansprechpartner, form_value

#-------------------------------------------------------------------------------
# anmeldung.py ist für die Anmeldung und Registrierung zuständig.
# Es gibt Formulare für das Registrieren als Benutzer mit einer spezifischen Rolle "Ansprechpartner", "Bearbeiter", "Gründer"
# Nach der Registrierung kann man sich mit seiner angegebenen E-Mail und dem Passwort anmelden und erhält Zugriff auf die Funktionen die in profil.py definiert sind
#-------------------------------------------------------------------------------

st.title("Anmeldung")

#gibt das Anmeldeformular aus, wenn noch niemand eingeloggt ist und speichert die Anmeldung als session_state und updatet in der Datenbank Tabelle: "benutzer" die Spalte: "letzer_login"
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
            if st.session_state["rolle"] == "bearbeiter":
                st.session_state["bearbeiter_id"]=benutzer["bearbeiter_id"]
            elif st.session_state["rolle"] == "gruender":
                st.session_state["gruender_id"]=benutzer["gruender_id"]
            elif st.session_state["rolle"] == "ansprechpartner":
                st.session_state["ansprechpartner_id"] = benutzer["ansprechpartner_id"]

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






# Registriert einen neuen Benutzer je nach eingetragener Rolle.
# Ein Eintrag in einer der Tabellen von "ansprechpartner", "gruenderteam", "bearbeiter" wird erstellt
# und die ID wird mit in die benutzer Tabelle übernommen und ein Eintrag angelegt
st.title("Registrieren")

rolle_registrierung = st.selectbox(
    "Rolle",
    ["Ansprechpartner", "gruender", "bearbeiter"]
)

if rolle_registrierung == "Ansprechpartner":
    with st.form("form_ansprechpartner"):
        email = st.text_input("E-Mail")
        passwort = st.text_input(
            "Passwort",
            type="password"
        )

        vorname = st.text_input("Vorname")
        nachname = st.text_input("Nachname")
        strasse = st.text_input("Strasse")
        telefon = st.text_input("Telefon")

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT plz, ort FROM plz_ort")

        plz_liste = cursor.fetchall()
        cursor.close()
        connection.close()

        plz_dict = {
            f"{row[0]} - {row[1]}": row[0]
            for row in plz_liste
        }

        selected_plz_label = st.selectbox(
            "Postleitzahl & Ort",
            options=[
                "Bitte wählen..."
            ] + list(plz_dict.keys())
        )

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
            options=[
                "Bitte wählen..."
            ] + list(einrichtung_dict.keys())
        )

        registrieren = st.form_submit_button("Registrieren")

    if registrieren:

        if selected_plz_label != "Bitte wählen...":
            plz = plz_dict[selected_plz_label]
        else:
            plz = None

        if selected_einrichtung_label != "Bitte wählen...":
            einrichtung_id = einrichtung_dict[
                selected_einrichtung_label
            ]
        else:
            einrichtung_id = None

        form_value_ansprechpartner = {
            "Email": email,
            "Passwort": passwort,
            "Vorname": vorname,
            "Nachname": nachname,
            "Strasse": strasse,
            "Plz": plz,
            "Telefon": telefon,
            "Einrichtung_id": einrichtung_id
        }

        ansprechpartner_anlegen(
            form_value_ansprechpartner,
            "Ansprechpartner"
        )

        st.success("Registrierung als Ansprechpartner erfolgreich")



elif rolle_registrierung == "bearbeiter":

    with st.form("form_bearbeiter"):
        email = st.text_input("E-Mail")
        passwort = st.text_input("Passwort",type="password")
        vorname = st.text_input("Vorname")
        nachname = st.text_input("Nachname")

        registrieren = st.form_submit_button("Registrieren")

    if registrieren:

        bearbeiter_anlegen(
            vorname,
            nachname,
            email,
            passwort,
            "bearbeiter"
        )

        st.success("Registrierung als Bearbeiter erfolgreich")


elif rolle_registrierung == "gruender":

    with st.form("form_gruender"):


        email = st.text_input("E-Mail")

        passwort = st.text_input("Passwort", type="password")
        vorname = st.text_input("Vorname")
        nachname = st.text_input("Nachname")
        geburtsdatum = st.date_input(
            "Geburtsdatum",
            None,
            min_value=date(1900, 1, 1),
            max_value=datetime.now(),
            format="YYYY-MM-DD"
        )

        strasse = st.text_input("Strasse")
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT plz, ort FROM plz_ort")
        plz_liste = cursor.fetchall()
        cursor.close()
        connection.close()

        plz_dict = {
            f"{row[0]} - {row[1]}": row[0]
            for row in plz_liste
        }

        selected_plz_label = st.selectbox(
            "Postleitzahl & Ort",
            options=[
                "Bitte wählen..."
            ] + list(plz_dict.keys())
        )


        telefon = st.text_input("Telefon")
        nationalitaet = st.text_input("Nationalität")

        anzahl_kinder = st.selectbox(
            "Anzahl der Kinder",
            [None,0,1,2,3,4,5,6,7,8,9])

        hochschulstatus = st.selectbox(
            "Hochschulstatus",
            [
                "",
                "StudentIn",
                "AbsolventIn",
                "Promovierende/r",
                "Wissenschaftliche/r MitarbeiterIn",
                "Postdoc / GruppenleiterIn",
            ],
        )

        registrieren = st.form_submit_button("Registrieren")


    if registrieren:

        if selected_plz_label != "Bitte wählen...":
            plz = plz_dict[selected_plz_label]
        else:
            plz = None

        form_value = {
            "Email": email,
            "Passwort": passwort,
            "Vorname": vorname,
            "Nachname": nachname,
            "Geburtsdatum": geburtsdatum,
            "Strasse": strasse,
            "Plz": plz,
            "Telefon": telefon,
            "Nationalitaet": nationalitaet,
            "Anzahl_kinder": anzahl_kinder,
            "Hochschulstatus": hochschulstatus
        }

        gruender_anlegen(form_value,"gruender")
        st.success("Registrierung als Gründer erfolgreich")
