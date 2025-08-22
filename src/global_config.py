import os

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class GlobalConfig(metaclass=Singleton):
    def __init__(self):
        self.ollama_base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_chat_model = os.environ.get("OLLAMA_CHAT_MODEL", "llama2")
        self.ollama_embeddings_model = os.environ.get("OLLAMA_EMBEDDINGS_MODEL", "all-minilm")
        self.embeddings_data_path = os.environ.get("EMBEDDINGS_DATA_PATH", "/app/data")