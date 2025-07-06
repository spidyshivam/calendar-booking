import streamlit as st
import requests
import uuid
from dotenv import load_dotenv

st.title("📅 Google Calendar Booking Agent")

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you book an appointment?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={"message": prompt, "session_id": st.session_state.session_id}
                )
                response.raise_for_status()
                assistant_response = response.json()["response"]
                message_placeholder.markdown(assistant_response)
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to the backend: {e}")
                assistant_response = "Sorry, I'm having trouble connecting to my brain right now."
                message_placeholder.markdown(assistant_response)

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
