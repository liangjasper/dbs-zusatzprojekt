import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

st.title("Mein Dashboard")

vorname = st.text_input("vorname")
nachname = st.text_input("nachname")
geburtsdatum = st.text_input("geburtsdatum")
strasse = st.text_input("strasse")
plz = st.text_input("plz")
email = st.text_input("email")
telefon = st.text_input("telefon")
nationalitaet = st.text_input("nationalitaet")
anzahl_kinder=st.text_input("anzahl_kinder")
hochschulstatus=st.text_input("hochschulstatus")
team_id = st.text_input("team_id")



if st.button("Speichern"):
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

    cursor = connection.cursor()

    sql = """
        INSERT INTO gruender (vorname, nachname, geburtsdatum, strasse, plz, email, telefon, nationalitaet, anzahl_kinder, hochschulstatus, team_id)
        VALUES (%s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (vorname, nachname, geburtsdatum, strasse, plz, email, telefon, nationalitaet, anzahl_kinder, hochschulstatus, team_id))
    connection.commit()

    cursor.close()
    connection.close()

    st.success("Daten wurden gespeichert!")
