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
    "Albert Einstein": "Welcome to the world of relativity! I'm happy to discuss my theories and answer any questions you might have about space, time, and the universe.",
    "Marie Curie": "Greetings! I'm delighted to share my knowledge and experiences in the field of radioactivity and the discovery of radium and polonium.",
    "Charles Darwin": "Hello, fellow explorer! Let's delve into the fascinating world of evolution and natural selection. I'd be glad to clarify any doubts you may have.",
    "Nikola Tesla": "Welcome, my friend! I'm excited to discuss my groundbreaking inventions and innovations in the field of electricity and electromagnetism.",
    "Rosalind Franklin": "Hello there! I'm honored to share my insights into the structure of DNA and the role of X-ray crystallography in unraveling its mysteries.",
    "Stephen Hawking": "Greetings, fellow thinker! Let's embark on a journey through the cosmos and explore the mysteries of black holes, space-time, and the origin of the universe."
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
    st.chat_message("assistant").markdown(researchers[selected_researcher])

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
    prompt = f"As {selected_researcher}, answer the following question: {user_prompt}"

    # Send user's message to Gemini-Pro with updated prompt
    gemini_response = st.session_state.chat_session.send_message(prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
