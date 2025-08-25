from langchain_community.llms import Ollama
from .global_config import GlobalConfig
import json

config = GlobalConfig()

class ChatCompletion:
    def __init__(self):
        self.llm = Ollama(
            model=config.ollama_chat_model,
            base_url=config.ollama_base_url,
            temperature=0.7
        )

    def chat_stream(self, messages):
        """Stream chat completion responses"""
        try:
            # Convert messages to a single prompt for Ollama
            prompt = self._messages_to_prompt(messages)
            
            # Stream the response
            for chunk in self.llm.stream(prompt):
                # Format each chunk in a streaming format
                chunk_data = {
                    "choices": [{
                        "delta": {
                            "content": chunk
                        }
                    }]
                }
                yield f"data: {json.dumps(chunk_data)}\n\n"
                
            # Send final chunk to indicate completion
            final_chunk = {
                "choices": [{
                    "delta": {},
                    "finish_reason": "stop"
                }]
            }
            yield f"data: {json.dumps(final_chunk)}\n\n"
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            print(f"Error in chat completion: {e}")
            error_chunk = {
                "choices": [{
                    "delta": {
                        "content": "I apologize, but I encountered an error processing your request."
                    }
                }]
            }
            yield f"data: {json.dumps(error_chunk)}\n\n"
            yield "data: [DONE]\n\n"

    def chat(self, messages):
        """Non-streaming chat completion for backward compatibility"""
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