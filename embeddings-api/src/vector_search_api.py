from .lib.hyperdb import HyperDB
from .global_config import GlobalConfig
import os
import logging
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.document_loaders.json_loader import JSONLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VectorSearchAPI:
    def __init__(self):
        self.global_config = GlobalConfig()
        self.documents = []
        self.pickle_path = f"embeddings/ollama_embeddings.pickle.gz"
        
        logger.info(f"Initializing VectorSearchAPI with pickle path: {self.pickle_path}")
        logger.info(f"Data path configured as: {self.global_config.embeddings_data_path}")
        
        if os.path.isfile(self.pickle_path):
            logger.info(f"Found existing embeddings file at {self.pickle_path}")
            logger.info("Loading existing embeddings from pickle file...")
            self.db = HyperDB()
            self.db.load(self.pickle_path)
            logger.info(f"Successfully loaded {len(self.db.documents)} documents from pickle file")
        else:
            logger.info(f"No existing embeddings found at {self.pickle_path}")
            logger.info("Starting fresh embedding generation process...")
            self.load_and_process_documents()
            logger.info(f"Creating HyperDB with {len(self.documents)} processed documents")
            self.db = HyperDB(self.documents)
            self.db.finalize()
            logger.info("Saving generated embeddings to pickle file...")
            self.db.save(self.pickle_path)
            logger.info(f"Successfully saved embeddings to {self.pickle_path}")
            logger.info(f"Pickle file size: {os.path.getsize(self.pickle_path) / (1024*1024):.2f} MB")

    def load_and_process_documents(self):
        """Load and process documents from the configured data path"""
        data_path = self.global_config.embeddings_data_path
        
        logger.info(f"Starting document loading from: {data_path}")
        
        if not os.path.exists(data_path):
            logger.warning(f"Data path {data_path} does not exist. Creating empty database.")
            return
        
        try:
            # Load different types of documents
            all_docs = []
            
            logger.info("Scanning for text files (.txt)...")
            # Load text files
            if self._has_files_with_extensions(data_path, ['.txt']):
                logger.info("Found .txt files, loading...")
                txt_loader = DirectoryLoader(
                    data_path, 
                    glob="**/*.txt", 
                    loader_cls=TextLoader,
                    loader_kwargs={'encoding': 'utf-8'}
                )
                txt_docs = txt_loader.load()
                all_docs.extend(txt_docs)
                logger.info(f"Loaded {len(txt_docs)} text files")
            
            logger.info("Scanning for markdown files (.md, .markdown)...")
            # Load markdown files
            if self._has_files_with_extensions(data_path, ['.md', '.markdown']):
                logger.info("Found markdown files, loading...")
                try:
                    md_loader = DirectoryLoader(
                        data_path, 
                        glob="**/*.md", 
                        loader_cls=UnstructuredMarkdownLoader
                    )
                    md_docs = md_loader.load()
                    all_docs.extend(md_docs)
                    logger.info(f"Loaded {len(md_docs)} .md files")
                except Exception as e:
                    logger.error(f"Error loading .md files: {e}")
                    # Fallback to TextLoader for .md files
                    logger.info("Falling back to TextLoader for .md files")
                    md_loader = DirectoryLoader(
                        data_path, 
                        glob="**/*.md", 
                        loader_cls=TextLoader,
                        loader_kwargs={'encoding': 'utf-8'}
                    )
                    md_docs = md_loader.load()
                    all_docs.extend(md_docs)
                    logger.info(f"Loaded {len(md_docs)} .md files with TextLoader")
                
                # Also load .markdown files
                try:
                    markdown_loader = DirectoryLoader(
                        data_path, 
                        glob="**/*.markdown", 
                        loader_cls=UnstructuredMarkdownLoader
                    )
                    markdown_docs = markdown_loader.load()
                    all_docs.extend(markdown_docs)
                    logger.info(f"Loaded {len(markdown_docs)} .markdown files")
                except Exception as e:
                    logger.error(f"Error loading .markdown files: {e}")
                    # Fallback to TextLoader for .markdown files
                    logger.info("Falling back to TextLoader for .markdown files")
                    markdown_loader = DirectoryLoader(
                        data_path, 
                        glob="**/*.markdown", 
                        loader_cls=TextLoader,
                        loader_kwargs={'encoding': 'utf-8'}
                    )
                    markdown_docs = markdown_loader.load()
                    all_docs.extend(markdown_docs)
                    logger.info(f"Loaded {len(markdown_docs)} .markdown files with TextLoader")
            
            logger.info("Scanning for JSON files (.json)...")
            # Load JSON files
            if self._has_files_with_extensions(data_path, ['.json']):
                logger.info("Found JSON files, loading...")
                json_loader = DirectoryLoader(
                    data_path, 
                    glob="**/*.json", 
                    loader_cls=JSONLoader,
                    loader_kwargs={'jq_schema': '.', 'text_content': False}
                )
                json_docs = json_loader.load()
                all_docs.extend(json_docs)
                logger.info(f"Loaded {len(json_docs)} JSON files")
            
            logger.info(f"Total documents loaded: {len(all_docs)} from {data_path}")
            
            logger.info("Starting text splitting process...")
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", " ", ""]
            )
            
            split_docs = text_splitter.split_documents(all_docs)
            logger.info(f"Documents split into {len(split_docs)} chunks")
            
            logger.info("Processing chunks for embedding...")
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
            
            logger.info(f"Prepared {len(self.documents)} document chunks for embedding generation")
                
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            self.documents = []

    def _has_files_with_extensions(self, path, extensions):
        """Check if directory contains files with specified extensions"""
        found_files = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    found_files.append(os.path.join(root, file))
        
        if found_files:
            logger.info(f"Found {len(found_files)} files with extensions {extensions}")
            for file in found_files:  # Log all files for debugging
                logger.info(f"  - {file}")
        
        return len(found_files) > 0

    def get_embeddings(self, query_text):
        """Get relevant embeddings for a query"""
        logger.info(f"Processing query for embeddings: {str(query_text)[:100]}...")
        
        if isinstance(query_text, dict):
            query_text = query_text.get("content", str(query_text))
        
        logger.info("Performing vector similarity search...")
        results = self.db.query(query_text, top_k=50)
        logger.info(f"Found {len(results)} relevant document chunks")
        
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
        
        logger.info(f"Returning {len(embeddings)} embedding results for context")
        return embeddings