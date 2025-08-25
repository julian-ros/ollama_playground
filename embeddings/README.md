# Embeddings Directory

This directory is used for storing:
- Generated embedding pickle files (`ollama_embeddings.pickle.gz`)
- Any temporary embedding-related files

## Data Configuration

Configure your data path using the `EMBEDDINGS_DATA_PATH` environment variable.
The system will automatically process documents from that path and generate embeddings using OLLAMA's MiniLM model.

Supported document formats:
- Text files (`.txt`)
- Markdown files (`.md`, `.markdown`) 
- JSON files (`.json`)

The embeddings will be automatically generated at startup and cached for subsequent runs.