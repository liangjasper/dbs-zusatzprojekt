import streamlit as st

st.title("Profil")
if st.button("Abmelden"):
    st.session_state["eingeloggt"] = None
    st.session_state["benutzer_id"] = None
    st.session_state["email"] = None
    st.session_state["rolle"] = None
    st.rerun()

st.title("Persönliche Daten")

st.write("Benutzer: ", st.session_state["benutzer_id"])
st.write("Email: ", st.session_state["email"])
st.write("Rolle: ",st.session_state["rolle"])
st.write("Hier stehen bald weitere Perönlichen Daten")
st.title("Team")
if st.button("Team gründen"):
    st.warning("Funktion in bearbeitung")
if st.button("Team beitreten"):
    st.warning("Funktion in bearbeitung")
