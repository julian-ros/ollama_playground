#!/bin/bash

# Load environment variables from .env file
# This ensures the script picks up COMPOSE_LOG_SERVICES
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Define the services to log from the environment variable
# Default to empty string if not set, which will make the array empty
SERVICES_TO_LOG=${COMPOSE_LOG_SERVICES:-}

# Convert the comma-separated string into an array
IFS=',' read -r -a SERVICE_ARRAY <<< "$SERVICES_TO_LOG"

echo "Stopping and removing all previous containers, networks, and volumes..."
echo "Note: This will also remove Ollama models, which will be re-downloaded."
docker-compose down -v

echo "Building and starting all Docker Compose services in detached mode..."
# Use --build to ensure images are rebuilt if necessary
docker-compose up --build -d

# Check if specific services are defined for logging
if [ ${#SERVICE_ARRAY[@]} -eq 0 ]; then
    echo "COMPOSE_LOG_SERVICES is not set or empty. Attaching to logs of all services."
    docker-compose logs -f
else
    echo "Attaching to logs of specified services: ${SERVICE_ARRAY[*]}"
    docker-compose logs -f "${SERVICE_ARRAY[@]}"
fi

echo "To stop services, run: docker-compose down"