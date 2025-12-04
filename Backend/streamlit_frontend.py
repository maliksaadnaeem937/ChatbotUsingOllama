from email import message
import streamlit as st
from langchain_core.messages import HumanMessage,BaseMessage

from langgraph_backend import workflow


thread_id='1'
config={
            'configurable':{
                'thread_id':thread_id
            }
        }


if 'message_history' not in st.session_state:
    st.session_state.message_history = []
message_history = st.session_state.message_history
st.title("Chatbot Interface")

user_message=st.chat_input("Type here : ")

if user_message:
    message_history.append({"role":"user","content":user_message})

    initial_state = {"messages": [HumanMessage(content=user_message)]}

    final_state = workflow.invoke(initial_state, config=config)
    assistant_message = final_state["messages"][-1].content
    message_history.append({"role":"assistant","content":assistant_message})

        
    for message in message_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            
        
   
        
    
    
        
