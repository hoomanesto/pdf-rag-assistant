import streamlit as st
import requests

import os
os.environ["NO_PROXY"] = "127.0.0.1,localhost"
proxies={"http": None, "https": None}

st.set_page_config(page_title="RAG Chat", page_icon="🤖")

st.title("📚 RAG Chat System")

API_URL = "http://127.0.0.1:8000/ask"

# store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input box
user_input = st.chat_input("Ask something...")

if user_input:
    # show user message
    st.chat_message("user").write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # send to FastAPI
    response = requests.post(
    API_URL,
    json={"question": user_input},
    proxies={"http": None, "https": None}
)

    answer = response.json()["answer"]

    # show assistant message
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})