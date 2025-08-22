from src.global_config import GlobalConfig
from langchain.llms import OpenAI,AzureOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

config = GlobalConfig()

class Summarizer:

    def summarize(self, conversation):
        try:
            if config.use_azure.lower() == 'true':
                llm = AzureOpenAI(
                    temperature=0,
                    deployment_name=config.azure_chat_deployment_name,
                    model_name=config.azure_model_version,
                    openai_api_version=config.azure_api_version,
                    openai_api_base=config.azure_endpoint,
                    openai_api_key=config.azure_key
                )
            else:
                llm = OpenAI(
                    temperature=0,
                    openai_api_key= config.openai_api_key,
                    model_name="text-davinci-004"
                )

            summarizer = ConversationChain(llm=llm, memory=ConversationBufferWindowMemory(k=3))
            return summarizer.predict(input=conversation)
        except Exception as e:
            print (f'Error: {e}')

