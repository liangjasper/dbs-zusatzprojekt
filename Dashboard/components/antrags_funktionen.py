import streamlit as st
from database.connection import get_connection

def get_antrag(antrag_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    sql = """
          SELECT antrag.*,
                 gruendungsteam.*,
                 forschungseinrichtung.*
          FROM antrag
                   LEFT JOIN gruendungsteam
                             ON antrag.team_id = gruendungsteam.team_id
                   LEFT JOIN forschungseinrichtung
                             ON antrag.einrichtung_id = forschungseinrichtung.einrichtung_id
          WHERE antrag.antrag_id = %s
          """

    cursor.execute(sql, (antrag_id,))
    antrag = cursor.fetchone()

    sql = """
          SELECT *
          FROM gruender
          WHERE team_id = %s
          """

    cursor.execute(sql, (antrag["team_id"],))
    gruender = cursor.fetchall()

    sql = """
        SELECT zeitstempel, inhalt
        FROM notiz
        WHERE antrag_id = %s
        
        """
    cursor.execute(sql, (antrag["antrag_id"],))
    notiz = cursor.fetchall()
    sql = """
          SELECT *
          FROM ansprechpartner
          WHERE einrichtung_id = %s
          """
    cursor.execute(sql, (antrag["einrichtung_id"],))
    ansprechpartner = cursor.fetchall()
    if antrag["programm"]=="exist_women":
        sql = """
              SELECT *
              FROM dokumente
              WHERE dokument_id = (SELECT motivationspapier_id
                                   FROM exist_women
                                   WHERE antrag_id = %s) 
              """
        cursor.execute(sql, (antrag["antrag_id"],))
    elif antrag["programm"]=="exist_forschungstransfer":
        sql = """
              SELECT *
              FROM dokumente
              WHERE dokument_id IN (
                    SELECT projektbeschreibung_id
                    FROM exist_forschungstransfer
                    WHERE antrag_id =%s
                    UNION
                    SELECT businessplan_id
                    FROM exist_forschungstransfer
                    WHERE antrag_id =%s) 
              """
        cursor.execute(sql, (antrag["antrag_id"],antrag["antrag_id"]))
    elif antrag["programm"]=="exist_gruendungsfoerderung":
        sql = """
              SELECT *
              FROM dokumente
              WHERE dokument_id = (SELECT ideenpapier_id
                                   FROM exist_gruendungsfoerderung
                                   WHERE antrag_id = %s) 
              """
        cursor.execute(sql, (antrag["antrag_id"],))

    dokument = cursor.fetchall()

    cursor.close()
    connection.close()

    return antrag, gruender, notiz, ansprechpartner, dokument
