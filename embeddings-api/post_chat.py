import json
from fastapi import APIRouter, Request
from .src.vector_search_api import VectorSearchAPI
from .src.summarizer import Summarizer
from .src.chat_completion import ChatCompletion
from .src.global_config import GlobalConfig

chat_api = APIRouter()
vector_search_api = VectorSearchAPI()
conversation_summarizer = Summarizer()
chat_completion = ChatCompletion()
config = GlobalConfig

@chat_api.post("/chat")
async def chat(request: Request):
    try:
        query = await request.json()
        
        # Parse the request
        if isinstance(query["text"], str):
            # Legacy format support
            parsed_data = json.loads(query["text"])
            conversation = parsed_data["messages"]
            retrieve_embeddings = True  # Default behavior
            include_history_summary = True  # Default behavior
        else:
            # New format with flags
            conversation = query["text"]["messages"]
            retrieve_embeddings = query["text"].get("retrieve_embeddings", True)
            include_history_summary = query["text"].get("include_history_summary", True)
        
        # Extract conversation components
        system_messages = [msg for msg in conversation if msg["role"] == "system"]
        user_messages = [msg for msg in conversation if msg["role"] == "user"]
        assistant_messages = [msg for msg in conversation if msg["role"] == "assistant"]
        
        # Get the last user prompt
        last_user_prompt = user_messages[-1] if user_messages else {"role": "user", "content": ""}
        
        # Build conversation history (excluding the last user message)
        conversation_history = []
        for i in range(len(conversation) - 1):  # Exclude last message
            if conversation[i]["role"] in ["user", "assistant"]:
                conversation_history.append(conversation[i])
        
        messages = []
        
        # Add system message
        if system_messages:
            messages.append(system_messages[0])
        else:
            messages.append({
                "role": "system", 
                "content": "You are a helpful AI assistant. Use any provided context to answer questions accurately and remember details from the conversation."
            })
        
        # Add conversation summary if enabled and history exists
        if include_history_summary and conversation_history:
            summarized_conversation = conversation_summarizer.summarize(conversation_history)
            messages.append({
                "role": "user", 
                "content": f"Previous conversation summary: {summarized_conversation}"
            })

        # Add document embeddings if enabled
        if retrieve_embeddings:
            embeddings = vector_search_api.get_embeddings(last_user_prompt)
            if embeddings:
                combined_context = "\n\n".join(embeddings)
                messages.append({
                    "role": "user", 
                    "content": f"Document context: {combined_context}"
                })
        
        # Add the current user prompt
        messages.append(last_user_prompt)

        response = chat_completion.chat(messages)
        return response
    except Exception as e:
        print(f'Error in chat endpoint: {e}')
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": f"I apologize, but I encountered an error: {str(e)}"
                }
            }]
        }