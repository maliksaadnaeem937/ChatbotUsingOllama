# database.py
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://maliksaadnaeem937:rflMeVENy8K3FEQb@cluster0.0fuyh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"   # or your Atlas URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["chatbotdb"]  
