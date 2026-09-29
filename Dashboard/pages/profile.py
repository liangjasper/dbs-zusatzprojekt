import streamlit as st
from components.upload import uploade_file, lebenslauf_eintrag, get_documents_for_antrag
from components.build_join_team import build_team,join_team
from database.connection import get_connection
from components.antrags_funktionen import get_antrag
import pandas as pd
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

    cursor.execute("SELECT einrichtung_id, name FROM forschungseinrichtung")

    einrichtung_liste = cursor.fetchall()
    cursor.close()
    connection.close()

    einrichtung_dict = {
        f"{row[0]} - {row[1]}": row[0]
        for row in einrichtung_liste
    }
    st.write("Hier kannst du ein neues Team gründen")
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

    st.write("Hier kannst du einem Team beitreten")
    with st.form("join_team_form"):
        team_id = st.number_input("Team-ID",min_value=1,step=1)
        submitted = st.form_submit_button("Team beitreten")

        if submitted:
            join_team(team_id)
            st.success(f"Du bist Team {team_id} beigetreten!")

    #Uploader für den Lebenslauf
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

    connection_antrag = get_connection()
    cursor_antrag = connection_antrag.cursor(dictionary=True)

    # Abfrage holt alle Anträge, bei denen die team_id mit der team_id des Gründers übereinstimmt
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
        st.info("Bisher wurden noch keine Anträge für deine Einrichtung eingereicht.")

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

    st.title("kompletten Antrag anzeigen lassen")
    with st.form("kompletten_antrag_form"):
        antrag_id = st.number_input("Hier antrags_id eintragen")
        submit= st.form_submit_button("Antrag anzeigen")
    if submit:
        st.session_state["antrag_id"] = antrag_id

    if "antrag_id" in st.session_state:
        antrag, gruender, notiz, ansprechpartner, dokument = get_antrag(antrag_id)
        st.dataframe(antrag, use_container_width=True)
        st.dataframe(gruender, use_container_width=True)
        st.dataframe(notiz, use_container_width=True)
        st.dataframe(ansprechpartner, use_container_width=True)
        st.dataframe(dokument, use_container_width=True)
        for eintrag in dokument:
            st.download_button(
                label=f"{eintrag['dateiname']} Herunterladen",
                data=eintrag["datei"],
                file_name=eintrag["dateiname"],
                mime=eintrag["dateityp"]
            )

    st.title("Notiz erstellen")
    with st.form("notiz_erstellen"):
        notiz=st.text_input("Notiz schreiben")
        antrag_id = st.number_input("Antrags-ID schreiben")
        submit = st.form_submit_button("Notiz anlegen")
    if submit:
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
              INSERT INTO notiz (antrag_id, inhalt) 
              VALUE(%s, %s)
        """
        cursor.execute(sql,(antrag_id,notiz))
        connection.commit()
        cursor.close()
        connection.close()
    st.title("Dokumente")
    antrag_id= st.number_input("antrag_id")

    if st.button("Suchen...."):
        dokumente = get_documents_for_antrag(antrag_id)

        for dokument in dokumente:
            st.write(dokument["dateiname"])

            st.download_button(
                label="Herunterladen",
                data=dokument["datei"],
                file_name=dokument["dateiname"],
                mime=dokument["dateityp"]
            )

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

#------------- Funktionen im Profil des Ansprechpartners-----------------------------

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

