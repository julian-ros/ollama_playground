from .global_config import GlobalConfig
from langchain_community.llms import Ollama
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

config = GlobalConfig()

class Summarizer:
    def __init__(self):
        self.llm = Ollama(
            model=config.ollama_chat_model,
            base_url=config.ollama_base_url,
            temperature=0.3
        )

    def summarize(self, conversation):
        try:
            # Convert conversation to text format
            conversation_text = self._format_conversation(conversation)
            
            # Create summarization prompt
            prompt = f"""Please provide a concise summary of the following conversation:

{conversation_text}

Summary:"""
            
            summary = self.llm.invoke(prompt)
            return summary
            
        except Exception as e:
            print(f'Error in summarization: {e}')
            return "Unable to summarize conversation."

    def _format_conversation(self, conversation):
        """Format conversation messages into readable text"""
        formatted_parts = []
        
        for message in conversation:
            role = message.get("role", "")
            content = message.get("content", "")
            
            if role == "user":
                formatted_parts.append(f"User: {content}")
            elif role == "assistant":
                formatted_parts.append(f"Assistant: {content}")
        
        return "\n".join(formatted_parts)