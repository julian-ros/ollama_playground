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

# Pull all required models
echo "Pulling chat model for Streamlit: $OLLAMA_CHAT_MODEL_STREAMLIT"
ollama pull $OLLAMA_CHAT_MODEL_STREAMLIT

echo "Pulling embeddings model: $OLLAMA_EMBEDDINGS_MODEL"
ollama pull $OLLAMA_EMBEDDINGS_MODEL

# Only pull embeddings API chat model if it's different from Streamlit model
if [ "$OLLAMA_CHAT_MODEL_EMBEDDINGS_API" != "$OLLAMA_CHAT_MODEL_STREAMLIT" ]; then
    echo "Pulling chat model for embeddings API: $OLLAMA_CHAT_MODEL_EMBEDDINGS_API"
    ollama pull $OLLAMA_CHAT_MODEL_EMBEDDINGS_API
else
    echo "Embeddings API will use the same chat model as Streamlit: $OLLAMA_CHAT_MODEL_STREAMLIT"
fi

echo "Model(s) ready!"

# Keep the container running
wait