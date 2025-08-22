from src.lib.hyperdb import HyperDB
from src.global_config import GlobalConfig
import openai
import json
import os

class VectorSearchAPI:
    def __init__(self):
        self.global_config = GlobalConfig()
        openai.api_key = self.global_config.openai_api_key
        self.documents = []
        self.pickle_path = f"embeddings/mydata.pickle.gz"
        if os.path.isfile(self.pickle_path):
            self.db = HyperDB()
            self.db.load(self.pickle_path)
        else:
            self.load_embeddings()
            self.db = HyperDB(self.documents, key="description")
            self.db.finalize()
            self.db.save(self.pickle_path)

    def load_embeddings(self):
        embeddings_file_path = f"embeddings/mydata.jsonl"
        if os.path.isfile(embeddings_file_path):
            with open(embeddings_file_path, "r") as f:
                for line in f:
                    self.documents.append(json.loads(line))
        else:
            raise FileNotFoundError(f"Embeddings file {embeddings_file_path} not found.")

    def get_embeddings(self, query_text):
        results = self.db.query(query_text, top_k=50)
        embeddings = [result[0]["description"] for result in results]
        return embeddings