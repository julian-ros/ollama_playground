#!/bin/bash

# Install curl (required for health checks and API calls)
apk add --no-cache curl

# Start Ollama server in the background
ollama serve &

# Wait for Ollama to be ready
echo "Waiting for Ollama server to start..."
while ! curl -s http://localhost:11434/api/tags > /dev/null; do
    sleep 2
done

echo "Ollama server is ready!"

# Pull required models based on environment variable
if [ "$OLLAMA_MODEL_TYPE" = "chat" ]; then
    echo "Pulling chat model: $OLLAMA_CHAT_MODEL"
    ollama pull $OLLAMA_CHAT_MODEL
elif [ "$OLLAMA_MODEL_TYPE" = "embeddings" ]; then
    echo "Pulling embeddings model: $OLLAMA_EMBEDDINGS_MODEL"
    ollama pull $OLLAMA_EMBEDDINGS_MODEL
fi

echo "Model(s) ready!"

# Keep the container running
wait