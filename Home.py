from datetime import datetime
import os
import streamlit as st
import json
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import types
from firebase_admin import firestore
from firebase_config import sign_out_user, db

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def parse_json(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        st.error("The JSON string is not formatted correctly.")
        return None
    
def save_dream_to_firestore(user_email, dream_text, interpretation):
    doc_ref = db.collection("dreams").document()
    doc_ref.set({
        "user_email": user_email,
        "created_at": firestore.SERVER_TIMESTAMP,
        "dream": dream_text,
        "interpretation": interpretation
    })

st.title("Dream Interpreter🌙", anchor=False)

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    if st.button("Login to save your dream interpretations"):
        st.switch_page("pages/Login.py")
else:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success(f"Logged in as {st.session_state.user}")
    with col2:
        if st.button("Logout"):
            sign_out_user()
            st.switch_page("Home.py")

dream = st.text_area("Enter your dream below and I will interpret it for you. The more detailed the better. Do not put any personal information", height=200)

if st.button("💫 Interpret Dream 💫") and dream:
    model = genai.GenerativeModel('gemini-2.0-flash')

    system_prompt = '''You are a Dream Interpreter who is an expert at interpreting dreams. You will be given a dream as an input and you will interpret in as much detail as possible. After that you will return ONLY a json format where the following Titles will be the keys and content as the values depending on the dream. Also use an appropriate emoji at the end of each title. Make sure the json format is correct and organised. Do not write anything outside of the JSON object itself. Make sure to use emojis after every values. Escape the inner quotes of quotes with a backslash.
    Additionally, generate a Two-word title and a relevant emoji that best summarizes the dream. This title should be a two-word phrase and will be used as the dream's title.
{
        "Title": "...",  # Two words only (no emoji with title)
        "Emoji": "🌙",  # Relevant emoji for the dream
        "Dream Type": "...",
        "Emotion Intensity": "...",
        "Dominant Emotion": "...",
        "Vividness": "...",
        "Reality Connection": "...",
        "Symbols or Themes": "...",
        "Characters Involved": "...",
        "Settings": "...",
        "Potential Physical Reactions": "...",
        "Potential Lucidity Level": "...",
        "Shadow Aspect": "...",
        "Secret Message to Self": "...",
        "Detailed Interpretation": "..."

}'''
    user_content = dream

    prompt_parts = [
        system_prompt,
        "\nUser Dream:\n",
        user_content
    ]

    try:
        response = model.generate_content(
            prompt_parts,
            generation_config=types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=2048,
                top_p=0.95,
            )
        )
        dream_json = response.text

    except Exception as e:
        st.error(f"An error occurred while contacting the Gemini API: {e}")
        dream_json = None
        parsed_data = None
    
    if dream_json:
        if dream_json.startswith("```json"):
            dream_json = dream_json[len("```json"):].strip()
        if dream_json.startswith("```"):
             dream_json = dream_json[len("```"):].strip()
        if dream_json.endswith("```"):
            dream_json = dream_json[:-len("```")].strip()

        parsed_data = parse_json(dream_json)
    else:
        parsed_data = None

    if parsed_data:
        if st.session_state.user:
            save_dream_to_firestore(st.session_state.user, dream, parsed_data.copy())

        dream_title = parsed_data.get("Title", "Dream")
        dream_emoji = parsed_data.get("Emoji", "🌙")
        st.header(f"{dream_emoji} {dream_title} {dream_emoji}")
        
        parsed_data.pop("Title", None)
        parsed_data.pop("Emoji", None)
        
        iterator = iter(parsed_data.items())

        while True:
            try:
                key1, value1 = next(iterator)

                try:
                    key2, value2 = next(iterator)
                except StopIteration:
                    key2, value2 = None, None

                if key2 is None:
                    wide_col = st.columns(1)[0]
                    with wide_col:
                        st.subheader(key1, anchor=False)
                        st.write(value1)
                    break
                else:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader(key1, anchor=False)
                        st.write(value1)

                    with col2:
                        st.subheader(key2, anchor=False)
                        st.write(value2)

            except StopIteration:
                break
    else:
        if dream_json is not None:
            st.write("Oops! The AI response wasn't valid JSON. Please try again.")

footer="""<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: black;
    color: white;
    text-align: center;
    padding: 10px;
}
.footer p { margin: 0; }
</style>
<div class="footer"> <p>Made with ❤ by Aryan</p> </div>
"""
st.markdown(footer, unsafe_allow_html=True)