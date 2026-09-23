import streamlit as st
from database.connection import get_connection


def uploade_file(uploaded_file):

    if uploaded_file is None:
        return False

    try:
        connection = get_connection()
        cursor = connection.cursor()

        sql = """
              INSERT INTO dokumente (
                  dateiname,
                  dateityp, 
                  datei)
              VALUES (%s, %s, %s) \
              """

        cursor.execute(sql, (
            uploaded_file.name,
            uploaded_file.type,
            bytes(uploaded_file.getbuffer())
        ))
        dokument_id=cursor.lastrowid
        gruender_query= """
            SELECT gruender_id FROM benutzer WHERE benutzer_id = %s
        """
        cursor.execute(gruender_query, (st.session_state["benutzer_id"],))
        result = cursor.fetchone()
        gruender_id = result[0] if result else None
        sql = """
              INSERT INTO lebenslauf (gruender_id,
                                      dokument_id)
              VALUES (%s, %s) 
              """

        cursor.execute(sql, (
            gruender_id,
            dokument_id,
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    except Exception as e:

        # 1. Rollback, falls etwas schiefgegangen ist

        if "connection" in locals() and connection.is_connected():
            connection.rollback()

        # 2. Den Fehler ausgeben (hilft beim Debuggen)

        print(f"Fehler beim Speichern des Dokuments: {e}")

        # 3. Ressourcen sauber schließen

        if "cursor" in locals():
            cursor.close()

        if "connection" in locals() and connection.is_connected():
            connection.close()
        return False
