import streamlit as st
import requests
import time
import uuid

chat_uuid = "StreamLit_test#" + str(uuid.uuid4())

st.set_page_config(page_title="OTW-AI-Chatbot")
st.title("💬 OTW-AI-Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "state" not in st.session_state:
    st.session_state.state = {"messages": []}

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def response_generator(message):
    for word in message.split():
        yield word + " "
        time.sleep(0.1)


def get_answer(question):
    API_URL = "http://64.226.69.25/api/ask/"
    HEADERS = {
        "ChatID": chat_uuid,
        "Authorization": "254eca5a-84e1-4526-9a4c-a21343019b3b"
    }
    payload = {
        "question": question,
        "customer_id": "0"
    }
    response = requests.post(API_URL, json=payload, headers=HEADERS)
    data = response.json()
    return data["answer"], data["chat_history"]


user_input = st.chat_input("Write your message here")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.state["messages"].append({"role": "user", "content": user_input})

    answer, chat_history = get_answer(user_input)
    if answer:
        st.session_state.state["messages"].append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(answer))
        st.session_state.messages.append({"role": "assistant", "content": response})
