import os
from dotenv import load_dotenv
from groq import Groq
import streamlit as st
import json
import yaml
import streamlit_authenticator as stauth

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


# Load config
with open('users.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

# Hash the passwords
hashed_passwords = stauth.Hasher.hash_passwords(config['credentials'])

# Create authenticator without preauthorized parameter
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Login widget
try:
    authenticator.login(location='sidebar')
except Exception as e:
    st.error(e)

if st.session_state['authentication_status']:
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Register to save your entries')

# Sign-up widget
try:
    email_of_registered_user, \
    username_of_registered_user, \
    name_of_registered_user = authenticator.register_user(location='sidebar')
    if email_of_registered_user:
        st.success('User registered successfully')
except Exception as e:
    st.error(e)

def parse_json(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        st.error("The JSON string is not formatted correctly.")
        return None
    
def load_user_dreams(user):
    with open("dreams.json", "r") as file:
        data = json.load(file)
    return data.get(user, [])

def save_user_dream(user, dream_data):
    try:
        with open("dreams.json", "r+") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
            if user not in data:
                data[user] = []
            data[user].append(dream_data)
            file.seek(0)
            json.dump(data, file)
            file.truncate()
    except Exception as e:
        st.error(f"Error saving dream: {e}")
        

st.title("Dream Interpreter🌙", anchor=False)

if st.button("Load your dreams"):
    user = st.session_state.get("username", "default_user")
    dreams = load_user_dreams(user)
    for dream in dreams:
        st.markdown(dream)


dream = st.text_area("Enter your dream below and I will interpret it for you. The more detailed the better.", height=200, max_chars=2000)


if 'click' not in st.session_state:
    st.session_state.click = {1: False, 2: False}

def clicked(button):
    st.session_state.click[button] = True

st.button("💫 Interpret Dream 💫", on_click=clicked, args=[1])

if st.session_state.click.get(1, False):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": ''' You are a Dream Interpreter who is an expert at interpreting dreams. You will be given a dream as an input and you will
            interpret in as much as detail as possible. After that you will return a json format where the following Titles will be the keys and
            content as the values depending on the dream. Also use an appropriate emoji at the end of each title. Make sure the json format is correct and ogranised.
            Do not write anything outside of JSON. Make sure to use emojis after every values. Escape the inner quotes of quotes with a backslash. 
            {
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
                    
            }''',
        },
        {
            "role": "user",
            "content": dream,
        }
    ],
    
    
    model="llama3-70b-8192",
    temperature=0.8,
    max_tokens=2048,
    top_p=1,
    stop=None,
    stream=False,
    )
    
    dream_json = chat_completion.choices[0].message.content
    parsed_data = parse_json(dream_json)
    
    
    if parsed_data:
        st.title("🌟 Interpretation 🌟", anchor=False)

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
    
    st.button("💾 Save your dream 💾", on_click=clicked, args=[2])
    if st.session_state.click[2]:
        user = st.session_state.get("username", "default_user")
        save_user_dream(user, parsed_data)
        st.success("Dream saved successfully!")

    
    
    
    
# Footer
footer="""<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: black;
    color: white;
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    padding: 10px;
}

.footer p {
    margin: 0;
}
</style>

<div class="footer">
    <p>Made with ❤ by Aryan</p>
    <img src='https://groq.com/wp-content/uploads/2024/03/PBG-mark1-color.svg' alt='Powered by Groq for fast inference.' width='50' height='50'/>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

            
