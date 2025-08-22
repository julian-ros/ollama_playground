#!/bin/bash

# Start Ollama server in the background
ollama serve &

# Wait for Ollama to be ready (using ollama list instead of curl)
echo "Waiting for Ollama server to start..."
while ! ollama list > /dev/null 2>&1; do
    sleep 2
    echo "Still waiting for Ollama..."
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