import streamlit as st
from database.connection import get_connection


def uploade_file(uploaded_file):

    if uploaded_file is None:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
          INSERT INTO dokumente (dateiname,
                                 dateityp,
                                 datei)
          VALUES (%s, %s, %s) \
          """

    cursor.execute(sql, (
        uploaded_file.name,
        uploaded_file.type,
        bytes(uploaded_file.getbuffer())
    ))
    dokument_id = cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()
    return dokument_id


def lebenslauf_eintrag(dokument_id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = """
          INSERT INTO lebenslauf (gruender_id, dokument_id)
          VALUES (%s, %s) ON DUPLICATE KEY \
          UPDATE dokument_id = \
          VALUES (dokument_id) \
          """
    cursor.execute(sql, (st.session_state["gruender_id"], dokument_id))
    connection.commit()
    cursor.close()
    connection.close()


def download_file(dokument_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    sql = """
        SELECT dateiname, dateityp, datei
        FROM dokumente
        WHERE dokument_id = %s
    """

    cursor.execute(sql, (dokument_id,))
    dokument = cursor.fetchone()

    cursor.close()
    connection.close()

    return dokument