import pyrebase
import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

firebaseConfig = {
    "apiKey": os.environ.get("FIREBASE_API_KEY"),
    "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.environ.get("FIREBASE_PROJECT_ID"),
    "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.environ.get("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.environ.get("FIREBASE_APP_ID"),
    "databaseURL": os.environ.get("FIREBASE_DATABASE_URL")
}

try:
    firebase = pyrebase.initialize_app(firebaseConfig)
    firebase_auth = firebase.auth()
except Exception as e:
    st.error(f"Firebase initialization error: {e}")
    st.stop()

if not firebase_admin._apps:
    try:
        service_account_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH")
        
        if service_account_path and os.path.exists(service_account_path):
            cred = credentials.Certificate(service_account_path)
        else:
            service_account_info = {
                "type": "service_account",
                "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
                "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
                "private_key": os.environ.get("FIREBASE_PRIVATE_KEY"),
                "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
                "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.environ.get('FIREBASE_CLIENT_EMAIL')}"
            }
            
            if not all([service_account_info["project_id"], service_account_info["private_key"], service_account_info["client_email"]]):
                st.error("Missing required Firebase service account credentials")
                st.stop()
            
            cred = credentials.Certificate(service_account_info)
        
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        
    except Exception as e:
        st.error(f"Firebase Admin initialization error: {e}")
        pass

def sign_up_user(email, password):
    try:
        user = firebase_auth.create_user_with_email_and_password(email, password)
        return user, None
    except Exception as e:
        return None, str(e)

def sign_in_user(email, password):
    try:
        user = firebase_auth.sign_in_with_email_and_password(email, password)
        return user, None
    except Exception as e:
        return None, str(e)

def sign_out_user():
    if 'user_token' in st.session_state:
        del st.session_state['user_token']
    if 'user_email' in st.session_state:
        del st.session_state['user_email']
    if 'user' in st.session_state:
        del st.session_state['user']
        
def send_password_reset(email):
    firebase_auth.send_password_reset_email(email)