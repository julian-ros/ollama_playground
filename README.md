## DESCRIPTION

The API generates a vectorDB at initialization time from documents stored in the configured data path using OLLAMA and MiniLM embeddings.
The system now uses local OLLAMA models for both chat completion and embeddings generation, eliminating the need for external API keys.

The HyperDB module loads documents from a configurable path, processes them using Langchain document loaders and text splitters, and generates embeddings using OLLAMA's MiniLM model.

## ARCHITECTURE

The project consists of two main services:

- **Embeddings API** (`embeddings-api/`): FastAPI backend that processes documents and provides embeddings-enhanced chat
- **Streamlit Frontend** (`streamlit-frontend/`): Web interface for chatting with your documents

Both services run in Docker containers with dedicated OLLAMA instances:
- `ollama_chat`: Serves Llama3.2 for the Streamlit frontend
- `ollama_embeddings`: Serves MiniLM for document embeddings

## SETUP

### Prerequisites

- Docker and Docker Compose
- At least 8GB RAM (for running OLLAMA models)
- Documents to process (place in `data/` directory)

### Quick Start

1. **Clone and prepare the project:**
   ```bash
   git clone <your-repo>
   cd <project-directory>
   ```

2. **Configure models (optional):**
   ```bash
   # Edit .env file to change models
   nano .env
   ```
   
   Available models you can configure:
   - `OLLAMA_CHAT_MODEL_STREAMLIT`: Model for Streamlit chat (default: llama3.2)
   - `OLLAMA_CHAT_MODEL_EMBEDDINGS_API`: Model for embeddings API chat (default: llama2)
   - `OLLAMA_EMBEDDINGS_MODEL`: Model for document embeddings (default: all-minilm)

3. **Add your documents:**
   ```bash
   # Place your documents in the data directory
   cp your-documents/* data/
   ```

4. **Start all services:**
   ```bash
   docker-compose up --build
   ```

5. **Access the applications:**
   - Streamlit Frontend: http://localhost:8501
   - Embeddings API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## SERVICES

### Embeddings API (Port 8000)

FastAPI service that:
- Loads documents from `/app/data` at startup
- Generates embeddings using OLLAMA MiniLM
- Provides chat completion with document context
- Caches embeddings for fast subsequent startups

**Endpoints:**
- `POST /chat` - Chat with document context
- `POST /embeddings` - Get relevant document embeddings
- `POST /conversation-summary` - Summarize conversations

### Streamlit Frontend (Port 8501)

Web interface that:
- Provides a chat interface
- Can use document context (via embeddings API) or direct chat
- Connects to dedicated OLLAMA chat instance

### OLLAMA Services

- **ollama_chat** (Port 11434): Llama3.2 for frontend chat
- **ollama_embeddings** (Port 11435): MiniLM for document embeddings

## DATA CONFIGURATION

Place your documents in the `data/` directory. Supported formats:
- Text files (`.txt`)
- Markdown files (`.md`, `.markdown`)
- JSON files (`.json`)

The system will automatically:
1. Load all supported documents from the data directory
2. Split them into chunks using Langchain's text splitter
3. Generate embeddings using OLLAMA's MiniLM model
4. Store them in HyperDB for fast similarity search

## ENVIRONMENT VARIABLES

### Embeddings API
- `OLLAMA_BASE_URL`: OLLAMA server URL (default: `http://ollama_embeddings:11434`)
- `OLLAMA_CHAT_MODEL`: Chat model name (default: `llama2`)
- `OLLAMA_EMBEDDINGS_MODEL`: Embeddings model name (default: `all-minilm`)
- `EMBEDDINGS_DATA_PATH`: Path to documents (default: `/app/data`)

### Streamlit Frontend
- `EMBEDDINGS_API_URL`: Embeddings API URL (default: `http://embeddings-api:8000`)
- `OLLAMA_BASE_URL`: OLLAMA chat server URL (default: `http://ollama_chat:11434`)
- `OLLAMA_CHAT_MODEL`: Chat model name (default: `llama3.2`)

## DEVELOPMENT

### Building Individual Services

```bash
# Build embeddings API
docker build -f Dockerfile.embeddings-api -t embeddings-api .

# Build Streamlit frontend
docker build -f Dockerfile.streamlit-frontend -t streamlit-frontend .
```

### Running Services Individually

```bash
# Start OLLAMA services first
docker-compose up ollama_chat ollama_embeddings

# Then start your service
docker-compose up embeddings-api
# or
docker-compose up streamlit-frontend
```

