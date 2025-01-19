from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
from repositories.sessions import create_new_document, add_message_to_session, get_messages_for_session
from helpers.context_builder import create_context

import os
import requests
import logging

load_dotenv()

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL")
EMBEDDINGS_URL = os.getenv("EMBEDDINGS_URL")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

new_session_id = None


@app.on_event("startup")
async def on_startup():
    global new_session_id
    new_session_id = await create_new_document()
    logging.info(f"New session started: {new_session_id}")


class ChatRequest(BaseModel):
    query: str


@app.get("/")
def read_root():
    return {"message": "Backend is running"}


@app.post("/chat")
async def chat(request: ChatRequest):
    logging.info(f"Received query: {request.query}")
    query = request.query

    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    session_messages = await get_messages_for_session(new_session_id)
    formatted_messages = [{'id': item['id'], 'text': item['prompt']} for item in session_messages]

    payload = {"messages": formatted_messages, "query": query, "top_k": 3}
    logging.info(f"Sending payload to Embeddings: {payload}")

    try:
        embedd_response = requests.post(
            EMBEDDINGS_URL,
            json=payload
        )
        logging.info(f"Embeddings HTTP status: {embedd_response.status_code}")
        logging.info(f"Embeddings response headers: {embedd_response.headers}")
        logging.info(f"Embeddings response content: {embedd_response.text}")

        response_data = embedd_response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with Embeddings: {e}")
        return {"response": f"Error communicating with Embeddings {e}"}

    top_similar = [
        msg for msg in session_messages if any(item['id'] == msg['id'] for item in response_data)
    ]

    final_prompt = create_context(top_similar, query)

    payload = {"model": "llama3.2", "prompt": final_prompt, "stream": False}
    logging.info(f"Sending payload to Ollama: {payload}")

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload
        )
        logging.info(f"Ollama HTTP status: {response.status_code}")
        logging.info(f"Ollama response headers: {response.headers}")
        logging.info(f"Ollama response content: {response.text}")

        response.raise_for_status()
        response_data = response.json()

        if response_data:
            content = response_data
            await add_message_to_session(new_session_id, query, content['response'])
        else:
            logging.error("Unexpected or malformed response from Ollama")
            content = "Error: Unexpected or malformed response from Ollama."

    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with Ollama: {e}")
        content = "Error: Unable to communicate with Ollama service."

    return {"response": content}
