# Chatbot Using Ollama

A modern chatbot application with AI-powered conversations using local LLMs via Ollama.

## 🚀 Features

- **AI Chatbot**: Powered by Ollama with local LLM models
- **Modern Frontend**: Next.js with Firebase authentication
- **FastAPI Backend**: Python backend with async MongoDB
- **User Authentication**: Secure login with Firebase
- **Chat History**: Stores conversations in MongoDB
- **State Management**: Redux Toolkit for frontend state

## 📁 Project Structure

```
ChatbotUsingOllama/
├── FrontEnd/                    # Next.js frontend application
│   ├── components/             # React components
│   ├── src/app/               # Next.js app router pages
│   ├── src/store/             # Redux Toolkit slices
│   ├── src/utils/             # Firebase utilities
│   └── public/                # Static assets
├── Backend/                   # FastAPI backend server
│   ├── api.py                # FastAPI routes
│   ├── backend.py            # LangGraph workflow
│   ├── database.py           # MongoDB connection
│   ├── models.py             # Pydantic models
│   └── requirements.txt      # Python dependencies
└── README.md                 # This file
```

## 🛠️ Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)
- **Ollama** installed locally
- **MongoDB Atlas** account (or local MongoDB)
- **Firebase** account (for authentication)

## ⚡ Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/maliksaadnaeem937/ChatbotUsingOllama.git
cd ChatbotUsingOllama
```

### 2. Backend Setup
```bash
cd Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your credentials
echo MONGO_URL=your_mongodb_connection_string > .env
echo DbName=chatbot_db >> .env

# Start Ollama service (in separate terminal)
ollama serve

# Pull a model (example)
ollama pull llama2

# Run the backend server
python -m uvicorn api:app --reload
```
Backend runs at: `http://localhost:8000`

### 3. Frontend Setup
```bash
cd FrontEnd

# Install dependencies
npm install

# Create .env.local file
echo NEXT_PUBLIC_FIREBASE_API_KEY=your_firebase_key > .env.local
echo NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com >> .env.local
echo NEXT_PUBLIC_BACKEND_URL=http://localhost:8000 >> .env.local

# Run the development server
npm run dev
```
Frontend runs at: `http://localhost:3000`

### 4. Start Using
1. Open browser: `http://localhost:3000`
2. Sign in with Google via Firebase
3. Start chatting with the AI

## 🔧 Configuration

### Backend Environment (.env)
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/
DbName=chatbot_db
```

### Frontend Environment (.env.local)
```
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## 📚 API Endpoints

| Method | Endpoint    | Description               |
|--------|-------------|---------------------------|
| GET    | `/`         | Health check              |
| POST   | `/ask-llm`  | Send message to AI        |
| POST   | `/get-chats`| Fetch user's chat history |

## 🧩 Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **Ollama** - Local LLM integration
- **MongoDB** - NoSQL database
- **LangChain** - LLM framework
- **LangGraph** - Workflow management

### Frontend
- **Next.js** - React framework
- **Firebase** - Authentication
- **Redux Toolkit** - State management
- **Tailwind CSS** - Styling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is created for educational purposes.

## ❓ Need Help?

- Check if Ollama is running: `ollama list`
- Verify MongoDB connection in `.env` file
- Check browser console for frontend errors
- Look at backend terminal for API errors
