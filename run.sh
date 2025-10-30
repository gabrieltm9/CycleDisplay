#!/bin/bash
set -e

# Variables
IMAGE_NAME="cycledisplay"
CONTAINER_NAME="cycledisplay"
NETWORK_NAME="merged_net"
PORT=5000

# Create network if it doesn't exist
if ! docker network inspect $NETWORK_NAME >/dev/null 2>&1; then
    echo "Creating network: $NETWORK_NAME"
    docker network create $NETWORK_NAME
else
    echo "Network $NETWORK_NAME already exists"
fi

# Stop and remove existing container if running
if [ "$(docker ps -aq -f name=^${CONTAINER_NAME}$)" ]; then
    echo "Stopping and removing existing container: $CONTAINER_NAME"
    docker rm -f $CONTAINER_NAME >/dev/null 2>&1 || true
fi

# Run new container
echo "Starting $CONTAINER_NAME on network $NETWORK_NAME..."
docker run -d \
  --name $CONTAINER_NAME \
  --network $NETWORK_NAME \
  --restart unless-stopped \
  -p $PORT:$PORT \
  -v /etc/localtime:/etc/localtime:ro \
  -v /etc/timezone:/etc/timezone:ro \
  $IMAGE_NAME

# Show status
echo "Container '$CONTAINER_NAME' is now running."
docker ps --filter "name=$CONTAINER_NAME"
echo "CycleDisplay is live at http://localhost:$PORT!"