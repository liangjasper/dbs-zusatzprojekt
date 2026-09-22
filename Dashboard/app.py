import streamlit as st

st.set_page_config(
    page_title="EXIST-Gründungsstipendien",
    layout="wide"
)

#checkt den eingeloggt Status und zeigt die entsprechenden Daten des Eingeloggten
if st.session_state.get("eingeloggt",False):
    st.write("Benutzer: ", st.session_state["benutzer_id"])
    st.write("Email: ", st.session_state["email"])
    st.write("Rolle: ",st.session_state["rolle"])

#falls nicht eingeloggt werden formulare gezeigt. Falls eingeloggt wird eine andere Seite gezeigt
if not st.session_state.get("eingeloggt", False):
    pages = [
        st.Page(
            "pages/startseite.py",
            title="Startseite"
        ),
        st.Page(
            "pages/exist_gruendungsfoerderung.py",
            title="Gründungsförderung",
        ),
        st.Page(
            "pages/exist_women.py",
            title="EXIST Women",
        ),
        st.Page(
            "pages/exist_forschungstransfer.py",
            title="Forschungstransfer"
        ),
        st.Page(
            "pages/anmeldung.py",
            title="Anmeldung"
        )
    ]
else:
    pages = [
        st.Page(
            "pages/profile.py",
            title="Daten und tabellen"
        )
    ]

pg = st.navigation(
    pages,
    position="top"
)

pg.run()

