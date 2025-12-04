# database.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
MONGO_URL = os.getenv("MONGO_URL")



client = AsyncIOMotorClient(MONGO_URL)
db = client[os.getenv("DbName")]  
