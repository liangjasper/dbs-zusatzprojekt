import streamlit as st
from components.upload import uploade_file, lebenslauf_eintrag, get_documents_for_antrag
from components.build_join_team import build_team,join_team
from database.connection import get_connection
from components.antrags_funktionen import get_antrag
import pandas as pd

# Dieser Datei ist für das Management der einzelnen Profile zuständig.
# Hier werden die einzelnen Privilegien und Funktionen der Nutzer "Ansprechpartner", "Gründer" und "Bearbeiter" definiert
# Der Bereich ist erst nach der Registrierung und anschließenden Anmeldung erreichbar


st.title("Profil")
# Funktion um einen Nutzer von seinem Profil abzumelden
if st.button("Abmelden"):
    st.session_state["eingeloggt"] = None
    st.session_state["benutzer_id"] = None
    st.session_state["email"] = None
    st.session_state["rolle"] = None
    st.rerun()

st.title("Persönliche Daten")
# Persönliche Daten(Benutzer_id, email, Rolle und entsprechende IDs des angemeldeten Benutzers werden auf der Seite angezeigt.
st.write("Benutzer: ", st.session_state["benutzer_id"])
st.write("Email: ", st.session_state["email"])
st.write("Rolle: ",st.session_state["rolle"])
if st.session_state["rolle"] == "bearbeiter":
    st.write("Bearbeiter ID: ",st.session_state["bearbeiter_id"])
elif st.session_state["rolle"] == "gruender":
    st.write("Gründer ID:" ,st.session_state["gruender_id"])
elif st.session_state["rolle"] == "ansprechpartner":
    st.write("Ansprechpartner ID" ,st.session_state["ansprechpartner_id"])


#--------------Funktionen im Profil des Gründers--------------------------------
# Der Gründer hat die Möglichkeit in seinem Profil:
# 1. ein neues Team zu gründen
# 2. einem bestehenden Team beizutreten
# 3. seinen Lebenslauf hochzuladen
# 4. Anträge die für ihn eingereicht wurden einzusehen

if st.session_state["rolle"] == "gruender":

    st.title("Team")
    # funktionen und
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
    st.write("Hier kannst du ein neues Team gründen")

    # Die Form um ein neues Team zu Gründen wird hier bereitgestellt
    with st.form("team_form"):
        selected_einrichtung_label = st.selectbox("Forschungseinrichtung",options=["Bitte wählen..."] + list(einrichtung_dict.keys()))
        team_name=st.text_input("Team Name")
        submitted = st.form_submit_button("Team gründen")

        if submitted:

            if selected_einrichtung_label == "Bitte wählen...":
                st.error("Bitte wähle eine Forschungseinrichtung aus.")

            else:
                einrichtung_id = einrichtung_dict[selected_einrichtung_label]
                team_id = build_team(einrichtung_id,team_name)
                st.success(f"Team gegründet! Team-ID: {team_id, team_name}")

    # Die Form einem Team beizutreten wird hier bereitgestellt
    st.write("Hier kannst du einem Team beitreten")
    with st.form("join_team_form"):
        team_id = st.number_input("Team-ID",min_value=1,step=1)
        submitted = st.form_submit_button("Team beitreten")

        if submitted:
            join_team(team_id)
            st.success(f"Du bist Team {team_id} beigetreten!")

    # Uploader für den Lebenslauf
    uploaded_file = st.file_uploader(
        "Lebenslauf hochladen",
        type=["pdf", "docx", "png", "jpg"]
    )
    if uploaded_file is not None:
        st.success(f"{uploaded_file.name} wurde hochgeladen!")

        # file uploaden und document_id für den Lebenslauft Eintrag nutzen
        document_id = uploade_file(uploaded_file)
        lebenslauf_eintrag(document_id)
        if document_id is not None:
            st.success("Dokument wurde erfolgreich in der Datenbank gespeichert!")

    st.title("Anträge und andere Daten")
    # Hier werden alle Anträge die für den Gründer eingereicht wurden angezeigt
    connection_antrag = get_connection()
    cursor_antrag = connection_antrag.cursor(dictionary=True)

    sql_uebersicht = """
        SELECT a.antrag_id, a.gruendungstitel, a.programm, a.status, a.einreichungsdatum
        FROM antrag a
        JOIN gruender g ON a.team_id = g.team_id
        WHERE g.gruender_id = %s
        ORDER BY a.einreichungsdatum DESC
    """
    cursor_antrag.execute(sql_uebersicht, (st.session_state["gruender_id"],))
    antraege = cursor_antrag.fetchall()

    cursor_antrag.close()
    connection_antrag.close()

    if not antraege:
        st.warning("Bisher wurden noch keine Anträge für deine Einrichtung eingereicht.")

    else:
        st.subheader("Übersicht der Anträge")
        df_antraege = pd.DataFrame(antraege)
        st.dataframe(df_antraege,use_container_width=True,hide_index=True)
        optionen = {
            f"Antrag {a['antrag_id']} – {a['gruendungstitel']}":
                a["antrag_id"]
            for a in antraege
        }

        auswahl = st.selectbox(
            "Welchen Antrag möchtest du öffnen?",
            options=list(optionen.keys())
        )
        if st.button("Antrag anzeigen"):
            st.session_state["ausgewaehlter_antrag"] = optionen[auswahl]
            st.rerun()

    if "ausgewaehlter_antrag" in st.session_state:
        antrag_id = st.session_state["ausgewaehlter_antrag"]
        st.divider()
        st.header(f"Details zu Antrag {antrag_id}")

        antrag, gruender, notiz, ansprechpartner, dokument = get_antrag(antrag_id)

        st.subheader("Antragsdaten")
        st.dataframe(antrag, use_container_width=True, hide_index=True)

        st.subheader("Gründerdaten")
        st.dataframe(gruender, use_container_width=True, hide_index=True)

        st.subheader("Notiz zum Antrag")
        st.dataframe(notiz, use_container_width=True, hide_index=True)

        st.subheader("Ansprechpartner")
        st.dataframe( pd.DataFrame(ansprechpartner)[["vorname", "nachname", "email"]],use_container_width=True,hide_index=True)

        st.subheader("Hochgeladene Dokumente")
        st.dataframe(dokument, use_container_width=True,hide_index=True)

        for eintrag in dokument:
            st.download_button(
                label=f"{eintrag['dateiname']} herunterladen",
                data=eintrag["datei"],
                file_name=eintrag["dateiname"],
                mime=eintrag["dateityp"],
                key=f"download_{antrag_id}_{eintrag['dateiname']}"
            )
        # Auswahl wieder zurücksetzen
        if st.button("Antrag schließen"):
            del st.session_state["ausgewaehlter_antrag"]
            st.rerun()

