import os
from groq import Groq
import streamlit as st
import json

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def parse_json(json_string):
    try:
        # Attempt to load the string as JSON
        return json.loads(json_string)
    except json.JSONDecodeError:
        # If JSON decoding fails, display an error message
        st.error("The JSON string is not formatted correctly.")
        return None

st.title("Dream Interpreter🌙", anchor=False)
dream = st.text_area("Enter your dream below and I will interpret it for you. The more detailed the better.", height=200, max_chars=2000)

if st.button("💫 Interpret Dream 💫"):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": ''' You are a Dream Interpreter who is an expert at interpreting dreams. You will be given a dream as an input and you will
            interpret in as much as detail as possible. After that you will return a json format where the following Titles will be the keys and
            content as the values depending on the dream. Also use an appropriate emoji at the end of each title. Make sure the json format is correct and ogranised.
            Do not write anything outside of JSON. Make sure to use emojis after every values. Escape the inner quotes of quotes with a backslash. 
            {
                    "Dream Type": "Surreal 🤯",
                    "Emotion Intensity": "8/10 😨",
                    "Dominant Emotion": "Fear 😨",
                    "Vividness": "9/10 🔥",
                    "Reality Connection": "Current Life Concerns 💔",
                    "Symbols or Themes": "Falling, Loss of Control, Fear of Failure 🏗️",
                    "Characters Involved": "Only myself 👥",
                    "Settings": "Unfamiliar Building, Urban Cityscape 🏙️",
                    "Potential Physical Reactions": "Woke up with a sudden jerk, Fast heartbeat 💥",
                    "Potential Lucidity Level": "Non-Lucid 😴",
                    "Shadow Aspect": "Fear of Vulnerability 👤",
                    "Secret Message to Self": "Trust Your Instincts 🌌",
                    "Advice": "(Add a funny quote very much related to the dream that is also an advice. Make it Rude and Motivational with curse words like Listen Motherfucker or What the fuck.)",
                    "Roast": "(Roast the user depending on the context of the dream. Make it creative and witty.)",
                    "Detailed Interpretation": (Write this in markdown and format in a interesting way emphasizing important words/sentences.
                                                Escape any newline characters with a backslash. Do not use headings in this section and do not put any advice here.)", 
                                                "It seems like you are experiencing a sense of losing control or feeling overwhelmed in your waking life..."
                    
            }''',
        },
        {
            "role": "user",
            "content": dream,
        }
    ],
    
    
    model="llama3-70b-8192",
    temperature=0.8,
    # Requests can use up to
    # 32,768 tokens shared between prompt and completion.
    max_tokens=2048,
    top_p=1,
    stop=None,
    stream=False,
    )
    
    dream_json = chat_completion.choices[0].message.content
    # st.write(dream_json)
    # print(dream_json)
    parsed_data = parse_json(dream_json)
    # print(parsed_data)
    
    
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
    else:
        st.write("Oops! The AI is tired and outputting gibberish. Please press the button again.")
    
    
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

            
