import streamlit as st
from firebase_config import sign_up_user

if st.session_state.get("user") != None:
    st.warning("You are already logged in. Please log out to sign up a new account.")
    if st.button("Go to Home"):
        st.switch_page("main.py")
    st.stop()

st.title("Sign Up")

signup_email = st.text_input("Email")
signup_password = st.text_input("Password", type="password")

if st.button("Sign Up"):
    if not signup_email or not signup_password:
        st.error("Please enter email and password")
    elif "@" not in signup_email or "." not in signup_email:
        st.error("Please enter a valid email address")
    elif len(signup_password) < 6:
        st.error("Password must be at least 6 characters long")
    else:
        with st.spinner("Signing up..."):
            user, error = sign_up_user(signup_email, signup_password)
        if user:
            st.session_state.user = signup_email
            st.session_state.user_token = user['idToken']
            st.session_state.user_email = user['email']
            st.success("Account created and logged in!")
            st.switch_page("main.py")
        else:
            st.error(f"Sign up failed: {error}")

if st.button("Go to Login"):
    st.switch_page("pages/Login.py")
