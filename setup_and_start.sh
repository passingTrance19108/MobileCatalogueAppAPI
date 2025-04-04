#!/bin/bash
set -e

# Configuration
NETWORK_NAME="phoneCatalogNetwork"
MYSQL_CONTAINER_NAME="phone-catalogue-mysql"
API_CONTAINER_NAME="phone-catalogue-api"
MYSQL_ROOT_PASSWORD="mysecret"
MYSQL_DATABASE="mydb"
MYSQL_IMAGE="mysql:8"
API_IMAGE="phonecatapi"
API_PORT=5000
MYSQL_VOLUME_NAME="mysql_data_volume"
MYSQL_USER="user"
MYSQL_PASSWORD="password"
DATABASE_URI="mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@${MYSQL_CONTAINER_NAME}:3306/${MYSQL_DATABASE}"


# Create Docker network if it does not exist
if ! docker network ls | grep -q "$NETWORK_NAME"; then
    echo "Creating network: $NETWORK_NAME"
    docker network create "$NETWORK_NAME"
else
    echo "Network $NETWORK_NAME already exists"
fi

# Create volume for MySQL if it does not exist
if ! docker volume ls | grep -q "$MYSQL_VOLUME_NAME"; then
    echo "Creating volume: $MYSQL_VOLUME_NAME"
    docker volume create "$MYSQL_VOLUME_NAME"
else
    echo "Volume $MYSQL_VOLUME_NAME already exists"
fi

# Remove any existing containers (optional, for a clean start)
docker rm -f "$MYSQL_CONTAINER_NAME" || true
docker rm -f "$API_CONTAINER_NAME" || true

# Start MySQL container
echo "Starting MySQL container..."
docker run -d \
  --name "$MYSQL_CONTAINER_NAME" \
  --network "$NETWORK_NAME" \
  -e MYSQL_ROOT_PASSWORD="$MYSQL_ROOT_PASSWORD" \
  -e MYSQL_DATABASE="$MYSQL_DATABASE" \
  -e MYSQL_USER="$MYSQL_USER" \
  -e MYSQL_PASSWORD="$MYSQL_PASSWORD" \
  -v "$MYSQL_VOLUME_NAME":/var/lib/mysql \
  "$MYSQL_IMAGE"

# Wait for MySQL to be ready
echo "Waiting for MySQL to initialize..."
until docker exec "$MYSQL_CONTAINER_NAME" mysqladmin ping -h"localhost" --silent; do
    echo -n "."; sleep 2
done
echo ""
echo "MySQL is up!"

# Build the API image
echo "Building API image..."
docker build -t "$API_IMAGE" .

# Run the API container
echo "Starting REST API container..."
docker run -d \
  --name "$API_CONTAINER_NAME" \
  --network "$NETWORK_NAME" \
  -e DATABASE_URI="$DATABASE_URI" \
  -p "$API_PORT":5000 \
  "$API_IMAGE"

echo "✅ Both containers are up and running!"

