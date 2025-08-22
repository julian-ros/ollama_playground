import os

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class GlobalConfig(metaclass=Singleton):
    def __init__(self):
        self.openai_endpoint = os.environ["OPENAI_API_BASE"]
        self.openai_api_key = os.environ["OPENAI_API_KEY"]
        self.openai_llm_version = os.environ["OPENAI_CHAT_MODEL_VERSION"]
        self.openai_embeddings_version = os.environ["OPENAI_EMBEDDINGS_MODEL_VERSION"]
        self.azure_key = os.environ["AZURE_KEY"]
        self.azure_endpoint = os.environ["AZURE_OPENAI_BASE"]
        self.azure_api_version = os.environ["AZURE_API_VERSION"]
        self.azure_chat_deployment_name = os.environ["AZURE_CHAT_DEPLOYMENT_NAME"]
        self.azure_embeddings_deployment_name = os.environ["AZURE_EMBEDDINGS_DEPLOYMENT_NAME"]
        self.azure_model_version = os.environ["AZURE_MODEL_VERSION"]
        self.use_azure = os.environ["USE_AZURE"]
