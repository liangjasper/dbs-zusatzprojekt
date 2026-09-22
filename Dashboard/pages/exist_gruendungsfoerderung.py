import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from database.connection import get_connection
import mysql.connector

#Formular für die Gründungsförderung
load_dotenv()
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
legal_age=datetime.now().date()-relativedelta(years=18)

st.title("EXIST-Gründungsstipendien")



with st.form(key="gruender_form"):
    form_value["Vorname"] = st.text_input("Vorname")
    form_value["Nachname"] = st.text_input("Nachname")
    form_value["Geburtsdatum"] = st.date_input("Geburtsdatum",None, min_value=date(1900,1,1), max_value=datetime.now(), format="YYYY-MM-DD")
    form_value["Strasse"] = st.text_input("Strasse")
    form_value["Plz"] = st.text_input("Plz")
    form_value["Email"] = st.text_input("Email")
    form_value["Telefon"] = st.text_input("Telefon")
    form_value["Nationalitaet"] = st.text_input("Nationalität")
    form_value["Anzahl_kinder"]=st.selectbox("Anzahl der kinder",[None,0,1,2,3,4,5,6,7,8,9])
    form_value["Hochschulstatus"]=st.selectbox("Hochschulstatus", ["","StudentIn", "AbsolventIn"])
    form_value["Team_id"] = st.text_input("Team Id")

    submit_button = st.form_submit_button()
#Wenn der submit Button gedrückt wird, wird in der exist_gruendungsfoerderungstabelle ein eintrag angelegt. vorher wird noch das Alter geprüft und ob alle Felder ausgefüllt wurden
    if submit_button:
        if form_value["Geburtsdatum"]<legal_age:
            if not all(form_value.values()):
                st.warning("Bitte alle Felder ausfüllen")
            else:
                st.success("Dokument erfolgreich eingereicht")
                connection = get_connection()
                cursor = connection.cursor()

                sql = """
                      INSERT INTO gruender (
                          vorname,
                          nachname,
                          geburtsdatum,
                          strasse,
                          plz,
                          email,
                          telefon,
                          nationalitaet,
                          anzahl_kinder,
                          hochschulstatus,
                          team_id)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                      """

                cursor.execute(sql, (form_value["Vorname"] , form_value["Nachname"], form_value["Geburtsdatum"], form_value["Strasse"], form_value["Plz"], form_value["Email"], form_value["Telefon"], form_value["Nationalitaet"], form_value["Anzahl_kinder"], form_value["Hochschulstatus"], form_value["Team_id"]))
                connection.commit()

                cursor.close()
                connection.close()

                st.success("Daten wurden gespeichert!")
        else:
            st.warning("Bitte prüfe dein Alter. Einreichungen sind nur ab 18 Jahren möglich")


#Uploader für Files welche benötigt werden um das Formular zu vervollständigen. Z.B. Lebenslauf
uploaded_file = st.file_uploader(
    "Dokument hochladen",
    type=["pdf", "docx", "png", "jpg"]
)

if uploaded_file is not None:
    st.success(f"{uploaded_file.name} wurde hochgeladen!")
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO dokumente (
            dateiname,
            dateityp,
            datei
        )
        VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (
        uploaded_file.name,
        uploaded_file.type,
        bytes(uploaded_file.getbuffer())
    ))

    connection.commit()

    st.success("Dokument wurde gespeichert!")
