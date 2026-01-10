
from pydantic import BaseModel
from typing import List



class Message(BaseModel):
    type:str
    text:str
class ChatSchema(BaseModel):
    user_id:str
    messages:List[Message]=[]
    
    



