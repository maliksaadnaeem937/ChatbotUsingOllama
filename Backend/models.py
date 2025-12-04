
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
    
    



class ExpenseInput(BaseModel):
    title: str           
    description:Optional[str]=None   
    amount: float            # money spent
    category: str            # e.g., Food, Transport, Bills
    date: date               # date of expense  
         
        