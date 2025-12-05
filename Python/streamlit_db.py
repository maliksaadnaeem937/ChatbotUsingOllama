import streamlit as st
import time
import uuid
from langchain_core.messages import HumanMessage, AIMessage
from langgraph_backend import workflow, retrieve_all_threads

# ------------------ Helper functions ------------------

def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    st.session_state.message_history = []
    st.session_state.thread_id = generate_thread_id()
    add_thread_to_history(st.session_state.thread_id)

def add_thread_to_history(thread_id):
    if thread_id not in st.session_state.chat_threads:
        st.session_state.chat_threads.append(thread_id)

def load_conversation(thread_id):
    state = workflow.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])

# ------------------ Session state initialization ------------------

if 'message_history' not in st.session_state:
    st.session_state.message_history = []

if 'chat_threads' not in st.session_state:
    st.session_state.chat_threads = retrieve_all_threads()

# Only set thread_id if there are no previous threads
if 'thread_id' not in st.session_state:
    if len(st.session_state.chat_threads) == 0:
        st.session_state.thread_id = generate_thread_id()
        add_thread_to_history(st.session_state.thread_id)
    else:
        # Let user select thread from sidebar; don't auto-create
        st.session_state.thread_id = None

# ------------------ Sidebar UI ------------------

with st.sidebar:
    if st.button("New Chat"):
        reset_chat()

    st.header("My Conversations")
    for thread_id in st.session_state.chat_threads[::-1]:
        if st.button(thread_id):
            st.session_state.thread_id = thread_id
            messages = load_conversation(thread_id)
            temp_messages = []
            for msg in messages:
                role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
                temp_messages.append({'role': role, 'content': msg.content})
            st.session_state.message_history = temp_messages

# ------------------ Main chat UI ------------------

st.title("Langgraph Streaming Chat Bot")
message_history = st.session_state.message_history

# Show all previous messages
for message in message_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_message = st.chat_input("Type here:")

if user_message:
    # If no thread is selected yet, create a new one
    if st.session_state.thread_id is None:
        reset_chat()

    # Display user message
    message_history.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    # Prepare workflow input
    initial_state = {"messages": [HumanMessage(content=user_message)]}
    config = {'configurable': {'thread_id': st.session_state.thread_id}}

    # Streaming AI response
    def get_response():
        for msg_chunk, _ in workflow.stream(initial_state, config=config, stream_mode="messages"):
            if isinstance(msg_chunk, AIMessage) and msg_chunk.content:
                words = msg_chunk.content.split()
                for word in words:
                    yield word + " "
                    time.sleep(0.02)

    # Show AI streaming message
    with st.chat_message("assistant"):
        assistant_message = st.write_stream(get_response())

    # Save AI response
    message_history.append({"role": "assistant", "content": assistant_message})
