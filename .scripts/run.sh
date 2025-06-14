#!/bin/bash

set -e  # Exit immediately if a command fails

# Create the pod (ignore error if it already exists)
if ! podman pod exists todopod; then
  echo "🔧 Creating pod 'todopod'..."
  podman pod create --name todopod -p 8000:8000 -p 5432:5432
else
  echo "ℹ️ Pod 'todopod' already exists."
fi

# Start the Postgres container
if ! podman container exists db; then
  echo "🐘 Starting Postgres container..."
  podman run -d \
    --env-file .env \
    --name db \
    --pod todopod \
    postgres:17
else
  echo "ℹ️ Container 'db' already exists."
fi

# Build the FastAPI app image
echo "📦 Building FastAPI image..."
podman build -t todo-app -f backend/containers/app/Containerfile .

# Start the FastAPI app container
if ! podman container exists app; then
  echo "🚀 Starting FastAPI app container..."
  podman run -d \
    --name app \
    --pod todopod \
    todo-app
else
  echo "ℹ️ Container 'app' already exists."
fi
