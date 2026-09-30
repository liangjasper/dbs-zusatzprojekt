import streamlit as st

#-------------------------------------------------------------
# app.py gibt die "pages" und das Layout vor, welches für das Dashboard angezeigt wird
#-------------------------------------------------------------
st.set_page_config(
    page_title="EXIST-Gründungsstipendien",
    layout="wide"
)


#falls nicht eingeloggt werden formulare gezeigt. Falls eingeloggt wird eine andere Seite gezeigt
if not st.session_state.get("eingeloggt", False):
    pages = [
        st.Page(
            "pages/startseite.py",
            title="Startseite"
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
            title="Profil"
        )
    ]

if st.session_state.get("rolle") == "ansprechpartner":
    pages.extend([
        st.Page("pages/exist_forschungstransfer.py", title="Forschungstransfer"),
        st.Page("pages/exist_gruendungsfoerderung.py", title="Gründungsförderung"),
        st.Page("pages/exist_women.py", title="EXIST Women")
    ])


pg = st.navigation(
    pages,
    position="top"
)

pg.run()

