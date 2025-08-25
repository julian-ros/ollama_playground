import gzip
import pickle
import logging
import os
import numpy as np
from ..global_config import GlobalConfig
from langchain_community.embeddings import OllamaEmbeddings

from .galaxy_brain_math import (
    dot_product,
    adams_similarity,
    cosine_similarity,
    derridaean_similarity,
    euclidean_metric,
    hyper_SVM_ranking_algorithm_sort,
)

MAX_BATCH_SIZE = 100  # Reduced batch size for local processing

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_embedding(documents, key=None):
    """Embedding function that uses Ollama Embeddings."""
    logger.info(f"Starting embedding generation for {len(documents) if isinstance(documents, list) else 1} documents")
    config = GlobalConfig()
    
    logger.info(f"Using Ollama embeddings model: {config.ollama_embeddings_model}")
    logger.info(f"Ollama base URL: {config.ollama_base_url}")
    
    # Initialize Ollama embeddings
    embeddings_model = OllamaEmbeddings(
        model=config.ollama_embeddings_model,
        base_url=config.ollama_base_url
    )
    
    if isinstance(documents, list):
        if isinstance(documents[0], dict):
            texts = []
            if isinstance(key, str):
                if "." in key:
                    key_chain = key.split(".")
                else:
                    key_chain = [key]
                for doc in documents:
                    for k in key_chain:
                        doc = doc[k]
                    texts.append(doc.replace("\n", " "))
            elif key is None:
                for doc in documents:
                    text = ", ".join([f"{key}: {value}" for key, value in doc.items()])
                    texts.append(text)
        elif isinstance(documents[0], str):
            texts = documents
    else:
        texts = [documents] if isinstance(documents, str) else [str(documents)]
    
    logger.info(f"Prepared {len(texts)} text chunks for embedding")
    
    try:
        # Process in batches
        batches = [
            texts[i : i + MAX_BATCH_SIZE] for i in range(0, len(texts), MAX_BATCH_SIZE)
        ]
        
        logger.info(f"Processing embeddings in {len(batches)} batches (max {MAX_BATCH_SIZE} per batch)")
        
        all_embeddings = []
        for i, batch in enumerate(batches):
            logger.info(f'Creating embeddings for batch {i+1}/{len(batches)} ({len(batch)} items)')
            batch_embeddings = embeddings_model.embed_documents(batch)
            all_embeddings.extend([np.array(emb) for emb in batch_embeddings])
            logger.info(f'Completed batch {i+1}/{len(batches)} - generated {len(batch_embeddings)} embeddings')
        
        logger.info(f'Successfully generated {len(all_embeddings)} total embeddings')
        return all_embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        return []


