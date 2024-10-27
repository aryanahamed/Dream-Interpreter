import os
from groq import Groq
import streamlit as st

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Streamlit placeholder with title then text input
st.title("Dream Interpreter🌙", anchor=False)
dream = st.text_area("Enter your dream below and I will interpret it for you. The more detailed the better.")

if st.button("💫 Interpret Dream 💫"):
    chat_completion = client.chat.completions.create(
    #
    # Required parameters
    #
    messages=[
        # Set an optional system message. This sets the behavior of the
        # assistant and can be used to provide specific instructions for
        # how it should behave throughout the conversation.
        {
            "role": "system",
            "content": "You are a Dream Interpreter who is an expert at interpreting dreams. You will be given a dream as an input and you will interpret in as much as detail as possible. After that you will return a json format where the following Titles will be the keys and content as the values depending on the dream. Also use an appropriate emoji at the end of each title. Do not put values in a list structure. If there are multiple values just write them side by side with comma. Do not write anything outside of JSON. Make sure to use emojis after every values.\n\nDream Type: Could be Positive, Negative, Horrible, Disheartening, Joyful, Mysterious, Weird, Surreal, Lucid, Recurring etc.[Emoji]\n\nEmotion Intensity: Scale from 1-10 (how intense was the emotion)[Emoji]\n\nDominant Emotion: Fear, Happiness, Sadness, Excitement, Anger, Anxiety, Confusion, Surprise, Peacefulness[Emoji]\n\nVividness: Scale from 1-10 (how vivid or clear was the dream)[Emoji]\n\nReality Connection: Related to current life, Future-focused, Past memories, Fantasy, Alternate Reality[Emoji]\n\nSymbols or Themes: Common symbols (e.g., falling, flying, being chased, water, animals) Associated themes like success, conflict, or loss[Emoji]\n\nCharacters Involved: Family, Friends, Strangers, Animals, Celebrities, Unknown Entities[Emoji]\n\nSettings: Familiar place, Unknown location, Nature, Indoors, Cityscape, Fantasy land[Emoji]\n\nPotential Physical Reactions: Woke up sweating, Fast heartbeat, Heavy breathing, Calm wake-up[Emoji]\n\nPotential Lucidity Level: Lucid, Semi-Lucid, Non-Lucid[Emoji]\n\nDetailed Interpretation: [Give your interpretation here. Be as much accurate and detailed as possible. Try to understand what the user must have faced recently that caused the dream and try to relate it with recent events][No Emoji]",
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": dream,
        }
    ],

    # The language model which will generate the completion.
    model="llama3-70b-8192",

    #
    # Optional parameters
    #

    # Controls randomness: lowering results in less random completions.
    # As the temperature approaches zero, the model will become deterministic
    # and repetitive.
    temperature=1,

    # The maximum number of tokens to generate. Requests can use up to
    # 32,768 tokens shared between prompt and completion.
    max_tokens=2048,

    # Controls diversity via nucleus sampling: 0.5 means half of all
    # likelihood-weighted options are considered.
    top_p=1,

    # A stop sequence is a predefined or user-specified text string that
    # signals an AI to stop generating content, ensuring its responses
    # remain focused and concise. Examples include punctuation marks and
    # markers like "[end]".
    stop=None,

    # If set, partial message deltas will be sent.
    stream=False,
    )
    dream_json = chat_completion.choices[0].message.content
    
    st.write(dream_json)
    
    type(dream_json)