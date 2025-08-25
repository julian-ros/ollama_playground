# Data Directory

Place your documents here for the embeddings API to process.

## Supported Formats

- **Text files** (`.txt`): Plain text documents
- **Markdown files** (`.md`, `.markdown`): Markdown formatted documents  
- **JSON files** (`.json`): Structured JSON data

## Processing

The embeddings API will automatically:

1. **Discover** all supported files in this directory and subdirectories
2. **Load** them using appropriate Langchain document loaders
3. **Split** them into chunks using RecursiveCharacterTextSplitter
4. **Generate** embeddings using OLLAMA's MiniLM model
5. **Store** them in HyperDB for fast similarity search

## Configuration

The processing behavior can be configured via environment variables:

- `EMBEDDINGS_DATA_PATH`: Path to this data directory (default: `/app/data`)
- `OLLAMA_EMBEDDINGS_MODEL`: Model for generating embeddings (default: `all-minilm`)

## Cache

Generated embeddings are cached in `embeddings/ollama_embeddings.pickle.gz` to speed up subsequent startups.