from database import connection
from database.connection import get_connection

def benutzer_anlegen(email, passwort):

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO benutzer (
            email,
            passwort
        )
        VALUES (%s, %s)
    """

    cursor.execute(sql, (
        email,
        passwort
    ))

    connection.commit()

    cursor.close()
    connection.close()



def benutzer_anmelden(email, passwort):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    sql = """
        SELECT id, email, passwort
        FROM benutzer
        WHERE email = %s
        AND passwort = %s
    """

    cursor.execute(sql, (
        email,
        passwort
    ))

    benutzer = cursor.fetchone()

    cursor.close()
    connection.close()

    return benutzer