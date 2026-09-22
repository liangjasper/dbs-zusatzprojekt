from database.connection import get_connection

def forschungseinrichtung_anlegen(name, url,email, passwort, rolle,):

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO forschungseinrichtung (
            name,
            url
        )
        VALUES(%s,%s)    
    """
    cursor.execute(sql, (
        name,
        url
    ))
    forschungseinrichtung_id = cursor.lastrowid
    sql = """
        INSERT INTO benutzer (
            email,
            passwort,
            rolle,
            einrichtung_id
        )
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (
        email,
        passwort,
        rolle,
        forschungseinrichtung_id
    ))

    connection.commit()
    cursor.close()
    connection.close()


def bearbeiter_anlegen(vorname,nachname,email, passwort, rolle):

    connection=get_connection()
    cursor =connection.cursor()

    sql = """
        INSERT INTO bearbeiter (
        vorname,
        nachname,
        email
        )
        VALUES ( %s, %s, %s)
    """
    cursor.execute(sql,(
        vorname,
        nachname,
        email
    ))

    bearbeiter_id = cursor.lastrowid
    sql = """
        INSERT INTO benutzer (
            email,
            passwort,
            rolle,
            bearbeiter_id
        )
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (
        email,
        passwort,
        rolle,
        bearbeiter_id
    ))


    connection.commit()
    cursor.close()
    connection.close()

def benutzer_anlegen(email, passwort, rolle):
#name und URL müssen noch an benutzer_anelgen weiergegeben werden
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO benutzer (
            email,
            passwort,
            rolle
        )
        VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (
        email,
        passwort,
        rolle
    ))

    connection.commit()
    cursor.close()
    connection.close()



def benutzer_anmelden(email, passwort):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    sql = """
        SELECT benutzer_id, email, passwort,rolle
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