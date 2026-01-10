from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from fastapi.middleware.cors import CORSMiddleware
from database import db
from models import ChatSchema
from dotenv import load_dotenv
import PyPDF2
from io import BytesIO

load_dotenv()

app = FastAPI()

# ---------------- CORS ----------------
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- LLM ----------------
llm = ChatOllama(model="gpt-oss:20b-cloud")
chain = llm | StrOutputParser()

# ---------------- Request Models ----------------
class QueryRequest(BaseModel):
    query: str
    userId: str

class FetchChatsRequest(BaseModel):
    userId: str

# ---------------- Root ----------------
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# ---------------- Ask AI ----------------
@app.post("/ask-llm")
async def ask_llm(request: QueryRequest):
    try:
        user_query = request.query
        user_id = request.userId

        chat_doc = await db.chats.find_one({"user_id": user_id})
        db_messages = chat_doc["messages"] if chat_doc else []

        # System message to enforce plain text
        messages = [
            SystemMessage(
                content=(
                    "You are a plain-text AI assistant. Respond strictly in plain text only. "
                    "Do NOT use Markdown, HTML, code blocks, emojis, lists, or any formatting. "
                    "Only write the text content directly."
                )
            )
        ]

        for msg in db_messages:
            if msg["type"] == "user":
                messages.append(HumanMessage(content=msg["text"]))
            else:
                messages.append(AIMessage(content=msg["text"]))

        messages.append(HumanMessage(content=user_query))
        ai_response = chain.invoke(messages)

        # Save in DB
        new_messages = [
            {"type": "user", "text": user_query},
            {"type": "assistant", "text": ai_response}
        ]

        if chat_doc:
            await db.chats.update_one(
                {"user_id": user_id},
                {"$push": {"messages": {"$each": new_messages}}}
            )
        else:
            chat_data = ChatSchema(user_id=user_id, messages=new_messages).model_dump()
            await db.chats.insert_one(chat_data)

        return {"type": "ai", "text": ai_response}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ---------------- Upload Document + Ask AI ----------------
@app.post("/ask-llm-doc")
async def upload_document(
    userId: str = Form(...),
    userQuery: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # ---------------- Extract text from file ----------------
        content = ""
        file_content = await file.read()

        if file.filename.lower().endswith((".txt", ".md")):
            content = file_content.decode("utf-8")
        elif file.filename.lower().endswith(".pdf"):
            pdf_file = BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            content = "\n".join(
                page.extract_text() or "" for page in pdf_reader.pages
            )
        else:
            return JSONResponse(
                status_code=400,
                content={"error": "Unsupported file type. Only PDF or TXT allowed."}
            )

        # ---------------- Fetch previous chat ----------------
        chat_doc = await db.chats.find_one({"user_id": userId})
        db_messages = chat_doc["messages"] if chat_doc else []

        # ---------------- First LLM call (document answer) ----------------
        messages = [
            SystemMessage(
                content=(
                    "You are a document analysis assistant. "
                    "Answer ONLY from the document. "
                    "If the answer is not found, say: "
                    "'This information is not available in the document.'"
                )
            )
        ]

        for msg in db_messages:
            if msg["type"] == "user":
                messages.append(HumanMessage(content=msg["text"]))
            else:
                messages.append(AIMessage(content=msg["text"]))

        messages.append(
            HumanMessage(
                content=f"{userQuery}\n\nDocument content:\n{content}"
            )
        )

        raw_ai_response = chain.invoke(messages)

        # ---------------- Second LLM call (CLEAN RESPONSE) ----------------
        clean_messages = [
            SystemMessage(
                content=(
                    "You are a text cleaner. "
                    "Convert the given text into clean plain text. "
                    "Remove ALL HTML, markdown, emojis, bullet points, "
                    "special symbols, and formatting. "
                    "Do not add new information. "
                    "Return plain text only."
                )
            ),
            HumanMessage(content=raw_ai_response)
        ]

        cleaned_ai_response = chain.invoke(clean_messages)

        # ---------------- Save in DB ----------------
        new_messages = [
            {
                "type": "user",
                "text": f"{userQuery} [Document uploaded: {file.filename}]"
            },
            {
                "type": "assistant",
                "text": cleaned_ai_response
            }
        ]

        if chat_doc:
            await db.chats.update_one(
                {"user_id": userId},
                {"$push": {"messages": {"$each": new_messages}}}
            )
        else:
            chat_data = ChatSchema(
                user_id=userId,
                messages=new_messages
            ).model_dump()
            await db.chats.insert_one(chat_data)

        return {"ai_response": cleaned_ai_response}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
# ---------------- Fetch Chats ----------------
@app.post("/get-chats")
async def get_chats(request: FetchChatsRequest):
    try:
        user_id = request.userId
        chat_doc = await db.chats.find_one({"user_id": user_id})
        chat_history = chat_doc.get("messages", []) if chat_doc else []
        return {"messages": chat_history}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
