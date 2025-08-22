import json
from fastapi import APIRouter, Request
from src.vector_search_api import VectorSearchAPI
from src.summarizer import Summarizer
from src.chat_completion import ChatCompletion
from src.global_config import GlobalConfig

chat_api = APIRouter()
vector_search_api = VectorSearchAPI()
conversation_summarizer = Summarizer()
chat_completion = ChatCompletion()
config = GlobalConfig

@chat_api.post("/chat")
async def chat(request: Request):
    try:
        query = await request.json()
        conversation = json.loads(query["text"])["messages"]
        assistant_role = [message for message in conversation if message["role"] == "system"][0]
        conversation_history = [message for message in conversation if message["role"] == "user"][:-1]
        last_user_prompt = [message for message in conversation if message["role"] == "user"][-1]
        
        messages = []
        messages.append(assistant_role)
        if conversation_history:
            summarized_conversation = conversation_summarizer.summarize(conversation_history)
            messages.append({"role": "user", "content": summarized_conversation})

        embeddings = vector_search_api.get_embeddings(last_user_prompt)
        for embedding in embeddings:
            messages.append({"role": "user", "content": embedding})
        messages.append(last_user_prompt)

        response = chat_completion.chat(messages)
        return response
    except Exception as e:
        print(f'Error: {e}')
