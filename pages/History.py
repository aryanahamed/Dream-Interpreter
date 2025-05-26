from datetime import datetime
import streamlit as st
import json
from firebase_config import db, firestore

st.title("📜 Dream History")

if db is None:
    st.error("Database connection failed. Please check your Firebase configuration and restart the app.")
    st.stop()

def get_dream_history(user_email):
    dreams = (
        db.collection("dreams")
        .where("user_email", "==", user_email)
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .stream()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in dreams]

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
                    formatted_date = 'N/A'
                st.markdown(f"**Date:** {formatted_date}")
                st.markdown(f"**Dream:** {dream.get('dream', '')}")
                tooltips = {
                    "Dream Type": "The general category or theme of your dream (e.g., lucid, nightmare, recurring).",
                    "Emotion Intensity": "How strong the emotions felt during the dream were.",
                    "Dominant Emotion": "The main emotion you experienced in the dream.",
                    "Vividness": "How clear and detailed the dream felt.",
                    "Reality Connection": "How much the dream relates to your real life or current events.",
                    "Symbols or Themes": "Key symbols, motifs, or themes that appeared in your dream.",
                    "Characters Involved": "People, animals, or entities present in your dream.",
                    "Settings": "The locations or environments where the dream took place.",
                    "Potential Physical Reactions": "Physical sensations or reactions you noticed during or after the dream.",
                    "Potential Lucidity Level": "How aware you were that you were dreaming.",
                    "Shadow Aspect": "Hidden or unconscious aspects of yourself reflected in the dream.",
                    "Secret Message to Self": "A possible message your subconscious is trying to send you.",
                    "Detailed Interpretation": "A comprehensive analysis of your dream's meaning."
                }
                for key, value in interpretation.items():
                    if key != "Title" and key != "Emoji":
                        tooltip = tooltips.get(key, "")
                        st.markdown(
                            f"""**{key}:** <span title="{tooltip}" style="cursor: help; color: #888;">&#9432;</span> {value}""",
                            unsafe_allow_html=True
                        )
                delete_button = st.button("Delete", key=f"delete_{dream['id']}")
                if delete_button:
                    db.collection("dreams").document(dream["id"]).delete()
                    st.success("Dream deleted.")
                    st.experimental_rerun()
    else:
        st.info("No dream history found")
else:
    st.warning("You are not logged in.")
    if st.button("Go to Login"):
        st.switch_page("pages//Login.py")
