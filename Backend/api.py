from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage,BaseMessage,AIMessage


from database import db
from models import ChatSchema
import os

load_dotenv()

# Allow frontend URLs to call API
origins = [
    "http://localhost:3000",  # your frontend URL
    # add more origins if needed
]

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM directly
llm = ChatOllama(model="gpt-oss:20b-cloud")
chain = llm | StrOutputParser()

# Request model for sending a new query
class QueryRequest(BaseModel):
    query: str
    userId: str

# Request model for fetching previous chats
class FetchChatsRequest(BaseModel):
    userId: str

# Simple root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Endpoint to ask AI
@app.post("/ask-llm")
async def ask_llm(request: QueryRequest):
    user_query = request.query
    user_id = request.userId

    # 1️⃣ Fetch previous messages
    chat_doc = await db.chats.find_one({"user_id": user_id})
    db_messages = chat_doc["messages"] if chat_doc else []

    # 2️⃣ Convert DB messages to ChatMessageHistory format
    messages = []
    for msg in db_messages:
        if msg["type"] == "user":
            messages.append(HumanMessage(content=msg["text"]))
        else:
            messages.append(AIMessage(content=msg["text"]))

    # 3️⃣ Add the new user message
    messages.append(HumanMessage(content=user_query))

    # 4️⃣ Invoke LLM directly
    ai_response = chain.invoke(messages)

    # 5️⃣ Prepare messages to save in DB
    new_messages = [
        {"type": "user", "text": user_query},
        {"type": "assistant", "text": ai_response}
    ]

    if chat_doc:
        # Update existing chat
        await db.chats.update_one(
            {"user_id": user_id},
            {"$push": {"messages": {"$each": new_messages}}}
        )
    else:
        # Create new chat
        chat_data = ChatSchema(user_id=user_id, messages=new_messages).model_dump()
        await db.chats.insert_one(chat_data)

    # 6️⃣ Return AI response
    return {"type": "ai", "text": ai_response}

@app.post("/get-chats")
async def get_chats(request: FetchChatsRequest):
    user_id = request.userId

    # Fetch the chat document from MongoDB
    chat_doc = await db.chats.find_one({"user_id": user_id})

    if not chat_doc:
        # No chat found for this user
        return {"messages": []}

    # Extract messages
    chat_history = chat_doc.get("messages", [])
    return {"messages": chat_history}