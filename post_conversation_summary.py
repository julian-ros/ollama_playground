import json
from fastapi import APIRouter, Request
from src.summarizer import Summarizer

class Response:
    def __init__(self, result: bool, messages: list, status_code: int, exception: str = None):
        self.result = result
        self.messages = messages
        self.status_code = status_code
        self.exception = exception

conversation_summary_api = APIRouter()
conversation_summarizer = Summarizer()

@conversation_summary_api.post("/conversation-summary")
async def conversation_summary(request: Request):
    try:
        query = await request.json()
        conversation = json.loads(query["text"])["messages"]
        assistant_role = [message for message in conversation if message["role"] == "system"][0]
        conversation_history = [message for message in conversation if message["role"] == "user"][:-1]
        last_user_prompt = [message for message in conversation if message["role"] == "user"][-1]
        openai_data = []
        openai_data.append(assistant_role)
        if conversation_history: 
            summarized_conversation = conversation_summarizer.summarize(conversation_history)
            openai_data.append({"role": "user", "content": summarized_conversation})
        openai_data.append(last_user_prompt)
        return Response(result=True, messages=openai_data, status_code=200)

    except Exception as e:
        return Response(result=False, messages=None, status_code=500, exception=str(e))
