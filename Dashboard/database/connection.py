import mysql.connector
import os
from dotenv import load_dotenv

#----------------------------------------------------
# connection.py stellt mit get_connection die Schnittstelle zwischen dem dashboard und der Datenbank bereit.
# Login daten befinden sich in einer Lokal gespeicherten env
# Alle dateien im directory "pages" greifen auf die Funktion zu, um mit der Datenbank zu arbeiten
#----------------------------------------------------
load_dotenv()

def get_connection():

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
