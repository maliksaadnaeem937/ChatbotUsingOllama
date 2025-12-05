from database import db
import asyncio
async def get_users():
    users = await db.users.find().to_list(length=100)
    print(users)
    return users


asyncio.run(get_users())



