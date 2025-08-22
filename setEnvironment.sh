#!/bin/bash

# Set your Azure environment variables
export AZURE_KEY="41ea1ce9e6844194b645bb75a1ea7989"
export AZURE_OPENAI_BASE="https://espiga-gpt.openai.azure.com/"
export AZURE_API_VERSION="2024-02-01"
export AZURE_CHAT_DEPLOYMENT_NAME="espiga-gpt-llm"
export AZURE_EMBEDDINGS_DEPLOYMENT_NAME="espiga-ada-llm"
export AZURE_MODEL_VERSION="gpt-35-turbo"
export USE_AZURE="true"

# Set your OpenAI environment variables (if needed)
export OPENAI_API_BASE=""
export OPENAI_API_KEY=""
export OPENAI_CHAT_MODEL_VERSION=""
export OPENAI_EMBEDDINGS_MODEL_VERSION=""

# You can uncomment and set the OpenAI variables above if required

echo "Environment variables set successfully!"