#-------------- Funktionen im Profil des Bearbeiters--------------------
# Im Profil des Bearbeiters gibt es die funktionen:
# 1. Als Bearbeiter für einen Antrag einzutragen
# 2. Antragsstatus eines Antrags zu ändern
# 3. Anträge vollständig anzuzeigen
# 4. Notiz für einen Antrag zu erstellen
# 5. Neuen Mentor anzulegen

if st.session_state["rolle"] == "bearbeiter":
    st.title("Alle Anträge")
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM antrag")
    daten = cursor.fetchall()
    cursor.close()
    connection.close()
    st.dataframe(daten, use_container_width=True)

    st.title("Als Bearbeiter in Antrag eintragen")
    with st.form("bearbeiter_antrag_form"):
        antrag_id = st.number_input("Antrags-ID eintragen",min_value=1,step=1)
        submit = st.form_submit_button("Als Bearbeiter eintragen")

    if submit:
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
              UPDATE antrag
              SET bearbeiter_id = %s
              WHERE antrag_id = %s \
              """
        cursor.execute(sql,(st.session_state["bearbeiter_id"],antrag_id))
        connection.commit()
        cursor.close()
        connection.close()
        st.success("Als bearbeiter eintragen!")
        st.rerun()

    st.title("Antragsstatus ändern")
    with st.form("antragstatus_aendern_form"):
        antrag_id = st.number_input("Antrags-ID eintragen",min_value=1,step=1)
        status = st.selectbox(
            "Neuer Status",
            [
                "eingereicht",
                "in_pruefung",
                "in_korrektur",
                "bewilligt",
                "abgelehnt"
            ]
        )
        submit = st.form_submit_button("Status ändern")
    if submit:
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
            UPDATE antrag
            SET status = %s
            WHERE antrag_id = %s
        """
        cursor.execute(sql,(status, antrag_id))
        connection.commit()
        cursor.close()
        connection.close()
        st.rerun()
    st.title("Vollständige Anträge anzeigen lassen")
    with st.form("kompletten_antrag_form"):
        antrag_id = st.number_input("Hier antrags_id eintragen", min_value=1,step=1)
        submit= st.form_submit_button("Antrag anzeigen")
    if submit:
        st.session_state["antrag_id"] = antrag_id

    if "antrag_id" in st.session_state:
        antrag, gruender, notiz, ansprechpartner, dokument = get_antrag(antrag_id)
        st.subheader("Antrag")
        st.dataframe(antrag, use_container_width=True)

        st.subheader("Gruender")
        st.dataframe(gruender, use_container_width=True)

        st.subheader("Notiz")
        st.dataframe(notiz, use_container_width=True)

        st.subheader("Ansprechpartner")
        st.dataframe(ansprechpartner, use_container_width=True)

        st.subheader("Hochgeladenene Dokumente")
        st.dataframe(dokument, use_container_width=True)

        for eintrag in dokument:
            st.download_button(
                label=f"{eintrag['dateiname']} Herunterladen",
                data=eintrag["datei"],
                file_name=eintrag["dateiname"],
                mime=eintrag["dateityp"]
            )
        collapse = st.button("Antrag schließen")
        if collapse:
            del st.session_state["antrag_id"]
            st.rerun()

    st.title("Notiz erstellen")
    with st.form("notiz_erstellen"):
        notiz=st.text_input("Notiz schreiben")
        antrag_id = st.number_input("Antrags-ID", min_value=1,step=1)
        dokument_id = st.number_input("Dokument-ID", min_value=1, step=1)
        submit = st.form_submit_button("Notiz anlegen")
    if submit:
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
              INSERT INTO notiz (antrag_id, inhalt, dokument) 
              VALUE(%s, %s, %s)
        """
        cursor.execute(sql,(antrag_id, notiz, dokument_id))
        connection.commit()
        cursor.close()
        connection.close()
    #Hier gibt es die Funktion einen neuen Mentor anzulegen
    st.title("Neuen Mentor anlegen")
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

                    cursor.execute(sql, (vorname, nachname, email, telefon))
                    connection.commit()

                    st.success("Mentor wurde erfolgreich angelegt.")

                except Exception as e:
                    st.error(f"Fehler beim Speichern: {e}")

                finally:
                    cursor.close()
                    connection.close()

    st.title("Anträge pro Förderprogramm und Status")
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    sql = """
        SELECT
            programm,
            status,
            COUNT(*) AS anzahl_antraege
            FROM antrag
            GROUP BY programm, status
            ORDER BY programm, status;
    """
    cursor.execute(sql)
    ergebnisse = cursor.fetchall()
    df = pd.DataFrame(ergebnisse)
    st.dataframe(df, use_container_width=True)


#------------- Funktionen im Profil des Ansprechpartners-----------------------------
# Im Profil des Ansprechpartners gibt es die Funktionen:
# 1. Alle selbst eingereichten Anträge anzusehen
# Anträge stellt derAnsprechpartner über die pages: exist_forschungstransfer.py, exist_gruendungsfoerderung.py und exist_women.py
# Diese werden freigeschaltet, wenn eine Person mit Rolle Ansprechpartner sich einloggt
if st.session_state["rolle"] == "ansprechpartner":

    st.title("Alle von dir eingereichten Anträge")
    connection_antrag = get_connection()
    cursor_antrag = connection_antrag.cursor(dictionary=True)

    sql_uebersicht = """
        SELECT a.antrag_id, a.gruendungstitel, a.programm, a.status, a.einreichungsdatum
        FROM antrag a
        JOIN ansprechpartner ap ON a.einrichtung_id = ap.einrichtung_id
        WHERE ap.ansprechpartner_id = %s
        ORDER BY a.einreichungsdatum DESC
    """

    cursor_antrag.execute(sql_uebersicht,(st.session_state["ansprechpartner_id"],))
    antraege = cursor_antrag.fetchall()
    cursor_antrag.close()
    connection_antrag.close()


    if not antraege:
        st.warning("Bisher wurden noch keine Anträge für deine Einrichtung eingereicht.")

    else:
        st.subheader("Übersicht der Anträge")
        df_antraege = pd.DataFrame(antraege)
        st.dataframe(df_antraege,use_container_width=True,hide_index=True)
        optionen = {
            f"Antrag {a['antrag_id']} – {a['gruendungstitel']}":
                a["antrag_id"]
            for a in antraege
        }

        auswahl = st.selectbox(
            "Welchen Antrag möchtest du öffnen?",
            options=list(optionen.keys())
        )
        if st.button("Antrag anzeigen"):
            st.session_state["ausgewaehlter_antrag"] = optionen[auswahl]
            st.rerun()

    if "ausgewaehlter_antrag" in st.session_state:

        antrag_id = st.session_state["ausgewaehlter_antrag"]
        st.divider()
        st.header(f"Details zu Antrag {antrag_id}")

        antrag, gruender, notiz, ansprechpartner, dokument = get_antrag(antrag_id)

        st.subheader("Antragsdaten")
        st.dataframe(antrag,use_container_width=True, hide_index=True)

        st.subheader("Gründerdaten")
        st.dataframe(gruender, use_container_width=True, hide_index=True)

        st.subheader("Notiz zum Antrag")
        st.dataframe(notiz,use_container_width=True, hide_index=True)

        st.subheader("Ansprechpartner")
        st.dataframe(pd.DataFrame(ansprechpartner)[["vorname", "nachname", "email"]], use_container_width=True, hide_index=True)

        st.subheader("Hochgeladene Dokumente")
        st.dataframe(dokument,use_container_width=True, hide_index=True)
        for eintrag in dokument:
            st.download_button(
                label=f"{eintrag['dateiname']} herunterladen",
                data=eintrag["datei"],
                file_name=eintrag["dateiname"],
                mime=eintrag["dateityp"],
                key=f"download_{antrag_id}_{eintrag['dateiname']}"
            )
        # Auswahl wieder zurücksetzen
        if st.button("Antrag schließen"):
            del st.session_state["ausgewaehlter_antrag"]
            st.rerun()

