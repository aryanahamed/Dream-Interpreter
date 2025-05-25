from datetime import datetime
import streamlit as st
import json
from firebase_config import db, firestore

st.title("📜 Dream History")

def get_dream_history(user_email):
    dreams = (
        db.collection("dreams")
        .where("user_email", "==", user_email)
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .stream()
    )
    return [doc.to_dict() for doc in dreams]

user_email = st.session_state.get("user_email")
if user_email:
    st.subheader(f"Dream history for {user_email}")
    dream_history = get_dream_history(user_email)
    if dream_history:
        for idx, dream in enumerate(dream_history, 1):
            interpretation = dream.get("interpretation")
            if isinstance(interpretation, str):
                try:
                    interpretation = json.loads(interpretation.replace("'", '"'))
                except Exception:
                    interpretation = {"Detailed Interpretation": interpretation}
            title = interpretation.get("Title", f"Dream {idx}")
            emoji = interpretation.get("Emoji", "🌙")
            with st.expander(f"{emoji} {title} {emoji}"):
                raw_date = dream.get("created_at", 'N/A')
                if raw_date != 'N/A':
                    formatted_date = raw_date.strftime("%d-%m-%Y %I:%M %p")
                else:
                    pass
                st.markdown(f"**Date:** {formatted_date}")
                st.markdown(f"**Dream:** {dream.get('dream', '')}")
                for key, value in interpretation.items():
                    if key != "Title" and key != "Emoji":
                        st.markdown(f"**{key}:** {value}")
    else:
        st.info("No dream history found")
else:
    st.warning("You are not logged in.")
    if st.button("Go to Login"):
        st.switch_page("pages//Login.py")
