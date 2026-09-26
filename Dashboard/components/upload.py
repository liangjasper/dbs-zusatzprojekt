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
    gruender_query = """
                     SELECT gruender_id
                     FROM benutzer
                     WHERE benutzer_id = %s \
                     """
    cursor.execute(gruender_query, (st.session_state["benutzer_id"],))
    result = cursor.fetchone()
    gruender_id = result[0] if result else None
    sql = """
          INSERT INTO lebenslauf (gruender_id,
                                  dokument_id)
          VALUES (%s, %s) \
          """

    cursor.execute(sql, (
        gruender_id,
        dokument_id,
    ))
    connection.commit()
    cursor.close()
    connection.close()
    return True


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