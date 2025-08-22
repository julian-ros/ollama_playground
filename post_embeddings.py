import os
import json
from fastapi import APIRouter, Request
from src.vector_search_api import VectorSearchAPI

class Response:
    def __init__(self, result: bool, messages: list, status_code: int, exception: str = None):
        self.result = result
        self.messages = messages
        self.status_code = status_code
        self.exception = exception

embeddings_api = APIRouter()
vector_search_api = VectorSearchAPI()

@embeddings_api.post("/embeddings")
async def embeddings(request: Request):
    try:
        query = await request.json()
        conversation = json.loads(query["text"])["messages"]
        last_user_prompt = [message for message in conversation if message["role"] == "user"][-1]
        embeddings = vector_search_api.get_embeddings(last_user_prompt)
        openai_data = []
        for embedding in embeddings:
            openai_data.append({"role": "user", "content": embedding})
        openai_data.append(last_user_prompt)
        return Response(result=True, messages=openai_data, status_code=200)
    except Exception as e:
        return Response(result=False, messages=None, status_code=500, exception=str(e))
