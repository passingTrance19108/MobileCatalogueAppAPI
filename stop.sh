#!/bin/bash
set -e

# Configuration
NETWORK_NAME="phoneCatNetwork"
MYSQL_CONTAINER_NAME="mysql-server"
API_CONTAINER_NAME="phone-catalogue-api"

# Stop and remove the API container if it exists
if docker ps -a | grep -q "$API_CONTAINER_NAME"; then
    echo "Stopping and removing API container: $API_CONTAINER_NAME"
    docker stop "$API_CONTAINER_NAME" || true
    docker rm -f "$API_CONTAINER_NAME" 
else
    echo "API container $API_CONTAINER_NAME does not exist"
fi

# Stop and remove the MySQL container if it exists
if docker ps -a | grep -q "$MYSQL_CONTAINER_NAME"; then
    echo "Stopping and removing MySQL container: $MYSQL_CONTAINER_NAME"
    docker stop "$MYSQL_CONTAINER_NAME" || true
    docker rm -f "$MYSQL_CONTAINER_NAME"
else
    echo "MySQL container $MYSQL_CONTAINER_NAME does not exist"
fi

# Remove the Docker network if it exists
if docker network ls | grep -q "$NETWORK_NAME"; then
    echo "Removing network: $NETWORK_NAME"
    docker network rm "$NETWORK_NAME"
else
    echo "Network $NETWORK_NAME does not exist"
fi

echo "✅ Tear down complete! Volumes are not deleted."