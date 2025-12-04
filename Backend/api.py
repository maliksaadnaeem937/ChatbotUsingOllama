# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from backend import workflow
from langchain_core.messages import HumanMessage,AIMessage,BaseMessage
from fastapi.middleware.cors import CORSMiddleware

from database import db
from models import ChatSchema

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
    allow_headers=["*"],
)

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

    # 2️⃣ Convert DB messages to BaseMessage objects
    messages: list[BaseMessage] = [
        HumanMessage(content=msg["text"]) if msg["type"] == "user"
        else AIMessage(content=msg["text"])
        for msg in db_messages
    ]

    # 3️⃣ Add the new user message
    messages.append(HumanMessage(content=user_query))

    # 4️⃣ Create initial state and run workflow
    initial_state = {"messages": messages}
    final_state = workflow.invoke(initial_state)

    # 5️⃣ Get AI response (last message)
    ai_message_obj: BaseMessage = final_state["messages"][-1]
    ai_text = ai_message_obj.content

    # 6️⃣ Prepare messages to save in DB
    new_messages = [
        {"type": "user", "text": user_query},
        {"type": "assistant", "text": ai_text}
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

    # 7️⃣ Return AI response
    return {"type": "ai", "text": ai_text}






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
    print(chat_history)
    return {"messages": chat_history}
    
    
    
