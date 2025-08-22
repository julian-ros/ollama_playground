import openai
import json
from src.global_config import GlobalConfig

config = GlobalConfig()


class ChatCompletion:

    def chat(self, messages):
        if config.use_azure.lower() == 'true':
            openai.api_type = "azure"
            openai.api_version = config.azure_api_version 
            openai.api_base = config.azure_endpoint
            openai.api_key = config.azure_key

            response = openai.ChatCompletion.create(
                engine=config.azure_chat_deployment_name,
                messages= messages,
                temperature=0
            )
        else:
            openai.api_type = "open_ai"
            openai.api_base = config.openai_endpoint
            openai.api_key = config.openai_api_key
            response = openai.ChatCompletion.create(
                model=config.openai_llm_version,
                messages= messages,
                temperature=0.5,
                stream = True
            )

            for chunk in response:
                print(chunk)

        return response
