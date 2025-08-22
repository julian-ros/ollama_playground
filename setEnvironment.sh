#!/bin/bash

# Set your OLLAMA environment variables
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_CHAT_MODEL="llama2"
export OLLAMA_EMBEDDINGS_MODEL="all-minilm"
export EMBEDDINGS_DATA_PATH="/app/data"

echo "OLLAMA environment variables set successfully!"