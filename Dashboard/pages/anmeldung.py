import streamlit as st
from database.benutzer import benutzer_anmelden, ansprechpartner_anlegen, bearbeiter_anlegen, gruender_anlegen
from database.benutzer import benutzer_anlegen
from database.connection import get_connection
from datetime import datetime, date
from components.form_values import form_value_ansprechpartner, form_value
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






#Registriert einen neuen Benutzer je nach eingetragener Rolle. Ein Eintrag in einer der Tabellen von "Ansprechpartner", "gruenderteam", "bearbeiter" wird erstellt und die ID wird mit in die benutzer Tabelle übernommen und ein Eintrag angelegt
st.title("Registrieren")

rolle_registrierung = st.selectbox("Rolle", ["Ansprechpartner", "gruender", "bearbeiter"])


if rolle_registrierung == "Ansprechpartner":
    email_registrierung = st.text_input("E-Mail1")
    passwort_registrierung = st.text_input(
        "Passwort1",
        type="password"
    )
    form_value_ansprechpartner["Vorname"] = st.text_input("Vorname")
    form_value_ansprechpartner["Nachname"] = st.text_input("Nachname")
    form_value_ansprechpartner["Geburtsdatum"] = st.date_input("Geburtsdatum", None, min_value=date(1900, 1, 1),
                                               max_value=datetime.now(), format="YYYY-MM-DD")
    form_value_ansprechpartner["Strasse"] = st.text_input("Strasse")

    # Dropdown Menü für PLZ Eingabe
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
        options=["Bitte wählen..."] + list(plz_dict.keys())
    )
    if selected_plz_label != "Bitte wählen...":
        form_value_ansprechpartner["Plz"] = plz_dict[selected_plz_label]
    else:
        form_value_ansprechpartner["Plz"] = None

    form_value_ansprechpartner["Email"] = email_registrierung
    form_value_ansprechpartner["Telefon"] = st.text_input("Telefon")

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
        form_value_ansprechpartner["Einrichtung_id"] = einrichtung_dict[selected_einrichtung_label]
    else:
        form_value_ansprechpartner["Einrichtung_id"] = None
if rolle_registrierung == "bearbeiter":
    email_registrierung = st.text_input("E-Mail1")
    passwort_registrierung = st.text_input(
        "Passwort1",
        type="password"
    )
    vorname_registrierung = st.text_input("Vorname")
    nachname_registrierung = st.text_input("Nachname")



# Menü für die Dateneingabe mit der Rolle eines Gründers
if rolle_registrierung == "gruender":
    email_registrierung = st.text_input("E-Mail1")
    passwort_registrierung = st.text_input(
        "Passwort1",
        type="password"
    )
    form_value["Vorname"] = st.text_input("Vorname")
    form_value["Nachname"] = st.text_input("Nachname")
    form_value["Geburtsdatum"] = st.date_input("Geburtsdatum", None, min_value=date(1900, 1, 1),
                                               max_value=datetime.now(), format="YYYY-MM-DD")
    form_value["Strasse"] = st.text_input("Strasse")


    #Dropdown Menü für PLZ Eingabe
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
        options=["Bitte wählen..."] + list(plz_dict.keys())
    )
    if selected_plz_label != "Bitte wählen...":
        form_value["Plz"] = plz_dict[selected_plz_label]
    else:
        form_value["Plz"] = None

    form_value["Email"] = email_registrierung
    form_value["Telefon"] = st.text_input("Telefon")
    form_value["Nationalitaet"] = st.text_input("Nationalität")
    form_value["Anzahl_kinder"] = st.selectbox("Anzahl der kinder", [None, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    form_value["Hochschulstatus"] = st.selectbox(
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

if st.button("Registrieren"):
    if rolle_registrierung == "Ansprechpartner":
        ansprechpartner_anlegen(
            form_value_ansprechpartner,
            passwort_registrierung,
            rolle_registrierung,
        )
        st.success("Registrierung als Ansprechpartner erfolgreich")

    if rolle_registrierung == "bearbeiter":
        bearbeiter_anlegen(
            vorname_registrierung,
            nachname_registrierung,
            email_registrierung,
            passwort_registrierung,
            rolle_registrierung,
        )
        st.success("Registrierung als Bearbeiter/in erfolgreich")

    if rolle_registrierung == "gruender":
        gruender_anlegen(
            form_value,
            passwort_registrierung,
            rolle_registrierung
        )
        st.success("Registrierung als Gründer erfolgreich")