import streamlit as st

st.set_page_config(
    page_title="EXIST-Gründungsstipendien",
    layout="wide"
)

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

pg = st.navigation(
    pages,
    position="top"
)

pg.run()

