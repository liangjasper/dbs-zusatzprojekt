import streamlit as st
from database.connection import get_connection

def build_team(einrichtung_id, team_name):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
          INSERT INTO gruendungsteam (einrichtung_id,team_name)
          VALUES (%s,%s) 
          """

    cursor.execute(sql, (
        einrichtung_id, team_name
    ))
    team_id = cursor.lastrowid
    sql = """
          UPDATE gruender
          SET team_id = %s
          WHERE email = %s
          """

    cursor.execute(sql, (
        team_id,
        st.session_state["email"]
    ))
    connection.commit()
    cursor.close()
    connection.close()
    return team_id, team_name

#hier arbeite ich dran
def join_team(team_id):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
          UPDATE gruender
          SET team_id = %s
          WHERE email = %s
          """

    cursor.execute(sql, (
        team_id,
        st.session_state["email"]
    ))
    connection.commit()
    cursor.close()
    connection.close()
    return team_id