class HyperDB:
    def __init__(
        self,
        documents=None,
        vectors=None,
        key=None,
        embedding_function=None,
        similarity_metric="cosine",
    ):
        logger.info("Initializing HyperDB instance")
        documents = documents or []
        self.documents = []
        self.current_index = 0
        self.vectors = None
        self.embedding_function = embedding_function or (
            lambda docs: get_embedding(docs, key=key)
        )
        
        logger.info(f"HyperDB similarity metric: {similarity_metric}")
        
        # Initialize with a dummy vector to get dimensions
        if not documents and vectors is None:
            logger.info("Getting embedding dimensions with dummy vector")
            dummy_vector = self.embedding_function(["dummy"])
            if dummy_vector:
                vector_length = len(dummy_vector[0])
                logger.info(f"Detected embedding dimension: {vector_length}")
                self.vectors = np.empty((10000, vector_length), dtype=np.float32)
            else:
                logger.warning("Failed to get embedding dimensions, using default 384")
                self.vectors = np.empty((10000, 384), dtype=np.float32)  # Default MiniLM dimension
        else:
            if vectors is not None:
                logger.info(f"Loading HyperDB with pre-computed vectors: {len(vectors)} vectors")
                self.vectors = vectors
                self.documents = documents
                self.current_index = len(self.documents)
            else:
                logger.info("Initializing HyperDB with documents for embedding generation")
                dummy_vector = self.embedding_function(["dummy"])
                if dummy_vector:
                    vector_length = len(dummy_vector[0])
                    logger.info(f"Detected embedding dimension: {vector_length}")
                    self.vectors = np.empty((10000, vector_length), dtype=np.float32)
                else:
                    logger.warning("Failed to get embedding dimensions, using default 384")
                    self.vectors = np.empty((10000, 384), dtype=np.float32)
                logger.info(f"Adding {len(documents)} documents to HyperDB")
                self.add_documents(documents)
        
        logger.info(f"HyperDB initialized with {self.current_index} documents")

        if similarity_metric.__contains__("dot"):
            self.similarity_metric = dot_product
        elif similarity_metric.__contains__("cosine"):
            self.similarity_metric = cosine_similarity
        elif similarity_metric.__contains__("euclidean"):
            self.similarity_metric = euclidean_metric
        elif similarity_metric.__contains__("derrida"):
            self.similarity_metric = derridaean_similarity
        elif similarity_metric.__contains__("adams"):
            self.similarity_metric = adams_similarity
        else:
            raise Exception(
                "Similarity metric not supported. Please use either 'dot', 'cosine', 'euclidean', 'adams', or 'derrida'."
            )

    def dict(self, vectors=False):
        if vectors:
            return [
                {"document": document, "vector": vector.tolist(), "index": index}
                for index, (document, vector) in enumerate(
                    zip(self.documents, self.vectors[:self.current_index])
                )
            ]
        return [
            {"document": document, "index": index}
            for index, document in enumerate(self.documents)
        ]

    def add(self, documents, vectors=None):
        if not isinstance(documents, list):
            return self.add_document(documents, vectors)
        self.add_documents(documents, vectors)

    def add_document(self, document, vector=None):
        if vector is None:
            embeddings = self.embedding_function([document])
            if not embeddings:
                logging.warning(f"Failed to generate embedding for document: {document}")
                return
            vector = embeddings[0]
        
        if self.current_index >= len(self.vectors):
            # Expand the array
            new_vectors = np.empty((10000, len(vector)), dtype=np.float32)
            self.vectors = np.vstack([self.vectors, new_vectors])
        
        self.vectors[self.current_index] = vector
        self.current_index += 1
        self.documents.append(document)

    def finalize(self): 
        self.vectors = self.vectors[:self.current_index]
        
    def remove_document(self, index):
        self.vectors = np.delete(self.vectors, index, axis=0)
        self.documents.pop(index)
        self.current_index -= 1

    def add_documents(self, documents, vectors=None):
        if not documents:
            return
        
        if vectors is None:
            vectors = self.embedding_function(documents)
            if not vectors:
                logging.warning("Failed to generate embeddings for documents")
                return
        
        for vector, document in zip(vectors, documents):
            self.add_document(document, vector)

    def save(self, storage_file):
        logger.info(f"Saving HyperDB to {storage_file}")
        logger.info(f"Saving {self.current_index} documents and their vectors")
        data = {"vectors": self.vectors[:self.current_index], "documents": self.documents}
        with gzip.open(storage_file, "wb") as f:
            pickle.dump(data, f)
        file_size = os.path.getsize(storage_file) / (1024*1024)
        logger.info(f"Successfully saved HyperDB to {storage_file} ({file_size:.2f} MB)")

    def load(self, storage_file):
        try:
            logger.info(f"Loading HyperDB from {storage_file}")
            with gzip.open(storage_file, "rb") as f:
                data = pickle.load(f)
            self.vectors = data["vectors"].astype(np.float32)
            self.documents = data["documents"]
            self.current_index = len(self.documents)
            file_size = os.path.getsize(storage_file) / (1024*1024)
            logger.info(f"Successfully loaded HyperDB from {storage_file} ({file_size:.2f} MB)")
            logger.info(f"Loaded {self.current_index} documents with vectors")
        except FileNotFoundError:
            logger.error(f"HyperDB file {storage_file} not found.")

    def query(self, query_text, top_k=5, return_similarities=True):
        logger.info(f"Querying HyperDB with top_k={top_k}")
        if self.current_index == 0:
            logger.warning("HyperDB is empty, returning no results")
            return [] if return_similarities else []
            
        query_embeddings = self.embedding_function([query_text])
        if not query_embeddings:
            logger.error("Failed to generate query embedding")
            return [] if return_similarities else []
            
        query_vector = query_embeddings[0]
        logger.info("Performing similarity search...")
        ranked_results, similarities = hyper_SVM_ranking_algorithm_sort(
            self.vectors[:self.current_index], query_vector, top_k=top_k, metric=self.similarity_metric
        )
        logger.info(f"Found {len(ranked_results)} similar documents")
        if return_similarities:
            return list(
                zip([self.documents[index] for index in ranked_results], similarities)
            )
        return [self.documents[index] for index in ranked_results]