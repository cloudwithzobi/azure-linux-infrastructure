#!/bin/bash

# Disk Usage Alert Script
# Warns when disk usage exceeds a threshold

THRESHOLD=80

echo "==============================="
echo "  Disk Usage Check - $(date)"
echo "==============================="

USAGE=$(df / | grep / | awk '{print $5}' | sed 's/%//')

echo "Current disk usage: $USAGE%"

if [ "$USAGE" -gt "$THRESHOLD" ]; then
    echo "⚠️  WARNING: Disk usage is above ${THRESHOLD}%!"
    echo "   Consider cleaning up logs or unused files."
else
    echo "✅ Disk usage is healthy (threshold: ${THRESHOLD}%)"
fi

echo "==============================="
