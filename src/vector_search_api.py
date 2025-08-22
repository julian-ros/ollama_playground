from src.lib.hyperdb import HyperDB
from src.global_config import GlobalConfig
import os
import logging
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.document_loaders.json_loader import JSONLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO)

class VectorSearchAPI:
    def __init__(self):
        self.global_config = GlobalConfig()
        self.documents = []
        self.pickle_path = f"embeddings/ollama_embeddings.pickle.gz"
        
        if os.path.isfile(self.pickle_path):
            logging.info("Loading existing embeddings from pickle file...")
            self.db = HyperDB()
            self.db.load(self.pickle_path)
        else:
            logging.info("Generating new embeddings from data path...")
            self.load_and_process_documents()
            self.db = HyperDB(self.documents)
            self.db.finalize()
            self.db.save(self.pickle_path)
            logging.info(f"Embeddings saved to {self.pickle_path}")

    def load_and_process_documents(self):
        """Load and process documents from the configured data path"""
        data_path = self.global_config.embeddings_data_path
        
        if not os.path.exists(data_path):
            logging.warning(f"Data path {data_path} does not exist. Creating empty database.")
            return
        
        try:
            # Load different types of documents
            all_docs = []
            
            # Load text files
            if self._has_files_with_extensions(data_path, ['.txt']):
                txt_loader = DirectoryLoader(
                    data_path, 
                    glob="**/*.txt", 
                    loader_cls=TextLoader,
                    loader_kwargs={'encoding': 'utf-8'}
                )
                all_docs.extend(txt_loader.load())
            
            # Load markdown files
            if self._has_files_with_extensions(data_path, ['.md', '.markdown']):
                md_loader = DirectoryLoader(
                    data_path, 
                    glob="**/*.md", 
                    loader_cls=UnstructuredMarkdownLoader
                )
                all_docs.extend(md_loader.load())
                
                # Also load .markdown files
                markdown_loader = DirectoryLoader(
                    data_path, 
                    glob="**/*.markdown", 
                    loader_cls=UnstructuredMarkdownLoader
                )
                all_docs.extend(markdown_loader.load())
            
            # Load JSON files
            if self._has_files_with_extensions(data_path, ['.json']):
                json_loader = DirectoryLoader(
                    data_path, 
                    glob="**/*.json", 
                    loader_cls=JSONLoader,
                    loader_kwargs={'jq_schema': '.', 'text_content': False}
                )
                all_docs.extend(json_loader.load())
            
            logging.info(f"Loaded {len(all_docs)} documents from {data_path}")
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", " ", ""]
            )
            
            split_docs = text_splitter.split_documents(all_docs)
            logging.info(f"Split into {len(split_docs)} chunks")
            
            # Extract text content for embedding
            self.documents = []
            for doc in split_docs:
                # Create a document dict with metadata
                doc_dict = {
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "unknown"),
                    "description": doc.page_content  # This is what HyperDB will use for embedding
                }
                self.documents.append(doc_dict)
                
        except Exception as e:
            logging.error(f"Error loading documents: {e}")
            self.documents = []

    def _has_files_with_extensions(self, path, extensions):
        """Check if directory contains files with specified extensions"""
        for root, dirs, files in os.walk(path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    return True
        return False

    def get_embeddings(self, query_text):
        """Get relevant embeddings for a query"""
        if isinstance(query_text, dict):
            query_text = query_text.get("content", str(query_text))
        
        results = self.db.query(query_text, top_k=50)
        
        # Extract the content from results
        embeddings = []
        for result in results:
            if isinstance(result, tuple):
                doc, similarity = result
                if isinstance(doc, dict):
                    embeddings.append(doc.get("description", str(doc)))
                else:
                    embeddings.append(str(doc))
            else:
                if isinstance(result, dict):
                    embeddings.append(result.get("description", str(result)))
                else:
                    embeddings.append(str(result))
        
        return embeddings