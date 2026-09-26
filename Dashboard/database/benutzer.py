from database.connection import get_connection

def ansprechpartner_anlegen(form_values_ansprechpartner, rolle):

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO ansprechpartner (
              vorname,
              nachname,
              strasse,
              plz,
              email,
              telefon,
              einrichtung_id
          )
          VALUES (%s, %s, %s, %s, %s, %s, %s)  
    """
    cursor.execute(sql,(
        form_values_ansprechpartner["Vorname"], form_values_ansprechpartner["Nachname"], form_values_ansprechpartner["Strasse"],
        form_values_ansprechpartner["Plz"], form_values_ansprechpartner["Email"], form_values_ansprechpartner["Telefon"], form_values_ansprechpartner["Einrichtung_id"])
        )
    ansprechpartner_id=cursor.lastrowid

    sql = """
        INSERT INTO benutzer (
            email,
            passwort,
            rolle,
            ansprechpartner_id
        )
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (
        form_values_ansprechpartner["Email"],
        form_values_ansprechpartner["Passwort"],
        rolle,
        ansprechpartner_id
    ))

    connection.commit()
    cursor.close()
    connection.close()


def gruender_anlegen(form_value,rolle):
    connection=get_connection()
    cursor =connection.cursor()
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
              hochschulstatus
          )
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
          """

    cursor.execute(sql,(
        form_value["Vorname"], form_value["Nachname"], form_value["Geburtsdatum"], form_value["Strasse"],
        form_value["Plz"], form_value["Email"], form_value["Telefon"], form_value["Nationalitaet"],
        form_value["Anzahl_kinder"], form_value["Hochschulstatus"])
        )
    gruender_id = cursor.lastrowid
    sql = """
        INSERT INTO benutzer (
            email,
            passwort,
            rolle,
            gruender_id
        )
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (
        form_value["Email"],
        form_value["Passwort"],
        rolle,
        gruender_id
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
        SELECT benutzer_id, email, passwort,rolle, ansprechpartner_id, gruender_id, bearbeiter_id
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