### Logs and Debugging

```bash
# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f embeddings-api
docker-compose logs -f streamlit-frontend
```

## FEATURES

- **Local Processing**: No external API dependencies
- **Dynamic Document Loading**: Supports multiple document formats
- **Intelligent Text Splitting**: Uses Langchain's recursive character text splitter
- **Fast Similarity Search**: Powered by HyperDB with multiple similarity metrics
- **Conversation Summarization**: Maintains context across long conversations
- **Caching**: Embeddings are cached for faster startup
- **Health Checks**: All services include health monitoring
- **Scalable Architecture**: Separate services for different concerns

## TROUBLESHOOTING

### Common Issues

1. **Out of Memory**: OLLAMA models require significant RAM. Ensure you have at least 8GB available.

2. **Slow Startup**: First startup takes time to pull OLLAMA models. Subsequent starts are faster.

3. **No Documents Found**: Ensure documents are placed in the `data/` directory with supported extensions.

4. **Connection Errors**: Wait for all health checks to pass before using the services.

### Checking Service Health

```bash
# Check if all services are healthy
docker-compose ps

# Test embeddings API
curl http://localhost:8000/docs

# Test OLLAMA services
curl http://localhost:11434/api/tags
curl http://localhost:11435/api/tags
```
## API TESTING

### Testing Embeddings API Endpoints

Once your services are running, you can test the embeddings API endpoints using curl:

#### 1. Chat with Document Context

Test the main chat endpoint that uses document embeddings for context-aware responses:

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "text": {
      "messages": [
        {
          "role": "user",
          "content": "How do I create a task using the Julio API?"
        }
      ],
      "retrieve_embeddings": true,
      "include_history_summary": false
    }
  }'
```

#### 2. Streaming Chat Response

Test the streaming chat endpoint for real-time responses:

```bash
curl -X POST "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "text": {
      "messages": [
        {
          "role": "user",
          "content": "What are the authentication methods for Julio API?"
        }
      ],
      "retrieve_embeddings": true,
      "include_history_summary": false
    }
  }'
```

#### 3. Get Document Embeddings

Retrieve relevant document chunks based on a query:

```bash
curl -X POST "http://localhost:8000/embeddings" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "{\"messages\": [{\"role\": \"user\", \"content\": \"API authentication\"}]}"
  }'
```

#### 4. Conversation Summarization

Test the conversation summary feature:

```bash
curl -X POST "http://localhost:8000/conversation-summary" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "{\"messages\": [
      {\"role\": \"system\", \"content\": \"You are a helpful assistant.\"},
      {\"role\": \"user\", \"content\": \"Tell me about Julio API\"},
      {\"role\": \"assistant\", \"content\": \"Julio API is a task management service...\"},
      {\"role\": \"user\", \"content\": \"How do I authenticate?\"}
    ]}"
  }'
```

### Understanding API Responses

#### Chat Response Format
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "To create a task using the Julio API, you need to make a POST request to /v1/tasks with your API key..."
      }
    }
  ]
}
```

#### Embeddings Response Format
```json
{
  "result": true,
  "messages": [
    {
      "role": "user",
      "content": "API Key Authentication\n\nJulio API uses API keys for authentication..."
    },
    {
      "role": "user",
      "content": "Include your API key in the Authorization header..."
    }
  ],
  "status_code": 200
}
```

#### Streaming Response Format
Streaming responses return Server-Sent Events (SSE) format:
```
data: {"choices":[{"delta":{"content":"To"}}]}

data: {"choices":[{"delta":{"content":" create"}}]}

data: {"choices":[{"delta":{"content":" a"}}]}

data: [DONE]
```

### Testing Different Scenarios

#### Test Without Document Context
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "text": {
      "messages": [
        {
          "role": "user",
          "content": "What is the weather like?"
        }
      ],
      "retrieve_embeddings": false,
      "include_history_summary": false
    }
  }'
```

#### Test With Conversation History
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "text": {
      "messages": [
        {
          "role": "user",
          "content": "Tell me about Julio API"
        },
        {
          "role": "assistant",
          "content": "Julio API is a comprehensive task management service..."
        },
        {
          "role": "user",
          "content": "What about rate limits?"
        }
      ],
      "retrieve_embeddings": true,
      "include_history_summary": true
    }
  }'
```

### API Documentation

For interactive API testing, visit the automatically generated documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to test all endpoints directly from your browser with a user-friendly interface.
