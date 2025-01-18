from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from typing import List

import faiss

app = FastAPI()

encoder = SentenceTransformer("paraphrase-mpnet-base-v2")


class Message(BaseModel):
    id: int
    text: str


class RequestData(BaseModel):
    messages: List[Message]
    query: str
    top_k: int


class SimilarityResult(BaseModel):
    id: int
    text: str
    similarity: float


@app.post("/embeddings/get_similar_texts")
async def get_similar_texts(request_data: RequestData):
    messages = request_data.messages.copy()
    query = request_data.query
    top_k = request_data.top_k

    if messages:
        texts = [msg.text for msg in messages]
        embeddings = encoder.encode(texts)
        vector_dimensions = embeddings.shape[1]

        index = faiss.IndexFlatIP(vector_dimensions)
        faiss.normalize_L2(embeddings)
        index.add(embeddings)

        search_vector = encoder.encode([query])
        faiss.normalize_L2(search_vector)

        distances, ann = index.search(search_vector, top_k)

        results = []
        for i in range(len(ann[0])):
            idx = ann[0][i]
            if idx != -1 and idx < len(messages):
                similarity = float(1 - distances[0][i])
                if similarity < 0.70:
                    results.append(
                        SimilarityResult(
                            id=messages[idx].id,
                            text=messages[idx].text,
                            similarity=similarity
                        )
                    )

        results.sort(key=lambda x: x.similarity)
    else:
        results = []

    return results
