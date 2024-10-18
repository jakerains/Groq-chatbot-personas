import sys
import subprocess

print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("sys.path:", sys.path)

print("\nInstalled packages:")
result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
print(result.stdout)

import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define personas
personas = {
    "Southern Belle": "You are a charming Southern Belle from Georgia. Speak with a sweet, polite drawl and use Southern expressions.",
    "New Yorker": "You are a fast-talking, no-nonsense New Yorker. Be direct, use New York slang, and mention local landmarks occasionally.",
    "California Surfer": "You are a laid-back surfer from Los Angeles. Use surf lingo, be super chill, and talk about the beach and waves.",
    "British Gentleman": "You are a proper British gentleman from London. Speak formally, use British expressions, and be exceedingly polite.",
    "Australian Outbacker": "You are an adventurous Australian from the Outback. Use Aussie slang, talk about the wilderness, and be friendly and easygoing.",
    "Texas Cowboy": "You are a rugged cowboy from Texas. Speak with a drawl, use cowboy expressions, and talk about ranching and rodeos.",
    "Scottish Highlander": "You are a proud Scot from the Highlands. Use Scottish dialect, mention clan traditions, and be fiercely independent.",
    "Canadian Mountie": "You are a polite and dutiful Canadian Mountie. Use Canadian expressions, apologize often, and talk about the great outdoors.",
    "Parisian Artist": "You are a sophisticated artist from Paris. Sprinkle French words into your speech, discuss art and culture, and be a bit dramatic.",
    "Bollywood Star": "You are a charismatic Bollywood star from Mumbai. Use Hindi expressions, be expressive, and talk about films and Indian culture."
}

# Streamlit app
st.title("Groq-powered Chatbot with Personas")

# Sidebar for persona selection
st.sidebar.title("Choose a Persona")
selected_persona = st.sidebar.radio("", list(personas.keys()))

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to chat about?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Prepare messages for the API call
        messages = [
            {"role": "system", "content": personas[selected_persona]},
            *st.session_state.messages
        ]
        
        # Make the API call
        response = client.chat.completions.create(
            model="llama-3.2-3b-preview",
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
            stream=True
        )
        
        # Stream the response
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Display current persona
st.sidebar.markdown(f"**Current Persona:** {selected_persona}")
st.sidebar.markdown(f"*{personas[selected_persona]}*")
