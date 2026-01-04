
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import HumanMessage,BaseMessage,AIMessage

from langchain_core.output_parsers import StrOutputParser

from langgraph.graph import add_messages 
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()
import os




class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]
    
    
    

llm = ChatOllama(model="gpt-oss:20b-cloud")
# llm = ChatOllama(model="gemma3:4b")


def  chat_node(state:ChatState):
    chain=llm|StrOutputParser()
    response = chain.invoke(state["messages"])
    return {'messages':[response]}



# creating graph and nodes
graph=StateGraph(ChatState)

graph.add_node("chat_node",chat_node)

# creating edges 
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

workflow=graph.compile()







