#!/bin/bash

# Health Check Script
# Checks if Nginx and the app container are running

echo "==============================="
echo "  Health Check - $(date)"
echo "==============================="

# Check Nginx
if systemctl is-active --quiet nginx; then
    echo "✅ Nginx:  RUNNING"
else
    echo "❌ Nginx:  DOWN"
fi

# Check Docker container
if sudo docker ps | grep -q myapp; then
    echo "✅ myapp:  RUNNING"
else
    echo "❌ myapp:  DOWN"
fi

# Check HTTP response
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost)
if [ "$HTTP_CODE" == "200" ]; then
    echo "✅ HTTP:   RESPONDING (200 OK)"
else
    echo "❌ HTTP:   NOT RESPONDING (got $HTTP_CODE)"
fi

echo "==============================="
