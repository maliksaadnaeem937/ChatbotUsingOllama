import streamlit as st
import uuid
from db import init_db, create_conversation, get_conversations, save_message, get_messages
from chatbot import get_ai_response

# Initialize DB
init_db()
st.set_page_config(page_title="Ollama Chatbot", page_icon="🤖")
st.title("🤖 Ollama Chatbot")

# Sidebar: Conversations
st.sidebar.header("Conversations")
conversations = get_conversations()
conversation_dict = {title: cid for cid, title in conversations}

# Create new conversation
new_conv_title = st.sidebar.text_input("New Conversation Title")
if st.sidebar.button("Create") and new_conv_title.strip():
    new_id = str(uuid.uuid4())
    create_conversation(new_id, new_conv_title)

# Select conversation
selected_title = st.sidebar.selectbox(
    "Select Conversation",
    options=[title for title, _ in conversation_dict.items()],
    index=0 if conversation_dict else None
)
selected_id = conversation_dict.get(selected_title) if selected_title else None

# Initialize session_state
if "messages" not in st.session_state or st.session_state.get("selected_id") != selected_id:
    st.session_state["messages"] = get_messages(selected_id) if selected_id else []
    st.session_state["selected_id"] = selected_id

# Display chat
for role, content in st.session_state["messages"]:
    if role == "user":
        st.markdown(f"**You:** {content}")
    else:
        st.markdown(f"**Bot:** {content}")

# Input callback
def submit_message():
    user_input = st.session_state["input_box"]
    if not user_input.strip():
        return
    # Save user message
    save_message(selected_id, "user", user_input)
    st.session_state["messages"].append(("user", user_input))

    # Get AI response
    ai_reply = get_ai_response(st.session_state["messages"])
    save_message(selected_id, "assistant", ai_reply)
    st.session_state["messages"].append(("assistant", ai_reply))

    # Clear input safely
    st.session_state["input_box"] = ""

# Text input with callback
st.text_input("Type your message:", key="input_box", on_change=submit_message)
