import streamlit as st
import uuid
from db import init_db, create_conversation, get_conversations, save_message, get_messages
from chatbot import get_ai_response

# Initialize database
init_db()

st.set_page_config(page_title="Ollama Chatbot", page_icon="🤖")

st.title("🤖 Ollama Chatbot")

# --- Sidebar: Conversation Threads ---
st.sidebar.header("Conversations")

conversations = get_conversations()
conversation_dict = {title: cid for cid, title in conversations}

# Option to create new conversation
new_conv_title = st.sidebar.text_input("New Conversation Title")
if st.sidebar.button("Create"):
    if new_conv_title.strip() != "":
        new_id = str(uuid.uuid4())
        create_conversation(new_id, new_conv_title)
        st.experimental_rerun()

# Select conversation
selected_title = st.sidebar.selectbox(
    "Select Conversation",
    options=[title for title, _ in conversation_dict.items()],
    index=0 if conversation_dict else None
)
selected_id = conversation_dict.get(selected_title) if selected_title else None

# --- Main Chat Area ---
if selected_id:
    # Load previous messages
    chat_history = get_messages(selected_id)

    for role, content in chat_history:
        if role == "user":
            st.markdown(f"**You:** {content}")
        else:
            st.markdown(f"**Bot:** {content}")

    # Input for new message
    user_input = st.text_input("Type your message:", key="input")

    if st.button("Send"):
        if user_input.strip() != "":
            # Save user message
            save_message(selected_id, "user", user_input)

            # Get AI response
            full_history = get_messages(selected_id)
            ai_reply = get_ai_response(full_history)

            # Save AI response
            save_message(selected_id, "assistant", ai_reply)

            st.experimental_rerun()
