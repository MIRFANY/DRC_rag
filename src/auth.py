import streamlit as st
import hashlib
from config import APP_PASSWORD

def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

CORRECT_HASH = _hash(APP_PASSWORD)

def require_login():
    if st.session_state.get("authenticated"):
        return True

    st.markdown("## Health Compliance Assistant")
    st.markdown("Enter the team password to continue.")

    pw = st.text_input("Password", type="password", key="pw_input")

    if st.button("Sign in"):
        if _hash(pw) == CORRECT_HASH:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")

    st.stop()