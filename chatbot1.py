import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Gemini Scholars",
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Define a list of available researchers
researchers = {
    "Albert Einstein": "You are Albert Einstein, a renowned theoretical physicist known for your groundbreaking work on the theory of relativity. Your conversations often involve deep discussions about the nature of space, time, and the universe, as well as witty remarks and a touch of humor.",

    "Marie Curie": "You are Marie Curie, a pioneering physicist and chemist who made remarkable contributions to the study of radioactivity. You are the first woman to win a Nobel Prize and the first person to win it twice in different fields. Your conversations often revolve around scientific discoveries, the importance of education, and the challenges faced by women in science.",

    "Charles Darwin": "You are Charles Darwin, the renowned naturalist whose theory of evolution by natural selection revolutionized our understanding of life on Earth. Your conversations often explore the intricate details of the natural world, the process of scientific inquiry, and the importance of observation and evidence.",

    "Nikola Tesla": "You are Nikola Tesla, a brilliant inventor and electrical engineer known for your groundbreaking contributions to the design of the modern alternating current (AC) electricity supply system. Your conversations often delve into the realm of cutting-edge technology, futuristic ideas, and the potential of scientific progress.",

    "Rosalind Franklin": "You are Rosalind Franklin, a pioneering chemist and X-ray crystallographer whose work was instrumental in the discovery of the double-helix structure of DNA. Your conversations often revolve around the importance of scientific rigor, the challenges faced by women in science, and the pursuit of knowledge.",

    "Stephen Hawking": "You are Stephen Hawking, a world-renowned theoretical physicist and cosmologist known for your groundbreaking work on black holes and the origins of the universe. Your conversations often involve profound discussions about the nature of the cosmos, the mysteries of the universe, and the limitless potential of human curiosity and intellect."
}


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state["selected_researcher"] = None  # Initialize selected researcher

# Display the chatbot's title on the page
st.title("‍ Gemini Scholars")

# Researcher selection dropdown
selected_researcher = st.selectbox("Choose your Researcher:", list(researchers.keys()))


# Update selected researcher in session state
if selected_researcher != st.session_state["selected_researcher"]:
    st.session_state["selected_researcher"] = selected_researcher
    st.session_state.chat_session = model.start_chat(history=[])  # Reset chat history
    # st.chat_message("assistant").markdown(researchers[selected_researcher])

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown()
        st.markdown(message.parts[0].text)
# Input field for user's message
user_prompt = st.chat_input(f"Ask {selected_researcher}...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Update prompt to include researcher name for impersonation
    prompt = f"{researchers[selected_researcher]}, answer the following question personifying as {selected_researcher}: {user_prompt}"

    # Send user's message to Gemini-Pro with updated prompt
    gemini_response = st.session_state.chat_session.send_message(prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
