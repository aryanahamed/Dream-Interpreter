import streamlit as st
from firebase_config import sign_in_user, send_password_reset

if st.session_state.get("user") != None:
    st.warning("You are already logged in. Please log out to switch accounts.")
    if st.button("Go to Home"):
        st.switch_page("Home.py")
    st.stop()

st.title("Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if email and password:
        with st.spinner("Logging in..."):
            user, error = sign_in_user(email, password)
        if user:
            st.session_state.user = email
            st.session_state.user_token = user['idToken']
            st.session_state.user_email = user['email']
            st.success("Logged in successfully!")
            st.switch_page("Home.py")
        elif "INVALID_LOGIN_CREDENTIALS" in error:
            st.error("Invalid email or password. Please try again.")
        else:
            st.error(f"Login failed. Try again later.")
    else:
        st.error("Please enter email and password.")
        
if st.button("Forgot Password?"):
    try:
        send_password_reset(email)
        st.success("If an account exists for this email, a password reset link has been sent. Please check your inbox (and spam folder).")
    except Exception as e:
        st.error(f"Failed to process password reset request. Please ensure the email is valid and try again later.")
    else:
        st.warning("Please enter your email above to reset your password.")

if st.button("Sign Up"):
    st.switch_page("pages//SignUp.py")
    
