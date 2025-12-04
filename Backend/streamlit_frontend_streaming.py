from email import message
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
import time

from langgraph_backend import workflow

thread_id = '1'
config = {
    'configurable': {
        'thread_id': thread_id
    }
}

if 'message_history' not in st.session_state:
    st.session_state.message_history = []

message_history = st.session_state.message_history
st.title("Chatbot Interface")

# Show all previous messages
for message in message_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
user_message = st.chat_input("Type here: ")

if user_message:
    # Show user message
    message_history.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)
    
    # Send to AI
    initial_state = {"messages": [HumanMessage(content=user_message)]}
    
    # Simple generator function - just extracts content from chunks
    def get_response():
        for message_chunk, metadata in workflow.stream(
            initial_state,
            config=config,
            stream_mode="messages"
        ):
            # Only yield if it's AI message and has content
            if isinstance(message_chunk, AIMessage) and message_chunk.content:
                    # Split content into words for smoother effect
                    words = message_chunk.content.split()
                    for word in words:
                        yield word + " "
                        time.sleep(0.02)
    
    # Show AI response with streaming
    with st.chat_message("assistant"):
        assistant_message = st.write_stream(get_response())
    
    # Save AI response
    message_history.append({"role": "assistant", "content": assistant_message})