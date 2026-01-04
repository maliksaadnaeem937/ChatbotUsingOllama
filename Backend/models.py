
from pydantic import BaseModel
from typing import List

from datetime import date
from typing import Optional

class Message(BaseModel):
    type:str
    text:str
class ChatSchema(BaseModel):
    user_id:str
    messages:List[Message]=[]
    
    



