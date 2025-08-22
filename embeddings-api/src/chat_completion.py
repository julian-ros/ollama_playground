from langchain_community.llms import Ollama
from .global_config import GlobalConfig

config = GlobalConfig()

class ChatCompletion:
    def __init__(self):
        self.llm = Ollama(
            model=config.ollama_chat_model,
            base_url=config.ollama_base_url,
            temperature=0.7
        )

    def chat(self, messages):
        try:
            # Convert messages to a single prompt for Ollama
            prompt = self._messages_to_prompt(messages)
            response = self.llm.invoke(prompt)
            
            # Return in OpenAI-compatible format for existing code
            return {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": response
                    }
                }]
            }
        except Exception as e:
            print(f"Error in chat completion: {e}")
            return {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": "I apologize, but I encountered an error processing your request."
                    }
                }]
            }

    def _messages_to_prompt(self, messages):
        """Convert OpenAI-style messages to a single prompt for Ollama"""
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "")
            content = message.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)