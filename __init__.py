from fastapi import FastAPI
from post_embeddings import embeddings_api
from post_conversation_summary import conversation_summary_api
from post_chat import chat_api

app = FastAPI()

app.include_router(conversation_summary_api)
app.include_router(embeddings_api)
app.include_router(chat_api)