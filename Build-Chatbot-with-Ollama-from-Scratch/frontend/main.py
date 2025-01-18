import os

import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

st.title("A Chatbot with Ollama")

query = st.text_input("Enter your question:")

if st.button("Send"):
    if query:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"query": query})
                if response.status_code == 200:
                    full_response = response.json()
                    st.write("Full Response:", full_response['response'])
                    st.write("Response:", full_response['response']['response'])
                else:
                    st.error(f"Backend Error: {response.status_code}")
                    st.write("Backend Error Details:", response.text)
            except requests.exceptions.RequestException as e:
                st.error(f"Error communicating with the backend: {e}")
    else:
        st.error("Please enter a query before sending.")
