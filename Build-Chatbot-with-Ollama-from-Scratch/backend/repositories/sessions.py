import os
from typing import List, Dict, Optional

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = AsyncIOMotorClient(MONGO_DB_URL)
db = client[MONGO_DB_NAME]
collection = db[COLLECTION_NAME]

print(f'Collection connected..........')


class Message(BaseModel):
    prompt: str
    response: str


class ChatDocument(BaseModel):
    messages: List[Message]


async def create_new_document() -> Optional[str]:
    try:
        new_document = {
            "messages": []
        }

        result = await collection.insert_one(new_document)

        if result.inserted_id:
            return str(result.inserted_id)
        else:
            return None
    except Exception as e:
        print(f"Error creating new document: {e}")
        return None


async def get_messages_for_session(session_id: str) -> List[Dict]:
    try:
        object_id = ObjectId(session_id)

        document = await collection.find_one({"_id": object_id})

        if document:
            return document.get("messages", [])
        else:
            return []
    except Exception as e:
        print(f"Error retrieving messages for session {session_id}: {e}")
        return []


async def add_message_to_session(session_id: str, prompt: str, response: str):
    try:
        object_id = ObjectId(session_id)

        document = await collection.find_one({"_id": object_id})

        if document:
            messages = document.get("messages", [])

            next_id = messages[-1]["id"] + 1 if messages else 0

            new_message = {
                "id": next_id,
                "prompt": prompt,
                "response": response
            }

            await collection.update_one(
                {"_id": object_id},
                {"$push": {"messages": new_message}}
            )

            print("New message added successfully.")
        else:
            print("Document not found.")
    except Exception as e:
        print(f"Error adding message: {e}")
