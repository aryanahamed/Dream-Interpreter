import streamlit as st
from firebase_config import sign_out_user

st.title("👤 Profile")

user_email = st.session_state.get("user_email")
if user_email:
    st.subheader(f"Welcome, {user_email}")
    st.write("Nothing here yet 😅")
    if st.button("Logout"):
        sign_out_user()
        st.success("Logged out successfully!")
        st.switch_page("main.py")
else:
    st.warning("You are not logged in.")
    if st.button("Go to Login"):
        st.switch_page("pages//Login.py")
