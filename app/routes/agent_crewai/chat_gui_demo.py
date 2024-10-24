# -*- coding: utf-8 -*-

import json
import sys
from typing import Any

import requests
import streamlit as st

# Create a variable to store the current conversation step
conversation_step = 0
default_api_endpoint = "http://localhost:8080/blog_builder/researcher"
# default_api_endpoint = "http://localhost:8080/blog_builder/chat"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        api_endpoint = sys.argv[1]
    else:
        api_endpoint = default_api_endpoint


# Define a function to send the user's message to the API and update the conversation context
def send_message_to_api(message):
    global context, conversation_step
    data = {
        "query": message,
        "enable_internet_search": st.session_state.enable_internet,
        "enable_wikipedia": st.session_state.enable_wikipedia,
        "collection_id": st.session_state.collection_id,
    }
    headers = {"Integrations-API-Key": "dev-only-token"}
    response = requests.post(api_endpoint, json=data, headers=headers, stream=True)
    conversation_step += 1
    print(process_api_response)
    return response


# Define a function to process the API response and update the conversation history and log stream
def process_api_response(response) -> Any:
    global conversation_history, log_stream
    result = ""
    for line in response.iter_lines():
        if line:
            message = json.loads(line.decode("utf-8"))
            print(message)
            if message["status"] == "success":
                event = message["response"][0]
                if event["type"] == "log":
                    result = f"{event['message']}  \n"
                    yield result
                elif event["type"] == "text":
                    result = f"{event['message']}  \n"
                    st.session_state.messages.append({"role": "assistant", "content": result})
                    yield result
                elif event["type"] == "tool":
                    result = f"These are tool invocation parameters: + {json.dumps(event['properties'])}  \n"
                    st.session_state.messages.append({"role": "assistant", "content": result})
                    yield result
                elif event["type"] == "final_answer":
                    result = f"{event['message']} \n"
                    st.session_state.messages.append({"role": "assistant", "content": result})
                    yield result


def process_events(message):
    response = send_message_to_api(message)
    events = process_api_response(response)
    print("events", events)
    return events


st.title("Agent chat")

# Define the checkboxes

st.checkbox("Enable Wikipedia", key="enable_wikipedia", value=True)
st.checkbox("Enable internet search", key="enable_internet", value=True)
st.text_input("You can enter a collection id to search into:", value="", key="collection_id")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    print("This is the prompt")
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        context = ""
        for message in st.session_state.messages:
            context = context + f"{message['role']}:{message['content']}"
        response = st.write_stream(process_events(context))
        # Add assistant response to chat history
    print("This is the Agent response", response)
