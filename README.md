## DESCRIPTION

The API generates a vectorDB at initialization time from documents stored in the configured data path using OLLAMA and MiniLM embeddings.
The system now uses local OLLAMA models for both chat completion and embeddings generation, eliminating the need for external API keys.

The HyperDB module loads documents from a configurable path, processes them using Langchain document loaders and text splitters, and generates embeddings using OLLAMA's MiniLM model.

## SETUP

Set the required environment variables:
```bash
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_CHAT_MODEL="llama2"
export OLLAMA_EMBEDDINGS_MODEL="all-minilm"
export EMBEDDINGS_DATA_PATH="/path/to/your/data"
```

Or run the setup script:
```bash
source setEnvironment.sh
```

Install the requirements:
```bash
pip install -r requirements.txt
```

Make sure OLLAMA is running and has the required models:
```bash
# Start OLLAMA (if not already running)
ollama serve

# Pull required models
ollama pull llama2
ollama pull all-minilm
```

## EXECUTION

To run the API locally:
```bash
uvicorn src.__init__:app --reload
```

API endpoints:

### Chat Completion
```
[POST] http://127.0.0.1:8000/chat
```

### Embeddings Search
```
[POST] http://127.0.0.1:8000/embeddings
```

### Conversation Summary
```
[POST] http://127.0.0.1:8000/conversation-summary
```

Example request:
```json
{
    "text": "{\"messages\": [{\"role\": \"user\", \"content\": \"Tell me about the features in the documentation?\"}]}"
}
```

## DATA CONFIGURATION

Place your documents in the path specified by `EMBEDDINGS_DATA_PATH`. Supported formats:
- Text files (.txt)
- Markdown files (.md, .markdown)
- JSON files (.json)

The system will automatically:
1. Load all supported documents from the specified path
2. Split them into chunks using Langchain's text splitter
3. Generate embeddings using OLLAMA's MiniLM model
4. Store them in HyperDB for fast similarity search

## FEATURES

- **Local Processing**: No external API dependencies
- **Dynamic Document Loading**: Supports multiple document formats
- **Intelligent Text Splitting**: Uses Langchain's recursive character text splitter
- **Fast Similarity Search**: Powered by HyperDB with multiple similarity metrics
- **Conversation Summarization**: Maintains context across long conversations
- **Caching**: Embeddings are cached in pickle format for faster startup