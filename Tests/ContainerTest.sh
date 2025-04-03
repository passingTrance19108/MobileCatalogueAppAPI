#!/bin/bash
set -e

# Wait for the API to start
echo "Waiting for the API to be ready..."
sleep 10  # Adjust as needed for your environment

# Test the root endpoint
echo "Testing root endpoint..."
root_response=$(curl -s http://localhost:5000/)
if echo "$root_response" | grep -q "Welcome"; then
    echo "✅ Root endpoint OK: $root_response"
else
    echo "❌ Root endpoint failed. Response: $root_response"
    exit 1
fi

# Test the /phones endpoint (should return a JSON array)
echo "Testing /phones endpoint..."
phones_response=$(curl -s http://localhost:5000/phones)
echo "Response from /phones: $phones_response"
if echo "$phones_response" | grep -q "\["; then
    echo "✅ /phones endpoint returned a JSON array."
else
    echo "❌ /phones endpoint did not return a valid JSON array."
    exit 1
fi

# Test adding a phone record
echo "Testing adding a phone record via POST..."
post_response=$(curl -s -X POST http://localhost:5000/add_phone \
  -H "Content-Type: application/json" \
  -d '{
    "serial_number": "ABC12345678",
    "imei": "123456789012345",
    "model": "X100",
    "brand": "Nokia",
    "network_technologies": ["GSM", "LTE"],
    "number_of_cameras": 2,
    "number_of_cores": 4,
    "weight": 150,
    "battery_capacity": 3000,
    "cost": 299.99
  }')
echo "Response from POST /add_phone: $post_response"

# Allow time for the record to be written
sleep 2

# Test if the added record appears in /phones
echo "Verifying the added phone record via GET /phones..."
phones_response=$(curl -s http://localhost:5000/phones)
echo "Response from /phones: $phones_response"
if echo "$phones_response" | grep -q "ABC12345678"; then
    echo "✅ Added phone record found."
else
    echo "❌ Added phone record not found."
    exit 1
fi

echo "✅ Dockerized API and Database are working correctly!"
