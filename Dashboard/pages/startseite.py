import streamlit as st

st.title("Willkommen beim EXIST-Antragsportal")

st.write("""
Dieses Portal dient der Einreichung, Verwaltung und Überprüfung von Förderanträgen 
für die Programme EXIST-Women, EXIST-Gründungsstipendium und EXIST-Forschungstransfer.
""")

st.divider()

st.header("Wie funktioniert das Portal?")
st.write("Je nach Benutzerrolle stehen Ihnen nach der Anmeldung unterschiedliche Funktionen zur Verfügung:")

# Abschnitt für Gründer
st.subheader("Für Gründer:innen")
st.write("""
* **Registrierung:** Erstellen Sie ein Konto und füllen Sie Ihr Profil aus.
* **Team:** Treten Sie einem bestehenden Gründungsteam bei oder erstellen Sie ein neues.
* **Dokumente:** Laden Sie Ihren aktuellen Lebenslauf hoch.
* **Status:** Verfolgen Sie den aktuellen Bearbeitungsstatus Ihres Antrags über Ihr Profil.
""")

# Abschnitt für Ansprechpartner
st.subheader("Für Ansprechpartner:innen (Forschungseinrichtungen)")
st.write("""
* **Anträge einreichen:** Reichen Sie Anträge für die von Ihnen betreuten Teams ein.
* **Programme:** Nutzen Sie die spezifischen Formulare (Women, Gründungsstipendium, Forschungstransfer).
* **Uploads:** Laden Sie erforderliche Dokumente (z. B. Ideenpapier, Businessplan) hoch.
* **Übersicht:** Behalten Sie den Überblick über alle eingereichten Anträge Ihrer Einrichtung.
""")

# Abschnitt für Bearbeiter
st.subheader("Für Bearbeiter:innen (Projektträger Jülich)")
st.write("""
* **Dashboard:** Nutzen Sie die Statistiken, um Anträge nach Programm und Status auszuwerten.
* **Prüfung:** Sichten Sie neu eingereichte Anträge und die dazugehörigen Dokumente.
* **Entscheidung:** Aktualisieren Sie den Status eines Antrags (z. B. in Prüfung, bewilligt, abgelehnt).
* **Notizen:** Hinterlassen Sie interne Vermerke zu spezifischen Anträgen.
""")

st.divider()

st.info("Bitte navigieren Sie zur Seite 'Anmeldung', um sich in das System einzuloggen oder ein neues Konto zu erstellen.")


