import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
from dotenv import load_dotenv
import streamlit as st
from google.oauth2 import service_account
from google.cloud import firestore as cloud_firestore
import requests
import json
import python_jwt as jwt

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

db = None
auth_base_url = f"https://identitytoolkit.googleapis.com/v1"

def _make_auth_request(endpoint, payload):
    api_key = firebaseConfig["apiKey"]
    url = f"{auth_base_url}/{endpoint}?key={api_key}"
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        error_message = "Unknown error"
        try:
            error_data = e.response.json()
            error_message = error_data.get("error", {}).get("message", "Unknown error")
        except:
            pass
        return None, error_message

try:
    if not firebase_admin._apps:
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
                db = None
            else:
                cred = credentials.Certificate(service_account_info)
                firebase_admin.initialize_app(cred)
                db = firestore.client()
        
except Exception as e:
    st.error(f"Firebase Admin initialization error: {e}")
    db = None

def sign_up_user(email, password):
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    result, error = _make_auth_request("accounts:signUp", payload)
    if error:
        return None, error
    return result, None

def sign_in_user(email, password):
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    result, error = _make_auth_request("accounts:signInWithPassword", payload)
    if error:
        return None, error
    return result, None

def sign_out_user():
    if 'user_token' in st.session_state:
        del st.session_state['user_token']
    if 'user_email' in st.session_state:
        del st.session_state['user_email']
    if 'user' in st.session_state:
        del st.session_state['user']
        
def send_password_reset(email):
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": email
    }
    result, error = _make_auth_request("accounts:sendOobCode", payload)
    if error:
        st.error(f"Error sending password reset email: {error}")
        return False
    return True
